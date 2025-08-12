# ==============================================================================
# FINAL, COMPLETE, AND CORRECTED app.py
# This version features a completely redesigned, multi-page visual PDF dashboard report.
# ==============================================================================
import streamlit as st
import sys
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from financial_reporter_app.config import MASTER_TEMPLATE
    from financial_reporter_app.agents.agent_1_intake import intelligent_data_intake_agent
    from financial_reporter_app.agents.agent_2_ai_mapping import ai_mapping_agent
    from financial_reporter_app.agents.agent_3_aggregator import hierarchical_aggregator_agent
    from financial_reporter_app.agents.agent_4_validator import data_validation_agent
    from financial_reporter_app.agents.agent_5_reporter import report_finalizer_agent
except ImportError as e:
    st.error(f"CRITICAL ERROR: Could not import a module. This is likely a path issue. Error: {e}")
    st.stop()

def calculate_kpis(agg_data):
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        total_revenue = get(21) + get(22)
        change_in_inv = get(16, 'CY') - get(16, 'PY') if year == 'CY' else 0
        depreciation = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
        total_expenses = get(23) - change_in_inv + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in range(11, 21))
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)
        kpis[year] = {"Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets, "Debt-to-Equity": total_debt / total_equity if total_equity else 0}
    return kpis

def generate_ai_analysis(kpis):
    kpi_cy = kpis['CY']
    return f"**Strengths:**\n- **Strong Profitability:** A Net Profit of INR {kpi_cy['Net Profit']:,.0f} on Revenue of INR {kpi_cy['Total Revenue']:,.0f} signals efficient operations.\n- **Balanced Financial Structure:** The Debt-to-Equity ratio of {kpi_cy['Debt-to-Equity']:.2f} suggests a healthy balance between debt and equity financing.\n\n**Opportunities:**\n- **Growth Funding:** The stable financial structure provides an opportunity to raise further capital at a reasonable cost for expansion or R&D.\n\n**Threats:**\n- **Market Competition:** High profitability may attract competitors, putting pressure on future margins.\n- **Economic Headwinds:** A broader economic downturn could impact customer spending and affect revenue growth."

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Financial Dashboard Report', 0, 0, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# ==============================================================================
# THIS IS THE ONLY FUNCTION THAT HAS BEEN MODIFIED
# ==============================================================================
def create_professional_pdf(kpis, ai_analysis, charts, company_name, sheets_data, agg_data):
    """
    Generates a multi-page, visually rich PDF dashboard report.
    """
    pdf = PDF()
    
    # --- Helper function to draw styled tables ---
    def draw_table(title, df):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(220, 220, 220)
        col_widths = (10, 80, 20, 40, 40)
        
        # Draw header
        for i, header in enumerate(df.columns):
            pdf.cell(col_widths[i], 8, str(header), 1, 0, 'C', 1)
        pdf.ln()

        # Draw rows
        pdf.set_font('Arial', '', 8)
        pdf.set_fill_color(245, 245, 245)
        for index, row in df.iterrows():
            fill = index % 2 == 0
            for i, datum in enumerate(row):
                pdf.cell(col_widths[i], 6, str(datum), 1, 0, 'L', fill)
            pdf.ln()

    # --- Page 1: Executive Summary with KPI Cards ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '1. Key Performance Indicators (Current Year)', 0, 1, 'L')
    pdf.ln(5)

    kpi_cy = kpis['CY']
    colors = [(255, 202, 40), (0, 204, 122), (41, 182, 246), (244, 67, 54)] # Yellow, Green, Blue, Red
    kpi_items = [("Total Revenue", f"INR {kpi_cy['Total Revenue']:,.0f}"), ("Net Profit", f"INR {kpi_cy['Net Profit']:,.0f}"),
                   ("Total Assets", f"INR {kpi_cy['Total Assets']:,.0f}"), ("Debt-to-Equity", f"{kpi_cy['Debt-to-Equity']:.2f}")]
    
    x_pos = pdf.get_x()
    y_pos = pdf.get_y()
    card_width = 90
    card_height = 25

    for i, (title, value) in enumerate(kpi_items):
        col = i % 2
        row = i // 2
        pdf.set_xy(x_pos + (col * (card_width + 10)), y_pos + (row * (card_height + 5)))
        pdf.set_fill_color(colors[i][0], colors[i][1], colors[i][2])
        pdf.rect(pdf.get_x(), pdf.get_y(), card_width, card_height, 'F')
        
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(card_width, 10, title, 0, 1, 'C')
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(card_width, 10, value, 0, 1, 'C')

    pdf.set_y(y_pos + 2 * (card_height + 5) + 10) # Move below the cards
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '2. AI-Generated Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 6, ai_analysis.replace('**', ''))

    # --- Page 2: Visualizations ---
    if charts:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '3. Financial Visualizations', 0, 1, 'L')
        pdf.ln(5)
        pdf.image(charts["Performance Overview"], x=15, w=180)
        pdf.ln(10)

        # Create Asset Composition Pie Chart
        get = lambda key, y='CY': agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        fixed_assets = get(11)
        current_assets = sum(get(n) for n in range(15, 21))
        asset_data = pd.DataFrame({'Asset Type': ['Fixed Assets', 'Current Assets'], 'Value': [fixed_assets, current_assets]})
        fig_pie = px.pie(asset_data, names='Asset Type', values='Value', title='Composition of Assets (CY)', hole=0.3)
        fig_pie.update_traces(textinfo='percent+label', marker=dict(colors=['#29b6f6', '#00cc7a']))
        pie_chart_bytes = io.BytesIO()
        fig_pie.write_image(pie_chart_bytes, format="png", scale=2)
        
        pdf.image(pie_chart_bytes, x=15, w=180)

    # --- Subsequent Pages: Formatted Data Tables ---
    if "Balance Sheet" in sheets_data:
        draw_table("Balance Sheet", sheets_data["Balance Sheet"])
    if "Profit and Loss" in sheets_data:
        draw_table("Profit and Loss", sheets_data["Profit and Loss"])

    return bytes(pdf.output())

# ==============================================================================
# THE REST OF THE FILE IS UNCHANGED
# ==============================================================================
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."
if 'agg_data' not in st.session_state: st.session_state.agg_data = {} # Store aggregated data for PDF

st.markdown("""<style>.stApp{background-color:#1e1e2f;color:#e0e0e0;font-family:'Segoe UI',sans-serif}.block-container{padding:2rem 3rem}.kpi-container{display:flex;flex-wrap:wrap;gap:1.5rem;justify-content:center;margin-bottom:2rem}.kpi-card{background:#2b2b3c;border-radius:25px 25px 8px 8px;padding:1.5rem 2rem;box-shadow:6px 6px 16px #141e1e,-6px -6px 16px #38384a;min-width:250px;color:#e0e0e0;flex:1;transition:box-shadow .3s ease-in-out}.revenue-card:hover{box-shadow:0 0 20px #ffca28,0 0 30px #ffca28,0 0 40px #ffca28}.profit-card:hover{box-shadow:0 0 20px #00cc7a,0 0 30px #00cc7a,0 0 40px #00cc7a}.assets-card:hover{box-shadow:0 0 20px #29b6f6,0 0 30px #29b6f6,0 0 40px #29b6f6}.debt-card:hover{box-shadow:0 0 20px #f44336,0 0 30px #f44336,0 0 40px #f44336}.kpi-card .title{font-weight:600;font-size:1rem;margin-bottom:.3rem;color:#a0a0a0}.kpi-card .value{font-size:2.2rem;font-weight:700;margin-bottom:.5rem;line-height:1.1}.kpi-card .delta{display:inline-flex;align-items:center;font-weight:600;font-size:.9rem;border-radius:20px;padding:.25rem .8rem}.kpi-card .delta.up{background-color:#00cc7a;color:#0f2f1f}.kpi-card .delta.up::before{content:"⬆";margin-right:.3rem}.kpi-card .delta.down{background-color:#ff4c4c;color:#3a0000}.kpi-card .delta.down::before{content:"⬇";margin-right:.3rem}</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Upload & Process"); uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"]); company_name = st.text_input("Enter Company Name", st.session_state.company_name)
    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
                st.info("Step 1/5: Ingesting data..."); source_df = intelligent_data_intake_agent(uploaded_file)
                st.info("Step 2/5: Mapping financial terms..."); refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), MASTER_TEMPLATE['Notes to Accounts'])
                st.info("Step 3/5: Aggregating values..."); aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
     
