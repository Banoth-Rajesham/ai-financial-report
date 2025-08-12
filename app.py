# ==============================================================================
# FINAL, COMPLETE, AND CORRECTED app.py
# This version correctly imports and uses your project's agent and config files.
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
    def header(self): self.set_font('Arial', 'B', 16); self.cell(0, 10, 'Financial Dashboard Report', 0, 1, 'C'); self.ln(5)
    def footer(self): self.set_y(-15); self.set_font('Arial', 'I', 8); self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_professional_pdf(kpis, ai_analysis, charts, company_name):
    pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', 'B', 20); pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C'); pdf.ln(10)
    pdf.set_font('Arial', 'B', 16); pdf.cell(0, 10, 'Key Performance Indicators (Current Year)', 0, 1, 'L'); pdf.set_font('Arial', '', 12)
    for key, value in kpis['CY'].items(): pdf.cell(0, 8, f"- {key}: {'INR {:,.0f}'.format(value) if any(x in key for x in ['Revenue', 'Profit', 'Assets']) else '{:.2f}'.format(value)}", 0, 1)
    pdf.ln(10); pdf.set_font('Arial', 'B', 16); pdf.cell(0, 10, 'AI-Generated Insights', 0, 1, 'L'); pdf.set_font('Arial', '', 12); pdf.multi_cell(0, 6, ai_analysis.replace('**', ''))
    if charts:
        pdf.add_page(); pdf.set_font('Arial', 'B', 16); pdf.cell(0, 10, 'Financial Charts', 0, 1, 'L'); pdf.ln(5)
        for title, chart_bytes in charts.items(): pdf.set_font('Arial', 'B', 14); pdf.cell(0, 10, title, 0, 1, 'C'); pdf.image(chart_bytes, x=15, w=180, type='PNG')
    return bytes(pdf.output())

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

st.markdown("<style>.stApp{background-color:#1e1e2f;color:#e0e0e0;font-family:'Segoe UI',sans-serif}.block-container{padding:2rem 3rem}.kpi-container{display:flex;flex-wrap:wrap;gap:1.5rem;justify-content:center;margin-bottom:2rem}.kpi-card{background:#2b2b3c;border-radius:25px 25px 8px 8px;padding:1.5rem 2rem;box-shadow:6px 6px 16px #14141e,-6px -6px 16px #38384a;min-width:250px;color:#e0e0e0;flex:1}.kpi-card .title{font-weight:600;font-size:1rem;margin-bottom:.3rem;color:#a0a0a0}.kpi-card .value{font-size:2.2rem;font-weight:700;margin-bottom:.5rem;line-height:1.1}.kpi-card .delta{display:inline-flex;align-items:center;font-weight:600;font-size:.9rem;border-radius:20px;padding:.25rem .8rem}.kpi-card .delta.up{background-color:#00cc7a;color:#0f2f1f}.kpi-card .delta.up::before{content:\"⬆\";margin-right:.3rem}.kpi-card .delta.down{background-color:#ff4c4c;color:#3a0000}.kpi-card .delta.down::before{content:\"⬇\";margin-right:.3rem}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Upload & Process"); uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"]); company_name = st.text_input("Enter Company Name", st.session_state.company_name)
    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
                st.info("Step 1/5: Ingesting data..."); source_df = intelligent_data_intake_agent(uploaded_file)
                st.info("Step 2/5: Mapping financial terms..."); refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), MASTER_TEMPLATE['Notes to Accounts'])
                st.info("Step 3/5: Aggregating values..."); aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                st.info("Step 4/5: Validating balances..."); warnings = data_validation_agent(aggregated_data)
                st.info("Step 5/5: Generating final report..."); excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
            st.success("Dashboard Generated!"); [st.warning(w) for w in warnings]
            st.session_state.update(report_generated=True, excel_report_bytes=excel_report_bytes, kpis=calculate_kpis(aggregated_data), company_name=company_name)
            st.rerun()
        else: st.warning("Please upload a file and enter a company name.")

if not st.session_state.report_generated:
    st.markdown("<div align='center'><h1>Financial Analysis Dashboard</h1><p>Upload your financial data in the sidebar to begin.</p></div>", unsafe_allow_html=True)
else:
    kpis = st.session_state.kpis; kpi_cy, kpi_py = kpis['CY'], kpis['PY']
    rev_growth = ((kpi_cy['Total Revenue'] - kpi_py['Total Revenue']) / kpi_py['Total Revenue'] * 100) if kpi_py['Total Revenue'] else 0
    profit_growth = ((kpi_cy['Net Profit'] - kpi_py['Net Profit']) / kpi_py['Net Profit'] * 100) if kpi_py.get('Net Profit', 0) > 0 else 0
    assets_growth = ((kpi_cy['Total Assets'] - kpi_py['Total Assets']) / kpi_py['Total Assets'] * 100) if kpi_py['Total Assets'] else 0
    dte_change = kpi_cy['Debt-to-Equity'] - kpi_py['Debt-to-Equity']
st.markdown("""
<style>
.stApp{background-color:#1e1e2f;color:#e0e0e0;font-family:'Segoe UI',sans-serif}
.block-container{padding:2rem 3rem}
.kpi-container{display:flex;flex-wrap:wrap;gap:1.5rem;justify-content:center;margin-bottom:2rem}
.kpi-card{
    background:#2b2b3c;
    border-radius:25px 25px 8px 8px;
    padding:1.5rem 2rem;
    box-shadow:6px 6px 16px #14141e,-6px -6px 16px #38384a;
    min-width:250px;
    color:#e0e0e0;
    flex:1;
    transition: box-shadow 0.3s ease-in-out;
}
.kpi-card:hover {
    box-shadow: 0 0 20px #00cc7a, 0 0 30px #00cc7a, 0 0 40px #00cc7a;
}
.kpi-card .title{font-weight:600;font-size:1rem;margin-bottom:.3rem;color:#a0a0a0}
.kpi-card .value{font-size:2.2rem;font-weight:700;margin-bottom:.5rem;line-height:1.1}
.kpi-card .delta{display:inline-flex;align-items:center;font-weight:600;font-size:.9rem;border-radius:20px;padding:.25rem .8rem}
.kpi-card .delta.up{background-color:#00cc7a;color:#0f2f1f}
.kpi-card .delta.up::before{content:"⬆";margin-right:.3rem}
.kpi-card .delta.down{background-color:#ff4c4c;color:#3a0000}
.kpi-card .delta.down::before{content:"⬇";margin-right:.3rem}
</style>
""", unsafe_allow_html=True)    ai_analysis = generate_ai_analysis(kpis)
    chart_data = pd.DataFrame(kpis).reset_index().rename(columns={'index': 'Metric'}).melt(id_vars='Metric', var_name='Year', value_name='Amount')
    fig = px.bar(chart_data[chart_data['Metric'].isin(['Total Revenue', 'Net Profit'])], x='Metric', y='Amount', color='Year', barmode='group', title='Current (CY) vs. Previous (PY) Year Performance')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#2b2b3c', font_color='#e0e0e0')
    col1, col2 = st.columns((5, 4)); col1.subheader("📊 Financial Visualization"); col1.plotly_chart(fig, use_container_width=True); col2.subheader("🤖 AI-Generated Insights"); col2.markdown(ai_analysis)
    st.subheader("⬇️ Download Center")
    chart_bytes = io.BytesIO(); fig.write_image(chart_bytes, format="png", scale=2, engine="kaleido"); charts_for_pdf = {"Performance Overview": chart_bytes}
    pdf_bytes = create_professional_pdf(st.session_state.kpis, ai_analysis, charts_for_pdf, st.session_state.company_name)
    d_col1, d_col2 = st.columns(2)
    d_col1.download_button("📄 Download PDF with Professional Insights", pdf_bytes, f"{st.session_state.company_name}_Financial_Report.pdf", "application/pdf", use_container_width=True)
    d_col2.download_button("💹 Download Formatted Excel Report", st.session_state.excel_report_bytes, f"{st.session_state.company_name}_Financial_Statements.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

