# app.py
# ENHANCED 3D FINANCIAL DASHBOARD - FIXED VERSION

import streamlit as st
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fpdf import FPDF
import requests
import json
import time
import numpy as np
import os
import io
import math
import traceback

# This line tells the app where to find your 'agents' and 'config' files.
sys.path.append('financial_reporter_app')

try:
    from config import NOTES_STRUCTURE_AND_MAPPING
    from agents import (
        intelligent_data_intake_agent,
        ai_mapping_agent,
        hierarchical_aggregator_agent,
        report_finalizer_agent
    )
except Exception as e:
    st.error(f"CRITICAL ERROR: Could not import a module. This is likely a path issue. Error: {e}")
    st.stop()

# === CUSTOM CSS FOR 3D EFFECTS AND MODERN STYLING ===
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    /* ... (unchanged CSS content omitted here for brevity in this snippet) ... */
    /* Keep all your original CSS here exactly as in your earlier file */
    </style>
    """, unsafe_allow_html=True)

# === 3D KPI CARD COMPONENT ===
def create_3d_kpi_card(title, value, change, icon, column_key):
    trend_class = "positive-3d" if change >= 0 else "negative-3d"
    trend_arrow = "📈" if change >= 0 else "📉"
    # Avoid NaN / infinite formatting
    try:
        formatted_change = f"{change:+.1f}%"
    except Exception:
        formatted_change = "N/A"
    kpi_html = f"""
    <div class="kpi-3d-container">
        <div class="kpi-3d-card">
            <div class="kpi-icon-3d">{icon}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value-3d">{value}</div>
            <div class="kpi-change-3d {trend_class}">
                <span>{trend_arrow}</span>
                <span>{formatted_change}</span>
            </div>
        </div>
    </div>
    """
    return kpi_html

# === ENHANCED 3D CHARTS ===
def create_3d_revenue_trend(revenue_data):
    """Create a stunning 3D revenue trend visualization (defensive)"""
    try:
        months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        fig = go.Figure()

        # Current Year - 3D Line with single color (removed invalid 'colorscale')
        fig.add_trace(go.Scatter3d(
            x=list(range(12)),
            y=[1]*12,
            z=list(revenue_data['current_year']),
            mode='lines+markers',
            line=dict(color='#667eea', width=12),
            marker=dict(size=8, color='#667eea', opacity=0.9, symbol='diamond'),
            name='Current Year',
            hovertemplate='<b>%{text}</b><br>Revenue: ₹%{z:,.0f}<extra></extra>',
            text=months
        ))

        # Previous Year - 3D Line
        fig.add_trace(go.Scatter3d(
            x=list(range(12)),
            y=[0]*12,
            z=list(revenue_data['previous_year']),
            mode='lines+markers',
            line=dict(color='#764ba2', width=12),
            marker=dict(size=8, color='#764ba2', opacity=0.9, symbol='circle'),
            name='Previous Year',
            hovertemplate='<b>%{text}</b><br>Revenue: ₹%{z:,.0f}<extra></extra>',
            text=months
        ))

        # Add connecting ribbons for better 3D effect (mesh)
        for i in range(11):
            # ensure values are numeric
            p0 = float(revenue_data['previous_year'][i])
            p1 = float(revenue_data['previous_year'][i+1])
            c1 = float(revenue_data['current_year'][i+1])
            c0 = float(revenue_data['current_year'][i])
            fig.add_trace(go.Mesh3d(
                x=[i, i+1, i+1, i],
                y=[0, 0, 1, 1],
                z=[p0, p1, c1, c0],
                opacity=0.18,
                color='lightblue',
                showscale=False,
                showlegend=False
            ))

        fig.update_layout(
            title=dict(
                text="<b>🚀 3D Revenue Trend Analysis</b>",
                font=dict(size=20, color='#667eea', family='Poppins'),
                x=0.5
            ),
            scene=dict(
                xaxis=dict(
                    title="Months",
                    titlefont=dict(color='#667eea', size=14),
                    tickvals=list(range(12)),
                    ticktext=months,
                    backgroundcolor="rgba(255,255,255,0.8)",
                    gridcolor="rgba(102, 126, 234, 0.3)"
                ),
                yaxis=dict(
                    title="Year Comparison",
                    titlefont=dict(color='#667eea', size=14),
                    tickvals=[0, 1],
                    ticktext=['Previous Year', 'Current Year'],
                    backgroundcolor="rgba(255,255,255,0.8)",
                    gridcolor="rgba(118, 75, 162, 0.3)"
                ),
                zaxis=dict(
                    title="Revenue (₹)",
                    titlefont=dict(color='#667eea', size=14),
                    backgroundcolor="rgba(255,255,255,0.8)",
                    gridcolor="rgba(102, 126, 234, 0.3)"
                ),
                camera=dict(
                    eye=dict(x=1.8, y=1.8, z=1.5),
                    center=dict(x=0, y=0, z=0)
                ),
                bgcolor="rgba(248,250,252,0.95)"
            ),
            paper_bgcolor="rgba(255,255,255,0.95)",
            plot_bgcolor="rgba(255,255,255,0.95)",
            height=600,
            font=dict(family='Poppins')
        )
        return fig
    except Exception as e:
        # Return fallback figure with helpful annotation to avoid crashing the app
        tb = traceback.format_exc()
        fig = go.Figure()
        fig.add_annotation(
            text="Unable to render 3D revenue chart — using fallback.\n" + str(e),
            x=0.5, y=0.5, showarrow=False, font=dict(size=14, color='#ff0000')
        )
        return fig

def create_3d_asset_distribution(asset_data):
    """Create a stunning 3D donut chart for asset distribution"""
    try:
        filtered_data = {k: v for k, v in asset_data.items() if v > 0}
        if not filtered_data:
            fig = go.Figure()
            fig.add_annotation(text="No Asset Data Available", x=0.5, y=0.5,
                               font=dict(size=20, color='#667eea'), showarrow=False)
            return fig
        labels = list(filtered_data.keys())
        values = list(filtered_data.values())
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'][:len(labels)]
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=4)),
            textinfo='label+percent',
            textfont=dict(size=14, color='white', family='Poppins'),
            hovertemplate='<b>%{label}</b><br>Value: ₹%{value:,.0f}<br>Percentage: %{percent}<extra></extra>',
            rotation=45
        ))
        fig.update_layout(
            title=dict(text="<b>💎 3D Asset Distribution</b>", font=dict(size=20, color='#667eea', family='Poppins'), x=0.5),
            paper_bgcolor="rgba(255,255,255,0.95)",
            plot_bgcolor="rgba(255,255,255,0.95)",
            height=600,
            font=dict(family='Poppins'),
            annotations=[dict(text="<b>Total<br>Assets</b>", x=0.5, y=0.5, font=dict(size=18, color='#667eea', family='Poppins'), showarrow=False)],
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(family='Poppins'))
        )
        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text="Unable to render assets chart.", x=0.5, y=0.5, showarrow=False)
        return fig

def create_3d_performance_metrics(metrics):
    """Create a 3D radar chart for performance metrics"""
    try:
        categories = ['Profit Margin', 'Current Ratio', 'ROA', 'Liquidity Score']
        cy = metrics.get('CY', {})
        py = metrics.get('PY', {})

        cy_values = [
            min(abs(cy.get('Profit Margin', 0)), 100),
            min(cy.get('Current Ratio', 0) * 30, 100),
            min(abs(cy.get('ROA', 0)) * 2, 100),
            min(cy.get('Current Assets', 0) / max(cy.get('Total Assets', 1), 1) * 100, 100)
        ]
        py_values = [
            min(abs(py.get('Profit Margin', 0)), 100),
            min(py.get('Current Ratio', 0) * 30, 100),
            min(abs(py.get('ROA', 0)) * 2, 100),
            min(py.get('Current Assets', 0) / max(py.get('Total Assets', 1), 1) * 100, 100)
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=cy_values, theta=categories, fill='toself',
                                     fillcolor='rgba(102, 126, 234, 0.4)', line=dict(color='#667eea', width=4),
                                     marker=dict(size=8, color='#667eea'), name='Current Year',
                                     hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'))
        fig.add_trace(go.Scatterpolar(r=py_values, theta=categories, fill='toself',
                                     fillcolor='rgba(118, 75, 162, 0.4)', line=dict(color='#764ba2', width=4),
                                     marker=dict(size=8, color='#764ba2'), name='Previous Year',
                                     hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=12, color='#667eea'),
                                       gridcolor="rgba(102, 126, 234, 0.3)", linecolor="rgba(102, 126, 234, 0.3)"),
                       angularaxis=dict(tickfont=dict(size=14, color='#667eea', family='Poppins'),
                                        gridcolor="rgba(102, 126, 234, 0.3)", linecolor="rgba(102, 126, 234, 0.3)"),
                       bgcolor="rgba(248,250,252,0.95)"),
            title=dict(text="<b>⚡ 3D Performance Radar</b>", font=dict(size=20, color='#667eea', family='Poppins'), x=0.5),
            paper_bgcolor="rgba(255,255,255,0.95)", plot_bgcolor="rgba(255,255,255,0.95)", height=600,
            font=dict(family='Poppins'), showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        return fig
    except Exception:
        fig = go.Figure()
        fig.add_annotation(text="Unable to render performance radar.", x=0.5, y=0.5, showarrow=False)
        return fig

# --- EXISTING HELPER FUNCTIONS (UNCHANGED LOGIC, BUT SAFER) ---

def calculate_metrics(agg_data):
    metrics = {}
    for year in ['CY', 'PY']:
        get = lambda key, y=year: agg_data.get(str(key), {}).get('total', {}).get(y, 0)
        total_revenue = get(21) + get(22)
        total_expenses = sum(get(n) for n in [23, 24, 25, 11, 26])
        net_profit = total_revenue - total_expenses
        total_assets = sum(get(n) for n in [11, 12, 4, 13, 14, 15, 16, 17, 18, 19, 20])
        current_assets = sum(get(n) for n in [15, 16, 17, 18, 19, 20])
        current_liabilities = sum(get(n) for n in [7, 8, 9, 10])
        total_debt = sum(get(n) for n in [3, 7])
        total_equity = sum(get(n) for n in [1, 2]) or 1  # avoid zero division later
        metrics[year] = {
            "Total Revenue": total_revenue, "Net Profit": net_profit, "Total Assets": total_assets,
            "Current Assets": current_assets, "Fixed Assets": get(11), "Investments": get(12),
            "Profit Margin": (net_profit / total_revenue) * 100 if total_revenue else 0,
            "Current Ratio": (current_assets / current_liabilities) if current_liabilities else 0,
            "Debt-to-Equity": (total_debt / total_equity) if total_equity else 0,
            "ROA": (net_profit / total_assets) * 100 if total_assets else 0
        }
    return metrics

def generate_ai_analysis(metrics):
    try:
        YOUR_API_URL = st.secrets["ANALYSIS_API_URL"]
        YOUR_API_KEY = st.secrets["ANALYSIS_API_KEY"]
    except Exception:
        return "AI analysis could not be generated because API secrets are not configured."
    prompt = f"Provide a SWOT analysis for a company with this data: Current Year Revenue: {metrics['CY']['Total Revenue']:,.0f}, Previous Year Revenue: {metrics['PY']['Total Revenue']:,.0f}, Current Year Net Profit: {metrics['CY']['Net Profit']:,.0f}, Previous Year Net Profit: {metrics['PY']['Net Profit']:,.0f}."
    payload = {"prompt": prompt}
    headers = {"Authorization": f"Bearer {YOUR_API_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post(YOUR_API_URL, headers=headers, data=json.dumps(payload), timeout=45)
        response.raise_for_status()
        return response.json().get("analysis_text", "Could not parse AI analysis.")
    except Exception:
        return "Could not generate AI analysis due to an API connection error."

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
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
    chart_paths = {}
    for name, fig in charts.items():
        path = os.path.join(temp_dir, f"{name}.png")
        try:
            # This requires kaleido in the environment. If not available, skip image save.
            fig.write_image(path, scale=2, width=600, height=350)
            chart_paths[name] = path
        except Exception:
            # fallback: try to use to_image, else leave missing so PDF will not crash
            try:
                img_bytes = fig.to_image(format="png", scale=2, width=600, height=350)
                with open(path, "wb") as f:
                    f.write(img_bytes)
                chart_paths[name] = path
            except Exception:
                chart_paths[name] = None

    pdf = PDF('P', 'mm', 'A4')
    # If DejaVu fonts not present, FPDF will raise; wrap in try to avoid crash.
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
        pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf')
        pdf.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf')
        pdf.add_font('DejaVu', 'BI', 'DejaVuSans-BoldOblique.ttf')
        font_name = 'DejaVu'
    except Exception:
        font_name = 'Arial'  # fallback

    pdf.add_page()
    pdf.set_font(font_name, 'B', 12)
    pdf.cell(0, 10, 'Top KPI Summary', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font_name, 'B', 10)
    pdf.cell(60, 8, 'Metric', 1)
    pdf.cell(60, 8, 'Value', 1)
    pdf.cell(70, 8, 'Interpretation', 1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(font_name, '', 10)
    kpi_cy = metrics.get('CY', {}); kpi_py = metrics.get('PY', {})
    def get_change(cy, py):
        try:
            pct = (cy - py) / py * 100 if py else 100.0
            arrow = "⬆" if cy >= py else "⬇"
            return f' ({arrow} {abs(pct):.1f}%)'
        except Exception:
            return ""
    kpi_data = [
        ("Total Revenue", f"₹ {kpi_cy.get('Total Revenue',0):,.0f}{get_change(kpi_cy.get('Total Revenue',0), kpi_py.get('Total Revenue',0))}", "Indicates sales or operational growth."),
        ("Net Profit", f"₹ {kpi_cy.get('Net Profit',0):,.0f}{get_change(kpi_cy.get('Net Profit',0), kpi_py.get('Net Profit',0))}", "Indicates cost control or margin improvement."),
    ]
    for title, value, interp in kpi_data:
        pdf.cell(60, 8, title, 1)
        pdf.cell(60, 8, value, 1)
        pdf.cell(70, 8, interp, 1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_font(font_name, 'B', 12)
    pdf.cell(0, 10, 'Visualizations', new_x="LMARGIN", new_y="NEXT")
    # Add images if available
    try:
        if chart_paths.get("revenue_trend"):
            pdf.image(chart_paths["revenue_trend"], x=10, w=pdf.w / 2 - 15)
        if chart_paths.get("asset_distribution"):
            pdf.image(chart_paths["asset_distribution"], x=pdf.w / 2 + 5, w=pdf.w / 2 - 15)
    except Exception:
        pass
    pdf.ln(70)

    pdf.set_font(font_name, 'B', 12)
    pdf.cell(0, 10, 'AI-Generated SWOT Analysis', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font_name, '', 10)
    pdf.multi_cell(0, 5, str(ai_analysis))

    # Return bytes
    try:
        return pdf.output(dest='S').encode('latin-1')
    except Exception:
        # Last resort: write to temp file and return bytes
        tmp = os.path.join(temp_dir, "report.pdf")
        pdf.output(tmp)
        with open(tmp, "rb") as f:
            return f.read()

def generate_monthly_data(total):
    """Generate realistic monthly data distribution"""
    if total == 0:
        return [0]*12
    pattern = np.array([0.8, 0.85, 0.9, 1.0, 1.1, 1.15, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85])
    monthly = pattern * (total / 12)
    # preserve distribution proportions
    return (monthly / monthly.sum()) * total

# --- MAIN APP UI ---

load_custom_css()

st.set_page_config(page_title="🚀 AI Financial Reporter", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")
st.markdown('<h1 class="dashboard-title">🚀 Financial Dashboard 3D</h1>', unsafe_allow_html=True)

if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'excel_report_bytes' not in st.session_state:
    st.session_state.excel_report_bytes = None
if 'aggregated_data' not in st.session_state:
    st.session_state.aggregated_data = None

# Sidebar - upload
with st.sidebar:
    st.header("🎯 Upload & Process")
    uploaded_file = st.file_uploader("Upload financial data (Excel)", type=["xlsx", "xls"])
    company_name = st.text_input("Enter Company Name", "My Company Inc.")
    if st.button("🚀 Generate 3D Dashboard", type="primary", use_container_width=True):
        if uploaded_file:
            with st.spinner("🔄 Executing financial agent pipeline..."):
                try:
                    source_df = intelligent_data_intake_agent(uploaded_file)
                    if source_df is None:
                        st.error("Pipeline Failed: Data Intake")
                        st.stop()
                    refined_mapping = ai_mapping_agent(source_df['Particulars'].tolist(), NOTES_STRUCTURE_AND_MAPPING)
                    aggregated_data = hierarchical_aggregator_agent(source_df, refined_mapping)
                    if not aggregated_data:
                        st.error("Pipeline Failed: Aggregation")
                        st.stop()
                    excel_report_bytes = report_finalizer_agent(aggregated_data, company_name)
                    if excel_report_bytes is None:
                        st.error("Pipeline Failed: Report Finalizer")
                        st.stop()
                except Exception as e:
                    st.error(f"Pipeline error: {e}")
                    st.stop()
            st.session_state.report_generated = True
            st.session_state.aggregated_data = aggregated_data
            st.session_state.company_name = company_name
            st.session_state.excel_report_bytes = excel_report_bytes
            st.rerun()
        else:
            st.warning("⚠️ Please upload a file.")

# Main display
if st.session_state.report_generated:
    agg_data = st.session_state.aggregated_data
    metrics = calculate_metrics(agg_data)
    kpi_cy = metrics.get('CY', {})
    kpi_py = metrics.get('PY', {})

    get_change = lambda cy, py: ((cy - py) / abs(py) * 100) if (py not in (0, None)) else 0

    st.markdown('<div class="success-3d">✨ 3D Dashboard generated from extracted financial data! ✨</div>', unsafe_allow_html=True)
    st.markdown("## 💎 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        revenue_change = get_change(kpi_cy.get('Total Revenue', 0), kpi_py.get('Total Revenue', 0))
        revenue_kpi = create_3d_kpi_card("Total Revenue", f"₹{kpi_cy.get('Total Revenue', 0):,.0f}", revenue_change, "💰", "revenue")
        st.markdown(revenue_kpi, unsafe_allow_html=True)

    with col2:
        profit_change = get_change(kpi_cy.get('Net Profit', 0), kpi_py.get('Net Profit', 0))
        profit_kpi = create_3d_kpi_card("Net Profit", f"₹{kpi_cy.get('Net Profit', 0):,.0f}", profit_change, "📊", "profit")
        st.markdown(profit_kpi, unsafe_allow_html=True)

    with col3:
        assets_change = get_change(kpi_cy.get('Total Assets', 0), kpi_py.get('Total Assets', 0))
        assets_kpi = create_3d_kpi_card("Total Assets", f"₹{kpi_cy.get('Total Assets', 0):,.0f}", assets_change, "🏦", "assets")
        st.markdown(assets_kpi, unsafe_allow_html=True)

    with col4:
        debt_change = get_change(kpi_cy.get('Debt-to-Equity', 0), kpi_py.get('Debt-to-Equity', 0))
        debt_kpi = create_3d_kpi_card("Debt-to-Equity", f"{kpi_cy.get('Debt-to-Equity', 0):.2f}", debt_change, "⚖️", "debt")
        st.markdown(debt_kpi, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📈 3D Financial Visualizations")

    # Prepare data for 3D charts
    revenue_data = {
        'current_year': generate_monthly_data(kpi_cy.get('Total Revenue', 0)),
        'previous_year': generate_monthly_data(kpi_py.get('Total Revenue', 0))
    }
    asset_data = {
        'Current Assets': kpi_cy.get('Current Assets', 0),
        'Fixed Assets': kpi_cy.get('Fixed Assets', 0),
        'Investments': kpi_cy.get('Investments', 0)
    }

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown('<div class="chart-container-3d">', unsafe_allow_html=True)
        fig_3d_revenue = create_3d_revenue_trend(revenue_data)
        st.plotly_chart(fig_3d_revenue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-container-3d">', unsafe_allow_html=True)
        fig_3d_assets = create_3d_asset_distribution(asset_data)
        st.plotly_chart(fig_3d_assets, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-container-3d">', unsafe_allow_html=True)
    fig_3d_performance = create_3d_performance_metrics(metrics)
    st.plotly_chart(fig_3d_performance, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📊 Download Reports")

    with st.spinner("🎨 Generating enhanced reports..."):
        ai_analysis = generate_ai_analysis(metrics)

        months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        revenue_df = pd.DataFrame({
            'Month': months * 2,
            'Year': ['Previous Year'] * 12 + ['Current Year'] * 12,
            'Revenue': np.concatenate([
                generate_monthly_data(kpi_py.get('Total Revenue', 0)),
                generate_monthly_data(kpi_cy.get('Total Revenue', 0))
            ])
        })
        fig_revenue_pdf = px.area(revenue_df, x='Month', y='Revenue', color='Year', title="Revenue Trend", template="seaborn")
        asset_df = pd.DataFrame({
            'Asset Type': ['Current Assets', 'Fixed Assets', 'Investments'],
            'Value': [kpi_cy.get('Current Assets', 0), kpi_cy.get('Fixed Assets', 0), kpi_cy.get('Investments', 0)]
        }).query("Value > 0")
        fig_asset_pdf = px.pie(asset_df, names='Asset Type', values='Value', title="Asset Distribution", hole=0.3)

        charts = {"revenue_trend": fig_revenue_pdf, "asset_distribution": fig_asset_pdf}
        pdf_bytes = create_professional_pdf(metrics, ai_analysis, charts)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(label="💡 Download Professional Insights (PDF)",
                           data=pdf_bytes,
                           file_name=f"{st.session_state.company_name}_3D_Insights_Report.pdf",
                           mime="application/pdf",
                           use_container_width=True)
    with dl_col2:
        st.download_button(label="📊 Download Detailed Report (Excel)",
                           data=st.session_state.excel_report_bytes,
                           file_name=f"{st.session_state.company_name}_Detailed_Report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2 style="color: #667eea;">🎯 Welcome to the 3D Financial Dashboard</h2>
        <p style="font-size: 18px; color: #6b7280; margin: 20px 0;">
            Upload your financial data and experience stunning 3D visualizations!
        </p>
        <div style="background: rgba(255,255,255,0.9); padding: 30px; border-radius: 20px; margin: 20px auto; max-width: 600px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea;">✨ Features:</h3>
            <ul style="text-align: left; color: #6b7280;">
                <li>🚀 Beautiful 3D KPI cards with hover effects</li>
                <li>📊 Interactive 3D charts and visualizations</li>
                <li>💎 Modern glassmorphism design</li>
                <li>📈 Real-time financial analysis</li>
                <li>🎨 Professional PDF and Excel reports</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
