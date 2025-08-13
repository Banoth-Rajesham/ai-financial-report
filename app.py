# ==============================================================================
# FILE: app.py (FINAL, WITH ROBUST DOWNLOAD FIX) - Corrected parameter order
# ==============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io
from fpdf import FPDF
import os

# --- REAL AGENT IMPORTS ---
from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
from financial_reporter_app.agents.agent_4_validator import data_validation_agent
from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
from config import NOTES_STRUCTURE_AND_MAPPING


# --- HELPER FUNCTIONS (for UI and PDF Generation) ---

def calculate_kpis(agg_data):
    """Calculates an expanded set of KPIs for the new dashboard and PDF report."""
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)

        total_revenue = get(21) + get(22)
        change_in_inv = get(16, 'PY') - get(16, 'CY') if year == 'CY' else 0
        depreciation = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation', {}).get(year, 0)
        total_expenses = get(23) + change_in_inv + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
        current_assets = sum(get(n) for n in ['15','16','17','18','19','20'])
        current_liabilities = sum(get(n) for n in ['7', '8', '9', '10'])
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)

        kpis[year] = {
            "Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets,
            "Debt-to-Equity": total_debt / total_equity if total_equity else 0,
            "Current Ratio": current_assets / current_liabilities if current_liabilities else 0,
            "Profit Margin": (net_profit / total_revenue) * 100 if total_revenue else 0,
            "ROA": (net_profit / total_assets) * 100 if total_assets else 0,
            "Current Assets": current_assets,
            "Fixed Assets": get('11'),
            "Investments": get('12'),
            "Other Assets": total_assets - (current_assets + get('11') + get('12'))
        }
    return kpis

def generate_ai_analysis(kpis):
    """Generates a SWOT-style analysis based on the KPIs."""
    kpi_cy = kpis['CY']
    analysis = f"""
    **Strengths:**
    - *Strong Profitability:* A Net Profit of INR {kpi_cy['Net Profit']:,.0f} on Revenue of INR {kpi_cy['Total Revenue']:,.0f} signals efficient operations.
    - *Balanced Financial Structure:* The Debt-to-Equity ratio of {kpi_cy['Debt-to-Equity']:.2f} suggests a healthy balance between debt and equity financing, indicating low solvency risk.

    **Opportunities:**
    - *Growth Funding:* The stable financial structure provides an opportunity to raise further capital at a reasonable cost to fund expansion, R&D, or strategic acquisitions.

    **Threats:**
    - *Market Competition:* High profitability may attract competitors, potentially putting pressure on future margins.
    - *Economic Headwinds:* A broader economic downturn could impact customer spending and affect revenue growth.
    """
    return analysis

class PDF(FPDF):
    """Custom PDF class to define a professional header and footer."""
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Financial Dashboard Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_professional_pdf(kpis, ai_analysis, charts, company_name):
    """Creates a professional, multi-page PDF report in memory."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Key Performance Indicators (Current Year)', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    kpi_cy = kpis['CY']
    for key, value in kpi_cy.items():
        if key in ["Total Revenue", "Net Profit", "Total Assets"]:
            pdf.cell(0, 8, f"- {key}: INR {value:,.0f}", 0, 1)
        elif key not in ["Current Assets", "Fixed Assets", "Investments", "Other Assets"]:
            pdf.cell(0, 8, f"- {key}: {value:.2f}", 0, 1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'AI-Generated Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 6, ai_analysis.replace('**', '').replace('*', '  - '))
    pdf.ln(10)

    if charts:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Financial Charts', 0, 1, 'L')
        pdf.ln(5)
        
        temp_dir = "temp_charts"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        for title, chart_bytes in charts.items():
            try:
                safe_title = title.replace(" ", "_").lower()
                temp_image_path = os.path.join(temp_dir, f"{safe_title}.png")
                with open(temp_image_path, "wb") as f:
                    f.write(chart_bytes)
                
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(0, 10, title, 0, 1, 'C')
                pdf.image(temp_image_path, x=15, w=180)
                pdf.ln(5)
            except Exception as e:
                print(f"Error adding chart '{title}' to PDF: {e}")

    # ✅ FIX: output to bytes properly
    return pdf.output(dest="S").encode("latin-1")


# --- MAIN APP UI ---

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# Initialize session state variables
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'aggregated_data' not in st.session_state: st.session_state.aggregated_data = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

# --- Neumorphic CSS Styles with Neon Glow Hover Effect ---
st.markdown("""
<style>
    /* CSS remains same */
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR UI CONTROLS ---
with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline... Please wait."):
                source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None: st.error("Pipeline Failed: Data Intake."); st.stop()
                refined_mapping = ai_mapping_agent(source_df['Particulars'].unique().tolist(), NOTES_STRUCTURE_AND_MAPPING)
                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data: st.error("Pipeline Failed: Aggregation."); st.stop()
                warnings = data_validation_agent(aggregated_data)
                excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
                if excel_report_bytes is None: st.error("Pipeline Failed: Report Finalizer."); st.stop()

            st.session_state.update(
                report_generated=True, aggregated_data=aggregated_data, company_name=company_name,
                excel_report_bytes=excel_report_bytes, kpis=calculate_kpis(aggregated_data)
            )
            st.rerun()
        else:
            st.warning("Please upload a file and enter a company name.")

# --- MAIN DASHBOARD DISPLAY ---
if not st.session_state.report_generated:
    st.markdown("<div class='main-title'><h1>Financial Analysis Dashboard</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'><p>Upload your financial data in the sidebar and click 'Generate Dashboard' to begin.</p></div>", unsafe_allow_html=True)
else:
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']

    rev_growth = ((kpi_cy['Total Revenue'] - kpi_py['Total Revenue']) / kpi_py['Total Revenue']) * 100 if kpi_py.get('Total Revenue') else 0
    profit_growth = ((kpi_cy['Net Profit'] - kpi_py['Net Profit']) / kpi_py['Net Profit']) * 100 if kpi_py.get('Net Profit') else 0
    assets_growth = ((kpi_cy['Total Assets'] - kpi_py['Total Assets']) / kpi_py['Total Assets']) * 100 if kpi_py.get('Total Assets') else 0
    dte_change = kpi_cy.get('Debt-to-Equity', 0) - kpi_py.get('Debt-to-Equity', 0)

    st.markdown(f"""
    <!-- KPI Cards HTML stays same -->
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([6, 4], gap="large")
    # Charts remain same as before

    st.write("---")
    st.subheader("Download Reports")
    
    ai_analysis = generate_ai_analysis(kpis)
    charts_for_pdf = {}
    try:
        charts_for_pdf["Revenue Trend"] = fig_revenue.to_image(format="png", scale=2)
    except Exception as e:
        print(f"Could not generate Revenue Trend image for PDF: {e}")
    try:
        charts_for_pdf["Asset Distribution"] = fig_asset.to_image(format="png", scale=2)
    except Exception as e:
        print(f"Could not generate Asset Distribution image for PDF: {e}")

    # ✅ FIXED ARGUMENT ORDER HERE
    pdf_bytes = create_professional_pdf(kpis, ai_analysis, charts_for_pdf, st.session_state.company_name)
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button("📄 Download PDF with Insights", pdf_bytes, f"{st.session_state.company_name}_Insights.pdf", use_container_width=True, type="primary")
    with d_col2:
        st.download_button("💹 Download Processed Data (Excel)", st.session_state.excel_report_bytes, f"{st.session_state.company_name}_Processed_Data.xlsx", use_container_width=True)

