# ==============================================================================
# PASTE THIS ENTIRE, ENHANCED BLOCK INTO: financial_reporter_app/config.py
# This version merges your detailed structure with the aliases from the
# classic T-account format. Nothing has been deleted, only enhanced.
# ==============================================================================

NOTES_STRUCTURE_AND_MAPPING = {
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital No.of shares'],
                'Equity shares of Rs. 10 each': ['Authorised Equity shares of Rs. 10 each']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares ': ['Issued and fully paid up No.of shares'],
                # ADDED ALIAS from the T-account input to map the main "Share Capital" line item.
                'Equity shares of Rs. 10 each ': ['Issued and fully paid up Equity shares of Rs. 10 each', 'share capital'] # <-- ADDED ALIAS
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
            '2.1 Capital reserve': { 'Balance at the end of the year': ['Capital reserve at end', 'Capital reserve'] },
            '2.2 Securities premium account': { 'Balance at the end of the year ': ['Securities premium at end', 'Securities premium'] },
            '2.4 General reserve': {
                 # ADDED ALIAS from the T-account input
                'Balance at the end of the year   ': ['General reserve at end', 'general reserve'] # <-- ADDED ALIAS
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Add: Profit / (Loss) for the year': ['Profit / Loss for the year'],
                 # ADDED ALIAS from the T-account input
                'Balance at the end of the year     ': ['Surplus at end', 'profit & loss a/c', 'p&l account balance'] # <-- ADDED ALIAS
            }
        }
    },
    '3': {
        'title': 'Long term borrowings',
        'sub_items': {
            '3.0 Long term borrowings Summary': {
                 # ADDED ALIASES from the T-account input
                '(a) Term loans from banks': ['Term loans from banks', 'long-term loans', 'mortgage loan'], # <-- ADDED ALIASES
                '(b) Deferred payment liabilities': ['Deferred payment liabilities'],
                '(c) Deposits': ['Deposits'],
                '(d) Loans and advances from related parties': ['Loans and advances from related parties'],
                 # ADDED ALIAS from the T-account input
                '(e) Other loans and advances': ['Other loans and advances specify nature', 'debentures'] # <-- ADDED ALIAS
            }
        }
    },
    '4': {
        'title': 'Deferred Tax Asset/Liability',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            'Tax on Difference between Book & Tax depreciation': ['Tax on Difference between Book & Tax depreciation', 'Deferred Tax']
        }
    },
    '5': {'title': 'Other long term liabilities', 'sub_items': {}},
    '6': {'title': 'Long term provisions', 'sub_items': {}},
    '7': {
        'title': 'Short term borrowings',
        'sub_items': {
            '(a) Loans repayable on demand': {
                 # ADDED ALIAS from the T-account input
                'From banks - Secured': ['Secured from banks', 'bank overdraft'], # <-- ADDED ALIAS
                'From banks - Unsecured': ['Unsecured from banks'],
            }
        }
    },
    '8': {
        'title': 'Trade payables',
        'sub_items': {
            'Trade payables: Acceptances': ['Acceptances'],
             # ADDED ALIAS from the T-account input
            'Trade payables: Other than Acceptances': ['Other than Acceptances', 'sundry creditors'] # <-- ADDED ALIAS
        }
    },
    '9': {
        'title': 'Other current liabilities',
        'sub_items': {
            'Current maturities of long-term debt': ['Current maturities of long-term debt'],
             # ADDED ALIASES from the T-account input
            'Other payables (Salaries and consultant fee)': ['Other payables', 'Salaries and consultant fee', 'outstanding expenses', 'bills payable'] # <-- ADDED ALIASES
        }
    },
    '10': {'title': 'Short term provisions', 'sub_items': {}},
    '11': {
        'title': 'Fixed Assets (Tangible & Intangible)',
        'sub_items': {
             # ADDED ALIASES from the T-account input
            'Depreciation for the year': ['Depriciation for the year', 'Depreciation', 'to depreciation'], # <-- ADDED ALIAS
            'Opening WDV': ['Opening WDV'],
            'Additions': ['additions'],
            'Deleations': ['Deletions'],
            'Closing WDV': ['Closing WDV'],
            'Land & Building': ['land & building'], # <-- ADDED ITEM
            'Plant & Machinery': ['plant & machinery'], # <-- ADDED ITEM
            'Office Interiors': ['Office Interiors'],
            'Air Conditioners': ['Air Conditioners'],
            'Computers': ['Computers'],
            'Furniture': ['Furniture', 'furniture & fixtures'], # <-- ADDED ALIAS
            'Motor Vehicle': ['Motor Vehicle', 'motor vehicles'], # <-- ADDED ALIAS
        }
    },
    '12': {
        'title': 'Non-current Investments',
        'sub_items': {
            'B. Other Investments': {
                 # ADDED ALIAS from the T-account input
                '(h) Other non-current investments ': ['Other non-current investments (specify nature)', 'investments'] # <-- ADDED ALIAS
            }
        }
    },
    '13': {'title': 'Long term loans and advances', 'sub_items': {}},
    '14': {'title': 'Other non-current assets', 'sub_items': {}},
    '15': {'title': 'Current Investments', 'sub_items': {}},
    '16': {
        'title': 'Inventories',
        'sub_items': {
            '(d) Stock-in-trade': {
                 # ADDED ALIASES from the T-account input
                'Stock-in-trade': ['Stock-in-trade (acquired for trading)', 'stock/inventory', 'by closing stock', 'to opening stock'] # <-- ADDED ALIASES
            }
        }
    },
    '17': {
        'title': 'Trade Receivables',
        'sub_items': {
            'Other Trade receivables': {
                 # ADDED ALIASES from the T-account input
                'Unsecured, considered good ': ['Other trade receivables unsecured good', 'sundry debtors', 'bills receivable'] # <-- ADDED ALIASES
            }
        }
    },
    '18': {
        'title': 'Cash and cash equivalents',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            '(a) Cash on hand': ['Cash on hand', 'cash in hand'], # <-- ADDED ALIAS
            '(c) Balances with banks': {
                 # ADDED ALIAS from the T-account input
                '(i) In current accounts': ['Balances with banks in current accounts', 'cash at bank'] # <-- ADDED ALIAS
            }
        }
    },
    '19': {
        'title': 'Short term loans and advances',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            '(d) Prepaid expenses': ['Short-term Prepaid expenses', 'prepaid expenses'] # <-- ADDED ALIAS
        }
    },
    '20': {'title': 'Other current assets', 'sub_items': {}},
    '21': {
        'title': 'Revenue from Operations',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            'Sale of Services': ['Sale of Services', 'by sales'] # <-- ADDED ALIAS
        }
    },
    '22': {
        'title': 'Other income',
        'sub_items': {
             # ADDED ALIASES from the T-account input
            'Miscellaneous Income': ['Miscellaneous Income', 'by interest received', 'by dividend received', 'by commission received', 'by discount received', 'by bad debts recovered', 'by miscellaneous income'] # <-- ADDED ALIASES
        }
    },
    '23': {
        'title': 'Cost of Materials Consumed',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            'Purchases': ['Purchases', 'to purchases'] # <-- ADDED ALIAS
        }
    },
    '24': {
        'title': 'Employee benefit expenses',
        'sub_items': {
             # ADDED ALIASES from the T-account input
            'Salaries and Wages': ['Salaries and Wages', 'Salary', 'to salaries', 'to wages'] # <-- ADDED ALIASES
        }
    },
    '25': {
        'title': 'Finance Costs',
        'sub_items': {
             # ADDED ALIAS from the T-account input
            'Interest on borrowings': ['Interest on borrowings', 'to interest paid'] # <-- ADDED ALIAS
        }
    },
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'Accounting Fee': ['Accounting Fee'],
            'Audit Fees': ['Audit Fees', 'to audit fees'], # <-- ADDED ALIAS
            'Admin expenses': ['Admin expenses'],
            'Bank Charges': ['Bank Charges', 'to bank charges'], # <-- ADDED ALIAS
            'Consultancy charges': ['Consultancy charges'],
            'Electrcity charges': ['Electrcity charges', 'Electricity charges', 'to electricity'], # <-- ADDED ALIAS
            'Insurance': ['Insurance', 'to insurance'], # <-- ADDED ALIAS
            'Printing and stationary': ['Printing and stationary', 'to printing & stationery'], # <-- ADDED ALIAS
            'Rent': ['Rent', 'to rent'], # <-- ADDED ALIAS
            'Travelling Expense': ['Travelling Expense', 'to transportation'], # <-- ADDED ALIAS (mapped transportation here)
            'Telephone expenses': ['Telephone expenses', 'to telephone'], # <-- ADDED ALIAS
            'Repair and maintenance': ['Repair and maintenance', 'to repairs & maintenance'], # <-- ADDED ALIAS
            'Other expenses': ['Other expenses', 'to bad debts'] # <-- ADDED ALIAS (mapped bad debts here)
        }
    }
}

# The rest of your config.py file, including MASTER_TEMPLATE, does not need to be changed.
# The following is provided for completeness.

MASTER_TEMPLATE = {
    "Balance Sheet": [
        # Col A, Particulars, Note Number, Row Type (for styling)
        ("", "Particulars", "Note No.", "header_col"),
        ("I", "EQUITY AND LIABILITIES", None, "header"),
        ("1", "Shareholder's Funds", None, "sub_header"),
        ("", "Share Capital", "1", "item_no_alpha"),
        ("", "Reserves and Surplus", "2", "item_no_alpha"),
        ("2", "Non-Current Liabilities", None, "sub_header"),
        ("", "Long-Term Borrowings", "3", "item_no_alpha"),
        ("", "Deferred Tax Liabilities (Net)", "4", "item_no_alpha"),
        ("", "Other Long-Term Liabilities", "5", "item_no_alpha"),
        ("", "Long-Term Provisions", "6", "item_no_alpha"),
        ("3", "Current Liabilities", None, "sub_header"),
        ("", "Short-Term Borrowings", "7", "item_no_alpha"),
        ("", "Trade Payables", "8", "item_no_alpha"),
        ("", "Other Current Liabilities", "9", "item_no_alpha"),
        ("", "Short-Term Provisions", "10", "item_no_alpha"),
        ("", "TOTAL EQUITY AND LIABILITIES", ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], "total"),
        ("", "", None, "spacer"),
        ("II", "ASSETS", None, "header"),
        ("1", "Non-Current Assets", None, "sub_header"),
        ("", "Property, Plant and Equipment & Intangible Assets", "11", "item_no_alpha"),
        ("", "Non-Current Investments", "12", "item_no_alpha"),
        ("", "Long-Term Loans and Advances", "13", "item_no_alpha"),
        ("", "Other Non-Current Assets", "14", "item_no_alpha"),
        ("2", "Current Assets", None, "sub_header"),
        ("", "Current Investments", "15", "item_no_alpha"),
        ("", "Inventories", "16", "item_no_alpha"),
        ("", "Trade Receivables", "17", "item_no_alpha"),
        ("", "Cash and Cash Equivalents", "18", "item_no_alpha"),
        ("", "Short-Term Loans and Advances", "19", "item_no_alpha"),
        ("", "Other Current Assets", "20", "item_no_alpha"),
        ("", "TOTAL ASSETS", ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"], "total"),
    ],
    "Profit and Loss": [
        # Col A, Particulars, Note Number, Row Type (for styling)
        ("", "Particulars", "Note No.", "header_col"),
        ("I", "Revenue from Operations", "21", "item"),
        ("II", "Other Income", "22", "item"),
        ("III", "Total Revenue (I + II)", ["21", "22"], "total"),
        ("", "", None, "spacer"),
        ("IV", "Expenses", None, "header"),
        ("", "Cost of Materials Consumed", "23", "item_no_alpha"),
        ("", "Changes in inventories of finished goods, work-in-progress and Stock-in-Trade", "16", "item_no_alpha"),
        ("", "Employee Benefit Expenses", "24", "item_no_alpha"),
        ("", "Finance Costs", "25", "item_no_alpha"),
        ("", "Depreciation and Amortization Expense", "11", "item_no_alpha"),
        ("", "Other Expenses", "26", "item_no_alpha"),
        ("","Total Expenses", ["23", "16", "24", "25", "11", "26"], "total"),
        ("", "", None, "spacer"),
        ("V", "Profit Before Tax (III - IV)", "PBT", "total"),
        ("", "", None, "spacer"),
        ("VI", "Tax Expense", "27", "item"),
        ("", "", None, "spacer"),
        ("VII", "Profit/(Loss) for the period (V - VI)", "PAT", "total"),
    ],
    "Notes to Accounts": NOTES_STRUCTURE_AND_MAPPING
}
