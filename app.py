# ==============================================================================
# FILE: app.py (FINAL, WITH KPI HOVER GLOW EFFECT)
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
    """Calculates key performance indicators for the dashboard from the REAL aggregated data."""
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)

        total_revenue = get(21) + get(22)
        change_in_inv = get(16, 'PY') - get(16, 'CY') if year == 'CY' else 0
        depreciation = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation', {}).get(year, 0)
        total_expenses = get(23) + change_in_inv + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)

        kpis[year] = {
            "Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets,
            "Debt-to-Equity": total_debt / total_equity if total_equity else 0
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
        pdf.cell(0, 8, f"- {key}: {'INR {:,.0f}'.format(value) if 'Revenue' in key or 'Profit' in key or 'Assets' in key else '{:.2f}'.format(value)}", 0, 1)
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
        for title, chart_bytes in charts.items():
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, title, 0, 1, 'C')
            pdf.image(chart_bytes, x=15, w=180, type='PNG')
            pdf.ln(5)

    return bytes(pdf.output())

# --- MAIN APP UI ---

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# Initialize session state variables
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'aggregated_data' not in st.session_state: st.session_state.aggregated_data = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

# --- Neumorphic CSS Styles with Hover Glow Effect ---
st.markdown("""
<style>
    .stApp { background-color: #1e1e2f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .block-container { padding: 2rem 3rem; }
    .main-title h1 { font-weight: 700; color: #e0e0e0; font-size: 2.2rem; text-align: center; }
    .main-title p { color: #b0b0b0; font-size: 1.1rem; text-align: center; margin-bottom: 2rem; }
    .kpi-container { display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: center; margin-bottom: 2rem; }
    .kpi-card {
        background: #2b2b3c;
        border-radius: 25px 25px 8px 8px;
        padding: 1.5rem 2rem;
        box-shadow: 6px 6px 16px #14141e, -6px -6px 16px #38384a;
        min-width: 250px;
        color: #e0e0e0;
        flex: 1;
        border-bottom: 4px solid #4a4a6a;
        /* Added transition for smooth effect */
        transition: all 0.3s ease-in-out;
    }
    .kpi-card .title { font-weight: 600; font-size: 1rem; margin-bottom: 0.3rem; color: #a0a0a0; }
    .kpi-card .value { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; line-height: 1.1; }
    .kpi-card .delta { display: inline-flex; align-items: center; font-weight: 600; font-size: 0.9rem; border-radius: 20px; padding: 0.25rem 0.8rem; }
    .kpi-card .delta.up { background-color: #00cc7a; color: #0f2f1f; }
    .kpi-card .delta.up::before { content: "⬆"; margin-right: 0.3rem; }
    .kpi-card .delta.down { background-color: #ff4c4c; color: #3a0000; }
    .kpi-card .delta.down::before { content: "⬇"; margin-right: 0.3rem; }

    /* --- THIS IS THE NEW CODE FOR THE HOVER GLOW --- */
    .kpi-card:hover {
        transform: translateY(-5px); /* Lifts the card up slightly */
        box-shadow: 10px 10px 20px #14141e, -10px -10px 20px #38384a;
    }
    .kpi-container .kpi-card:nth-child(1):hover { border-bottom-color: #00aaff; } /* Revenue: Blue glow */
    .kpi-container .kpi-card:nth-child(2):hover { border-bottom-color: #00ff7f; } /* Profit: Green glow */
    .kpi-container .kpi-card:nth-child(3):hover { border-bottom-color: #ffcc00; } /* Assets: Yellow glow */
    .kpi-container .kpi-card:nth-child(4):hover { border-bottom-color: #ff5555; } /* Debt-to-Equity: Red glow */

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
                st.info("Step 1/5: Ingesting data...")
                source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None:
                    st.error("Pipeline Failed: Data Intake. The Excel file might be corrupted or in an unsupported format.")
                    st.stop()

                st.info("Step 2/5: Mapping financial terms...")
                refined_mapping = ai_mapping_agent(source_df['Particulars'].unique().tolist(), NOTES_STRUCTURE_AND_MAPPING)

                st.info("Step 3/5: Aggregating and propagating values...")
                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data:
                    st.error("Pipeline Failed: Aggregation. Could not process the data using the provided mappings.")
                    st.stop()

                st.info("Step 4/5: Validating financial balances...")
                warnings = data_validation_agent(aggregated_data)

                st.info("Step 5/5: Generating final reports...")
                excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
                if excel_report_bytes is None:
                    st.error("Pipeline Failed: Report Finalizer.")
                    st.stop()

            st.success("Dashboard Generated Successfully!")
            for w in warnings:
                st.warning(w)

            st.session_state.report_generated = True
            st.session_state.aggregated_data = aggregated_data
            st.session_state.company_name = company_name
            st.session_state.excel_report_bytes = excel_report_bytes
            st.session_state.kpis = calculate_kpis(aggregated_data)
            st.rerun()
        else:
            st.warning("Please upload a file and enter a company name.")

# --- MAIN DASHBOARD DISPLAY (Conditionally Rendered) ---
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
    """, unsafe_allow_html=True)

    ai_analysis = generate_ai_analysis(kpis)

    chart_data = pd.DataFrame(kpis).reset_index().rename(columns={'index': 'Metric'})
    chart_data = chart_data.melt(id_vars='Metric', var_name='Year', value_name='Amount')
    fig = px.bar(chart_data[chart_data['Metric'].isin(['Total Revenue', 'Net Profit'])],
                 x='Metric', y='Amount', color='Year', barmode='group',
                 title='Current (CY) vs. Previous (PY) Year Performance')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#2b2b3c', font_color='#e0e0e0')

    col1, col2 = st.columns((5, 4))
    with col1:
        st.subheader("📊 Financial Visualization")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("🤖 AI-Generated Insights")
        st.markdown(ai_analysis)

    st.subheader("⬇️ Download Center")

    chart_bytes = io.BytesIO()
    fig.write_image(chart_bytes, format="png", scale=2, engine="kaleido")
    charts_for_pdf = {"Performance Overview": chart_bytes}

    pdf_bytes = create_professional_pdf(
        kpis=st.session_state.kpis,
        ai_analysis=ai_analysis,
        charts=charts_for_pdf,
        company_name=st.session_state.company_name
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button(
            label="📄 Download PDF with Professional Insights",
            data=pdf_bytes,
            file_name=f"{st.session_state.company_name}_Financial_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with d_col2:
        st.download_button(
            label="💹 Download Excel with Processed Data",
            data=st.session_state.excel_report_bytes,
            file_name=f"{st.session_state.company_name}_Processed_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
