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

# ------------------------------------------------------------------------------
# STREAMLIT PAGE CONFIG — must be set before other Streamlit calls
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------
def calculate_kpis(agg_data: dict) -> dict:
    """
    Calculates an expanded set of KPIs from the aggregated structure:
    agg_data[str(note_no)]['total'][year] should be numeric.
    """
    kpis = {}
    for year in ["CY", "PY"]:
        get = lambda key, y=year: agg_data.get(str(key), {}).get("total", {}).get(y, 0.0)

        # Basic Schedule III-style groups (adjust numbers to your mapping)
        # Revenue: 21 (Revenue from Operations) + 22 (Other Income)
        total_revenue = get(21) + get(22)

        # Example inventory change (if 16 is inventories): change only affects CY calc
        change_in_inv = get(16, "PY") - get(16, "CY") if year == "CY" else 0.0

        # Depreciation from note 11 sub-item (optional; fallback to 0)
        depreciation = (
            agg_data.get("11", {})
            .get("sub_items", {})
            .get("Depreciation", {})
            .get(year, 0.0)
        )

        # Expenses: 23(COGS) + change_in_inv + 24(Employee) + 25(Finance) + depreciation + 26(Other Exp)
        total_expenses = get(23) + change_in_inv + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses

        # Assets: sum of notes 11..20 (example grouping)
        total_assets = sum(get(n) for n in ["11","12","13","14","15","16","17","18","19","20"])
        current_assets = sum(get(n) for n in ["15","16","17","18","19","20"])
        current_liabilities = sum(get(n) for n in ["7","8","9","10"])  # example grouping

        total_debt = get(3) + get(7)     # LT borrowings + ST borrowings
        total_equity = get(1) + get(2)   # Equity share capital + Other equity

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


class PDF(FPDF):
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
    """Create a simple textual PDF. Returns bytes for st.download_button."""
    pdf = PDF()
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
        elif isinstance(value, (int, float)):
            line = f"- {key}: {value:.2f}"
        else:
            line = f"- {key}: {value}"
        pdf.cell(0, 8, line, ln=1, align="L")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI-Generated Insights", 0, 1, align="L")
    pdf.set_font("Arial", "", 12)

    analysis_text = str(ai_analysis).replace("**", "").replace("*", "  - ")
    pdf.multi_cell(0, 6, analysis_text, 0, align="L")
    pdf.ln(4)

    # FPDF returns a string; encode to bytes. latin-1 is the safe default.
    # Option 2 (explicit conversion)
    return bytes(pdf.output(dest="S"))




# ------------------------------------------------------------------------------
# Cache the heavy pipeline
# ------------------------------------------------------------------------------
@st.cache_data(show_spinner="Running full analysis pipeline...")
def run_full_pipeline(source_df: pd.DataFrame, company_name_for_cache: str):
    """
    Runs the computationally expensive agents on a finalized dataframe
    (having 'Particulars', 'Amount_CY', 'Amount_PY') and caches the results.
    """
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


# ------------------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------------------
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "awaiting_py_upload" not in st.session_state:
    st.session_state.awaiting_py_upload = False
if "cy_df" not in st.session_state:
    st.session_state.cy_df = None
if "final_df" not in st.session_state:
    st.session_state.final_df = None
if "excel_report_bytes" not in st.session_state:
    st.session_state.excel_report_bytes = None
if "aggregated_data" not in st.session_state:
    st.session_state.aggregated_data = None
if "kpis" not in st.session_state:
    st.session_state.kpis = None
if "company_name" not in st.session_state:
    st.session_state.company_name = "My Company Inc."

# ------------------------------------------------------------------------------
# Styles
# ------------------------------------------------------------------------------
st.markdown(
    """
<style>
    .stApp { background-color: #1e1e2f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .block-container { padding: 1rem 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .main-title h1 { font-weight: 700; color: #e0e0e0; font-size: 2.2rem; text-align: center; }
    .main-title p { color: #b0b0b0; font-size: 1.1rem; text-align: center; margin-bottom: 2rem; }
    .kpi-container { display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: center; margin-bottom: 2rem; }
    .kpi-card {
        background: #2b2b3c;
        border-radius: 25px;
        padding: 1.5rem 2rem;
        box-shadow: 6px 6px 16px #14141e, -6px -6px 16px #38384a;
        min-width: 250px;
        color: #e0e0e0;
        flex: 1;
        border: 2px solid transparent;
        transition: all 0.3s ease-in-out;
    }
    .kpi-card .title { font-weight: 600; font-size: 1rem; margin-bottom: 0.3rem; color: #a0a0a0; }
    .kpi-card .value { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; line-height: 1.1; }
    .kpi-card .delta { display: inline-flex; align-items: center; font-weight: 600; font-size: 0.9rem; border-radius: 20px; padding: 0.25rem 0.8rem; }
    .kpi-card .delta.up { background-color: #00cc7a; color: #0f2f1f; }
    .kpi-card .delta.up::before { content: "⬆"; margin-right: 0.3rem; }
    .kpi-card .delta.down { background-color: #ff4c4c; color: #3a0000; }
    .kpi-card .delta.down::before { content: "⬇"; margin-right: 0.3rem; }
    .kpi-card:hover { transform: translateY(-5px); }
    .kpi-container .kpi-card:nth-child(1):hover { box-shadow: 0 0 25px rgba(0, 170, 255, 0.8); }
    .kpi-container .kpi-card:nth-child(2):hover { box-shadow: 0 0 25px rgba(0, 255, 127, 0.8); }
    .kpi-container .kpi-card:nth-child(3):hover { box-shadow: 0 0 25px rgba(255, 204, 0, 0.8); }
    .kpi-container .kpi-card:nth-child(4):hover { box-shadow: 0 0 25px rgba(255, 85, 85, 0.8); }
    .chart-container { background-color: #2b2b3c; border-radius: 15px; padding: 1rem; box-shadow: 6px 6px 16px #14141e, -6px -6px 16px #38384a; }
    .ratio-card { background-color: #2b2b3c; border-radius: 15px; padding: 1rem; box-shadow: 6px 6px 16px #14141e, -6px -6px 16px #38384a; height: 100%; }
    .ratio-row { display: flex; justify-content: space-between; padding: 0.85rem 0.5rem; border-bottom: 1px solid #4a4a6a; }
    .ratio-row:last-child { border-bottom: none; }
    .ratio-label { color: #a0a0a0; }
    .ratio-value { font-weight: 600; color: #e0e0e0; }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# Sidebar (CY & PY upload flow)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.header("Upload & Process")
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.session_state.awaiting_py_upload:
        st.warning("Previous Year (PY) data not found in the first file. Please upload the PY file.")
        py_file = st.file_uploader(
            "Upload Previous Year's Data for Schedule III compliance",
            type=["xlsx", "xls"],
            key="py_uploader",
        )

        if st.button("Combine and Generate", type="primary", use_container_width=True):
            if py_file and st.session_state.cy_df is not None:
                with st.spinner("Processing and merging files..."):
                    py_df, _ = intelligent_data_intake_agent(io.BytesIO(py_file.getvalue()))
                    cy_df = st.session_state.cy_df

                    if py_df is not None:
                        # Normalize columns & safe merge with suffixes
                        cy_df = cy_df.rename(columns=lambda c: c.strip())
                        py_df = py_df.rename(columns=lambda c: c.strip())

                        merged_df = pd.merge(
                            cy_df[["Particulars", "Amount_CY"]],
                            py_df[["Particulars", "Amount_CY"]],
                            on="Particulars",
                            how="outer",
                            suffixes=("_CY", "_PY"),
                        ).rename(
                            columns={"Amount_CY_CY": "Amount_CY", "Amount_CY_PY": "Amount_PY"}
                        ).fillna(0)

                        st.session_state.final_df = merged_df
                        st.session_state.awaiting_py_upload = False
                        st.rerun()
                    else:
                        st.error("Could not process the Previous Year file.")
            else:
                st.error("Please upload the Previous Year file to proceed.")

    else:
        uploaded_file = st.file_uploader(
            "Upload Financial Data (CY or CY+PY)",
            type=["xlsx", "xls"],
            key="cy_uploader",
        )

        if st.button("Generate Dashboard", type="primary", use_container_width=True):
            if uploaded_file and company_name:
                with st.spinner("Processing file..."):
                    # Agent 1 expected to return (dataframe, has_py)
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

# ------------------------------------------------------------------------------
# Main pipeline trigger
# ------------------------------------------------------------------------------
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
        # Clean transient state, then rerun to display
        st.session_state.final_df = None
        st.session_state.cy_df = None
        st.rerun()

# ------------------------------------------------------------------------------
# Main dashboard display
# ------------------------------------------------------------------------------
if not st.session_state.report_generated:
    if not st.session_state.awaiting_py_upload:
        st.markdown(
            "<div class='main-title'><h1>Schedule III Financial Dashboard</h1>"
            "<p>AI-powered analysis from any Excel format</p></div>",
            unsafe_allow_html=True,
        )
else:
    # Title + company
    st.markdown(
        "<div class='main-title'><h1>Schedule III Financial Dashboard</h1></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='main-title'><p>Displaying analysis for: <strong>{st.session_state.company_name}</strong></p></div>",
        unsafe_allow_html=True,
    )

    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis["CY"], kpis["PY"]

    # Growth deltas
    rev_growth = (
        ((kpi_cy["Total Revenue"] - kpi_py.get("Total Revenue", 0)) / kpi_py.get("Total Revenue", 0)) * 100
        if kpi_py.get("Total Revenue", 0) else 0
    )
    profit_growth = (
        ((kpi_cy["Net Profit"] - kpi_py.get("Net Profit", 0)) / kpi_py.get("Net Profit", 0)) * 100
        if kpi_py.get("Net Profit", 0) else 0
    )
    assets_growth = (
        ((kpi_cy["Total Assets"] - kpi_py.get("Total Assets", 0)) / kpi_py.get("Total Assets", 0)) * 100
        if kpi_py.get("Total Assets", 0) else 0
    )
    dte_change = kpi_cy.get("Debt-to-Equity", 0) - kpi_py.get("Debt-to-Equity", 0)

    # KPI strip
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="title">Total Revenue (CY)</div>
                <div class="value">₹{kpi_cy.get('Total Revenue', 0):,.0f}</div>
                <div class="delta {'up' if rev_growth >= 0 else 'down'}">{rev_growth:.1f}% vs PY</div>
            </div>
            <div class="kpi-card">
                <div class="title">Net Profit (CY)</div>
                <div class="value">₹{kpi_cy.get('Net Profit', 0):,.0f}</div>
                <div class="delta {'up' if profit_growth >= 0 else 'down'}">{profit_growth:.1f}% vs PY</div>
            </div>
            <div class="kpi-card">
                <div class="title">Total Assets (CY)</div>
                <div class="value">₹{kpi_cy.get('Total Assets', 0):,.0f}</div>
                <div class="delta {'up' if assets_growth >= 0 else 'down'}">{assets_growth:.1f}% vs PY</div>
            </div>
            <div class="kpi-card">
                <div class="title">Debt-to-Equity (CY)</div>
                <div class="value">{kpi_cy.get('Debt-to-Equity', 0):.2f}</div>
                <div class="delta {'down' if dte_change <= 0 else 'up'}">{dte_change:+.2f} vs PY</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Charts & Ratios
    col1, col2 = st.columns([6, 4], gap="large")
    with col1:
        # Revenue trend (synthetic monthly split from annual totals)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        revenue_df = pd.DataFrame({
            "Month": months * 2,
            "Year": ["Previous Year"] * 12 + ["Current Year"] * 12,
            "Revenue": np.concatenate([
                np.linspace(kpi_py.get("Total Revenue", 0) * 0.07, kpi_py.get("Total Revenue", 0) * 0.09, 12),
                np.linspace(kpi_cy.get("Total Revenue", 0) * 0.07, kpi_cy.get("Total Revenue", 0) * 0.09, 12),
            ])
        })
        fig_revenue = px.area(revenue_df, x="Month", y="Revenue", color="Year", title="<b>Revenue Trend</b>")
        fig_revenue.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Profit margin by quarter around CY margin (synthetic demo)
        base_pm = kpi_cy.get("Profit Margin", 0.0)
        profit_margin_df = pd.DataFrame({
            "Quarter": ["Q1", "Q2", "Q3", "Q4"],
            "Margin": np.clip(np.random.uniform(base_pm - 1.0, base_pm + 1.0, 4), -9999, 9999)
        })
        fig_margin = px.line(profit_margin_df, x="Quarter", y="Margin", title="<b>Profit Margin Trend</b>", markers=True)
        fig_margin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_margin, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        asset_df = pd.DataFrame({
            "Asset Type": ["Current Assets", "Fixed Assets", "Investments", "Other Assets"],
            "Value": [
                kpi_cy.get("Current Assets", 0.0),
                kpi_cy.get("Fixed Assets", 0.0),
                kpi_cy.get("Investments", 0.0),
                kpi_cy.get("Other Assets", 0.0),
            ]
        })
        asset_df = asset_df[asset_df["Value"] > 0]
        if not asset_df.empty:
            fig_asset = px.pie(asset_df, names="Asset Type", values="Value", title="<b>Asset Distribution</b>")
            fig_asset.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0")
            st.plotly_chart(fig_asset, use_container_width=True)
        else:
            st.info("No positive asset values to display.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="ratio-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ffffff;'>Key Financial Ratios</h4>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='ratio-row'> <span class='ratio-label'>Current Ratio</span> <span class='ratio-value'>{kpi_cy.get('Current Ratio', 0):.2f}</span> </div>
            <div class='ratio-row'> <span class='ratio-label'>Profit Margin</span> <span class='ratio-value'>{kpi_cy.get('Profit Margin', 0):.2f}%</span> </div>
            <div class='ratio-row'> <span class='ratio-label'>Return on Assets (ROA)</span> <span class='ratio-value'>{kpi_cy.get('ROA', 0):.2f}%</span> </div>
            <div class='ratio-row'> <span class='ratio-label'>Debt-to-Equity</span> <span class='ratio-value'>{kpi_cy.get('Debt-to-Equity', 0):.2f}</span> </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("Download Reports")

    ai_analysis = generate_ai_analysis(kpis)
    pdf_bytes = create_professional_pdf(kpis, ai_analysis, st.session_state.company_name)

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button(
            "📄 Download PDF with Insights",
            data=pdf_bytes,
            file_name=f"{st.session_state.company_name}_Insights.pdf",
            use_container_width=True,
            type="primary",
        )
    with d_col2:
        st.download_button(
            "💹 Download Processed Data (Excel)",
            data=st.session_state.excel_report_bytes,
            file_name=f"{st.session_state.company_name}_Processed_Data.xlsx",
            use_container_width=True,
        )



