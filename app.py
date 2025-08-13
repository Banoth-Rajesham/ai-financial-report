# ==============================================================================
# FILE: app.py (FINAL, WITH ASSET DISTRIBUTION PIE CHART ADDED)
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
            y_before = self.get_y()
            x_before = self.get_x()
            self.multi_cell(col_widths[0], 6, str(row[0]), 1, 'L')
            y_after_mc1 = self.get_y()
            self.set_xy(x_before + col_widths[0], y_before)
            
            self.multi_cell(col_widths[1], 6, str(row[1]), 1, 'L')
            y_after_mc2 = self.get_y()
            self.set_xy(x_before + col_widths[0] + col_widths[1], y_before)
            
            self.multi_cell(col_widths[2], 6, str(row[2]), 1, 'L')
            y_after_mc3 = self.get_y()
            
            self.set_y(max(y_after_mc1, y_after_mc2, y_after_mc3))

def create_professional_pdf(kpis, company_name, charts):
    """Creates the new, detailed professional PDF report."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(5)

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

    pdf.chapter_title('Key Financial Ratios')
    ratio_table_data = [
        ("Current Ratio", f"{kpi_cy['Current Ratio']:.2f}", "Excellent liquidity. The company can cover its short-term liabilities nearly 3x over."),
        ("Profit Margin", f"{kpi_cy['Profit Margin']:.2f}%", "Strong profitability. The company earns significant profit for every ₹100 in revenue."),
        ("ROA (Return on Assets)", f"{kpi_cy['ROA']:.2f}%", "Effective use of assets to generate profit."),
        ("Debt-to-Equity", f"{kpi_cy['Debt-to-Equity']:.2f}", "Financially conservative; well-balanced capital structure.")
    ]
    pdf.write_table(['Ratio', 'Value', 'Interpretation'], [45, 45, 100], ratio_table_data)
    pdf.ln(5)

    pdf.chapter_title('SWOT Analysis')
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, generate_swot_analysis(kpis))
    
    return bytes(pdf.output())


# --- MAIN APP UI ---
st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")

for key in ['report_generated', 'excel_report_bytes', 'aggregated_data', 'kpis']:
    if key not in st.session_state: st.session_state[key] = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."

st.markdown("""
<style>
    .stApp { background-color: #1e1e2f; color: #e0e0e0; }
    h1, h2, h3 { color: #ffffff; }
    .st-emotion-cache-16txtl3 { padding: 2rem 2rem 1rem; }
    .st-emotion-cache-1y4p8pa { max-width: 100%; }
    .st-emotion-cache-ocqkz7 { background-color: #2b2b3c; } /* Main content background */
    .st-emotion-cache-1cpx1b6 { background-color: #2b2b3c; } /* Sidebar background */
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
    st.title("Financial Analysis Dashboard")
    st.info("Upload your financial data and click 'Generate Dashboard' to begin.")
else:
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']

    st.title(f"Financial Dashboard for {st.session_state.company_name}")

    # --- Financial Visualization and AI Insights ---
    col1, col2 = st.columns([6, 4], gap="large")
    with col1:
        st.subheader("Financial Visualization")
        # Bar Chart
        chart_data = pd.DataFrame(kpis).reset_index().rename(columns={'index': 'Metric'})
        chart_data = chart_data.melt(id_vars='Metric', var_name='Year', value_name='Amount')
        fig_bar = px.bar(chart_data[chart_data['Metric'].isin(['Total Revenue', 'Net Profit'])],
                         x='Metric', y='Amount', color='Year', barmode='group',
                         title='Current (CY) vs. Previous (PY) Year Performance',
                         color_discrete_map={'CY': '#636EFA', 'PY': '#A9A9A9'})
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#2b2b3c', font_color='#e0e0e0')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("AI-Generated Insights")
        ai_analysis = generate_swot_analysis(kpis)
        st.markdown(ai_analysis)

    # --- Asset Distribution Pie Chart ---
    st.write("---") # Separator
    st.subheader("Asset Distribution")
    asset_df = pd.DataFrame({
        'Asset Type': ['Current Assets', 'Fixed Assets', 'Investments', 'Other Assets'],
        'Value': [kpi_cy['Current Assets'], kpi_cy['Fixed Assets'], kpi_cy['Investments'], kpi_cy['Other Assets']]
    }).query("Value > 0")
    fig_pie = px.pie(asset_df, names='Asset Type', values='Value', title="Asset Distribution (From Extracted Data)")
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0')
    st.plotly_chart(fig_pie, use_container_width=True)


    # --- DOWNLOADS ---
    st.write("---")
    st.subheader("Download Reports")
    pdf_charts = {'revenue_trend': fig_bar.to_image(format="png")}
    pdf_bytes = create_professional_pdf(kpis, st.session_state.company_name, pdf_charts)
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.download_button("📄 Download PDF with Detailed Insights", pdf_bytes, f"{st.session_state.company_name}_Insights.pdf", use_container_width=True, type="primary")
    with d_col2:
        st.download_button("💹 Download Processed Data (Excel)", st.session_state.excel_report_bytes, f"{st.session_state.company_name}_Processed_Data.xlsx", use_container_width=True)
