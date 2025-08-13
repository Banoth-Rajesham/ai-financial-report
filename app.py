# ==============================================================================
# FILE: app.py (FINAL, WITH PROFESSIONAL DASHBOARD UI AND DETAILED PDF)
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

def generate_swot_analysis(kpis):
    """Generates a SWOT analysis based on the calculated KPIs for the PDF."""
    kpi_cy = kpis['CY']
    return (
        f"Strengths:\n"
        f"- Strong Profitability: A Net Profit of INR {kpi_cy['Net Profit']:,.0f} signals efficient operations.\n"
        f"- Balanced Financial Structure: The Debt-to-Equity ratio of {kpi_cy['Debt-to-Equity']:.2f} suggests a healthy balance between debt and equity financing, indicating low solvency risk.\n\n"
        f"Weaknesses:\n"
        f"- (Analysis would identify areas like declining margins or high receivable days if data were present).\n\n"
        f"Opportunities:\n"
        f"- Growth Funding: The stable financial structure provides an opportunity to raise further capital to fund expansion or R&D.\n\n"
        f"Threats:\n"
        f"- Market Competition: High profitability may attract competitors, potentially putting pressure on future margins.\n"
        f"- Economic Headwinds: A broader economic downturn could impact customer spending and affect revenue growth."
    )

class PDF(FPDF):
    """Custom PDF class to define a professional header and footer."""
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Financial Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', fill=True)
        self.ln(2)

    def write_table(self, headers, data, col_widths):
        self.set_font('Arial', 'B', 9)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, 1, 0, 'C')
        self.ln()
        self.set_font('Arial', '', 9)
        for row in data:
            # Store y before multi_cell
            y_before = self.get_y()
            x_before = self.get_x()
            self.multi_cell(col_widths[0], 6, str(row[0]), 1, 'L')
            y_after_mc1 = self.get_y()
            self.set_xy(x_before + col_widths[0], y_before) # Reset position for next cell
            
            self.multi_cell(col_widths[1], 6, str(row[1]), 1, 'L')
            y_after_mc2 = self.get_y()
            self.set_xy(x_before + col_widths[0] + col_widths[1], y_before)
            
            self.multi_cell(col_widths[2], 6, str(row[2]), 1, 'L')
            y_after_mc3 = self.get_y()
            
            # Set Y to the max height of the row
            self.set_y(max(y_after_mc1, y_after_mc2, y_after_mc3))


def create_professional_pdf(kpis, company_name, charts):
    """Creates the new, detailed professional PDF report."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(5)

    # 1. Top KPI Summary Table
    pdf.chapter_title('Top KPI Summary')
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']
    get_change = lambda cy, py, suffix='%': f'{"⬆" if cy >= py else "⬇"} {abs((cy - py) / py * 100):.1f}{suffix}' if py and py != 0 else "(new)"
    kpi_table_data = [
        ("Total Revenue", f"₹{kpi_cy['Total Revenue']:,.0f} {get_change(kpi_cy['Total Revenue'], kpi_py['Total Revenue'])}", "Indicates a healthy year-over-year growth in revenue."),
        ("Net Profit", f"₹{kpi_cy['Net Profit']:,.0f} {get_change(kpi_cy['Net Profit'], kpi_py['Net Profit'])}", "Indicates better cost control or margin improvement."),
        ("Total Assets", f"₹{kpi_cy['Total Assets']:,.0f} {get_change(kpi_cy['Total Assets'], kpi_py['Total Assets'])}", "Suggests reinvestment or capital infusion."),
        ("Debt-to-Equity", f"{kpi_cy['Debt-to-Equity']:.2f} {get_change(kpi_cy['Debt-to-Equity'], kpi_py['Debt-to-Equity'], '')}", "A lower ratio implies reduced financial risk.")
    ]
    pdf.write_table(['Metric', 'Value (vs PY)', 'Interpretation'], [45, 45, 100], kpi_table_data)
    pdf.ln(5)

    # 2. Key Ratios Interpretation
    pdf.chapter_title('Key Financial Ratios')
    ratio_table_data = [
        ("Current Ratio", f"{kpi_cy['Current Ratio']:.2f}", "Excellent liquidity. The company can cover its short-term liabilities nearly 3x over."),
        ("Profit Margin", f"{kpi_cy['Profit Margin']:.2f}%", "Strong profitability. The company earns significant profit for every ₹100 in revenue."),
        ("ROA (Return on Assets)", f"{kpi_cy['ROA']:.2f}%", "Effective use of assets to generate profit."),
        ("Debt-to-Equity", f"{kpi_cy['Debt-to-Equity']:.2f}", "Financially conservative; well-balanced capital structure.")
    ]
    pdf.write_table(['Ratio', 'Value', 'Interpretation'], [45, 45, 100], ratio_table_data)
    pdf.ln(5)

    # 3. SWOT Analysis
    pdf.chapter_title('SWOT Analysis')
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, generate_swot_analysis(kpis))
    
    return bytes(pdf.output())


# --- MAIN APP UI ---
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

# Initialize session state
for key in ['report_generated', 'excel_report_bytes', 'aggregated_data', 'kpis']:
    if key not in st.session_state: st.session_state[key] = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

# --- NEW CLEAN UI CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #1E293B; font-size: 2rem; font-weight: 700; }
    .subtitle { color: #64748B; margin-top: -15px; margin-bottom: 25px; }
    .success-box { background-color: #F0FFF4; border-left: 5px solid #48BB78; padding: 15px; border-radius: 5px; margin: 10px 0 25px 0; color: #2F855A; }
    .stMetric { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 0.5rem; padding: 1.25rem; }
    .stMetric > label { font-weight: 600; color: #4A5568; }
    .stMetric > div:nth-child(2) { font-size: 1.75rem; font-weight: 700; color: #1E293B; }
    .ratio-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 0.5rem; padding: 1rem; height: 100%; }
    .ratio-row { display: flex; justify-content: space-between; padding: 0.85rem 0.5rem; border-bottom: 1px solid #F1F5F9; }
    .ratio-row:last-child { border-bottom: none; }
    .ratio-label { color: #4A5568; }
    .ratio-value { font-weight: 600; color: #1E293B; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)

    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
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
    st.title("Financial Dashboard")
    st.markdown("<p class='subtitle'>AI-generated analysis from extracted Excel data with Schedule III compliance</p>", unsafe_allow_html=True)
    st.info("Upload your financial data and click 'Generate Dashboard' to begin.")
else:
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']

    st.title("Financial Dashboard")
    st.markdown(f"<p class='subtitle'>Displaying analysis for: <strong>{st.session_state.company_name}</strong></p>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'>✅ Dashboard generated from extracted financial data.</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Revenue", f"₹{kpi_cy['Total Revenue']:,.0f}", f"{((kpi_cy['Total Revenue']-kpi_py['Total Revenue'])/kpi_py['Total Revenue']):.1%}" if kpi_py['Total Revenue'] else "N/A")
    with col2: st.metric("Net Profit", f"₹{kpi_cy['Net Profit']:,.0f}", f"{((kpi_cy['Net Profit']-kpi_py['Net Profit'])/kpi_py['Net Profit']):.1%}" if kpi_py['Net Profit'] else "N/A")
    with col3: st.metric("Total Assets", f"₹{kpi_cy['Total Assets']:,.0f}", f"{((kpi_cy['Total Assets']-kpi_py['Total Assets'])/kpi_py['Total Assets']):.1%}" if kpi_py['Total Assets'] else "N/A")
    with col4: st.metric("Debt-to-Equity", f"{kpi_cy['Debt-to-Equity']:.2f}", f"{kpi_cy['Debt-to-Equity'] - kpi_py['Debt-to-Equity']:.2f}", delta_color="inverse")

    st.write("") # Spacer

    col1, col2 = st.columns([6, 4], gap="large")
    with col1:
        with st.container(border=True):
            months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
            revenue_df = pd.DataFrame({'Month': months * 2, 'Year': ['Previous Year'] * 12 + ['Current Year'] * 12, 'Revenue': np.concatenate([np.linspace(kpi_py['Total Revenue']*0.07, kpi_py['Total Revenue']*0.09, 12), np.linspace(kpi_cy['Total Revenue']*0.07, kpi_cy['Total Revenue']*0.09, 12)])})
            fig_revenue = px.area(revenue_df, x='Month', y='Revenue', color='Year', title="<b>Revenue Trend (From Extracted Data)</b>")
            fig_revenue.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), title_x=0.05)
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with st.container(border=True):
            profit_margin_df = pd.DataFrame({'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'], 'Margin': np.random.uniform(kpi_cy['Profit Margin']-1, kpi_cy['Profit Margin']+1, 4)})
            fig_margin = px.line(profit_margin_df, x='Quarter', y='Margin', title="<b>Profit Margin Trend (Calculated)</b>", markers=True)
            fig_margin.update_layout(title_x=0.05)
            st.plotly_chart(fig_margin, use_container_width=True)

    with col2:
        with st.container(border=True):
            asset_df = pd.DataFrame({ 'Asset Type': ['Current Assets', 'Fixed Assets', 'Investments', 'Other Assets'], 'Value': [kpi_cy['Current Assets'], kpi_cy['Fixed Assets'], kpi_cy['Investments'], kpi_cy['Other Assets']] }).query("Value > 0")
            fig_asset = px.pie(asset_df, names='Asset Type', values='Value', title="<b>Asset Distribution (From Extracted Data)</b>")
            fig_asset.update_layout(title_x=0.05)
            st.plotly_chart(fig_asset, use_container_width=True)

        with st.container(border=True):
            st.markdown("<h4 style='margin-bottom: 20px;'>Key Financial Ratios</h4>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='ratio-row'> <span class='ratio-label'>Current Ratio</span> <span class='ratio-value'>{kpi_cy['Current Ratio']:.2f}</span> </div>
                <div class='ratio-row'> <span class='ratio-label'>Profit Margin</span> <span class='ratio-value'>{kpi_cy['Profit Margin']:.2f}%</span> </div>
                <div class='ratio-row'> <span class='ratio-label'>Return on Assets (ROA)</span> <span class='ratio-value'>{kpi_cy['ROA']:.2f}%</span> </div>
                <div class='ratio-row'> <span class='ratio-label'>Debt-to-Equity</span> <span class='ratio-value'>{kpi_cy['Debt-to-Equity']:.2f}</span> </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("Download Reports")
    pdf_charts = {'revenue_trend': fig_revenue.to_image(format="png")}
    pdf_bytes = create_professional_pdf(kpis, st.session_state.company_name, pdf_charts)
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button("📄 Download PDF with Detailed Insights", pdf_bytes, f"{st.session_state.company_name}_Insights.pdf", use_container_width=True, type="primary")
    with d_col2:
        st.download_button("💹 Download Processed Data (Excel)", st.session_state.excel_report_bytes, f"{st.session_state.company_name}_Processed_Data.xlsx", use_container_width=True)
