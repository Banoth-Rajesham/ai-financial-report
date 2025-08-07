# FINAL, COMPLETE, AND CORRECTED app.py

import streamlit as st
import sys
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import requests
import json
import time
import numpy as np
import os
import io # Required for creating the in-memory Excel file

# This line tells the app to also look inside the sub-folder for helper files.
sys.path.append('financial_reporter_app')

try:
    from config import NOTES_STRUCTURE_AND_MAPPING
    from agents import (
        intelligent_data_intake_agent,
        ai_mapping_agent,
        hierarchical_aggregator_agent,
        data_validation_agent,
        report_finalizer_agent
    )
except ImportError as e:
    st.error(f"CRITICAL ERROR: Could not import a module. This is likely a path issue. Error: {e}")
    st.stop()


# --- HELPER FUNCTIONS ---

def calculate_metrics(agg_data):
    metrics = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(key, {}).get('total', {}).get(y, 0)
        total_revenue = get('21') + get('22')
        total_expenses = sum(get(n) for n in ['23', '24', '25', '11', '26'])
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in ["11", "12", "4", "13", "14", "15", "16", "17", "18", "19", "20"])
        current_assets = sum(get(n) for n in ['15', '16', '17', '18', '19', '20'])
        current_liabilities = sum(get(n) for n in ['7', '8', '9', '10'])
        total_debt = sum(get(n) for n in ['3', '7'])
        total_equity = sum(get(n) for n in ['1', '2'])
        metrics[year] = {
            "Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets,
            "Current Assets": current_assets, "Fixed Assets": get('11'), "Investments": get('12'),
            "Profit Margin": (net_profit / total_revenue) * 100 if total_revenue else 0,
            "Current Ratio": current_assets / current_liabilities if current_liabilities else 0,
            "Debt-to-Equity": total_debt / total_equity if total_equity else 0,
            "ROA": (net_profit / total_assets) * 100 if total_assets else 0
        }
    return metrics

def generate_ai_analysis(metrics):
    try:
        YOUR_API_URL = st.secrets["ANALYSIS_API_URL"]
        YOUR_API_KEY = st.secrets["ANALYSIS_API_KEY"]
    except (FileNotFoundError, KeyError) as e:
        return "AI analysis could not be generated because API secrets are not configured."

    prompt = (
        f"Analyze this financial data: CY Revenue={metrics['CY']['Total Revenue']:,.0f}, PY Revenue={metrics['PY']['Total Revenue']:,.0f}; CY Net Profit={metrics['CY']['Net Profit']:,.0f}, PY Net Profit={metrics['PY']['Net Profit']:,.0f}; CY D/E Ratio={metrics['CY']['Debt-to-Equity']:.2f}, PY D/E Ratio={metrics['PY']['Debt-to-Equity']:.2f}. Provide a concise SWOT analysis."
    )
    payload = {"prompt": prompt}
    headers = {"Authorization": f"Bearer {YOUR_API_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post(YOUR_API_URL, headers=headers, data=json.dumps(payload), timeout=45)
        response.raise_for_status()
        return response.json().get("analysis_text", "Could not parse AI analysis.")
    except requests.exceptions.RequestException as e:
        return f"Could not generate AI analysis. API connection error: {e}"

# --- PDF Generation Code ---
class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, 'Financial Dashboard Report', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_professional_pdf(metrics, ai_analysis, charts):
    temp_dir = "temp_charts"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    chart_paths = {}
    for name, fig in charts.items():
        path = os.path.join(temp_dir, f"{name}.png")
        fig.write_image(path, scale=2, width=600, height=350)
        chart_paths[name] = path
    
    pdf = PDF('P', 'mm', 'A4')
    
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf')
    pdf.add_font('DejaVu', 'BI', 'DejaVuSans-BoldOblique.ttf')
    
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 10, 'Top KPI Summary', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('DejaVu', 'B', 10)
    pdf.cell(60, 8, 'Metric', 1)
    pdf.cell(60, 8, 'Value', 1)
    pdf.cell(70, 8, 'Interpretation', 1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('DejaVu', '', 10)
    kpi_cy = metrics['CY']; kpi_py = metrics['PY']
    get_change = lambda cy, py: f' ({"⬆" if cy >= py else "⬇"} {abs((cy - py) / py * 100):.1f}%)' if py else " (new)"
    kpi_data = [
        ("Total Revenue", f"₹ {kpi_cy['Total Revenue']:,.0f}{get_change(kpi_cy['Total Revenue'], kpi_py['Total Revenue'])}", "Indicates sales or operational growth."),
        ("Net Profit", f"₹ {kpi_cy['Net Profit']:,.0f}{get_change(kpi_cy['Net Profit'], kpi_py['Net Profit'])}", "Indicates cost control or margin improvement."),
    ]
    for title, value, interp in kpi_data:
        pdf.cell(60, 8, title, 1)
        pdf.cell(60, 8, value, 1)
        pdf.cell(70, 8, interp, 1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 10, 'Visualizations', new_x="LMARGIN", new_y="NEXT")
    pdf.image(chart_paths["revenue_trend"], x=10, w=pdf.w / 2 - 15)
    pdf.image(chart_paths["asset_distribution"], x=pdf.w / 2 + 5, w=pdf.w / 2 - 15)
    pdf.ln(70)
    
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 10, 'AI-Generated SWOT Analysis', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('DejaVu', '', 10)
    pdf.multi_cell(0, 5, ai_analysis)
    
    return bytes(pdf.output())

# --- Excel Generation Code ---
def create_excel_report(aggregated_data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary_data = []
        for note_num, note_content in NOTES_STRUCTURE_AND_MAPPING.items():
            note_title = note_content.get('title', f'Note {note_num}')
            cy_total = aggregated_data.get(note_num, {}).get('total', {}).get('CY', 0)
            py_total = aggregated_data.get(note_num, {}).get('total', {}).get('PY', 0)
            summary_data.append([note_num, note_title, cy_total, py_total])
        
        summary_df = pd.DataFrame(summary_data, columns=["Note No.", "Particulars", "Current Year", "Previous Year"])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        for note_num, note_details in aggregated_data.items():
            if 'sub_items' in note_details and note_details['sub_items']:
                
                # ========================================================== #
                # == THIS IS THE FIX for the "Invalid character /" error  == #
                # ========================================================== #
                raw_title = NOTES_STRUCTURE_AND_MAPPING.get(note_num, {}).get('title', f'Note {note_num}')
                # Replace illegal characters and limit length for sheet names
                safe_title = raw_title.replace('/', '-').replace('\\', '-').replace('?', '').replace('*', '').replace('[', '').replace(']', '')
                sheet_title = safe_title[:31]
                # ========================================================== #

                df = pd.DataFrame.from_dict(note_details['sub_items'], orient='index')
                df.loc['Total'] = note_details.get('total', {})
                if 'CY' in df.columns and 'PY' in df.columns:
                    df = df[['CY', 'PY']]
                df.to_excel(writer, sheet_name=sheet_title)
    
    excel_bytes = output.getvalue()
    return excel_bytes


# --- MAIN APP UI ---

st.set_page_config(page_title="AI Financial Reporter", page_icon="🤖", layout="wide")
st.title("Financial Dashboard")

if 'report_generated' not in st.session_state: st.session_state.report_generated = False

with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload financial data (Excel)", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", "My Company Inc.")
    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file:
            with st.spinner("Executing financial agent pipeline..."):
                source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None: st.error("Pipeline Failed: Data Intake"); st.stop()
                
                refined_mapping = ai_mapping_agent(source_df['Particulars'].unique().tolist(), NOTES_STRUCTURE_AND_MAPPING)
                
                aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data: st.error("Pipeline Failed: Aggregation"); st.stop()
                
            st.success("Dashboard Generated!")
            st.session_state.report_generated = True
            st.session_state.aggregated_data = aggregated_data
            st.session_state.company_name = company_name
            st.rerun()
        else:
            st.warning("Please upload a file.")

if st.session_state.report_generated:
    agg_data = st.session_state.aggregated_data
    metrics = calculate_metrics(agg_data)
    kpi_cy = metrics.get('CY', {}); kpi_py = metrics.get('PY', {})
    get_change = lambda cy, py: ((cy - py) / abs(py) * 100) if py != 0 else 0
    st.success("Dashboard generated from extracted financial data.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{kpi_cy.get('Total Revenue', 0):,.0f}", f"{get_change(kpi_cy.get('Total Revenue', 0), kpi_py.get('Total Revenue', 0)):.1f}%")
    col2.metric("Net Profit", f"₹{kpi_cy.get('Net Profit', 0):,.0f}", f"{get_change(kpi_cy.get('Net Profit', 0), kpi_py.get('Net Profit', 0)):.1f}%")
    col3.metric("Total Assets", f"₹{kpi_cy.get('Total Assets', 0):,.0f}", f"{get_change(kpi_cy.get('Total Assets', 0), kpi_py.get('Total Assets', 0)):.1f}%")
    col4.metric("Debt-to-Equity", f"₹{kpi_cy.get('Debt-to-Equity', 0):.2f}", f"{get_change(kpi_cy.get('Debt-to-Equity', 0), kpi_py.get('Debt-to-Equity', 0)):.1f}%", delta_color="inverse")
    
    months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
    def generate_monthly(total):
        if total == 0: return [0]*12
        pattern = np.array([0.8, 0.85, 0.9, 1.0, 1.1, 1.15, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85])
        monthly = pattern * (total / 12)
        return (monthly / monthly.sum()) * total
    revenue_df = pd.DataFrame({'Month': months * 2, 'Year': ['Previous Year'] * 12 + ['Current Year'] * 12, 'Revenue': np.concatenate([generate_monthly(kpi_py.get('Total Revenue',0)), generate_monthly(kpi_cy.get('Total Revenue',0))])})
    fig_revenue = px.area(revenue_df, x='Month', y='Revenue', color='Year', title="<b>Revenue Trend</b>", template="seaborn")
    
    asset_data = {'Asset Type': ['Current Assets', 'Fixed Assets', 'Investments'], 'Value': [kpi_cy.get('Current Assets',0), kpi_cy.get('Fixed Assets',0), kpi_cy.get('Investments',0)]}
    asset_df = pd.DataFrame(asset_data).query("Value > 0")
    fig_asset = px.pie(asset_df, names='Asset Type', values='Value', title="<b>Asset Distribution</b>", hole=0.3)
    
    chart_col1, chart_col2 = st.columns(2)
    chart_col1.plotly_chart(fig_revenue, use_container_width=True)
    chart_col2.plotly_chart(fig_asset, use_container_width=True)
    
    st.divider()
    
    with st.spinner("Generating Reports..."):
        ai_analysis = generate_ai_analysis(metrics)
        charts = {"revenue_trend": fig_revenue, "asset_distribution": fig_asset}
        pdf_bytes = create_professional_pdf(metrics, ai_analysis, charts)
        excel_bytes = create_excel_report(agg_data)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="💡 Download Professional Insights (PDF)", 
            data=pdf_bytes, 
            file_name=f"{st.session_state.company_name}_Insights_Report.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
    with dl_col2:
        st.download_button(
            label="📊 Download Detailed Data (Excel)", 
            data=excel_bytes, 
            file_name=f"{st.session_state.company_name}_Detailed_Report.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
            use_container_width=True
        )
else:
    st.info("Upload your financial data and click 'Generate Dashboard' to begin.")
