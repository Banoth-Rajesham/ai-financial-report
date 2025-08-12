# ==============================================================================
# FINAL, COMPLETE, AND CORRECTED app.py
# ==============================================================================
import streamlit as st
import sys
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import io

try:
    # Get the project's root directory to add it to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)
    
    # Now, all imports will work correctly as the root is in the path
    from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING
    from agents.agent_1_intake import intelligent_data_intake_agent
    from agents.agent_2_ai_mapping import ai_mapping_agent
    from agents.agent_3_aggregator import hierarchical_aggregator_agent
    from agents.agent_4_validator import data_validation_agent
    from agents.agent_5_reporter import report_finalizer_agent
except ImportError as e:
    st.error(f"CRITICAL ERROR: Could not import a module. This is likely a path issue. Error: {e}")
    st.stop()


def calculate_kpis(agg_data):
    kpis = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        total_revenue = get(21) + get(22)
        change_in_inv = (get(16, 'CY') - get(16, 'PY')) if year == 'CY' else 0
        depreciation = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
        total_expenses = get(23) + get(24) + get(25) + depreciation + get(26)
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in range(11, 21))
        total_debt = get(3) + get(7)
        total_equity = get(1) + get(2)
        if total_equity == 0:
            debt_to_equity = 0
        else:
            debt_to_equity = total_debt / total_equity
        kpis[year] = {
            "Total Revenue": total_revenue,
            "Net Profit": net_profit,
            "Total Assets": total_assets,
            "Debt-to-Equity": debt_to_equity
        }
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

def create_professional_pdf(kpis, ai_analysis, charts, company_name, sheets_data, agg_data):
    """
    Generates a multi-page, visually rich PDF dashboard report.
    """
    pdf = PDF()
    def draw_table(title, df):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'L')
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(220, 220, 220)
        num_columns = len(df.columns)
        page_width = pdf.w - 2 * pdf.l_margin
        col_width = page_width / num_columns if num_columns > 0 else 0
        for i, header in enumerate(df.columns):
            pdf.cell(col_width, 8, str(header), 1, 0, 'C', 1)
        pdf.ln()
        pdf.set_font('Arial', '', 8)
        pdf.set_fill_color(245, 245, 245)
        for index, row in df.iterrows():
            fill = index % 2 == 0
            for i, datum in enumerate(row):
                pdf.cell(col_width, 6, str(datum), 1, 0, 'L', fill)
            pdf.ln()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '1. Key Performance Indicators (Current Year)', 0, 1, 'L')
    pdf.ln(5)
    kpi_cy = kpis['CY']
    colors = [(255, 202, 40), (0, 204, 122), (41, 182, 246), (244, 67, 54)]
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
    pdf.set_y(y_pos + 2 * (card_height + 5) + 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '2. AI-Generated Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 6, ai_analysis.replace('**', ''))
    if charts and agg_data:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '3. Financial Visualizations', 0, 1, 'L')
        pdf.ln(5)
        pdf.image(charts["Performance Overview"], x=15, w=180)
        pdf.ln(10)
        get = lambda key, y='CY': agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        fixed_assets = get(11)
        current_assets = sum(get(n) for n in range(15, 21))
        asset_data = pd.DataFrame({'Asset Type': ['Fixed Assets', 'Current Assets'], 'Value': [fixed_assets, current_assets]})
        fig_pie = px.pie(asset_data, names='Asset Type', values='Value', title='Composition of Assets (CY)', hole=0.3)
        fig_pie.update_traces(textinfo='percent+label', marker=dict(colors=['#29b6f6', '#00cc7a']))
        fig_pie.update_layout(title_font_color='black', legend_font_color='black', legend_title_font_color='black')
        pie_chart_bytes = io.BytesIO()
        fig_pie.write_image(pie_chart_bytes, format="png", scale=2)
        pdf.image(pie_chart_bytes, x=15, w=180)
    if sheets_data:
        for sheet_name, df in sheets_data.items():
            if not df.empty:
                draw_table(sheet_name, df)
    return bytes(pdf.output())

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")
if 'report_generated' not in st.session_state: st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state: st.session_state.excel_report_bytes = None
if 'kpis' not in st.session_state: st.session_state.kpis = None
if 'company_name' not in st.session_state: st.session_state.company_name = "My Company Inc."
if 'agg_data' not in st.session_state: st.session_state.agg_data = {}

st.markdown("""<style>.stApp{background-color:#1e1e2f;color:#e0e0e0;font-family:'Segoe UI',sans-serif}.block-container{padding:2rem 3rem}.kpi-container{display:flex;flex-wrap:wrap;gap:1.5rem;justify-content:center;margin-bottom:2rem}.kpi-card{background:#2b2b3c;border-radius:25px 25px 8px 8px;padding:1.5rem 2rem;box-shadow:6px 6px 16px #141e1e,-6px -6px 16px #38384a;min-width:250px;color:#e0e0e0;flex:1;transition:box-shadow .3s ease-in-out}.revenue-card:hover{box-shadow:0 0 20px #ffca28,0 0 30px #ffca28,0 0 40px #ffca28}.profit-card:hover{box-shadow:0 0 20px #00cc7a,0 0 30px #00cc7a,0 0 40px #00cc7a}.assets-card:hover{box-shadow:0 0 20px #29b6f6,0 0 30px #29b6f6,0 0 40px #29b6f6}.debt-card:hover{box-shadow:0 0 20px #f44336,0 0 30px #f44336,0 0 40px #f44336}.kpi-card .title{font-weight:600;font-size:1rem;margin-bottom:.3rem;color:#a0a0a0}.kpi-card .value{font-size:2.2rem;font-weight:700;margin-bottom:.5rem;line-height:1.1}.kpi-card .delta{display:inline-flex;align-items:center;font-weight:600;font-size:.9rem;border-radius:20px;padding:.25rem .8rem}.kpi-card .delta.up{background-color:#00cc7a;color:#0f2f1f}.kpi-card .delta.up::before{content:"⬆";margin-right:.3rem}.kpi-card .delta.down{background-color:#ff4c4c;color:#3a0000}.kpi-card .delta.down::before{content:"⬇";margin-right:.3rem}</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)
    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
                st.info("Step 1/5: Ingesting data...")
                source_df = intelligent_data_intake_agent(uploaded_file)
                st.info("Step 2/5: Mapping financial terms...")
                refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), NOTES_STRUCTURE_AND_MAPPING)
                st.info("Step 3/5: Aggregating values...")
                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                st.info("Step 4/5: Validating balances...")
                warnings = data_validation_agent(aggregated_data)
                st.info("Step 5/5: Generating final report...")
                excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
            st.success("Dashboard Generated!")
            [st.warning(w) for w in warnings]
            st.session_state.update(
                report_generated=True,
                excel_report_bytes=excel_report_bytes,
                kpis=calculate_kpis(aggregated_data),
                company_name=company_name,
                agg_data=aggregated_data
            )
            st.rerun()
        else:
            st.warning("Please upload a file and enter a company name.")

if not st.session_state.report_generated:
    st.markdown("<div align='center'><h1>Financial Analysis Dashboard</h1><p>Upload your financial data in the sidebar to begin.</p></div>", unsafe_allow_html=True)
else:
    kpis = st.session_state.kpis
    kpi_cy, kpi_py = kpis['CY'], kpis['PY']
    rev_growth = ((kpi_cy['Total Revenue'] - kpi_py['Total Revenue']) / kpi_py['Total Revenue'] * 100) if kpi_py['Total Revenue'] else 0
    profit_growth = ((kpi_cy['Net Profit'] - kpi_py['Net Profit']) / kpi_py['Net Profit'] * 100) if kpi_py.get('Net Profit', 0) > 0 else 0
    assets_growth = ((kpi_cy['Total Assets'] - kpi_py['Total Assets']) / kpi_py['Total Assets'] * 100) if kpi_py['Total Assets'] else 0
    dte_change = kpi_cy['Debt-to-Equity'] - kpi_py['Debt-to-Equity']
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card revenue-card">
            <div class="title">Total Revenue (CY)</div>
            <div class="value">₹{kpi_cy['Total Revenue']:,.0f}</div>
            <div class="delta {'up' if rev_growth >= 0 else 'down'}">{rev_growth:.1f}% vs PY</div>
        </div>
        <div class="kpi-card profit-card">
            <div class="title">Net Profit (CY)</div>
            <div class="value">₹{kpi_cy['Net Profit']:,.0f}</div>
            <div class="delta {'up' if profit_growth >= 0 else 'down'}">{profit_growth:.1f}% vs PY</div>
        </div>
        <div class="kpi-card assets-card">
            <div class="title">Total Assets (CY)</div>
            <div class="value">₹{kpi_cy['Total Assets']:,.0f}</div>
            <div class="delta {'up' if assets_growth >= 0 else 'down'}">{assets_growth:.1f}% vs PY</div>
        </div>
        <div class="kpi-card debt-card">
            <div class="title">Debt-to-Equity (CY)</div>
            <div class="value">{kpi_cy['Debt-to-Equity']:.2f}</div>
            <div class="delta {'down' if dte_change <= 0 else 'up'}">{dte_change:+.2f} vs PY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    ai_analysis = generate_ai_analysis(kpis)
    chart_data = pd.DataFrame(kpis).reset_index().rename(columns={'index': 'Metric'}).melt(id_vars='Metric', var_name='Year', value_name='Amount')
    fig = px.bar(chart_data[chart_data['Metric'].isin(['Total Revenue', 'Net Profit'])], x='Metric', y='Amount', color='Year', barmode='group', title='Current (CY) vs. Previous (PY) Year Performance')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#2b2b3c', font_color='#e0e0e0')
    col1, col2 = st.columns((5, 4))
    col1.subheader("📊 Financial Visualization")
    col1.plotly_chart(fig, use_container_width=True)
    col2.subheader("🤖 AI-Generated Insights")
    col2.markdown(ai_analysis)
    st.subheader("⬇️ Download Center")
    chart_bytes = io.BytesIO()
    fig.write_image(chart_bytes, format="png", scale=2, engine="kaleido")
    charts_for_pdf = {"Performance Overview": chart_bytes}
    excel_file_for_pdf = io.BytesIO(st.session_state.excel_report_bytes)
    sheets_data = pd.read_excel(excel_file_for_pdf, sheet_name=None)
    cleaned_sheets_data = {name: df.dropna(how='all').fillna('') for name, df in sheets_data.items() if not df.dropna(how='all').fillna('').empty}
    pdf_bytes = create_professional_pdf(st.session_state.kpis, ai_analysis, charts_for_pdf, st.session_state.company_name, cleaned_sheets_data, st.session_state.agg_data)
    d_col1, d_col2 = st.columns(2)
    d_col1.download_button(
        "📊 Download Visual PDF Report",
        pdf_bytes,
        f"{st.session_state.company_name}_Dashboard_Report.pdf",
        "application/pdf",
        use_container_width=True
    )
    d_col2.download_button(
        "💹 Download Formatted Excel Data",
        st.session_state.excel_report_bytes,
        f"{st.session_state.company_name}_Financial_Statements.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()

st.header("Generate PDF Report from a Previously Downloaded Excel File")
st.markdown("Use this section to upload the single formatted Excel report you've already generated to create a professional PDF. This section is more flexible and can handle modified files.")

excel_file = st.file_uploader("Upload Formatted Excel Report", type=["xlsx", "xls"], key="excel_uploader")
company_name_pdf = st.text_input("Enter Company Name for Report", st.session_state.company_name, key="pdf_company_name")

if st.button("Generate PDF Report", type="secondary", use_container_width=True, key="generate_pdf_button"):
    if excel_file and company_name_pdf:
        with st.spinner("Processing Excel file and generating report..."):
            try:
                all_sheets_raw = pd.read_excel(excel_file, sheet_name=None, header=None, nrows=10)
                combined_df = pd.DataFrame()
                sheets_for_pdf = {}
                sheet_names_to_include = ['Balance Sheet', 'Profit and Loss'] + [f'Note {i}' for i in range(1, 28)]
                for sheet_name in sheet_names_to_include:
                    if sheet_name in all_sheets_raw:
                        df_raw = all_sheets_raw[sheet_name]
                        header_row_candidates = df_raw.apply(lambda row: row.astype(str).str.contains('Particulars', case=False).any(), axis=1)
                        header_row_index = header_row_candidates[header_row_candidates].index
                        if not header_row_index.empty:
                            header_index_to_use = header_row_index[0]
                            df_correctly_read = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_index_to_use)
                            df_correctly_read = df_correctly_read.dropna(subset=['Particulars']).fillna('')
                            sheets_for_pdf[sheet_name] = df_correctly_read
                            combined_df = pd.concat([combined_df, df_correctly_read], ignore_index=True)
                if 'Particulars' not in combined_df.columns:
                    st.error("The uploaded Excel file does not contain a 'Particulars' column in any of the sheets. Please check your file format.")
                else:
                    agg_data_from_excel = {}
                    def find_value(keyword, df_to_search=combined_df):
                        row = df_to_search[df_to_search['Particulars'].astype(str).str.contains(keyword, na=False, case=False, regex=False)]
                        if not row.empty:
                            cy_col_candidates = [col for col in df_to_search.columns if '2025' in str(col)]
                            py_col_candidates = [col for col in df_to_search.columns if '2024' in str(col)]
                            if cy_col_candidates and py_col_candidates:
                                cy_val = row[cy_col_candidates[0]].iloc[0]
                                py_val = row[py_col_candidates[0]].iloc[0]
                                return cy_val, py_val
                        return 0, 0
                    def find_sub_item_value(main_keyword, sub_keyword, df_to_search=combined_df):
                        main_row_index = df_to_search[df_to_search['Particulars'].astype(str).str.contains(main_keyword, na=False, case=False, regex=False)].index
                        if not main_row_index.empty:
                            for i in range(main_row_index[0] + 1, len(df_to_search)):
                                if sub_keyword in str(df_to_search.iloc[i]['Particulars']):
                                    cy_col_candidates = [col for col in df_to_search.columns if '2025' in str(col)]
                                    py_col_candidates = [col for col in df_to_search.columns if '2024' in str(col)]
                                    if cy_col_candidates and py_col_candidates:
                                        cy_val = df_to_search.iloc[i][cy_col_candidates[0]]
                                        py_val = df_to_search.iloc[i][py_col_candidates[0]]
                                        return cy_val, py_val
                        return 0, 0
                    cy_equity, py_equity = find_value("Shareholder's funds")
                    cy_total_liab_equity, py_total_liab_equity = find_value("TOTAL EQUITY AND LIABILITIES")
                    cy_total_assets, py_total_assets = find_value("TOTAL ASSETS")
                    cy_total_revenue, py_total_revenue = find_value("Total Revenue")
                    cy_pbt, py_pbt = find_value("Profit before tax")
                    cy_pat, py_pat = find_value("Profit/(Loss) for the period")
                    depreciation_cy, depreciation_py = find_sub_item_value("Fixed Assets", "Depreciation for the year", sheets_for_pdf.get('Note 11', pd.DataFrame()))
                    agg_data_from_excel = {
                        '1': {'total': {'CY': cy_equity, 'PY': py_equity}},
                        '2': {'total': {'CY': cy_total_liab_equity - cy_equity, 'PY': py_total_liab_equity - py_equity}},
                        '3': {'total': {'CY': 0, 'PY': 0}},
                        '7': {'total': {'CY': 0, 'PY': 0}},
                        '11': {'total': {'CY': cy_total_assets, 'PY': py_total_assets}, 'sub_items': {'Depreciation for the year': {'CY': depreciation_cy, 'PY': depreciation_py}}},
                        '15': {'total': {'CY': 0, 'PY': 0}},
                        '16': {'total': {'CY': 0, 'PY': 0}},
                        '17': {'total': {'CY': 0, 'PY': 0}},
                        '18': {'total': {'CY': 0, 'PY': 0}},
                        '19': {'total': {'CY': 0, 'PY': 0}},
                        '20': {'total': {'CY': 0, 'PY': 0}},
                        '21': {'total': {'CY': cy_total_revenue, 'PY': py_total_revenue}},
                        '22': {'total': {'CY': 0, 'PY': 0}},
                        '23': {'total': {'CY': 0, 'PY': 0}},
                        '24': {'total': {'CY': 0, 'PY': 0}},
                        '25': {'total': {'CY': 0, 'PY': 0}},
                        '26': {'total': {'CY': 0, 'PY': 0}},
                        'PBT': {'total': {'CY': cy_pbt, 'PY': py_pbt}},
                        'PAT': {'total': {'CY': cy_pat, 'PY': py_pat}},
                    }
                    re_kpis = calculate_kpis(agg_data_from_excel)
                    re_ai_analysis = generate_ai_analysis(re_kpis)
                    re_chart_data = pd.DataFrame(re_kpis).reset_index().rename(columns={'index': 'Metric'}).melt(id_vars='Metric', var_name='Year', value_name='Amount')
                    re_fig = px.bar(re_chart_data[re_chart_data['Metric'].isin(['Total Revenue', 'Net Profit'])], x='Metric', y='Amount', color='Year', barmode='group', title='Current (CY) vs. Previous (PY) Year Performance')
                    re_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#2b2b3c', font_color='#e0e0e0')
                    re_chart_bytes = io.BytesIO()
                    re_fig.write_image(re_chart_bytes, format="png", scale=2, engine="kaleido")
                    re_charts_for_pdf = {"Performance Overview": re_chart_bytes}
                    re_pdf_bytes = create_professional_pdf(re_kpis, re_ai_analysis, re_charts_for_pdf, company_name_pdf, sheets_for_pdf, agg_data_from_excel)
                    st.success("PDF Report Generated!")
                    st.download_button("📄 Download Comprehensive PDF Report", re_pdf_bytes, f"{company_name_pdf}_Comprehensive_Financial_Report.pdf", "application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"An error occurred while processing the Excel file: {e}. Please ensure the file is an Excel workbook and contains the necessary financial data.")
                import traceback
                traceback.print_exc()
    else:
        st.warning("Please upload a formatted Excel report and enter the company name.")
