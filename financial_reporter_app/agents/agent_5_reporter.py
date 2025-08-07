# PASTE THIS ENTIRE CODE BLOCK INTO: agent_5_reporter.py

import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side
from config import SCHEDULE_III_CONFIG, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: This agent takes the final aggregated data and constructs a
    Schedule III compliant, multi-sheet Excel report.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")

    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            # --- 1. PREPARE BALANCE SHEET ---
            bs_data = []
            for item in SCHEDULE_III_CONFIG['balance_sheet']:
                row = {
                    'Particulars': item['label'],
                    'Note': item.get('note', ''),
                    'CY': 0,
                    'PY': 0
                }
                if item.get('is_total'):
                    # Calculate totals based on the 'sum_of' key
                    for note_to_sum in item.get('sum_of', []):
                        row['CY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                        row['PY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                elif 'note' in item and item['note']:
                    note_str = str(item['note'])
                    row['CY'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                    row['PY'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
                bs_data.append(row)

            bs_df = pd.DataFrame(bs_data).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
            
            # --- 2. PREPARE PROFIT & LOSS ---
            pl_data = []
            for item in SCHEDULE_III_CONFIG['profit_and_loss']:
                row = {
                    'Particulars': item['label'],
                    'Note': item.get('note', ''),
                    'CY': 0,
                    'PY': 0
                }
                if item.get('is_total'):
                    # Handle special case for Total Revenue
                    if item['id'] == 'total_revenue':
                        for note_to_sum in item.get('sum_of', []):
                            row['CY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                            row['PY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                    # Handle other totals
                    else:
                         for note_to_sum in item.get('sum_of', []):
                            row['CY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                            row['PY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                elif 'note' in item and item['note']:
                     note_str = str(item['note'])
                     row['CY'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                     row['PY'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
                pl_data.append(row)

            pl_df = pd.DataFrame(pl_data).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})

            # --- 3. WRITE MAIN SHEETS ---
            bs_df.to_excel(writer, sheet_name='Balance Sheet', index=False, startrow=3)
            pl_df.to_excel(writer, sheet_name='Profit and Loss', index=False, startrow=3)
            
            # Add titles to main sheets
            ws_bs = writer.sheets['Balance Sheet']
            ws_bs['A1'] = company_name
            ws_bs['A2'] = 'Balance Sheet'
            
            ws_pl = writer.sheets['Profit and Loss']
            ws_pl['A1'] = company_name
            ws_pl['A2'] = 'Profit and Loss'


            # ========================================================== #
            # == THIS IS THE CRUCIAL PART THAT ADDS ALL THE NOTES     == #
            # ========================================================== #
            for note_num_str, note_data in aggregated_data.items():
                if note_num_str in NOTES_STRUCTURE_AND_MAPPING and 'sub_items' in note_data:
                    sheet_name = f'Note {note_num_str}'
                    note_title = NOTES_STRUCTURE_AND_MAPPING[note_num_str]['title']

                    note_df_data = []
                    for particular, values in note_data['sub_items'].items():
                        note_df_data.append({
                            'Particulars': particular,
                            'As at March 31, 2025': values.get('CY', 0),
                            'As at March 31, 2024': values.get('PY', 0)
                        })

                    note_df = pd.DataFrame(note_df_data)

                    # Add the total row
                    total_row = pd.DataFrame([{
                        'Particulars': 'Total',
                        'As at March 31, 2025': note_data['total'].get('CY', 0),
                        'As at March 31, 2024': note_data['total'].get('PY', 0)
                    }])
                    note_df = pd.concat([note_df, total_row], ignore_index=True)

                    # Write to Excel
                    note_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                    ws_note = writer.sheets[sheet_name]
                    ws_note['A1'] = f'Note {note_num_str}: {note_title}'
            # ========================================================== #


        print("✅ Report Finalizer SUCCESS: Report generated.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        return None
