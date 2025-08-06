# agents.py

import pandas as pd
import streamlit as st
import copy
import requests
import json
import io
import traceback
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from config import MASTER_TEMPLATE

# --- AGENT 1: DATA INTAKE ---
def intelligent_data_intake_agent(file_object):
    try:
        xls = pd.ExcelFile(file_object)
        all_data = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for i in range(df.shape[1] - 2):
                col1, col2, col3 = df.iloc[:, i], df.iloc[:, i + 1], df.iloc[:, i+2]
                if (col1.apply(type).eq(str).sum() > len(col1.dropna()) * 0.6 and
                    pd.to_numeric(col2, errors='coerce').notna().sum() > len(col2.dropna()) * 0.6 and
                    pd.to_numeric(col3, errors='coerce').notna().sum() > len(col3.dropna()) * 0.6):
                    pair_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                    pair_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    pair_df.dropna(subset=['Particulars'], inplace=True)
                    all_data.append(pair_df)
        if not all_data: return None
        source_df = pd.concat(all_data, ignore_index=True)
        source_df['Amount_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce').fillna(0)
        source_df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce').fillna(0)
        return source_df
    except Exception:
        return None

# --- AGENT 2: AI MAPPING ---
def ai_mapping_agent(source_particulars, mapping_structure):
    updated_mapping = copy.deepcopy(mapping_structure)
    all_known_keywords = set()
    def get_all_keywords(node):
        for key, value in node.items():
            if isinstance(value, list):
                for kw in value: all_known_keywords.add(kw.lower())
            if isinstance(value, dict): get_all_keywords(value)
    get_all_keywords(updated_mapping)
    unmapped_terms = {p.lower() for p in source_particulars if p.lower() not in all_known_keywords}
    if not unmapped_terms: return updated_mapping
    try:
        YOUR_API_URL = st.secrets["MAPPING_API_URL"]
        YOUR_API_KEY = st.secrets["MAPPING_API_KEY"]
        known_categories = [cat for note in mapping_structure.values() for cat in note.get('sub_items', {}).keys()]
        payload = {"terms_to_map": list(unmapped_terms), "available_categories": known_categories}
        headers = {"Authorization": f"Bearer {YOUR_API_KEY}", "Content-Type": "application/json"}
        response = requests.post(YOUR_API_URL, headers=headers, data=json.dumps(payload), timeout=45)
        response.raise_for_status()
        ai_responses = response.json()
    except Exception:
        ai_responses = {}
    def find_and_update(node, target_key, new_keyword):
        for key, value in node.items():
            if key == target_key and isinstance(value, list):
                if new_keyword not in value: value.append(new_keyword); return True
            if isinstance(value, dict) and find_and_update(value, target_key, new_keyword): return True
        return False
    for term, category in ai_responses.items():
        find_and_update(updated_mapping, category, term)
    return updated_mapping

# --- AGENT 3: AGGREGATOR ---
def hierarchical_aggregator_agent(source_df, notes_structure):
    def initialize_structure(template):
        return {k: initialize_structure(v) if isinstance(v, dict) else {'CY': 0, 'PY': 0} for k, v in template.items()}
    def match_and_aggregate(data, template, df):
        total_cy, total_py = 0, 0
        for key, t_val in template.items():
            if isinstance(t_val, dict):
                sub_cy, sub_py = match_and_aggregate(data[key], t_val, df)
                data[key]['total'] = {'CY': sub_cy, 'PY': sub_py}
                total_cy += sub_cy; total_py += sub_py
            else:
                item_cy, item_py = 0, 0
                keywords = [kw.lower() for kw in t_val]
                for kw in keywords:
                    matched = df[df['Particulars'].str.lower().str.contains(kw, na=False)]
                    if not matched.empty:
                        item_cy += matched['Amount_CY'].sum(); item_py += matched['Amount_PY'].sum()
                data[key] = {'CY': item_cy, 'PY': item_py}
                total_cy += item_cy; total_py += item_py
        return total_cy, total_py
    aggregated_data = {}
    for note_num, note_data in notes_structure.items():
        if 'sub_items' in note_data:
            result = initialize_structure(note_data['sub_items'])
            note_cy, note_py = match_and_aggregate(result, note_data['sub_items'], source_df)
            aggregated_data[note_num] = {'total': {'CY': note_cy, 'PY': note_py}, 'sub_items': result, 'title': note_data['title']}
    return aggregated_data

# --- AGENT 4: VALIDATOR ---
def data_validation_agent(aggregated_data):
    warnings = []
    for year in ['CY', 'PY']:
        get = lambda key, y=year: aggregated_data.get(key, {}).get('total', {}).get(y, 0)
        equity_notes = ['1', '2']
        liability_notes = ['3', '5', '6', '7', '8', '9', '10']
        asset_notes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        deferred_tax = get('4')
        total_equity = sum(get(n) for n in equity_notes)
        total_liabilities = sum(get(n) for n in liability_notes)
        total_assets = sum(get(n) for n in asset_notes)
        final_le = total_equity + total_liabilities + deferred_tax
        final_a = total_assets + deferred_tax
        if abs(final_a - final_le) > 5.0:
            warnings.append(f"CRITICAL ({'2025' if year == 'CY' else '2024'}): Assets ({final_a:,.0f}) != L+E ({final_le:,.0f})")
    return warnings

# --- AGENT 5: REPORTER ---
def report_finalizer_agent(aggregated_data, company_name):
    try:
        wb = Workbook()
        wb.remove(wb.active)
        # (Styling and report generation logic is pasted here)
        company_title_font = Font(name='Calibri', size=16, bold=True, color="0070C0")
        sheet_title_font = Font(name='Calibri', size=14, bold=True)
        header_font = Font(name='Calibri', size=11, bold=True)
        total_font = Font(name='Calibri', size=11, bold=True)
        item_font = Font(name='Calibri', size=11)
        header_fill = PatternFill(start_color="DDEBF7", fill_type="solid")
        thin_side = Side(style='thin', color="000000")
        top_border = Border(top=thin_side); bottom_border = Border(bottom=thin_side)
        number_format = '#,##0;(#,##0);"-"'
        
        def build_styled_sheet(ws, sheet_name, template_data):
            ws.title = sheet_name
            ws.column_dimensions['A'].width = 5; ws.column_dimensions['B'].width = 45
            ws.column_dimensions['C'].width = 8; ws.column_dimensions['D'].width = 20
            ws.column_dimensions['E'].width = 20
            ws.merge_cells('A1:E1'); cell = ws['A1']; cell.value = company_name; cell.font = company_title_font; cell.alignment = Alignment(horizontal='center')
            ws.merge_cells('A2:E2'); cell = ws['A2']; cell.value = sheet_name; cell.font = sheet_title_font; cell.alignment = Alignment(horizontal='center')
            row = 4
            headers = ["", "Particulars", "Note", "As at March 31, 2025", "As at March 31, 2024"]
            for col, text in enumerate(headers, 1): ws.cell(row, col, text).font = header_font; ws.cell(row, col).border = bottom_border
            row += 1
            for idx, desc, note_key, line_type in template_data:
                if line_type == 'header':
                    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
                    ws.cell(row, 1, desc).font = header_font; ws.cell(row, 1).fill = header_fill
                elif line_type in ['item', 'item_no_alpha']:
                    ws.cell(row, 1, idx if line_type == 'item' else "")
                    ws.cell(row, 2, desc)
                    ws.cell(row, 3, note_key).alignment = Alignment(horizontal='center')
                    get_val = lambda k, y: aggregated_data.get(k, {}).get('total', {}).get(y, 0)
                    ws.cell(row, 4, get_val(note_key, 'CY')).number_format = number_format
                    ws.cell(row, 5, get_val(note_key, 'PY')).number_format = number_format
                elif line_type == 'total':
                    ws.cell(row, 2, desc).font = total_font
                    total_cy = sum(aggregated_data.get(n, {}).get('total', {}).get('CY', 0) for n in note_key)
                    total_py = sum(aggregated_data.get(n, {}).get('total', {}).get('PY', 0) for n in note_key)
                    ws.cell(row, 4, total_cy).font = total_font; ws.cell(row, 4).number_format = number_format
                    ws.cell(row, 5, total_py).font = total_font; ws.cell(row, 5).number_format = number_format
                    for c in range(1, 6): ws.cell(row, c).border = top_border
                row += 1
        
        build_styled_sheet(wb.create_sheet("Balance Sheet", 0), "Balance Sheet", MASTER_TEMPLATE["Balance Sheet"])
        build_styled_sheet(wb.create_sheet("Profit and Loss", 1), "Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])
        
        output_buffer = io.BytesIO()
        wb.save(output_buffer)
        return output_buffer.getvalue()
    except Exception as e:
        traceback.print_exc()
        return None