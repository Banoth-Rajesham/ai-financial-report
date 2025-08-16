# ==============================================================================
# FILE: config.py (DEFINITIVE MASTER VERSION)
# This version combines your detailed structure with comprehensive aliases
# to ensure the maximum possible mapping of all values.
# ==============================================================================

NOTES_STRUCTURE_AND_MAPPING = {
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital No.of shares', 'Number of shares'],
                'Equity shares of Rs. 10 each': ['Authorised Equity shares of Rs. 10 each']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares': ['Issued and fully paid up No.of shares', 'Number of shares'],
                'Equity shares of Rs. 10 each': [
                    'Issued and fully paid up Equity shares of Rs. 10 each',
                    'Equity shares of Rs. 10 each',
                    'Issued, subscribed and paid-up',
                    'Share Capital',
                    'Equity Capital',
                    'Paid-up Capital'
                ]
            },
            'Issued, subscribed and Partly up capital': {
                'Number of shares': ['Issued and Partly up No.of shares'],
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
            'Capital reserve': ['Capital reserve', 'Capital reserve at end'],
            'Securities premium account': ['Securities premium', 'share premium', 'Securities premium at end'],
            'General reserve': ['General reserve', 'General reserve at end'],
            'Surplus / (Deficit) in Statement of Profit and Loss': [
                'Retained Earnings',
                'Surplus',
                'P&L Account Balance',
                'Profit & Loss A/c',
                'Surplus at end'
            ]
        }
    },
    '3': {
        'title': 'Long term borrowings',
        'sub_items': {
            'Long term borrowings': [
                'Term loans from banks',
                'term loan',
                'long term borrowings',
                'Mortgage Loan',
                'debentures'
            ]
        }
    },
    '4': {
        'title': 'Deferred Tax Asset/Liability',
        'sub_items': {
            'Deferred Tax (Net)': [
                'deferred tax asset',
                'deferred tax liability',
                'deferred tax',
                'Tax on Difference between Book & Tax depreciation'
            ]
        }
    },
    '5': {'title': 'Other long term liabilities', 'sub_items': {'Other long term liabilities': ['other long term liabilities']}},
    '6': {'title': 'Long term provisions', 'sub_items': {'Long term provisions': ['long term provisions']}},
    '7': {
        'title': 'Short term borrowings',
        'sub_items': {
            'Short term borrowings': [
                'short term borrowings',
                'bank overdraft',
                'Loans repayable on demand'
            ]
        }
    },
    '8': {
        'title': 'Trade payables',
        'sub_items': {
            'Trade payables': [
                'Trade payables',
                'sundry creditors',
                'Other than Acceptances'
            ]
        }
    },
    '9': {
        'title': 'Other current liabilities',
        'sub_items': {
            'Other current liabilities': [
                'other current liabilities',
                'bills payable',
                'outstanding expenses',
                'Other payables',
                'Statutory remittances'
            ]
        }
    },
    '10': {
        'title': 'Short term provisions',
        'sub_items': {
            'Short term provisions': [
                'short term provisions',
                'provision for tax',
                'Provision for Audit Fees',
                'Provision for Accounting Fee'
            ]
        }
    },
    '11': {
        'title': 'Fixed Assets (Tangible & Intangible)',
        'sub_items': {
            'Tangible Assets': [
                'tangible assets', 'net fixed assets', 'fixed assets', 'land & building', 'plant & machinery',
                'motor vehicles', 'Furniture & Fixture', 'Office Interiors', 'Air Conditioners', 'Battery',
                'CCTV Camera', 'Computers', 'Curtains', 'Electronic Items', 'Epson Printer', 'Fan', 'Furniture',
                'Inverter', 'Mobile Phone', 'Motor Vehicle', 'Refrigerator', 'Television', 'Water Dispenser', 'Water Filter'
            ],
            'Intangible Assets': ['Intangible Assets'],
            'Capital Work-in-Progress': ['Capital Work-in-Progress', 'CWIP'],
            'Depreciation': ['Depreciation', 'Depriciation for the year', 'to depreciation', 'Dep as per IT ACT', 'Dep as per Comp']
        }
    },
    '12': {'title': 'Non-current Investments', 'sub_items': {'Non-current Investments': ['non-current investments', 'investments']}},
    '13': {'title': 'Long term loans and advances', 'sub_items': {'Long term loans and advances': ['long term loans and advances']}},
    '14': {'title': 'Other non-current assets', 'sub_items': {'Other non-current assets': ['other non-current assets']}},
    '15': {'title': 'Current Investments', 'sub_items': {'Current Investments': ['current investments']}},
    '16': {
        'title': 'Inventories',
        'sub_items': {
            'Inventories': [
                'inventories', 'stock/inventories', 'closing stock', 'opening stock',
                'to opening stock', 'by closing stock', 'Stock-in-trade'
            ]
        }
    },
    '17': {
        'title': 'Trade Receivables',
        'sub_items': {
            'Trade Receivables': [
                'trade receivables',
                'sundry debtors',
                'bills receivable'
            ]
        }
    },
    '18': {
        'title': 'Cash and cash equivalents',
        'sub_items': {
            'Cash and cash equivalents': [
                'cash and cash equivalents',
                'cash at bank',
                'Cash on hand',
                'Balances with banks'
            ]
        }
    },
    '19': {
        'title': 'Short term loans and advances',
        'sub_items': {
            'Short term loans and advances': [
                'short term loans and advances',
                'prepaid'
            ]
        }
    },
    '20': {
        'title': 'Other current assets',
        'sub_items': {
            'Other current assets': [
                'other current assets',
                'Advance Tax',
                'Input GST'
            ]
        }
    },
    '21': {
        'title': 'Revenue from Operations',
        'sub_items': {
            'Revenue from Operations': [
                'revenue from operations',
                'by sales',
                'Sale of Services'
            ]
        }
    },
    '22': {
        'title': 'Other income',
        'sub_items': {
            'Other income': [
                'other income', 'by interest received', 'by dividend received', 'by commission received',
                'by discount received', 'by bad debts recovered', 'miscellaneous income', 'Refund on GST'
            ]
        }
    },
    '23': {
        'title': 'Cost of Materials Consumed',
        'sub_items': {
            'Cost of Materials Consumed': [
                'cost of materials consumed',
                'to purchases',
                'Purchases'
            ]
        }
    },
    '24': {
        'title': 'Employee benefit expenses',
        'sub_items': {
            'Employee benefit expenses': [
                'employee benefit expenses', 'to wages', 'to salaries', 'Salaries and Wages',
                'Contribution to provident and other funds', 'Gratuity Expenses', 'Staff welfare Expenses'
            ]
        }
    },
    '25': {
        'title': 'Finance Costs',
        'sub_items': {
            'Finance Costs': [
                'finance costs',
                'to interest paid',
                'Interest on borrowings',
                'Other Interest',
                'Interest on Income Tax',
                'Bank Charges'
            ]
        }
    },
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'All Other Expenses': [
                'Accounting Fee', 'Audit Fees', 'Accomodation Charges', 'Admin expenses', 'Books and periodicals',
                'Business Promotion', 'Consultancy charges', 'Donations', 'Electrcity charges', 'Electricity charges',
                'Entertainment Expenses', 'EPFO charges', 'Freight charges', 'GST Charges', 'Income Tax', 'Insurance',
                'Internet Charges', 'Medical Insurance', 'ELD Annual Subscription', 'Office expenses', 'Recruitment Expenses',
                'Professional Tax', 'Printing and stationary', 'Software Charges', 'Stamps and Postage', 'Rent',
                'Subscription Charges', 'Web Hosting and Domain', 'Vehicle Maintenance', 'Travelling Expense',
                'Telephone expenses', 'Repair and maintenance', 'Water Charges', 'Registration Fee', 'Posters',
                'Pantry Purchases', 'Painter Charges', 'Office Maintenance', 'Food Expenses', 'Education Fee',
                'Visa Charges', 'Computers on Rent', 'ComputerExpenses', 'Computer Expenses', 'Commission Charges',
                'Allowances', 'Other expenses', 'Vehicle Accessories', 'MCA Fee', 'Round Off', 'miscellaneous expenses',
                'to bad debts', 'to printing & stationery', 'to electricity', 'to insurance', 'to rent', 'to telephone', 'to repairs & maintenance'
            ]
        }
    },
    "27": { "title": "Tax expense", "sub_items": { 'Current tax': ['current tax', 'taxation'] } }
}

# The MASTER_TEMPLATE is correct and does not need changes.
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
