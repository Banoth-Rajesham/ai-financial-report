# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

NOTES_STRUCTURE_AND_MAPPING = {
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital No.of shares'],
                'Equity shares of Rs. 10 each': ['Authorised Equity shares of Rs. 10 each', 'authorised share capital']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares ': ['Issued and fully paid up No.of shares'],
                'Equity shares of Rs. 10 each ': ['Issued and fully paid up Equity shares of Rs. 10 each', 'Issued, subscribed and paid-up', 'Share Capital', 'Equity Capital', 'Paid-up Capital']
            },
            'Issued, subscribed and Partly up capital': {
                'Number of shares  ': ['Issued and Partly up No.of shares'],
                'Equity shares of Rs.10 each fully paid up.': ['Issued and Partly up Equity shares of Rs.10 each']
            },
            '1.1 Reconciliation of number of shares': {
                'Equity shares at the beginning of the year': ['Equity shares at beginning'],
                'Add: Additions during the year': ['Additions to share capital on account of fresh issue'],
                'Ded: Deductions during the year': ['Deductions from share capital on account of shares bought back'],
                'Balance at the end of the year': ['Balance at the end of the year shares']
            },
            '1.2 Details of share held by shareholders holding more than 5%': {
                'M A Waheed Khan': ['shareholding M A Waheed Khan'],
                'M A Qhuddus Khan': ['shareholding M A Qhuddus Khan'],
                'M A Khadir Khan Asif': ['shareholding M A Khadir Khan Asif'],
                'M A Rauf Khan': ['shareholding M A Rauf Khan']
            }
        }
    },
    '2': {
        'title': 'Reserve and surplus',
        'sub_items': {
            '2.1 Capital reserve': { 'Balance at the end of the year': ['Capital reserve'] },
            '2.2 Securities premium account': { 'Balance at the end of the year ': ['Securities premium', 'share premium'] },
            '2.4 General reserve': { 'Balance at the end of the year    ': ['General reserve'] },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': { 'Balance at the end of the year      ': ['Retained Earnings', 'Surplus', 'P&L Account Balance', 'Profit & Loss A/c', 'Reserves and surplus'] }
        }
    },
    '3': {'title': 'Long term borrowings', 'sub_items': {'3.0 Long term borrowings Summary': {'(a) Term loans from banks': ['Term loans from banks', 'term loan', 'long term borrowings', 'Mortgage Loan'], '(e) Other loans and advances': ['Other loans and advances specify nature', 'debentures']}}},
    '4': {'title': 'Deferred Tax Asset/Liability','sub_items': {'Tax on Difference between Book & Tax depreciation': ['deferred tax asset', 'deferred tax liability', 'deferred tax']}},
    '5': {'title': 'Other long term liabilities', 'sub_items': {'(b) Others': {'Others (specify nature)': ['other long term liabilities']}}},
    '6': {'title': 'Long term provisions', 'sub_items': {'(b) Provision - Others': {'Provision - others (give details)': ['long term provisions']}}},
    '7': {'title': 'Short term borrowings', 'sub_items': {'(a) Loans repayable on demand': {'From banks - Unsecured': ['short term borrowings', 'bank overdraft']}}},
    '8': {'title': 'Trade payables', 'sub_items': {'Trade payables: Other than Acceptances': ['trade payables', 'sundry creditors']}},
    '9': {'title': 'Other current liabilities', 'sub_items': {'Other payables (Salaries and consultant fee)': ['other current liabilities', 'bills payable', 'outstanding expenses']}},
    '10': {'title': 'Short term provisions', 'sub_items': {'(b) Provision - Others': {'Provision for tax (net)':['short term provisions', 'provision for tax']}}},
    '11': {'title': 'Fixed Assets (Tangible & Intangible)', 'sub_items': {'Closing WDV': ['tangible assets', 'net fixed assets', 'fixed assets', 'land & building', 'plant & machinery', 'motor vehicles', 'Furniture & Fixture'], 'Depreciation for the year': ['Depreciation', 'Depriciation for the year', 'to depreciation']}},
    '12': {'title': 'Non-current Investments', 'sub_items': {'B. Other Investments': {'(h) Other non-current investments ': ['non-current investments', 'investments']}}},
    '13': {'title': 'Long term loans and advances', 'sub_items': {'(e) Prepaid expenses - Unsecured, considered good': ['long term loans and advances']}},
    '14': {'title': 'Other non-current assets', 'sub_items': {'(d) Others': {'Others (specify nature)':['other non-current assets']}}},
    '15': {'title': 'Current Investments', 'sub_items': {'B. Other current investments': {'(g) Other investments (specify nature)': ['current investments']}}},
    '16': {'title': 'Inventories', 'sub_items': {'(d) Stock-in-trade': {'Stock-in-trade': ['inventories', 'stock/inventories', 'closing stock', 'opening stock', 'to opening stock', 'by closing stock']}}},
    '17': {'title': 'Trade Receivables', 'sub_items': {'Other Trade receivables': {'Unsecured, considered good ': ['trade receivables', 'sundry debtors', 'bills receivable']}}},
    '18': {'title': 'Cash and cash equivalents', 'sub_items': {'(c) Balances with banks': {'(i) In current accounts': ['cash and cash equivalents', 'cash at bank']}}},
    '19': {'title': 'Short term loans and advances', 'sub_items': {'(d) Prepaid expenses': ['short term loans and advances', 'prepaid']}},
    '20': {'title': 'Other current assets', 'sub_items': {'(a) Unbilled revenue': ['other current assets']}},
    '21': {'title': 'Revenue from Operations', 'sub_items': {'Sale of Services': ['revenue from operations', 'by sales']}},
    '22': {'title': 'Other income', 'sub_items': {'Miscellaneous Income': ['other income', 'by interest received', 'by dividend received', 'by commission received', 'by discount received', 'by bad debts recovered', 'miscellaneous income']}},
    '23': {'title': 'Cost of Materials Consumed', 'sub_items': {'Purchases': ['cost of materials consumed', 'to purchases']}},
    '24': {'title': 'Employee benefit expenses', 'sub_items': {'Salaries and Wages': ['employee benefit expenses', 'to wages', 'to salaries']}},
    '25': {'title': 'Finance Costs', 'sub_items': {'Interest on borrowings': ['finance costs', 'to interest paid']}},
    '26': {'title': 'Other expenses', 'sub_items': {'Accounting Fee': ['Accounting Fee'],'Audit Fees': ['Audit Fees'],'Admin expenses': ['Admin expenses'],'Bank Charges': ['Bank Charges'],'Consultancy charges': ['Consultancy charges'],'Electrcity charges': ['Electrcity charges', 'Electricity charges', 'to electricity'],'Insurance': ['Insurance', 'to insurance'],'Rent': ['Rent', 'to rent'],'Travelling Expense': ['Travelling Expense'],'Telephone expenses': ['Telephone expenses', 'to telephone'],'Repair and maintenance': ['Repair and maintenance', 'to repairs & maintenance'],'Other expenses': ['Other expenses', 'miscellaneous expenses', 'to bad debts', 'to printing & stationery']}},
    "27": { "title": "Tax expense", "sub_items": {'Current tax': ['current tax', 'taxation']}}
}

MASTER_TEMPLATE = {
    "Balance Sheet": [
        ("", "Particulars", "Note", "header_col"),
        ("I", "EQUITY AND LIABILITIES", None, "header"),
        ("1", "Shareholder's funds", None, "sub_header"),
        ("(a)", "Share Capital", "1", "item"),
        ("(b)", "Reserves and surplus", "2", "item"),
        ("2", "Non-current liabilities", None, "sub_header"),
        ("(a)", "Long-term borrowings", "3", "item"),
        ("(b)", "Deferred tax liabilities (Net)", "4", "item"),
        ("(c)", "Other Long-term liabilities", "5", "item"),
        ("(d)", "Long-term provisions", "6", "item"),
        ("3", "Current liabilities", None, "sub_header"),
        ("(a)", "Short-term borrowings", "7", "item"),
        ("(b)", "Trade payables", "8", "item"),
        ("(c)", "Other current liabilities", "9", "item"),
        ("(d)", "Short-term provisions", "10", "item"),
        ("", "TOTAL EQUITY AND LIABILITIES", ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], "total"),
        ("", "", None, "spacer"),
        ("II", "ASSETS", None, "header"),
        ("1", "Non-current assets", None, "sub_header"),
        ("(a)", "Fixed assets (Tangible & Intangible)", "11", "item"),
        ("(b)", "Non-current investments", "12", "item"),
        ("(c)", "Deferred tax assets (Net)", "4", "item"),
        ("(d)", "Long-term loans and advances", "13", "item"),
        ("(e)", "Other non-current assets", "14", "item"),
        ("2", "Current assets", None, "sub_header"),
        ("(a)", "Current investments", "15", "item"),
        ("(b)", "Inventories", "16", "item"),
        ("(c)", "Trade receivables", "17", "item"),
        ("(d)", "Cash and cash equivalents", "18", "item"),
        ("(e)", "Short-term loans and advances", "19", "item"),
        ("(f)", "Other current assets", "20", "item"),
        ("", "TOTAL ASSETS", ["11", "12", "4", "13", "14", "15", "16", "17", "18", "19", "20"], "total"),
    ],
    "Profit and Loss": [
        ("", "Particulars", "Note", "header_col"),
        ("I", "Revenue from operations", "21", "item"),
        ("II", "Other Income", "22", "item"),
        ("III", "Total Revenue (I + II)", ["21", "22"], "total"),
        ("", "", None, "spacer"),
        ("IV", "Expenses", None, "header"),
        ("", "Cost of Materials Consumed", "23", "item_no_alpha"),
        ("", "Changes in inventories", "16", "item_no_alpha"),
        ("", "Employee benefit expenses", "24", "item_no_alpha"),
        ("", "Finance Costs", "25", "item_no_alpha"),
        ("", "Depreciation and amortization expenses", "11", "item_no_alpha"),
        ("", "Other expenses", "26", "item_no_alpha"),
        ("","Total Expenses", ["23", "16", "24", "25", "11", "26"], "total"),
        ("", "", None, "spacer"),
        ("V", "Profit before tax (III - IV)", "PBT", "total"),
        ("", "", None, "spacer"),
        ("VI", "Tax expense", None, "header"),
        ("", "Current tax", "27", "item_no_alpha"),
        ("", "Deferred tax", "4", "item_no_alpha"),
        ("","Total Tax Expense", ["27", "4"], "total"),
        ("", "", None, "spacer"),
        ("VII", "Profit/(Loss) for the period (V - VI)", "PAT", "total"),
    ],
    "Notes to Accounts": NOTES_STRUCTURE_AND_MAPPING
}

def apply_main_sheet_styling(ws, template, company_name):
    title_font = Font(bold=True, size=16); subtitle_font = Font(bold=True, size=12)
    header_font = Font(bold=True); bold_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    ws.column_dimensions['A'].width = 5; ws.column_dimensions['B'].width = 65; ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 20; ws.column_dimensions['E'].width = 20
    ws.merge_cells('A1:E1'); ws['A1'] = company_name; ws['A1'].font = title_font; ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2'); ws['A2'] = ws.title; ws['A2'].font = subtitle_font; ws['A2'].alignment = Alignment(horizontal='center')
    for cell in ws[4]: cell.font = header_font; cell.alignment = Alignment(horizontal='center')
    for i, row_template in enumerate(template):
        row_num = i + 5
        if row_template[3] in ['header', 'sub_header']: ws[f'B{row_num}'].font = bold_font
        elif row_template[3] == 'total':
            for cell in ws[row_num]: cell.font = bold_font
        for col_letter in ['D', 'E']:
            if ws[f'{col_letter}{row_num}'].value is not None: ws[f'{col_letter}{row_num}'].number_format = currency_format

def apply_note_sheet_styling(ws):
    header_font = Font(bold=True, color="FFFFFF"); title_font = Font(bold=True, size=14); total_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    ws.column_dimensions['A'].width = 65; ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 20
    ws.merge_cells('A1:C1'); ws['A1'].font = title_font
    for cell in ws[2]: cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid"); cell.font = header_font
    for row_idx, row in enumerate(ws.iter_rows(min_row=3, max_col=3), start=3):
        is_total = (str(ws[f'A{row_idx}'].value).strip().lower() == 'total')
        for cell in row:
            if cell.column > 1: cell.number_format = currency_format
            if is_total: cell.font = total_font; cell.border = Border(top=Side(style='thin'))

def report_finalizer_agent(aggregated_data, company_name):
    """AGENT 5: Constructs a detailed, styled, multi-sheet Excel report."""
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            def get_val(note_id, year):
                if note_id == "16_change": return (aggregated_data.get('16', {}).get('total', {}).get('CY', 0) or 0) - (aggregated_data.get('16', {}).get('total', {}).get('PY', 0) or 0) if year == 'CY' else 0
                if note_id == "11_dep": return aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
                return aggregated_data.get(str(note_id), {}).get('total', {}).get(year, 0)

            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                rows = []
                for r_template in template:
                    row = {' ': r_template[0], 'Particulars': r_template[1], 'Note': r_template[2] if isinstance(r_template[2], str) else "", 'CY': None, 'PY': None}
                    if r_template[3] in ["item", "item_no_alpha"]:
                        row['CY'], row['PY'] = get_val(r_template[2], 'CY'), get_val(r_template[2], 'PY')
                    rows.append(row)
                df = pd.DataFrame(rows).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
                for i, r_template in enumerate(template):
                    if r_template[3] == 'total':
                        notes_to_sum = r_template[2]
                        if isinstance(notes_to_sum, list):
                            cy_sum = df[df['Note'].isin(notes_to_sum)]['As at March 31, 2025'].sum()
                            py_sum = df[df['Note'].isin(notes_to_sum)]['As at March 31, 2024'].sum()
                            df.iloc[i, 3], df.iloc[i, 4] = cy_sum, py_sum
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3); apply_main_sheet_styling(writer.sheets[sheet_name], template, company_name)

            for note_num in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info, note_data = NOTES_STRUCTURE_AND_MAPPING[note_num], aggregated_data.get(note_num)
                if note_data and note_data.get('sub_items'):
                    df_data, title = [], note_info['title']
                    def process(items, level=0):
                        for key, val in items.items():
                            if isinstance(val, dict) and 'CY' in val: df_data.append({'Particulars': '  '*level+key, 'CY': val.get('CY'), 'PY': val.get('PY')})
                            elif isinstance(val, dict): df_data.append({'Particulars': '  '*level+key, 'CY': None, 'PY': None}); process(val, level+1)
                    process(note_data['sub_items'])
                    df = pd.DataFrame(df_data).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY'), 'As at March 31, 2024': note_data['total'].get('PY')}])
                    df = pd.concat([df, total_row], ignore_index=True)
                    sheet_name=f'Note {note_num}'; df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1); ws=writer.sheets[sheet_name]; ws['A1'].value=f'Note {note_num}: {title}'; apply_note_sheet_styling(ws)
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}"); import traceback; traceback.print_exc(); return None
