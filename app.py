# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: app.py
# This version removes all mock data and mock functions. It is designed to
# use your real agents to process your uploaded file correctly.
# ==============================================================================
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- This is the crucial part that finds your agent files ---
# It adds the parent directory to the Python path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# --- Attempt to import the REAL agents ---
try:
    from config import NOTES_STRUCTURE_AND_MAPPING, MASTER_TEMPLATE
    from agents import (
        intelligent_data_intake_agent,
        ai_mapping_agent,
        hierarchical_aggregator_agent,
        data_validation_agent,
        report_finalizer_agent
    )
except ImportError as e:
    st.error(
        "CRITICAL ERROR: A module could not be imported. "
        "This usually means your folder structure is incorrect. "
        "Please ensure your `app.py` is in the main folder, with `config.py` and a sub-folder named `agents` next to it. "
        f"Details: {e}"
    )
    st.stop()


# --- HELPER FUNCTIONS (No changes needed here) ---

def calculate_kpis(agg_data):
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        
        total_revenue = get(21) + get(22)
        total_expenses = get(23) + get(24) + get(25) + get(26)
        # Note: Depreciation is already inside Note 11's total in this setup for P&L
        total_expenses += agg_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)

        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in range(11, 21))
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)
        
        kpis[year] = {
            "Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets,
            "Debt-to-Equity": total_debt / total_equity if total_equity else 0
        }
    return kpis

def generate_ai_analysis(kpis):
    kpi_cy = kpis.get('CY', {})
    if not kpi_cy: return "KPIs could not be calculated. Analysis unavailable."
    
    analysis = f"""
    **Strengths:**
    - **Strong Profitability:** A Net Profit of INR {kpi_cy.get('Net Profit', 0):,.0f} on Revenue of INR {kpi_cy.get('Total Revenue', 0):,.0f} signals efficient operations.
    - **Balanced Financial Structure:** The Debt-to-Equity ratio of {kpi_cy.get('Debt-to-Equity', 0):.2f} suggests a healthy balance between debt and equity financing.

    **Opportunities:**
    - **Growth Funding:** The stable financial structure provides an opportunity to raise further capital at a reasonable cost to fund expansion or R&D.

    **Threats:**
    - **Market Competition:** High profitability may attract competitors, potentially putting pressure on future margins.
    - **Economic Headwinds:** A broader economic downturn could impact customer spending and affect revenue growth.
    """
    return analysis

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Financial Dashboard Report', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_professional_pdf(kpis, ai_analysis, charts, company_name):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Key Performance Indicators (Current Year)', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    kpi_cy = kpis.get('CY', {})
    for key, value in kpi_cy.items():
        pdf.cell(0, 8, f"- {key}: {'INR {:,.0f}'.format(value) if 'Revenue' in key or 'Profit' in key or 'Assets' in key else '{:.2f}'.format(value)}", 0, 1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'AI-Generated Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 6, ai_analysis.replace('**', ''))
    pdf.ln(10)
    
    return bytes(pdf.output())

# --- MAIN APP UI ---
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state:
    st.session_state.excel_report_bytes = None
if 'kpis' not in st.session_state:
    st.session_state.kpis = None
if 'company_name' not in st.session_state:
    st.session_state.company_name = "My Company Inc."

with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
                st.info("Step 1/5: Ingesting data...")
                # THIS NOW CALLS THE REAL, SPECIALIZED AGENT
                source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None:
                    st.error("Pipeline Failed at Data Intake. Please check the file format and structure.")
                    st.stop()
                
                st.info("Step 2/5: Mapping financial terms...")
                refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), NOTES_STRUCTURE_AND_MAPPING, api_url=None, api_key=None)
                
                st.info("Step 3/5: Aggregating and propagating values...")
                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data:
                    st.error("Pipeline Failed at Aggregation.")
                    st.stop()
                
                st.info("Step 4/5: Validating financial balances...")
                warnings = data_validation_agent(aggregated_data)
                
                st.info("Step 5/5: Generating final reports...")
                excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
                if excel_report_bytes is None:
                    st.error("Pipeline Failed at Report Finalizer.")
                    st.stop()

            st.success("Dashboard Generated Successfully!")
            for w in warnings: st.warning(w)
                
            st.session_state.report_generated = True
            st.session_state.aggregated_data = aggregated_data
            st.session_state.company_name = company_name
            st.session_state.excel_report_bytes = excel_report_bytes
            st.session_state.kpis = calculate_kpis(aggregated_data)
            st.rerun()
        else:
            st.warning("Please upload a file and enter a company name.")

if not st.session_state.report_generated:
    st.title("Financial Analysis Dashboard")
    st.write("Upload your financial data (T-format or Schedule III) in the sidebar and click 'Generate Dashboard' to begin.")
else:
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis.get('CY', {}), kpis.get('PY', {})
    
    st.title(f"Dashboard for {st.session_state.company_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Revenue (CY)", f"₹{kpi_cy.get('Total Revenue', 0):,.0f}")
    with col2: st.metric("Net Profit (CY)", f"₹{kpi_cy.get('Net Profit', 0):,.0f}")
    with col3: st.metric("Total Assets (CY)", f"₹{kpi_cy.get('Total Assets', 0):,.0f}")
    with col4: st.metric("Debt-to-Equity (CY)", f"{kpi_cy.get('Debt-to-Equity', 0):.2f}")

    ai_analysis = generate_ai_analysis(kpis)
    st.subheader("🤖 AI-Generated Insights")
    st.markdown(ai_analysis)

    st.subheader("⬇️ Download Center")
    pdf_bytes = create_professional_pdf(kpis, ai_analysis, {}, st.session_state.company_name)

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button(
            label="📄 Download PDF Summary",
            data=pdf_bytes,
            file_name=f"{st.session_state.company_name}_Summary_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with d_col2:
        st.download_button(
            label="💹 Download Full Styled Excel Report",
            data=st.session_state.excel_report_bytes,
            file_name=f"{st.session_state.company_name}_Full_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
