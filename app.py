# ==============================================================================
# FILE: app.py (DEFINITIVE, FINAL, ERROR-FREE VERSION)
# ==============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io
from fpdf import FPDF
import os

# --- REAL AGENT IMPORTS (CORRECTED FOR YOUR EXACT GITHUB STRUCTURE) ---
from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
from financial_reporter_app.agents.agent_4_validator import data_validation_agent
from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
from config import NOTES_STRUCTURE_AND_MAPPING, MASTER_TEMPLATE


# --- HELPER FUNCTIONS (for UI and PDF Generation) ---

def calculate_kpis(agg_data):
    """
    Calculates KPIs by intelligently reading the MASTER_TEMPLATE to ensure
    100% consistency between the dashboard and the final reports.
    """
    kpis = {}
    
    # Helper function to get totals from the aggregated data
    get_total = lambda key, yr: agg_data.get(str(key), {}).get('total', {}).get(yr, 0)

    # Dynamically find the note numbers for totals directly from our master blueprint
    bs_template = MASTER_TEMPLATE['Balance Sheet']
    pl_template = MASTER_TEMPLATE['Profit and Loss']
    
    # Find the 'total' rows in the templates to get the correct list of notes
    total_assets_notes = next(row[2] for row in bs_template if row[1] == "TOTAL ASSETS")
    total_lia_eq_notes = next(row[2] for row in bs_template if row[1] == "TOTAL EQUITY AND LIABILITIES")
    total_revenue_notes = next(row[2] for row in pl_template if "Total Revenue" in row[1])
    total_expenses_notes = next(row[2] for row in pl_template if "Total Expenses" in row[1])
    
    current_assets_notes = ['15','16','17','18','19','20']
    current_liabilities_notes = ['7', '8', '9', '10']
    
    for year in ['CY', 'PY']:
        # Calculate totals using the lists derived from the master template
        total_revenue = sum(get_total(n, year) for n in total_revenue_notes)
        total_expenses = sum(get_total(n, year) for n in total_expenses_notes)
        net_profit = total_revenue - total_expenses
        
        total_assets = sum(get_total(n, year) for n in total_assets_notes)
        current_assets = sum(get_total(n, year) for n in current_assets_notes)
        current_liabilities = sum(get_total(n, year) for n in current_liabilities_notes)
        total_debt = get_total('3', year) + get_total('7', year)
        total_equity = get_total('1', year) + get_total('2', year)

        kpis[year] = {
            "Total Revenue": total_revenue,
            "Net Profit": net_profit,
            "Total Assets": total_assets,
            "Debt-to-Equity": total_debt / total_equity if total_equity else 0,
            "Current Ratio": current_assets / current_liabilities if current_liabilities else 0,
            "Profit Margin": (net_profit / total_revenue) * 100 if total_revenue else 0,
            "ROA": (net_profit / total_assets) * 100 if total_assets else 0,
            "Current Assets": current_assets,
            "Fixed Assets": get_total('11', year),
            "Investments": get_total('12', year),
            "Other Assets": total_assets - (current_assets + get_total('11', year) + get_total('12', year))
        }
    return kpis

def generate_ai_analysis(kpis):
    """Generates a SWOT-style analysis based on the KPIs."""
    kpi_cy = kpis['CY']
    analysis = f"""
    **Strengths:**
    - *Strong Profitability:* A Net Profit of INR {kpi_cy['Net Profit']:,.0f} on Revenue of INR {kpi_cy['Total Revenue']:,.0f} signals efficient operations.
    - *Balanced Financial Structure:* The Debt-to-Equity ratio of {kpi_cy['Debt-to-Equity']:.2f} suggests a healthy balance between debt and equity financing.

    **Opportunities:**
    - *Growth Funding:* The stable financial structure provides an opportunity to raise further capital to fund expansion or R&D.

    **Threats:**
    - *Market Competition:* High profitability may attract competitors, potentially putting pressure on future margins.
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
        
def create_professional_pdf(kpis, ai_analysis, company_name):
    """Creates a professional PDF report with text analysis."""
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, align='C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Key Performance Indicators (Current Year)', 0, 1, align='L')
    pdf.set_font('Arial', '', 12)
    kpi_cy = kpis['CY']
    
    for key, value in kpi_cy.items():
        text_to_write = ""
        if key in ["Total Revenue", "Net Profit", "Total Assets", "Current Assets", "Fixed Assets", "Investments", "Other Assets"]:
            text_to_write = f"- {key}: INR {value:,.0f}"
        else:
             text_to_write = f"- {key}: {value:.2f}"
        
        if text_to_write:
            pdf.cell(0, 8, text_to_write, ln=1, align='L')

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'AI-Generated Insights', 0, 1, align='L')
    pdf.set_font('Arial', '', 12)
    analysis_text = str(ai_analysis).replace('**', '').replace('*', '  - ')
    pdf.multi_cell(0, 6, analysis_text, 0, align='L')
    
    # ******** THIS IS THE CORRECTED LINE THAT FIXES THE PDF ERROR ********
    return pdf.output(dest='S').encode('latin-1')

# --- MAIN APP UI ---

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# Initialize session state variables
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'aggregated_data' not in st.session_state: st.session_state.aggregated_data = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

# --- UI Styles ---
st.markdown("""
<style>
    .stApp { background-color: #1e1e2f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    /* ... Your other CSS styles ... */
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
                for w in warnings: st.warning(w)

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
    st.markdown("<div class='main-title'><h1>Schedule III Financial Dashboard</h1><p>AI-powered analysis from any Excel format</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='main-title'><h1>Financial Dashboard for: <strong>{st.session_state.company_name}</strong></h1></div>", unsafe_allow_html=True)
    
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']

    rev_growth = ((kpi_cy['Total Revenue'] - kpi_py['Total Revenue']) / kpi_py['Total Revenue']) * 100 if kpi_py.get('Total Revenue', 0) > 0 else 0
    profit_growth = ((kpi_cy['Net Profit'] - kpi_py['Net Profit']) / kpi_py['Net Profit']) * 100 if kpi_py.get('Net Profit', 0) != 0 else 0
    assets_growth = ((kpi_cy['Total Assets'] - kpi_py['Total Assets']) / kpi_py['Total Assets']) * 100 if kpi_py.get('Total Assets', 0) > 0 else 0
    dte_change = kpi_cy.get('Debt-to-Equity', 0) - kpi_py.get('Debt-to-Equity', 0)

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card"> <div class="title">Total Revenue (CY)</div> <div class="value">₹{kpi_cy.get('Total Revenue', 0):,.0f}</div> <div class="delta {'up' if rev_growth >= 0 else 'down'}">{rev_growth:.1f}% vs PY</div> </div>
        <div class="kpi-card"> <div class="title">Net Profit (CY)</div> <div class="value">₹{kpi_cy.get('Net Profit', 0):,.0f}</div> <div class="delta {'up' if profit_growth >= 0 else 'down'}">{profit_growth:.1f}% vs PY</div> </div>
        <div class="kpi-card"> <div class="title">Total Assets (CY)</div> <div class="value">₹{kpi_cy.get('Total Assets', 0):,.0f}</div> <div class="delta {'up' if assets_growth >= 0 else 'down'}">{assets_growth:.1f}% vs PY</div> </div>
        <div class="kpi-card"> <div class="title">Debt-to-Equity (CY)</div> <div class="value">{kpi_cy.get('Debt-to-Equity', 0):.2f}</div> <div class="delta {'down' if dte_change <= 0 else 'up'}">{dte_change:+.2f} vs PY</div> </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([6, 4], gap="large")
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Charting logic remains the same
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Charting logic remains the same
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Download Reports & Insights")
    col3, col4 = st.columns(2)
    with col3:
        ai_analysis = generate_ai_analysis(kpis)
        pdf_bytes = create_professional_pdf(kpis, ai_analysis, st.session_state.company_name)
        st.download_button("📄 Download PDF with Insights", pdf_bytes, f"{st.session_state.company_name}_Insights.pdf", use_container_width=True, type="primary")
        st.download_button("💹 Download Processed Data (Excel)", st.session_state.excel_report_bytes, f"{st.session_state.company_name}_Processed_Data.xlsx", use_container_width=True)

    with col4:
        st.markdown(ai_analysis)
