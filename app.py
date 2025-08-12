# ==============================================================================
# PASTE THIS ENTIRE BLOCK INTO: app.py
# This is the final version that runs the real agent pipeline.
# ==============================================================================
import streamlit as st
import sys
import os
import pandas as pd
from fpdf import FPDF
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

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
    st.error(f"CRITICAL ERROR: A required module could not be imported. Details: {e}")
    st.stop()

def calculate_kpis(agg_data):
    kpis = {}; get = lambda key, y: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
    for year in ['CY', 'PY']:
        total_revenue = get(21, year) + get(22, year)
        depreciation = agg_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
        total_expenses = get(23, year) + get(24, year) + get(25, year) + get(26, year) + depreciation
        total_assets = sum(get(n, year) for n in range(11, 21)); total_equity = get(1, year) + get(2, year)
        kpis[year] = {"Total Revenue": total_revenue, "Net Profit": total_revenue - total_expenses, "Total Assets": total_assets, "Debt-to-Equity": (get(3, year) + get(7, year)) / total_equity if total_equity else 0}
    return kpis

def generate_ai_analysis(kpis): return f"**Strengths:**\n- **Profitability:** A Net Profit of INR {kpis.get('CY', {}).get('Net Profit', 0):,.0f} on Revenue of INR {kpis.get('CY', {}).get('Total Revenue', 0):,.0f} signals operational efficiency."

class PDF(FPDF):
    def header(self): self.set_font('Arial', 'B', 16); self.cell(0, 10, 'Financial Report Summary', 0, 1, 'C')
    def footer(self): self.set_y(-15); self.set_font('Arial', 'I', 8); self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_professional_pdf(kpis, ai_analysis, company_name):
    pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', 'B', 20); pdf.cell(0, 15, f'Financial Report for {company_name}', 0, 1, 'C'); pdf.ln(5)
    kpi_cy = kpis.get('CY', {}); pdf.set_font('Arial', 'B', 16); pdf.cell(0, 10, 'Key Performance Indicators (CY)', 0, 1, 'L'); pdf.set_font('Arial', '', 12)
    for key, value in kpi_cy.items(): pdf.cell(0, 8, f"- {key}: {'INR {:,.0f}'.format(value) if isinstance(value, (int, float)) and value > 1000 else '{:.2f}'.format(value)}", 0, 1)
    pdf.ln(5); pdf.set_font('Arial', 'B', 16); pdf.cell(0, 10, 'AI-Generated Insights', 0, 1, 'L'); pdf.set_font('Arial', '', 12); pdf.multi_cell(0, 6, ai_analysis.replace('**', ''))
    return bytes(pdf.output())

st.set_page_config(page_title="Financial Dashboard", page_icon="📈", layout="wide")
if 'report_generated' not in st.session_state: st.session_state.report_generated = False; st.session_state.company_name = "ABC Private Limited"

with st.sidebar:
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload Financial Data", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", st.session_state.company_name)
    if st.button("Generate Dashboard", type="primary", use_container_width=True):
        if uploaded_file and company_name:
            with st.spinner("Executing financial agent pipeline..."):
                st.info("Step 1/5: Ingesting data..."); source_df = intelligent_data_intake_agent(uploaded_file)
                if source_df is None: st.error("Pipeline Failed at Data Intake."); st.stop()
                st.info("Step 2/5: Mapping terms..."); refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), NOTES_STRUCTURE_AND_MAPPING)
                st.info("Step 3/5: Aggregating values..."); aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                if not aggregated_data: st.error("Pipeline Failed at Aggregation."); st.stop()
                st.info("Step 4/5: Validating balances..."); warnings = data_validation_agent(aggregated_data)
                st.info("Step 5/5: Generating reports..."); excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
                if excel_report_bytes is None: st.error("Pipeline Failed at Report Finalizer."); st.stop()
            st.success("Dashboard Generated!"); [st.warning(w) for w in warnings]
            st.session_state.update(report_generated=True, kpis=calculate_kpis(aggregated_data), company_name=company_name, excel_report_bytes=excel_report_bytes)
            st.rerun()

if not st.session_state.report_generated:
    st.title("Financial Analysis Dashboard"); st.write("Upload your financial data in the sidebar to begin.")
else:
    kpis = st.session_state.kpis; kpi_cy = kpis.get('CY', {}); st.title(f"Dashboard for {st.session_state.company_name}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue (CY)", f"₹{kpi_cy.get('Total Revenue', 0):,.0f}"); c2.metric("Net Profit (CY)", f"₹{kpi_cy.get('Net Profit', 0):,.0f}")
    c3.metric("Assets (CY)", f"₹{kpi_cy.get('Total Assets', 0):,.0f}"); c4.metric("D/E Ratio (CY)", f"{kpi_cy.get('Debt-to-Equity', 0):.2f}")
    st.subheader("⬇️ Download Center"); d1, d2 = st.columns(2)
    d1.download_button("📄 Download PDF Summary", create_professional_pdf(kpis, generate_ai_analysis(kpis), company_name), f"{company_name}_Summary.pdf", "application/pdf", use_container_width=True)
    d2.download_button("💹 Download Styled Excel", st.session_state.excel_report_bytes, f"{company_name}_Full_Report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
