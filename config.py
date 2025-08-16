# ==============================================================================
# FILE: config.py (DEFINITIVE MASTER VERSION FOR 100% MAPPING)
# ==============================================================================

NOTES_STRUCTURE_AND_MAPPING = {
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital No.of shares', 'Number of shares'],
                'Equity shares of Rs. 10 each': ['Authorised Equity shares of Rs. 10 each', 'Equity shares of Rs. 10 each']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares': ['Issued and fully paid up No.of shares', 'Number of shares'],
                'Equity shares of Rs. 10 each': ['Issued and fully paid up Equity shares of Rs. 10 each', 'Equity shares of Rs. 10 each', 'Share Capital', 'Equity Capital']
            },
            'Issued, subscribed and Partly up capital': {
                'Number of shares': ['Issued and Partly up No.of shares'],
                'Equity shares of Rs.10 each fully paid up.': ['Issued and Partly up Equity shares of Rs.10 each']
            },
            '1.1 Reconciliation of number of shares': {
                'Equity shares at the beginning of the year': ['Equity shares at beginning', 'opening balance'],
                'Add: Additions during the year': ['Additions during the year', 'fresh issue'],
                'Ded: Deductions during the year': ['Deductions during the year', 'shares bought back'],
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
            '2.1 Capital reserve': {
                'Balance at the beginning of the year': ['Capital reserve at beginning'],
                'Add: Additions during the year': ['Additions to Capital reserve'],
                'Less: Utilized/transferred during the year': ['Utilized from Capital reserve'],
                'Balance at the end of the year': ['Capital reserve at end', 'Capital reserve']
            },
            '2.2 Securities premium account': {
                'Balance at the beginning of the year': ['Securities premium at beginning'],
                'Add: Premium on shares issued during the year': ['Premium on shares issued'],
                'Balance at the end of the year': ['Securities premium at end', 'Securities premium', 'share premium']
            },
            '2.4 General reserve': {
                'Balance at the beginning of the year': ['General reserve at beginning'],
                'Add: Transferred from surplus in Statement of Profit and Loss': ['Transferred to general reserve from surplus'],
                'Balance at the end of the year': ['General reserve at end', 'General reserve']
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Balance at the beginning of the year': ['Surplus at beginning', 'Opening Balance'],
                'Add: Profit / (Loss) for the year': ['Profit / Loss for the year', 'Net Profit'],
                'Less: Interim dividend': ['Interim dividend'],
                'Less: Transferred to General reserve': ['Transferred from surplus to general reserve'],
                'Balance at the end of the year': ['Surplus at end', 'Retained Earnings', 'Surplus']
            }
        }
    },
    '3': { 'title': 'Long term borrowings', 'sub_items': {'Long term borrowings': ['Term loans from banks', 'long term borrowings', 'Mortgage Loan']} },
    '4': { 'title': 'Deferred Tax Asset/Liability', 'sub_items': {'Deferred Tax': ['Deferred Tax', 'Tax on Difference between Book & Tax depreciation']} },
    '5': { 'title': 'Other long term liabilities', 'sub_items': {'Other long term liabilities': ['Other long term liabilities']} },
    '6': { 'title': 'Long term provisions', 'sub_items': {'Long term provisions': ['Long term provisions']} },
    '7': { 'title': 'Short term borrowings', 'sub_items': {'Short term borrowings': ['short term borrowings', 'bank overdraft']} },
    '8': { 'title': 'Trade payables', 'sub_items': {'Trade payables': ['Trade payables', 'sundry creditors', 'Other than Acceptances']} },
    '9': { 'title': 'Other current liabilities', 'sub_items': {'Other current liabilities': ['Other current liabilities', 'Other payables']} },
    '10': { 'title': 'Short term provisions', 'sub_items': {'Short term provisions': ['short term provisions', 'Provision for tax', 'Provision for Audit Fees']} },
    '11': {
        'title': 'Fixed Assets (Tangible & Intangible)',
        'sub_items': {
            'Depreciation for the year': ['Depriciation for the year', 'Depreciation', 'Dep as per IT ACT', 'Dep as per Comp'],
            'Opening WDV': ['Opening WDV', 'WDV as on 31-03-2024'],
            'Additions': ['additions before 30.09', 'additions after 30.09', 'Additions'],
            'Deletions': ['Deletions', 'Sales/Adjustments'],
            'Closing WDV': ['W.d.v as on 31/3/2025', 'WDV on 31/03/2025', 'Closing Balance'],
            'Office Interiors': ['Office Interiors'],
            'Air Conditioners': ['Air Conditioners'],
            'Battery': ['Battery'],
            'CCTV Camera': ['CC TV Camera', 'CCTV Camera'],
            'Computers': ['Computers'],
            'Curtains': ['Curtains'],
            'Electronic Items': ['Electronic Items'],
            'Epson Printer': ['Epson Printer'],
            'Fan': ['Fan'],
            'Furniture': ['Furniture', 'Furniture & Fixture'],
            'Inverter': ['Inverter'],
            'Mobile Phone': ['Mobile Phone', 'Mobile phone'],
            'Motor Vehicle': ['Motor Vehicle'],
            'Refrigerator': ['Refridgerator', 'Refrigerator'],
            'Television': ['Television'],
            'Water Dispenser': ['Water Dispenser'],
            'Water Filter': ['Water Filter']
        }
    },
    '12': { 'title': 'Non-current Investments', 'sub_items': {'Non-current Investments': ['non-current investments', 'investments']} },
    '13': { 'title': 'Long term loans and advances', 'sub_items': {'Long term loans and advances': ['long term loans and advances']} },
    '14': { 'title': 'Other non-current assets', 'sub_items': {'Other non-current assets': ['other non-current assets']} },
    '15': { 'title': 'Current Investments', 'sub_items': {'Current Investments': ['current investments']} },
    '16': { 'title': 'Inventories', 'sub_items': {'Inventories': ['Inventories', 'Stock-in-trade']} },
    '17': { 'title': 'Trade Receivables', 'sub_items': {'Trade Receivables': ['Trade Receivables', 'sundry debtors']} },
    '18': { 'title': 'Cash and cash equivalents', 'sub_items': {'Cash and cash equivalents': ['Cash and cash equivalents', 'Cash on hand', 'Balances with banks']} },
    '19': { 'title': 'Short term loans and advances', 'sub_items': {'Short term loans and advances': ['Short term loans and advances']} },
    '20': { 'title': 'Other current assets', 'sub_items': {'Advance Tax & Other Receivables': ['Advance Tax & Other Receivables', 'Input GST', 'Advance Tax']} },
    '21': { 'title': 'Revenue from Operations', 'sub_items': {'Sale of Services': ['Sale of Services', 'revenue from operations']} },
    '22': { 'title': 'Other income', 'sub_items': {'Other income': ['Miscellaneous Income', 'Refund on GST', 'other income']} },
    '23': { 'title': 'Cost of Materials Consumed', 'sub_items': {'Purchases': ['Purchases', 'cost of materials consumed']} },
    '24': { 'title': 'Employee benefit expenses', 'sub_items': {'Employee benefit expenses': ['Salaries and Wages', 'Salary', 'Staff welfare Expenses']} },
    '25': { 'title': 'Finance Costs', 'sub_items': {'Finance Costs': ['Interest on borrowings', 'Other Interest', 'Interest on Income Tax', 'Bank Charges']} },
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'Other expenses': [
                'Accounting Fee', 'Audit Fees', 'Accomodation Charges', 'Admin expenses', 'Books and periodicals',
                'Business Promotion', 'Consultancy charges', 'Donations', 'Electrcity charges', 'Electricity charges',
                'Entertainment Expenses', 'EPFO charges', 'Freight charges', 'GST Charges', 'Income Tax', 'Insurance',
                'Internet Charges', 'Medical Insurance', 'ELD Annual Subscription', 'Office expenses', 'Recruitment Expenses',
                'Professional Tax', 'Printing and stationary', 'Software Charges', 'Stamps and Postage', 'Rent',
                'Subscription Charges', 'Web Hosting and Domain', 'Vehicle Maintenance', 'Travelling Expense',
                'Telephone expenses', 'Repair and maintenance', 'Water Charges', 'Registration Fee', 'Posters',
                'Pantry Purchases', 'Painter Charges', 'Office Maintenance', 'Food Expenses', 'Education Fee',
                'Visa Charges', 'Computers on Rent', 'ComputerExpenses', 'Computer Expenses', 'Commission Charges',
                'Allowances', 'Other expenses', 'Vehicle Accessories', 'MCA Fee', 'Round Off'
            ]
        }
    }
}
# MASTER_TEMPLATE remains the same. It is correct.
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
        ("", "Employee benefit expenses", "24", "item_no_alpha"),
        ("", "Finance Costs", "25", "item_no_alpha"),
        ("", "Depreciation and amortization expenses", "11", "item_no_alpha"),
        ("", "Other expenses", "26", "item_no_alpha"),
        ("","Total Expenses", ["23", "24", "25", "11", "26"], "total"),
        ("", "", None, "spacer"),
        ("V", "Profit before tax (III - IV)", "PBT", "total"),
        ("", "", None, "spacer"),
        ("VI", "Tax expense", None, "header"),
        # Note 27 for Current Tax is assumed but not in the detailed notes, can be handled if data exists
        ("", "Current tax", "27", "item_no_alpha"), 
        ("", "Deferred tax", "4", "item_no_alpha"),
        ("","Total Tax Expense", ["27", "4"], "total"),
        ("", "", None, "spacer"),
        ("VII", "Profit/(Loss) for the period (V - VI)", "PAT", "total"),
    ],
    "Notes to Accounts": NOTES_STRUCTURE_AND_MAPPING
}
