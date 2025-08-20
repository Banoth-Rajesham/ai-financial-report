# ==============================================================================
# FILE: app.py (FINAL — corrected & runnable)
# ==============================================================================

import io
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from fpdf import FPDF

# --- REAL AGENT IMPORTS ---
from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
from financial_reporter_app.agents.agent_4_validator import data_validation_agent
from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
from config import NOTES_STRUCTURE_AND_MAPPING

# --------------------------------------------------------------------------
# STREAMLIT PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# --------------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------------

def calculate_kpis(agg_data: dict) -> dict:
    """Compute KPIs for CY and PY from aggregated data."""
    kpis = {}
    for year in ["CY", "PY"]:
        get = lambda key, y=year: agg_data.get(str(key), {}).get("total", {}).get(y, 0.0)
        total_revenue = get(21) + get(22)
        change_in_inv = get(16, "PY") - get(16, "CY") if year == "CY" else 0.0
        depreciation = agg_data.get("11", {}).get("sub_items", {}).get("Depreciation", {}).get(year, 0.0)
        total_expenses = get(23) + change_in_inv + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in ["11","12","13","14","15","16","17","18","19","20"])
        current_assets = sum(get(n) for n in ["15","16","17","18","19","20"])
        current_liabilities = sum(get(n) for n in ["7","8","9","10"])
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)

        kpis[year] = {
            "Total Revenue": float(total_revenue),
            "Net Profit": float(net_profit),
            "Total Assets": float(total_assets),
            "Debt-to-Equity": (total_debt / total_equity) if total_equity else 0.0,
            "Current Ratio": (current_assets / current_liabilities) if current_liabilities else 0.0,
            "Profit Margin": ((net_profit / total_revenue) * 100.0) if total_revenue else 0.0,
            "ROA": ((net_profit / total_assets) * 100.0) if total_assets else 0.0,
            "Current Assets": float(current_assets),
            "Fixed Assets": float(get("11")),
            "Investments": float(get("12")),
            "Other Assets": float(total_assets - (current_assets + get("11") + get("12"))),
        }
    return kpis

def generate_ai_analysis(kpis: dict) -> str:
    """Simple narrative from KPIs."""
    kpi_cy = kpis["CY"]
    return (
        f"**Strengths:**\n"
        f"- *Strong Profitability:* Net Profit of INR {kpi_cy['Net Profit']:,.0f} "
        f"on Revenue of INR {kpi_cy['Total Revenue']:,.0f}.\n"
        f"- *Balanced Structure:* Debt-to-Equity of {kpi_cy['Debt-to-Equity']:.2f}.\n\n"
        f"**Opportunities:**\n"
        f"- Expansion funding and product diversification.\n\n"
        f"**Threats:**\n"
        f"- Competitive pressure; macro slowdowns could compress margins."
    )

class ReportPDF(FPDF):
    """Custom PDF with header & footer."""
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Financial Dashboard Report", 0, 1, "C")
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def create_professional_pdf(kpis: dict, ai_analysis: str, company_name: str) -> bytes:
    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, f"Financial Report for {company_name}", 0, 1, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Key Performance Indicators (Current Year)", 0, 1, align="L")
    pdf.set_font("Arial", "", 12)
    kpi_cy = kpis["CY"]
    for key, value in kpi_cy.items():
        if key in ["Total Revenue", "Net Profit", "Total Assets", "Current Assets", "Fixed Assets", "Investments", "Other Assets"]:
            line = f"- {key}: INR {value:,.0f}"
        else:
            line = f"- {key}: {value:.2f}"
        pdf.cell(0, 8, line, ln=1, align="L")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI-Generated Insights", 0, 1, align="L")
    pdf.set_font("Arial", "", 12)
    analysis_text = str(ai_analysis).replace("**", "").replace("*", "  - ")
    pdf.multi_cell(0, 6, analysis_text, 0, align="L")
    pdf.ln(4)
    return pdf.output(dest="S").encode("latin-1")

# --------------------------------------------------------------------------
# Cached full pipeline
# --------------------------------------------------------------------------
@st.cache_data(show_spinner="Running full analysis pipeline...")
def run_full_pipeline(source_df: pd.DataFrame, company_name_for_cache: str):
    refined_mapping = ai_mapping_agent(
        source_df["Particulars"].astype(str).unique().tolist(),
        NOTES_STRUCTURE_AND_MAPPING,
    )
    aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
    if not aggregated_data:
        return None, None, ["Pipeline Failed: Aggregation."]
    warnings = data_validation_agent(aggregated_data)
    excel_report_bytes = report_finalizer_agent(aggregated_data, company_name_for_cache)
    if excel_report_bytes is None:
        return None, None, ["Pipeline Failed: Report Finalizer."]
    return aggregated_data, excel_report_bytes, warnings

# --------------------------------------------------------------------------
# Session state initialization
# --------------------------------------------------------------------------
for key in ["report_generated", "awaiting_py_upload", "cy_df", "final_df", "excel_report_bytes", "aggregated_data", "kpis", "company_name"]:
    if key not in st.session_state:
        st.session_state[key] = False if "report_generated" == key or "awaiting_py_upload" == key else None
st.session_state.company_name = st.session_state.company_name or "My Company Inc."

# --------------------------------------------------------------------------
# Sidebar: file upload & process
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("Upload & Process")
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.session_state.awaiting_py_upload:
        st.warning("Previous Year (PY) data not found in the first file. Please upload the PY file.")
        py_file = st.file_uploader("Upload Previous Year's Data for Schedule III compliance", type=["xlsx", "xls"], key="py_uploader")
        if st.button("Combine and Generate", use_container_width=True):
            if py_file and st.session_state.cy_df is not None:
                py_df, _ = intelligent_data_intake_agent(io.BytesIO(py_file.getvalue()))
                cy_df = st.session_state.cy_df
                if py_df is not None:
                    cy_df = cy_df.rename(columns=lambda c: c.strip())
                    py_df = py_df.rename(columns=lambda c: c.strip())
                    merged_df = pd.merge(
                        cy_df[["Particulars","Amount_CY"]],
                        py_df[["Particulars","Amount_CY"]],
                        on="Particulars", how="outer", suffixes=("_CY","_PY")
                    ).rename(columns={"Amount_CY_CY":"Amount_CY","Amount_CY_PY":"Amount_PY"}).fillna(0)
                    st.session_state.final_df = merged_df
                    st.session_state.awaiting_py_upload = False
                    st.rerun()
                else:
                    st.error("Could not process the Previous Year file.")
            else:
                st.error("Please upload the Previous Year file to proceed.")
    else:
        uploaded_file = st.file_uploader("Upload Financial Data (CY or CY+PY)", type=["xlsx", "xls"], key="cy_uploader")
        if st.button("Generate Dashboard", use_container_width=True):
            if uploaded_file and company_name:
                source_df, has_py = intelligent_data_intake_agent(io.BytesIO(uploaded_file.getvalue()))
                if source_df is None:
                    st.error("Pipeline Failed: Could not read the uploaded file.")
                elif has_py:
                    st.session_state.final_df = source_df
                    st.session_state.company_name = company_name
                    st.rerun()
                else:
                    st.session_state.cy_df = source_df
                    st.session_state.company_name = company_name
                    st.session_state.awaiting_py_upload = True
                    st.rerun()
            else:
                st.warning("Please upload a file and enter a company name.")

# --------------------------------------------------------------------------
# Main pipeline trigger
# --------------------------------------------------------------------------
if st.session_state.final_df is not None and not st.session_state.awaiting_py_upload:
    final_df = st.session_state.final_df
    company_name = st.session_state.company_name
    aggregated_data, excel_report_bytes, warnings = run_full_pipeline(final_df, company_name)
    if aggregated_data is None:
        st.error(warnings[0] if warnings else "Pipeline Failed.")
    else:
        for w in warnings:
            st.warning(w)
        st.session_state.update(
            report_generated=True,
            aggregated_data=aggregated_data,
            excel_report_bytes=excel_report_bytes,
            kpis=calculate_kpis(aggregated_data),
        )
        st.session_state.final_df = None
        st.session_state.cy_df = None
        st.rerun()

# --------------------------------------------------------------------------
# Main dashboard display
# --------------------------------------------------------------------------
if st.session_state.report_generated:
    kpis = st.session_state.kpis
    ai_analysis = generate_ai_analysis(kpis)
    insights_pdf_bytes = create_professional_pdf(kpis, ai_analysis, st.session_state.company_name)

    # Download buttons (PDF/Excel)
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button("📄 Download PDF with Insights", data=insights_pdf_bytes, file_name=f"{st.session_state.company_name}_Insights.pdf", use_container_width=True)
    with d_col2:
        st.download_button("💹 Download Processed Data (Excel)", data=st.session_state.excel_report_bytes, file_name=f"{st.session_state.company_name}_Processed_Data.xlsx", use_container_width=True)

    # --------------------------------------------------------------------------
    # SWOT Analysis
    # --------------------------------------------------------------------------
    kpi_cy = kpis["CY"]
    kpi_py = kpis.get("PY", {})
    strengths, weaknesses, opportunities, threats = [], [], [], []

    current_ratio = kpi_cy.get("Current Ratio",0)
    debt_equity = kpi_cy.get("Debt-to-Equity",0)
    profit_margin = kpi_cy.get("Profit Margin",0)
    roa = kpi_cy.get("ROA",0)
    asset_turnover = (kpi_cy["Total Revenue"]/kpi_cy["Total Assets"]) if kpi_cy.get("Total Assets") else 0

    # Strengths
    if current_ratio>1.5: strengths.append(f"Current Ratio {current_ratio:.2f} indicates strong liquidity.")
    if debt_equity<1: strengths.append(f"Debt-to-Equity {debt_equity:.2f} indicates low leverage.")
    if profit_margin>15: strengths.append(f"Profit Margin {profit_margin:.2f}% shows healthy profitability.")
    if roa>10: strengths.append(f"ROA {roa:.2f}% suggests efficient asset utilization.")
    if asset_turnover>1: strengths.append(f"Asset Turnover {asset_turnover:.2f} indicates solid revenue per asset.")
    if not strengths: strengths.append("No significant strengths identified.")

    # Weaknesses
    if current_ratio<1: weaknesses.append(f"Current Ratio {current_ratio:.2f} suggests liquidity risk.")
    if debt_equity>2: weaknesses.append(f"High Debt-to-Equity ({debt_equity:.2f}) indicates heavy leverage.")
    if profit_margin<5: weaknesses.append(f"Profit Margin {profit_margin:.2f}% is very low.")
    if not weaknesses: weaknesses.append("No major weaknesses identified.")

    # Opportunities
    if profit_margin<20: opportunities.append("Scope to expand margins via pricing, mix and cost optimization.")
    if asset_turnover<2: opportunities.append("Improve asset utilization via capacity fill and working-capital discipline.")
    opportunities.append("Evaluate growth in new geographies/segments to diversify revenue.")
    if not opportunities: opportunities.append("No clear opportunities identified.")

    # Threats
    if profit_margin<kpi_py.get("Profit Margin",0): threats.append("Profit margin declined vs PY; watch pricing and input costs.")
    if (debt_equity - kpi_py.get("Debt-to-Equity",0))>0.2: threats.append("Leverage increased vs PY; monitor debt servicing and covenants.")
    if not threats: threats.append("No immediate threats identified.")

    max_len = max(len(strengths), len(weaknesses), len(opportunities), len(threats))
    strengths += [""]*(max_len-len(strengths))
    weaknesses += [""]*(max_len-len(weaknesses))
    opportunities += [""]*(max_len-len(opportunities))
    threats += [""]*(max_len-len(threats))

    swot_df = pd.DataFrame({"Strengths":strengths,"Weaknesses":weaknesses,"Opportunities":opportunities,"Threats":threats})
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        swot_df.to_excel(writer, sheet_name="SWOT Analysis", index=False)
    st.download_button("📥 Download SWOT Analysis (Excel)", data=excel_buffer.getvalue(), file_name="SWOT_Analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    # SWOT PDF
    class SwotPDF(FPDF):
        def header(self): self.set_font("Arial","B",12); self.cell(0,10,"SWOT Analysis",ln=True,align="C")
    swot_pdf = SwotPDF()
    swot_pdf.add_page()
    swot_pdf.set_font("Arial",size=10)
    for title, items in [("Strengths", strengths),("Weaknesses", weaknesses),("Opportunities", opportunities),("Threats", threats)]:
        swot_pdf.set_font("Arial","B",11)
        swot_pdf.cell(0,10,f"{title}:",ln=True)
        swot_pdf.set_font("Arial",size=10)
        for i in items: swot_pdf.multi_cell(0,8,f"- {i}")
    sw
