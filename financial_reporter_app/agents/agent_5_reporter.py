# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, WITH PROFESSIONAL STYLING)
# This version creates a visually appealing Excel report with colors and borders.
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes final data and writes a complete, multi-sheet Excel report
    with professional styling inspired by the Someka template.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # --- DEFINE COLOR PALETTE AND STYLES ---
            colors = {
                'asset_bg': '#E2EFDA',
                'lia_bg': '#FDE9D9',
                'eq_bg': '#D9E1F2',
                'total_bg_asset': '#C6E0B4',
                'total_bg_lia': '#F8CBAD',
                'total_bg_eq': '#B4C6E7',
                'grand_total_bg': '#A9D08E',
                'header_bg': '#44546A',
                'header_font': '#FFFFFF',
                'border_light': '#D0D0D0',
                'border_dark': '#000000'
            }

            # --- DEFINE CELL FORMATS ---
            # Main Headers
            fmt_header_assets = workbook.add_format({'bold': True, 'font_color': colors['header_font'], 'bg_color': colors['header_bg'], 'align': 'center', 'valign': 'vcenter', 'border': 1})
            fmt_header_lia = workbook.add_format({'bold': True, 'font_color': colors['header_font'], 'bg_color': colors['header_bg'], 'align': 'center', 'valign': 'vcenter', 'border': 1})
            fmt_header_eq = workbook.add_format({'bold': True, 'font_color': colors['header_font'], 'bg_color': colors['header_bg'], 'align': 'center', 'valign': 'vcenter', 'border': 1})
            
            # Sub-Header Formats
            fmt_subheader_asset = workbook.add_format({'bold': True, 'bg_color': colors['asset_bg'], 'top': 1, 'bottom': 1, 'border_color': colors['border_dark']})
            fmt_subheader_lia = workbook.add_format({'bold': True, 'bg_color': colors['lia_bg'], 'top': 1, 'bottom': 1, 'border_color': colors['border_dark']})
            fmt_subheader_eq = workbook.add_format({'bold': True, 'bg_color': colors['eq_bg'], 'top': 1, 'bottom': 1, 'border_color': colors['border_dark']})

            # Data Row Formats
            num_format = '#,##0'
            fmt_data_asset = workbook.add_format({'bg_color': colors['asset_bg'], 'num_format': num_format})
            fmt_data_lia = workbook.add_format({'bg_color': colors['lia_bg'], 'num_format': num_format})
            fmt_data_eq = workbook.add_format({'bg_color': colors['eq_bg'], 'num_format': num_format})

            # Total Row Formats
            fmt_total_asset = workbook.add_format({'bold': True, 'bg_color': colors['total_bg_asset'], 'num_format': num_format, 'top': 1, 'bottom': 1})
            fmt_total_lia = workbook.add_format({'bold': True, 'bg_color': colors['total_bg_lia'], 'num_format': num_format, 'top': 1, 'bottom': 1})
            fmt_total_eq = workbook.add_format({'bold': True, 'bg_color': colors['total_bg_eq'], 'num_format': num_format, 'top': 1, 'bottom': 1})
            
            # Grand Total Format
            fmt_grand_total = workbook.add_format({'bold': True, 'bg_color': colors['grand_total_bg'], 'num_format': num_format, 'top': 1, 'bottom': 2})

            # --- 1. RENDER THE BALANCE SHEET ---
            bs_sheet = workbook.add_worksheet("Balance Sheet")
            bs_sheet.hide_gridlines(2)
            bs_sheet.set_column('A:A', 25)
            bs_sheet.set_column('B:C', 18)
            bs_sheet.set_column('D:D', 5) # Spacer column
            bs_sheet.set_column('E:E', 25)
            bs_sheet.set_column('F:G', 18)
            
            # --- ASSETS SIDE ---
            bs_sheet.merge_range('A1:C1', 'ASSETS', fmt_header_assets)
            bs_sheet.write('A2', 'Line Item', bold_format)
            bs_sheet.write('B2', 'Beginning Balance', bold_format)
            bs_sheet.write('C2', 'End Balance', bold_format)
            
            # Get data from notes
            get_total = lambda key, yr: aggregated_data.get(str(key), {}).get('total', {}).get(yr, 0)

            # Current Assets
            row = 2
            bs_sheet.write(row, 0, 'Current Assets', fmt_subheader_asset)
            bs_sheet.write(row, 1, None, fmt_subheader_asset)
            bs_sheet.write(row, 2, None, fmt_subheader_asset)
            row += 1
            
            # Cash and cash equivalents
            bs_sheet.write(row, 0, 'Cash', fmt_data_asset)
            bs_sheet.write(row, 1, get_total(18, 'PY'), fmt_data_asset)
            bs_sheet.write(row, 2, get_total(18, 'CY'), fmt_data_asset)
            row += 1
            
            # Trade Receivables
            bs_sheet.write(row, 0, 'Trade Accounts Receivable', fmt_data_asset)
            bs_sheet.write(row, 1, get_total(17, 'PY'), fmt_data_asset)
            bs_sheet.write(row, 2, get_total(17, 'CY'), fmt_data_asset)
            row += 1
            
            # Inventories
            bs_sheet.write(row, 0, 'Inventories', fmt_data_asset)
            bs_sheet.write(row, 1, get_total(16, 'PY'), fmt_data_asset)
            bs_sheet.write(row, 2, get_total(16, 'CY'), fmt_data_asset)
            row += 5 # Add empty rows
            
            # Total Current Assets
            total_ca_py = get_total(18, 'PY') + get_total(17, 'PY') + get_total(16, 'PY')
            total_ca_cy = get_total(18, 'CY') + get_total(17, 'CY') + get_total(16, 'CY')
            bs_sheet.write(row, 0, 'Total Current Assets', fmt_total_asset)
            bs_sheet.write(row, 1, total_ca_py, fmt_total_asset)
            bs_sheet.write(row, 2, total_ca_cy, fmt_total_asset)
            row += 1

            # Non-Current Assets
            bs_sheet.write(row, 0, 'Non-Current Assets', fmt_subheader_asset)
            bs_sheet.write(row, 1, None, fmt_subheader_asset)
            bs_sheet.write(row, 2, None, fmt_subheader_asset)
            row += 1
            
            # Fixed Assets
            bs_sheet.write(row, 0, 'Property, Plant & Equipment', fmt_data_asset)
            bs_sheet.write(row, 1, get_total(11, 'PY'), fmt_data_asset)
            bs_sheet.write(row, 2, get_total(11, 'CY'), fmt_data_asset)
            row += 1
            
            # Non-current Investments
            bs_sheet.write(row, 0, 'Equity Investments', fmt_data_asset)
            bs_sheet.write(row, 1, get_total(12, 'PY'), fmt_data_asset)
            bs_sheet.write(row, 2, get_total(12, 'CY'), fmt_data_asset)
            row += 1
            
            # Total Non-Current Assets
            total_nca_py = get_total(11, 'PY') + get_total(12, 'PY')
            total_nca_cy = get_total(11, 'CY') + get_total(12, 'CY')
            bs_sheet.write(row, 0, 'Total Non-Current Assets', fmt_total_asset)
            bs_sheet.write(row, 1, total_nca_py, fmt_total_asset)
            bs_sheet.write(row, 2, total_nca_cy, fmt_total_asset)
            row += 1
            
            # Total Assets
            bs_sheet.write(row, 0, 'Total Assets', fmt_grand_total)
            bs_sheet.write(row, 1, total_ca_py + total_nca_py, fmt_grand_total)
            bs_sheet.write(row, 2, total_ca_cy + total_nca_cy, fmt_grand_total)


            # --- LIABILITIES & EQUITY SIDE ---
            bs_sheet.merge_range('E1:G1', 'LIABILITIES & EQUITY', fmt_header_lia)
            bs_sheet.write('E2', 'Line Item', bold_format)
            bs_sheet.write('F2', 'Beginning Balance', bold_format)
            bs_sheet.write('G2', 'End Balance', bold_format)
            
            row = 2
            # Current Liabilities
            bs_sheet.write(row, 4, 'Current Liabilities', fmt_subheader_lia)
            bs_sheet.write(row, 5, None, fmt_subheader_lia)
            bs_sheet.write(row, 6, None, fmt_subheader_lia)
            row += 1
            
            # Short-Term Debt
            bs_sheet.write(row, 4, 'Short-Term Debt', fmt_data_lia)
            bs_sheet.write(row, 5, get_total(7, 'PY'), fmt_data_lia)
            bs_sheet.write(row, 6, get_total(7, 'CY'), fmt_data_lia)
            row += 1
            
            # Trade Accounts Payable
            bs_sheet.write(row, 4, 'Trade Accounts Payable', fmt_data_lia)
            bs_sheet.write(row, 5, get_total(8, 'PY'), fmt_data_lia)
            bs_sheet.write(row, 6, get_total(8, 'CY'), fmt_data_lia)
            row += 1
            
            # Other Accrued Liabilities
            bs_sheet.write(row, 4, 'Other Accrued Liabilities', fmt_data_lia)
            bs_sheet.write(row, 5, get_total(9, 'PY'), fmt_data_lia)
            bs_sheet.write(row, 6, get_total(9, 'CY'), fmt_data_lia)
            row += 1
            
            # Total Current Liabilities
            total_cl_py = get_total(7, 'PY') + get_total(8, 'PY') + get_total(9, 'PY')
            total_cl_cy = get_total(7, 'CY') + get_total(8, 'CY') + get_total(9, 'CY')
            bs_sheet.write(row, 4, 'Total Current Liabilities', fmt_total_lia)
            bs_sheet.write(row, 5, total_cl_py, fmt_total_lia)
            bs_sheet.write(row, 6, total_cl_cy, fmt_total_lia)
            row += 1
            
            # Non-Current Liabilities
            bs_sheet.write(row, 4, 'Non-Current Liabilities', fmt_subheader_lia)
            bs_sheet.write(row, 5, None, fmt_subheader_lia)
            bs_sheet.write(row, 6, None, fmt_subheader_lia)
            row += 1
            
            # Long-Term Debt
            bs_sheet.write(row, 4, 'Long-Term Debt', fmt_data_lia)
            bs_sheet.write(row, 5, get_total(3, 'PY'), fmt_data_lia)
            bs_sheet.write(row, 6, get_total(3, 'CY'), fmt_data_lia)
            row += 1
            
            # Total Non-Current Liabilities
            total_ncl_py = get_total(3, 'PY')
            total_ncl_cy = get_total(3, 'CY')
            bs_sheet.write(row, 4, 'Total Non-Current Liabilities', fmt_total_lia)
            bs_sheet.write(row, 5, total_ncl_py, fmt_total_lia)
            bs_sheet.write(row, 6, total_ncl_cy, fmt_total_lia)
            row += 1
            
            # Total Liabilities
            bs_sheet.write(row, 4, 'Total Liabilities', fmt_total_lia)
            bs_sheet.write(row, 5, total_cl_py + total_ncl_py, fmt_total_lia)
            bs_sheet.write(row, 6, total_cl_cy + total_ncl_cy, fmt_total_lia)
            row += 1
            
            # Equity
            bs_sheet.write(row, 4, 'EQUITY', fmt_subheader_eq)
            bs_sheet.write(row, 5, None, fmt_subheader_eq)
            bs_sheet.write(row, 6, None, fmt_subheader_eq)
            row += 1
            
            # Common Shares
            bs_sheet.write(row, 4, 'Common Shares', fmt_data_eq)
            bs_sheet.write(row, 5, get_total(1, 'PY'), fmt_data_eq)
            bs_sheet.write(row, 6, get_total(1, 'CY'), fmt_data_eq)
            row += 1
            
            # Retained Earnings
            bs_sheet.write(row, 4, 'Retained Earnings', fmt_data_eq)
            bs_sheet.write(row, 5, get_total(2, 'PY'), fmt_data_eq)
            bs_sheet.write(row, 6, get_total(2, 'CY'), fmt_data_eq)
            row += 1
            
            # Total Equity
            total_eq_py = get_total(1, 'PY') + get_total(2, 'PY')
            total_eq_cy = get_total(1, 'CY') + get_total(2, 'CY')
            bs_sheet.write(row, 4, 'Total Equity', fmt_total_eq)
            bs_sheet.write(row, 5, total_eq_py, fmt_total_eq)
            bs_sheet.write(row, 6, total_eq_cy, fmt_total_eq)
            row += 1

            # Total Liabilities & Equity
            bs_sheet.write(row, 4, 'Total Liabilities & Equity', fmt_grand_total)
            bs_sheet.write(row, 5, total_cl_py + total_ncl_py + total_eq_py, fmt_grand_total)
            bs_sheet.write(row, 6, total_cl_cy + total_ncl_cy + total_eq_cy, fmt_grand_total)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
