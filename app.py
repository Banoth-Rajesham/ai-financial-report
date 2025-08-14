# ==============================================================================
# FILE: app.py (DIAGNOSTIC VERSION)
# ==============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io
from fpdf import FPDF
import os

# --- REAL AGENT IMPORTS ---
# We only need the first agent for this diagnostic test.
from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
from financial_reporter_app.agents.agent_4_validator import data_validation_agent
from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
from config import NOTES_STRUCTURE_AND_MAPPING


# --- HELPER FUNCTIONS (Kept for completeness, but not used in diagnostic mode) ---

def calculate_kpis(agg_data):
    """Calculates an expanded set of KPIs for the new dashboard and PDF report."""
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)

        total_revenue = get(21) + get(22)
        change_in_inv = get(16, 'PY') - get(16, 'CY') if year == 'CY' else 0
        depreciation_node = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation', {})
        depreciation = depreciation_node.get(year, 0) if depreciation_node else 0
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
    **Opportunities:**
    - *Growth Funding:* The stable financial structure provides an opportunity to raise further capital.
    **Threats:**
    - *Market Competition:* High profitability may attract competitors.
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
    # ... (rest of PDF creation logic is kept but won't be called)
    return bytes(pdf.output(dest='S'))

# --- MAIN APP UI ---

st.set_page_config(page_title="Financial Dashboard - DIAGNOSTIC MODE", page_icon="ախ", layout="wide")

# --- Initialize Session State ---
if 'diagnostic_ran' not in st.session_state:
    st.session_state.diagnostic_ran = False
if 'source_df' not in st.session_state:
    st.session_state.source_df = None

# --- Neumorphic CSS Styles ---
# (Your CSS is kept as is, but will not be fully utilized in diagnostic mode)
st.markdown("""<style>... a lot of css ...</style>""", unsafe_allow_html=True) # Your CSS here

# --- SIDEBAR UI CONTROLS ---
with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", "My Company Inc.")

    # --- MODIFIED BUTTON LOGIC ---
    if st.button("Run Diagnostic", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Agent 1 (Data Intake): Reading and parsing Excel file..."):
                # We will ONLY run the first agent and store its output.
                st.session_state.source_df = intelligent_data_intake_agent(uploaded_file)
                st.session_state.diagnostic_ran = True # Mark that the diagnostic has run
        else:
            st.warning("Please upload a file and enter a company name.")


# --- MAIN DISPLAY AREA ---

st.markdown("<div class='main-title'><h1>Schedule III Financial Dashboard</h1></div>", unsafe_allow_html=True)

# --- NEW DIAGNOSTIC DISPLAY LOGIC ---
if st.session_state.diagnostic_ran:
    
    st.error("DIAGNOSTIC MODE ENABLED: The normal dashboard is disabled.")
    st.subheader("Raw Data Extracted by Agent 1")
    st.write("This table shows exactly what the first agent was able to read from your Excel file. The rest of the pipeline has been stopped.")
    
    source_df = st.session_state.source_df
    
    if source_df is None:
        st.error("Agent 1 returned `None`. This means a critical error occurred during file reading. Please check the application logs for more details.")
    elif source_df.empty:
        st.warning("Agent 1 returned an EMPTY table. This means it could not find any rows of data to extract. Please check that your Excel file has data and that the headers (like 'Particulars', 'Amount', 'Liabilities', 'Assets') are present and spelled correctly.")
    else:
        st.success(f"Agent 1 successfully extracted {len(source_df)} rows. Please review the data below for correctness.")
        st.dataframe(source_df, use_container_width=True)
        st.subheader("Please Analyze This Table")
        st.write("Look at the table above and tell me what is wrong with it. For example:")
        st.markdown("""
        - **"The table is empty."**
        - **"The `Amount_CY` column is all zeros."**
        - **"The `Particulars` column has strange names like 'Liabilities|Unnamed: 1'."**
        - **"The table is missing half of the data."**
        """)
        st.write("Your answer will allow me to write the final, perfect fix for `agent_1_intake.py`.")

else:
    # This is the default view before you click the button
    st.info("Please upload your Excel file and click 'Run Diagnostic' to begin analysis.")
    # The original dashboard code is now skipped.
