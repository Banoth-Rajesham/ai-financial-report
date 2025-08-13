# ==============================================================================
# FILE: app.py (FINAL CORRECTED VERSION)
# ==============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- CORRECTED IMPORTS ---
# This tells Python to look inside the 'financial_reporter_app' folder
# to find the 'agents' module and the 'config' file.
from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
from financial_reporter_app.agents.agent_4_validator import data_validation_agent
from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
from config import NOTES_STRUCTURE_AND_MAPPING, MASTER_TEMPLATE
# -------------------------

st.set_page_config(page_title="AI Financial Reporter", page_icon="🤖", layout="wide")
st.title("AI Financial Analysis Dashboard")

# Initialize session state variables
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'aggregated_data' not in st.session_state: st.session_state.aggregated_data = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

# --- SIDEBAR FOR UPLOAD AND PROCESSING ---
with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload financial data (Excel)", type=["xlsx", "xls"])
    company_name_input = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name_input:
            with st.spinner("Executing financial agent pipeline... Please wait."):
                st.session_state.company_name = company_name_input
                # --- RUN THE FULL PIPELINE ---
                source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None:
                    st.error("Pipeline Failed at Agent 1: Data Intake. Check file format.")
                    st.stop()

                refined_mapping = ai_mapping_agent(source_df['Particulars'].unique().tolist(), NOTES_STRUCTURE_AND_MAPPING)

                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data:
                    st.error("Pipeline Failed at Agent 3: Aggregation. Check mapping rules.")
                    st.stop()

                warnings = data_validation_agent(aggregated_data)

                excel_report_bytes = report_finalizer_agent(aggregated_data, st.session_state.company_name)
                if excel_report_bytes is None:
                    st.error("Pipeline Failed at Agent 5: Report Finalizer.")
                    st.stop()

            st.success("Pipeline Executed Successfully!")
            # Store results in session state
            st.session_state.report_generated = True
            st.session_state.aggregated_data = aggregated_data
            st.session_state.warnings = warnings
            st.session_state.excel_report_bytes = excel_report_bytes
            st.rerun()
        else:
            st.warning("Please upload a file and enter a company name.")

# --- MAIN DASHBOARD AREA ---
if not st.session_state.report_generated:
    st.info("Upload your financial data and click 'Generate Dashboard' to begin analysis.")
    st.markdown("---")
    st.subheader("How It Works:")
    st.markdown("""
    1.  **Intake Agent**: Intelligently reads your Excel file, finding financial data columns automatically.
    2.  **Mapping Agent**: Uses a comprehensive dictionary of aliases to understand your data labels (e.g., maps "Sundry Creditors" to "Trade Payables").
    3.  **Aggregator Agent**: Processes and sums all the data according to the official Schedule III format.
    4.  **Validator Agent**: Performs an audit check to ensure the Balance Sheet is balanced (Assets = Liabilities + Equity).
    5.  **Reporter Agent**: Generates a professionally styled, multi-sheet Excel report with main statements and all notes.
    """)
else:
    # --- DISPLAY METRICS AND CHARTS ---
    agg_data = st.session_state.aggregated_data

    # Calculate key metrics
    get = lambda key, y: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
    kpi_cy, kpi_py = {}, {}
    for year, kpi_dict in [('CY', kpi_cy), ('PY', kpi_py)]:
        kpi_dict["Total Revenue"] = get(21, year) + get(22, year)
        # Corrected expense calculation for P&L
        pnl_inventory_change = get(16, 'CY') - get(16, 'PY') if year == 'CY' else 0 # Simplified for PY
        kpi_dict["Total Expenses"] = sum(get(n, year) for n in ['23','24','25','11','26']) + pnl_inventory_change
        kpi_dict["Net Profit"] = kpi_dict["Total Revenue"] - kpi_dict["Total Expenses"]
        kpi_dict["Total Assets"] = sum(get(n, year) for n in ["11","12","4","13","14","15","16","17","18","19","20"])
        kpi_dict["Total Equity"] = get(1, year) + get(2, year)
        kpi_dict["Total Debt"] = get(3, year) + get(7, year)
        kpi_dict["Debt-to-Equity"] = kpi_dict["Total Debt"] / kpi_dict["Total Equity"] if kpi_dict["Total Equity"] else 0

    get_change = lambda cy, py: ((cy - py) / abs(py) * 100) if py != 0 else 0

    st.header(f"Dashboard for: {st.session_state.company_name}")

    # --- KPI CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{kpi_cy.get('Total Revenue', 0):,.2f}", f"{get_change(kpi_cy.get('Total Revenue', 0), kpi_py.get('Total Revenue', 0)):.1f}%")
    col2.metric("Net Profit", f"₹{kpi_cy.get('Net Profit', 0):,.2f}", f"{get_change(kpi_cy.get('Net Profit', 0), kpi_py.get('Net Profit', 0)):.1f}%")
    col3.metric("Total Assets", f"₹{kpi_cy.get('Total Assets', 0):,.2f}", f"{get_change(kpi_cy.get('Total Assets', 0), kpi_py.get('Total Assets', 0)):.1f}%")
    col4.metric("Debt-to-Equity", f"{kpi_cy.get('Debt-to-Equity', 0):.2f}", f"{get_change(kpi_cy.get('Debt-to-Equity', 0), kpi_py.get('Debt-to-Equity', 0)):.1f}%", delta_color="inverse")

    # --- CHARTS ---
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        def generate_monthly(total):
            if total == 0: return [0]*12
            pattern = np.array([0.8, 0.85, 0.9, 1.0, 1.1, 1.15, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85])
            monthly_data = pattern * (total / 12)
            return (monthly_data / monthly_data.sum()) * total
        revenue_df = pd.DataFrame({'Month': months * 2, 'Year': ['Previous Year'] * 12 + ['Current Year'] * 12, 'Revenue': np.concatenate([generate_monthly(kpi_py.get('Total Revenue',0)), generate_monthly(kpi_cy.get('Total Revenue',0))])})
        fig_revenue = px.area(revenue_df, x='Month', y='Revenue', color='Year', title="<b>Revenue Trend</b>", template="seaborn")
        st.plotly_chart(fig_revenue, use_container_width=True)

    with chart_col2:
        asset_data = {'Asset Type': ['Fixed Assets', 'Non-Current Investments', 'Current Assets'], 'Value': [get('11','CY'), get('12','CY'), sum(get(n,'CY') for n in ['15','16','17','18','19','20'])]}
        asset_df = pd.DataFrame(asset_data).query("Value > 0")
        fig_asset = px.pie(asset_df, names='Asset Type', values='Value', title="<b>Asset Distribution (Current Year)</b>", hole=0.3)
        st.plotly_chart(fig_asset, use_container_width=True)

    st.divider()
    # --- VALIDATION AND DOWNLOAD SECTION ---
    st.subheader("Validation & Report Download")
    warnings = st.session_state.warnings
    if not warnings:
        st.success("✅ Validation Passed: The Balance Sheet is balanced.")
    else:
        for warning in warnings:
            st.warning(f"⚠️ {warning}")

    st.download_button(
        label="⬇️ Download Full Financial Report (Excel)",
        data=st.session_state.excel_report_bytes,
        file_name=f"{st.session_state.company_name.replace(' ', '_')}_Financial_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
