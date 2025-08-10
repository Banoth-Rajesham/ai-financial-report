# ==============================================================================
# PASTE THIS ENTIRE BLOCK INTO: financial_reporter_app/config.py
# This is your full, original structure with enhanced aliases for universal input.
# ==============================================================================

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
            '2.1 Capital reserve': {
                'Balance at the beginning of the year': ['Capital reserve at beginning'],
                'Add: Additions during the year': ['Additions to Capital reserve'],
                'Less: Utilized/transferred during the year': ['Utilized from Capital reserve'],
                'Balance at the end of the year': ['Capital reserve at end', 'Capital Reserve']
            },
            '2.2 Securities premium account': {
                'Balance at the beginning of the year ': ['Securities premium at beginning'],
                'Add: Premium on shares issued during the year': ['Premium on shares issued'],
                'Less: Utilising during the year for': {},
                'Balance at the end of the year ': ['Securities premium at end', 'Securities Premium']
            },
            '2.4 General reserve': {
                'Balance at the beginning of the year   ': ['General reserve at beginning'],
                'Add: Transferred from surplus in Statement of Profit and Loss': ['Transferred to general reserve from surplus'],
                'Balance at the end of the year   ': ['General reserve at end', 'General Reserve']
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Balance at the beginning of the year     ': ['Surplus at beginning'],
                'Add: Profit / (Loss) for the year': ['Profit / Loss for the year', 'Net Profit for the year'],
                'Balance at the end of the year     ': ['Surplus at end', 'Retained Earnings', 'Surplus', 'P&L Account Balance', 'Profit & Loss A/c']
            }
        }
    },
    '3': {
        'title': 'Long term borrowings',
        'sub_items': {
            '3.0 Long term borrowings Summary': {
                '(a) Term loans from banks': ['Term loans from banks', 'term loan', 'long term borrowings', 'Mortgage Loan'],
                '(b) Deferred payment liabilities': ['Deferred payment liabilities'],
                '(c) Deposits': ['Deposits'],
                '(d) Loans and advances from related parties': ['Loans and advances from related parties', 'Loan from Director'],
                '(e) Other loans and advances': ['Other loans and advances specify nature', 'debentures']
            }
        }
    },
    '4': {'title': 'Deferred Tax Asset/Liability','sub_items': {'Deferred Tax (Net)': ['deferred tax asset', 'deferred tax liability', 'deferred tax']}},
    '5': {'title': 'Other long term liabilities', 'sub_items': {'Other long term liabilities': ['other long term liabilities']}},
    '6': {'title': 'Long term provisions', 'sub_items': {'Long term provisions': ['long term provisions']}},
    '7': {'title': 'Short term borrowings', 'sub_items': {'(a) Loans repayable on demand': {'From banks - Unsecured': ['short term borrowings', 'bank overdraft']}}},
    '8': {'title': 'Trade payables', 'sub_items': {'Trade payables: Other than Acceptances': ['trade payables', 'sundry creditors']}},
    '9': {'title': 'Other current liabilities', 'sub_items': {'Other payables (Salaries and consultant fee)': ['other current liabilities', 'bills payable', 'outstanding expenses']}},
    '10': {'title': 'Short term provisions', 'sub_items': {'(b) Provision - Others': {'Provision for tax (net)':['short term provisions', 'provision for tax']}}},
    '11': {
        'title': 'Fixed Assets (Tangible & Intangible)',
        'sub_items': {
            'Depreciation for the year': ['Depreciation', 'Depriciation for the year', 'to depreciation'],
            'Closing WDV': ['tangible assets', 'net fixed assets', 'fixed assets', 'land & building', 'plant & machinery', 'motor vehicles', 'Furniture & Fixture']
        }
    },
    '12': {'title': 'Non-current Investments', 'sub_items': {'B. Other Investments': {'(f) Investment in mutual funds': ['non-current investments', 'investments']}}},
    '13': {'title': 'Long term loans and advances', 'sub_items': {'(e) Prepaid expenses - Unsecured, considered good': ['long term loans and advances']}},
    '14': {'title': 'Other non-current assets', 'sub_items': {'(d) Others': {'Others (specify nature)':['other non-current assets']}}},
    '15': {'title': 'Current Investments', 'sub_items': {'B. Other current investments': {'(g) Other investments (specify nature)': ['current investments']}}},
    '16': {
        'title': 'Inventories',
        'sub_items': {
            '(d) Stock-in-trade': {'Stock-in-trade': ['inventories', 'stock/inventories', 'closing stock', 'opening stock', 'to opening stock', 'by closing stock']}
        }
    },
    '17': {'title': 'Trade Receivables', 'sub_items': {'Other Trade receivables': {'Unsecured, considered good ': ['trade receivables', 'sundry debtors', 'bills receivable']}}},
    '18': {'title': 'Cash and cash equivalents', 'sub_items': {'(c) Balances with banks': {'(i) In current accounts': ['cash and cash equivalents', 'cash at bank']}}},
    '19': {'title': 'Short term loans and advances', 'sub_items': {'(d) Prepaid expenses': ['short term loans and advances', 'prepaid']}},
    '20': {'title': 'Other current assets', 'sub_items': {'(a) Unbilled revenue': ['other current assets']}},
    '21': {
        'title': 'Revenue from Operations',
        'sub_items': {
            'Sale of Services': ['revenue from operations', 'by sales']
        }
    },
    '22': {
        'title': 'Other income',
        'sub_items': {
            'Miscellaneous Income': ['other income', 'by interest received', 'by dividend received', 'by commission received', 'by discount received', 'by bad debts recovered', 'miscellaneous income']
        }
    },
    '23': {
        'title': 'Cost of Materials Consumed',
        'sub_items': {
            'Purchases': ['cost of materials consumed', 'to purchases']
        }
    },
    '24': {
        'title': 'Employee benefit expenses',
        'sub_items': {
            'Salaries and Wages': ['employee benefit expenses', 'to wages', 'to salaries']
        }
    },
    '25': {
        'title': 'Finance Costs',
        'sub_items': {
            'Interest on borrowings': ['finance costs', 'to interest paid']
        }
    },
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'Accounting Fee': ['Accounting Fee'],
            'Audit Fees': ['Audit Fees'],
            'Admin expenses': ['Admin expenses'],
            'Bank Charges': ['Bank Charges'],
            'Consultancy charges': ['Consultancy charges'],
            'Electrcity charges': ['Electrcity charges', 'Electricity charges', 'to electricity'],
            'Insurance': ['Insurance', 'to insurance'],
            'Rent': ['Rent', 'to rent'],
            'Travelling Expense': ['Travelling Expense'],
            'Telephone expenses': ['Telephone expenses', 'to telephone'],
            'Repair and maintenance': ['Repair and maintenance', 'to repairs & maintenance'],
            'Other expenses': ['Other expenses', 'miscellaneous expenses', 'to bad debts', 'to printing & stationery']
        }
    },
    "27": { "title": "Tax expense", "sub_items": {
        'Current tax': ['current tax', 'taxation']
    } }
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
