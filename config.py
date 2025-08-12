# ==============================================================================
# PASTE THIS ENTIRE, ENHANCED BLOCK INTO: financial_reporter_app/config.py
#
# This file is the central configuration "brain" for the entire application.
#
# 1. NOTES_STRUCTURE_AND_MAPPING:
#    - Defines the structure of all financial notes (1-27).
#    - Contains a comprehensive list of ALIASES. The aggregator agent uses
#      these aliases to find and map terms from any input file.
#
# 2. MASTER_TEMPLATE:
#    - Defines the exact layout and structure for the main "Balance Sheet"
#      and "Profit and Loss" sheets in the final report.
# ==============================================================================

NOTES_STRUCTURE_AND_MAPPING = {
    # ========================== #
    # == EQUITY AND LIABILITIES == #
    # ========================== #
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital No.of shares', 'Authorised - Number of shares'],
                'Equity shares of various face values': ['Authorised Equity shares', 'Authorised share capital', 'authorised capital']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares ': ['Issued and fully paid up No.of shares', 'Issued - Number of shares'],
                'Equity shares of various face values ': ['Issued and fully paid up Equity shares', 'Issued, subscribed and paid-up', 'Share Capital', 'Equity Capital', 'Paid-up Capital', 'paid up share capital']
            },
            '1.1 Reconciliation of number of shares': {
                'Equity shares at the beginning of the year': ['Equity shares at beginning', 'Shares outstanding at the beginning of the year'],
                'Add: Additions during the year': ['Additions to share capital on account of fresh issue', 'Shares issued during the year'],
                'Ded: Deductions during the year': ['Deductions from share capital on account of shares bought back', 'Shares bought back during the year'],
                'Balance at the end of the year': ['Balance at the end of the year shares', 'Shares outstanding at the end of the year']
            }
        }
    },
    '2': {
        'title': 'Reserves and Surplus',
        'sub_items': {
            'Capital Reserve': ['Capital reserve'],
            'Securities Premium Account': ['Securities premium', 'share premium', 'Securities Premium Reserve'],
            'General Reserve': ['General reserve'],
            'Surplus / (Deficit) in Statement of Profit and Loss': ['Retained Earnings', 'Surplus', 'P&L Account Balance', 'Profit & Loss A/c', 'Reserves and surplus', 'retained surplus', 'p&l appropriation']
        }
    },
    '3': {
        'title': 'Long-term Borrowings',
        'sub_items': {
            'Secured Loans': {
                'Term loans from banks': ['Term loans from banks', 'term loan', 'long term borrowings', 'Mortgage Loan', 'secured loans - banks'],
            },
            'Unsecured Loans': {
                 'Loans from Directors': ['loans from directors', 'unsecured loans - directors'],
                 'Other loans and advances': ['Other loans and advances specify nature', 'debentures', 'unsecured loans - others']
            }
        }
    },
    '4': {
        'title': 'Deferred Tax Asset/Liability',
        'sub_items': {
            'Deferred Tax Liability': ['deferred tax liability', 'dtl'],
            'Deferred Tax Asset': ['deferred tax asset', 'dta'],
            'Net Deferred Tax': ['deferred tax', 'deferred tax (net)']
        }
    },
    '5': {
        'title': 'Other Long-term Liabilities',
        'sub_items': {
            'Other non-current liabilities': ['other long term liabilities', 'other non-current liabilities']
        }
    },
    '6': {
        'title': 'Long-term Provisions',
        'sub_items': {
            'Provision for employee benefits': ['provision for gratuity', 'provision for leave encashment'],
            'Provision - Others': ['long term provisions', 'other long term provisions']
        }
    },
    '7': {
        'title': 'Short-term Borrowings',
        'sub_items': {
            'Loans repayable on demand (Secured)': ['cash credit facility', 'working capital loan', 'bank overdraft'],
            'Loans repayable on demand (Unsecured)': ['short term borrowings', 'loans from related parties', 'unsecured short term loans']
        }
    },
    '8': {
        'title': 'Trade Payables',
        'sub_items': {
            'Total outstanding dues of micro and small enterprises': ['trade payables - msme', 'dues to micro and small enterprises'],
            'Total outstanding dues of creditors other than micro and small enterprises': ['trade payables', 'sundry creditors', 'accounts payable', 'creditors', 'payables', 'trade creditors']
        }
    },
    '9': {
        'title': 'Other Current Liabilities',
        'sub_items': {
            'Current maturities of long-term debt': ['current maturities of long term debt'],
            'Statutory Dues Payable': ['statutory dues', 'gst payable', 'tds payable', 'pf payable'],
            'Expenses Payable': ['other current liabilities', 'bills payable', 'outstanding expenses', 'accrued expenses', 'expenses payable']
        }
    },
    '10': {
        'title': 'Short-term Provisions',
        'sub_items': {
            'Provision for tax (net of advance tax)': ['short term provisions', 'provision for tax', 'provision for taxation', 'income tax provision'],
            'Provision - Others': ['provision for expenses', 'other short term provisions']
        }
    },
    # ========================== #
    # ======== ASSETS ========== #
    # ========================== #
    '11': {
        'title': 'Property, Plant and Equipment and Intangible Assets',
        'sub_items': {
            'Tangible Assets': {
                'Land and Building': ['land & building', 'buildings'],
                'Plant and Machinery': ['plant & machinery'],
                'Motor Vehicles': ['motor vehicles'],
                'Furniture and Fixtures': ['Furniture & Fixture'],
                'Office Equipment': ['office equipment', 'computers and peripherals']
            },
            'Intangible Assets': {
                'Goodwill': ['goodwill'],
                'Software': ['software', 'computer software']
            },
            # This keyword maps to the final Closing WDV (Written Down Value)
            'Closing Net Carrying Amount': ['tangible assets', 'net fixed assets', 'fixed assets', 'property, plant and equipment', 'net block'],
            # This is a critical alias for the P&L calculation
            'Depreciation for the year': ['Depreciation', 'Depriciation for the year', 'to depreciation', 'depreciation and amortization expense', 'amortization']
        }
    },
    '12': {'title': 'Non-current Investments', 'sub_items': {'Investments in Mutual Funds': ['non-current investments', 'investments', 'investment in mutual funds', 'long term investments']}},
    '13': {'title': 'Long-term Loans and Advances', 'sub_items': {'Capital Advances': ['capital advances'], 'Security Deposits': ['security deposits', 'long term loans and advances']}},
    '14': {'title': 'Other Non-current Assets', 'sub_items': {'Other non-current assets': ['other non-current assets']}},
    '15': {'title': 'Current Investments', 'sub_items': {'Other current investments': ['current investments', 'short term investments']}},
    '16': {
        'title': 'Inventories',
        'sub_items': {
            'Raw Materials': ['raw materials'],
            'Work-in-progress': ['work-in-progress', 'wip'],
            'Finished Goods': ['finished goods', 'stock-in-trade'],
            # This alias maps to the final closing inventory value on the Balance Sheet
            'Closing Inventory': ['inventories', 'stock/inventories', 'closing stock', 'by closing stock']
        }
    },
    '17': {'title': 'Trade Receivables', 'sub_items': {'Unsecured, considered good': ['trade receivables', 'sundry debtors', 'bills receivable', 'accounts receivable', 'debtors', 'customer dues']}},
    '18': {'title': 'Cash and Cash Equivalents', 'sub_items': {'Balances with banks in current accounts': ['cash and cash equivalents', 'cash at bank', 'bank balances'], 'Cash on hand': ['cash in hand']}},
    '19': {'title': 'Short-term Loans and Advances', 'sub_items': {'Advances to suppliers': ['advances to suppliers'], 'Prepaid Expenses': ['short term loans and advances', 'prepaid', 'prepaid expenses']}},
    '20': {'title': 'Other Current Assets', 'sub_items': {'Unbilled Revenue': ['unbilled revenue', 'other current assets']}},

    # ========================== #
    # == PROFIT AND LOSS ITEMS == #
    # ========================== #
    '21': {'title': 'Revenue from Operations', 'sub_items': {'Sale of Services/Products': ['revenue from operations', 'by sales', 'sales', 'turnover', 'sale of products', 'income from operations']}},
    '22': {
        'title': 'Other Income',
        'sub_items': {
            'Interest Income': ['interest received', 'interest income'],
            'Dividend Income': ['by dividend received', 'dividend income'],
            'Miscellaneous Income': ['other income', 'by commission received', 'by discount received', 'by bad debts recovered', 'miscellaneous income', 'other non-operating income']
        }
    },
    '23': {'title': 'Cost of Materials Consumed', 'sub_items': {'Cost of Materials': ['cost of materials consumed', 'to purchases', 'purchases of stock-in-trade', 'material consumed']}},
    '24': {'title': 'Employee Benefit Expenses', 'sub_items': {'Salaries, Wages and Bonus': ['employee benefit expenses', 'to wages', 'to salaries', 'salaries and wages'], 'Staff Welfare Expenses': ['staff welfare expenses']}},
    '25': {'title': 'Finance Costs', 'sub_items': {'Interest Expense': ['finance costs', 'to interest paid', 'interest on loans', 'interest expense'], 'Bank Charges': ['Bank Charges']}},
    '26': {
        'title': 'Other Expenses',
        'sub_items': {
            # Each key here is a sub-category. Add aliases to the list.
            'Rent': ['Rent', 'to rent', 'office rent'],
            'Power and Fuel': ['Electrcity charges', 'Electricity charges', 'to electricity', 'power and fuel'],
            'Repairs and Maintenance': ['Repair and maintenance', 'to repairs & maintenance'],
            'Insurance': ['Insurance', 'to insurance'],
            'Rates and Taxes': ['rates and taxes'],
            'Communication Expenses': ['Telephone expenses', 'to telephone', 'communication expenses', 'postage and courier'],
            'Travelling and Conveyance': ['Travelling Expense', 'conveyance expenses', 'travel expenses'],
            'Printing and Stationery': ['to printing & stationery', 'printing and stationery'],
            'Legal and Professional Fees': ['Consultancy charges', 'legal fees', 'professional fees'],
            'Auditors Remuneration': ['Audit Fees', 'auditors remuneration'],
            'Marketing Expenses': ['marketing expenses', 'advertisement and promotion'],
            'Miscellaneous Expenses': ['Other expenses', 'miscellaneous expenses', 'to bad debts', 'sundry expenses', 'general expenses', 'Accounting Fee', 'Admin expenses']
        }
    },
    "27": {"title": "Tax Expense", "sub_items": {'Current Tax': ['current tax', 'taxation', 'income tax'], 'Deferred Tax Charge/Credit': ['deferred tax charge', 'deferred tax credit']}}
}


# ==============================================================================
# MASTER REPORT TEMPLATE
# This dictionary defines the exact row-by-row structure of the main financial
# statements. The 'report_finalizer_agent' uses this to build the sheets.
# The `row_type` controls styling, and the `note` number links to the data
# aggregated using the mappings above.
# ==============================================================================
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
        # The logic for "Changes in Inventories" should be (Opening Stock - Closing Stock)
        # This template assumes the aggregator agent provides the final value under Note 16.
        #("", "Changes in inventories of finished goods, work-in-progress and Stock-in-Trade", "16", "item_no_alpha"),
        ("", "Employee Benefit Expenses", "24", "item_no_alpha"),
        ("", "Finance Costs", "25", "item_no_alpha"),
        # The aggregator maps 'Depreciation for the year' to Note 11
        ("", "Depreciation and Amortization Expense", "11", "item_no_alpha"),
        ("", "Other Expenses", "26", "item_no_alpha"),
        ("","Total Expenses", ["23", "24", "25", "11", "26"], "total"),
        ("", "", None, "spacer"),
        ("V", "Profit Before Tax (III - IV)", "PBT", "total"),
        ("", "", None, "spacer"),
        ("VI", "Tax Expense", None, "header"),
        ("", "Current Tax", "27", "item_no_alpha"),
        ("", "Deferred Tax", "4", "item_no_alpha"),
        ("","Total Tax Expense", ["27", "4"], "total"),
        ("", "", None, "spacer"),
        ("VII", "Profit/(Loss) for the period (V - VI)", "PAT", "total"),
    ],
    # This provides a way for other agents to access the mapping if needed
    "Notes to Accounts": NOTES_STRUCTURE_AND_MAPPING
}
