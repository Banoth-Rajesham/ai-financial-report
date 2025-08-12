import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from datetime import datetime
from io import BytesIO
import base64
from fpdf import FPDF

sys.path.append('financial_reporter_app')

NEUMORPHIC_CSS = """
<style>
body {
    background-color: #121212;
    color: #E0E0E0;
    font-family: 'Poppins', sans-serif;
}
.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: #121212;
    box-shadow: 9px 9px 16px #0d0d0d, -9px -9px 16px #1a1a1a;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.block-container:hover {
    transform: translateY(-5px);
    box-shadow: 12px 12px 20px #0d0d0d, -12px -12px 20px #1a1a1a;
}
.stButton>button {
    background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
    color: #E0E0E0;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    box-shadow: 5px 5px 10px #0a0a0a, -5px -5px 10px #1f1f1f;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    box-shadow: 0 0 15px #00ffcc, 0 0 25px #39ff14;
    transform: translateY(-4px) scale(1.05);
}
.stTextInput>div>div>input, .stSelectbox>div>div>select {
    background: #121212;
    color: #E0E0E0;
    border-radius: 12px;
    border: none;
    padding: 0.5rem;
    box-shadow: inset 4px 4px 6px #0d0d0d, inset -4px -4px 6px #1a1a1a;
}
h1, h2, h3, h4, h5 {
    color: #E0E0E0;
}
</style>
"""

st.markdown(NEUMORPHIC_CSS, unsafe_allow_html=True)

def generate_monthly_data():
    np.random.seed(0)
    months = pd.date_range(start="2024-01-01", periods=12, freq='M')
    revenue = np.random.randint(20000, 50000, 12)
    expenses = np.random.randint(10000, 30000, 12)
    profit = revenue - expenses
    return pd.DataFrame({"Month": months, "Revenue": revenue, "Expenses": expenses, "Profit": profit})

def create_dark_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Revenue'], mode='lines+markers',
                             name='Revenue', line=dict(color='#00ffcc', width=3)))
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Expenses'], mode='lines+markers',
                             name='Expenses', line=dict(color='#39ff14', width=3)))
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Profit'], mode='lines+markers',
                             name='Profit', line=dict(color='#ADFF2F', width=3)))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#121212',
        plot_bgcolor='#121212',
        font=dict(color='#E0E0E0'),
        hovermode='x unified'
    )
    return fig

def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Financial Report", ln=True, align='C')
    for i, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Month'].strftime('%b %Y')}: Revenue ${row['Revenue']}, Expenses ${row['Expenses']}, Profit ${row['Profit']}", ln=True)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

st.title("💹 3D Financial Dashboard - Dark Neumorphic")

df = generate_monthly_data()
fig = create_dark_chart(df)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)

col1, col2 = st.columns(2)
with col1:
    if st.button("📄 Export to PDF"):
        pdf_data = export_pdf(df)
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="financial_report.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
with col2:
    if st.button("📊 Export to CSV"):
        csv_data = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv_data).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="financial_report.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
