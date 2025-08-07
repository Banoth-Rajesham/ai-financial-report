# PASTE THIS ENTIRE, COMPLETE CODE BLOCK INTO: config.py

# This is the missing blueprint for the Balance Sheet and P&L sheets
SCHEDULE_III_CONFIG = {
    'balance_sheet': [
        {'id': 'equity_and_liabilities', 'label': 'EQUITY AND LIABILITIES', 'is_header': True},
        {'id': 'shareholder_funds', 'label': "Shareholder's funds", 'is_subheader': True},
        {'id': 'share_capital', 'label': '(a) Share Capital', 'note': 1},
        {'id': 'reserves_surplus', 'label': '(b) Reserves and surplus', 'note': 2},
        {'id': 'non_current_liabilities', 'label': 'Non-current liabilities', 'is_subheader': True},
        {'id': 'long_term_borrowings', 'label': '(a) Long-term borrowings', 'note': 3},
        {'id': 'deferred_tax_liabilities', 'label': '(b) Deferred tax liabilities (Net)', 'note': 4},
        {'id': 'other_long_term_liabilities', 'label': '(c) Other Long-term liabilities', 'note': 5},
        {'id': 'long_term_provisions', 'label': '(d) Long-term provisions', 'note': 6},
        {'id': 'current_liabilities', 'label': 'Current liabilities', 'is_subheader': True},
        {'id': 'short_term_borrowings', 'label': '(a) Short-term borrowings', 'note': 7},
        {'id': 'trade_payables', 'label': '(b) Trade payables', 'note': 8},
        {'id': 'other_current_liabilities', 'label': '(c) Other current liabilities', 'note': 9},
        {'id': 'short_term_provisions', 'label': '(d) Short-term provisions', 'note': 10},
        {'id': 'total_equity_and_liabilities', 'label': 'TOTAL EQUITY AND LIABILITIES', 'is_total': True, 'sum_of': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {'id': 'assets', 'label': 'ASSETS', 'is_header': True},
        {'id': 'non_current_assets', 'label': 'Non-current assets', 'is_subheader': True},
        {'id': 'fixed_assets', 'label': '(a) Fixed assets (Tangible & Intangible)', 'note': 11},
        {'id': 'non_current_investments', 'label': '(b) Non-current investments', 'note': 12},
        {'id': 'deferred_tax_assets', 'label': '(c) Deferred tax assets (Net)', 'note': 4},
        {'id': 'long_term_loans_advances', 'label': '(d) Long-term loans and advances', 'note': 13},
        {'id': 'other_non_current_assets', 'label': '(e) Other non-current assets', 'note': 14},
        {'id': 'current_assets', 'label': 'Current assets', 'is_subheader': True},
        {'id': 'current_investments', 'label': '(a) Current Investments', 'note': 15},
        {'id': 'inventories', 'label': '(b) Inventories', 'note': 16},
        {'id': 'trade_receivables', 'label': '(c) Trade receivables', 'note': 17},
        {'id': 'cash_equivalents', 'label': '(d) Cash and cash equivalents', 'note': 18},
        {'id': 'short_term_loans_advances', 'label': '(e) Short-term loans and advances', 'note': 19},
        {'id': 'other_current_assets', 'label': '(f) Other current assets', 'note': 20},
        {'id': 'total_assets', 'label': 'TOTAL ASSETS', 'is_total': True, 'sum_of': [11, 12, 4, 13, 14, 15, 16, 17, 18, 19, 20]},
    ],
    'profit_and_loss': [
        {'id': 'revenue', 'label': 'I. Revenue', 'is_header': True},
        {'id': 'revenue_from_operations', 'label': 'Revenue from operations', 'note': 21},
        {'id': 'other_income', 'label': 'Other income', 'note': 22},
        {'id': 'total_revenue', 'label': 'Total Revenue', 'is_total': True, 'sum_of': [21, 22]},
        {'id': 'expenses', 'label': 'II. Expenses', 'is_header': True},
        {'id': 'cost_of_materials', 'label': 'Cost of materials consumed', 'note': 23},
        {'id': 'employee_benefits', 'label': 'Employee benefits expense', 'note': 24},
        {'id': 'finance_costs', 'label': 'Finance costs', 'note': 25},
        {'id': 'depreciation_amortization', 'label': 'Depreciation and amortization expense', 'note': 11},
        {'id': 'other_expenses', 'label': 'Other expenses', 'note': 26},
        {'id': 'total_expenses', 'label': 'Total expenses', 'is_total': True, 'sum_of': [23, 24, 25, 11, 26]},
        {'id': 'profit_before_tax', 'label': 'III. Profit before tax (I - II)', 'is_calculated': True, 'op': ['total_revenue', '-', 'total_expenses']},
        {'id': 'tax_expense', 'label': 'IV. Tax expense:', 'is_header': True},
        {'id': 'current_tax', 'label': 'Current tax', 'note': 27},
        {'id': 'deferred_tax', 'label': 'Deferred tax', 'note': 4},
        {'id': 'total_tax_expense', 'label': 'Total Tax Expense', 'is_total': True, 'sum_of': [27, 4]},
        {'id': 'profit_for_period', 'label': 'V. Profit for the period (III - IV)', 'is_calculated': True, 'op': ['profit_before_tax', '-', 'total_tax_expense']}
    ]
}

# This is your exact, unchanged mapping structure.
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
                'Equity shares of Rs. 10 each ': ['Issued and fully paid up Equity shares of Rs. 10 each']
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
                'Balance at the end of the year': ['Capital reserve at end']
            },
            '2.2 Securities premium account': {
                'Balance at the beginning of the year ': ['Securities premium at beginning'],
                'Add: Premium on shares issued during the year': ['Premium on shares issued'],
                'Less: Utilising during the year for': {
                    'Issuing bonus shares': ['Utilising securities premium for bonus shares'],
                    'Writing off preliminary expenses': ['Utilising securities premium for preliminary expenses'],
                    'Writing off shares/debentures issue expenses': ['Utilising securities premium for issue expenses'],
                    'Premium on redemption of redeemable preference shares/debentures': ['Utilising securities premium for redemption'],
                    'Buy back of shares': ['Utilising securities premium for buy back'],
                    'Others': ['Utilising securities premium for others']
                },
                'Balance at the end of the year ': ['Securities premium at end']
            },
            '2.3 Shares options outstanding account': {
                'Balance at the beginning of the year  ': ['Shares options outstanding at beginning'],
                'Add: Amounts recorded on grants/modifications/cancellations': ['grants/modifications to shares options outstanding'],
                'Less: Written back to Statement of Profit and Loss': ['Written back from shares options outstanding'],
                'Transferred to Securities premium account': ['shares options transferred to securities premium'],
                'Less: Deferred stock compensation expense': ['Deferred stock compensation expense'],
                'Balance at the end of the year  ': ['Shares options outstanding at end']
            },
            '2.4 General reserve': {
                'Balance at the beginning of the year   ': ['General reserve at beginning'],
                'Add: Transferred from surplus in Statement of Profit and Loss': ['Transferred to general reserve from surplus'],
                'Less: Utilised / transferred during the year for': {
                    'Issuing bonus shares ': ['Utilising general reserve for bonus shares'],
                    'Others ': ['Utilising general reserve for others']
                },
                'Balance at the end of the year   ': ['General reserve at end']
            },
            '2.5 Hedging reserve': {
                'Balance at the beginning of the year    ': ['Hedging reserve at beginning'],
                'Add / (Less): Effect of foreign exchange rate variations': ['Effect of foreign exchange on hedging reserve'],
                'Add / (Less): Transferred to Statement of Profit and Loss': ['Transferred from hedging reserve to P&L'],
                'Balance at the end of the year    ': ['Hedging reserve at end']
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Balance at the beginning of the year     ': ['Surplus at beginning'],
                'Add: Profit / (Loss) for the year': ['Profit / Loss for the year'],
                'Add: Amounts transferred from': {
                    'General reserve ': ['Amount transferred from general reserve'],
                    'Other reserves': ['Amount transferred from other reserves']
                },
                'Less: Interim dividend': ['Interim dividend'],
                'Dividends proposed to be distributed': ['Dividends proposed to be distributed'],
                'Tax on dividend': ['Tax on dividend'],
                'Less: Transferred to': {
                    'General reserve  ': ['Transferred from surplus to general reserve'],
                    'Capital redemption reserve': ['Transferred from surplus to capital redemption reserve'],
                    'Debenture redemption reserve': ['Transferred from surplus to debenture redemption reserve'],
                    'Other reserves ': ['Transferred from surplus to other reserves']
                },
                'Balance at the end of the year     ': ['Surplus at end']
            }
        }
    },
    '3': {
        'title': 'Long term borrowings',
        'sub_items': {
            '3.0 Long term borrowings Summary': {
                '(a) Term loans from banks': ['Term loans from banks'],
                '(b) Deferred payment liabilities': ['Deferred payment liabilities'],
                '(c) Deposits': ['Deposits'],
                '(d) Loans and advances from related parties': ['Loans and advances from related parties'],
                '(e) Other loans and advances': ['Other loans and advances specify nature']
            },
            '3.1 (i) Details of terms of repayment': {
                'Term loans from banks: XXX Bank': ['Term loan XXX Bank'],
                'Term loans from banks: YYY Bank': ['Term loan YYY Bank'],
                'Term loans from other parties: ABC Ltd': ['Term loan ABC Ltd'],
                'Term loans from other parties: XYZ Ltd': ['Term loan XYZ Ltd'],
                'Deferred payment for acquisition of fixed assets': ['Deferred payment for fixed assets'],
                'Deposits: Inter-corporate deposit 1': ['Inter-corporate deposit 1'],
                'Deposits: Inter-corporate deposit 2': ['Inter-corporate deposit 2'],
                'Loans and advances from related parties: RP 1': ['Loan from RP 1'],
                'Loans and advances from related parties: RP 2': ['Loan from RP 2'],
                'Other loans and advances: Advance 1': ['Advance 1'],
                'Other loans and advances: Advance 2': ['Advance 2']
            },
            '3.1 (ii) Details of long-term borrowings guaranteed by directors': {
                'Term loans from banks guaranteed': ['Term loans from banks guaranteed by director'],
                'Term loans from other parties guaranteed': ['Term loans from other parties guaranteed by director'],
                'Deferred payment liabilities guaranteed': ['Deferred payment liabilities guaranteed by director'],
                'Loans and advances from related parties guaranteed': ['Loans from related parties guaranteed by director'],
                'Other loans and advances guaranteed': ['Other loans and advances guaranteed by director']
            },
            '3.1 (iii) Details of default in repayment': {
                'Default - Bonds / debentures - Principal': ['Default bonds principal'],
                'Default - Bonds / debentures - Interest': ['Default bonds interest'],
                'Default - Term loans from banks - Principal': ['Default bank term loan principal'],
                'Default - Term loans from banks - Interest': ['Default bank term loan interest'],
                'Default - Term loans from other parties - Principal': ['Default other term loan principal'],
                'Default - Term loans from other parties - Interest': ['Default other term loan interest'],
                'Default - Deferred payment liabilities - Principal': ['Default deferred payment principal'],
                'Default - Deferred payment liabilities - Interest': ['Default deferred payment interest'],
                'Default - Deposits - Principal': ['Default deposits principal'],
                'Default - Deposits - Interest': ['Default deposits interest'],
                'Default - Loans and advances from related parties - Principal': ['Default related party loan principal'],
                'Default - Loans and advances from related parties - Interest': ['Default related party loan interest'],
                'Default - Other loans and advances - Principal': ['Default other loans principal'],
                'Default - Other loans and advances - Interest': ['Default other loans interest']
            }
        }
    },
    '4': {
        'title': 'Deferred Tax Asset/Liability',
        'sub_items': {
            'Tax on Difference between Book & Tax depreciation': ['Tax on Difference between Book & Tax depreciation', 'Deferred Tax'],
            'Tax on Disputed statutory liabilities': ['Tax Disputed statutory liabilities', 'Tax on disputed statutory liabilities paid and claimed as deduction for tax purposes but not debited to Profit & loss statement'],
            'Tax on Other items giving rise to time difference': ['Tax on Other items giving rise to time difference']
        }
    },
    '5': {
        'title': 'Other long term liabilities',
        'sub_items': {
            '(a) Trade Payables': {
                'Acceptances': ['Acceptances'],
                'Other than Acceptances': ['Other than Acceptances']
            },
            '(b) Others': {
                'Payables on purchase of fixed assets': ['Payables on purchase of fixed assets'],
                'Contractually reimbursable expenses': ['Contractually reimbursable expenses'],
                'Interest accrued but not due on borrowings': ['Interest accrued but not due on borrowings'],
                'Interest accrued on trade payables': ['Interest accrued on trade payables'],
                'Interest accrued on others': ['Interest accrued on others'],
                'Trade / security deposits received': ['Trade / security deposits received'],
                'Advances from customers': ['Advances from customers'],
                'Income received in advance (Unearned revenue)': ['Income received in advance (Unearned revenue)'],
                'Others (specify nature)': ['Others (specify nature)']
            }
        }
    },
    '6': {
        'title': 'Long term provisions',
        'sub_items': {
            '(a) Provision for employee benefits': {
                'Provision for compensated absences': ['Provision for compensated absences'],
                'Provision for gratuity (net) (Refer Note 30.4.b)': ['Provision for gratuity (net) (Refer Note 30.4.b)'],
                'Provision for post-employment medical benefits (Refer Note 30.4.b)': ['Provision for post-employment medical benefits (Refer Note 30.4.b)'],
                'Provision for other defined benefit plans (net) (give details) (Refer Note 30.4.b)': ['Provision for other defined benefit plans (net) (give details) (Refer Note 30.4.b)'],
                'Provision for other employee benefits (give details)': ['Provision for other employee benefits (give details)']
            },
            '(b) Provision - Others': {
                'Provision for premium payable on redemption of bonds (Refer Note 5 Long-term borrowings)': ['Provision for premium payable on redemption of bonds (Refer Note 5 Long-term borrowings)'],
                'Provision for estimated loss on derivatives': ['Provision for estimated loss on derivatives'],
                'Provision for warranty (Refer Note 30.14)': ['Provision for warranty (Refer Note 30.14)'],
                'Provision for estimated losses on onerous contracts (Refer Note 30.14)': ['Provision for estimated losses on onerous contracts (Refer Note 30.14)'],
                'Provision for other contingencies (Refer Note 30.14)': ['Provision for other contingencies (Refer Note 30.14)'],
                'Provision - others (give details)': ['Provision - others (give details)']
            }
        }
    },
    '7': {
        'title': 'Short term borrowings',
        'sub_items': {
            '(a) Loans repayable on demand': {
                'From banks - Secured': ['Secured from banks'],
                'From banks - Unsecured': ['Unsecured from banks'],
                'From other parties - Secured': ['Secured from other parties'],
                'From other parties - Unsecured': ['Unsecured from other parties']
            }
        }
    },
    '8': {
        'title': 'Trade payables',
        'sub_items': {
            'Trade payables: Acceptances': ['Acceptances'],
            'Trade payables: Other than Acceptances': ['Other than Acceptances']
        }
    },
    '9': {
        'title': 'Other current liabilities',
        'sub_items': {
            'Current maturities of long-term debt': ['Current maturities of long-term debt'],
            'Interest accrued but not due on borrowings': ['Interest accrued but not due on borrowings'],
            'Interest accrued and due on borrowings': ['Interest accrued and due on borrowings'],
            'Income received in advance (Unearned revenue)': ['Income received in advance', 'Unearned revenue'],
            'Unpaid dividends': ['Unpaid dividends'],
            'Application money received for allotment of securities': ['Application money received for allotment of securities'],
            'Other payables (Salaries and consultant fee)': ['Other payables', 'Salaries and consultant fee'],
            'Statutory remittances (GST, TDS, etc.)': ['Statutory remittances', 'GST payable', 'TDS payable', 'PT payable', 'EPF payable'],
            'Payables on purchase of fixed assets': ['Payables on purchase of fixed assets'],
            'Contractually reimbursable expenses': ['Contractually reimbursable expenses'],
            'Interest accrued on trade payables': ['Interest accrued on trade payables'],
            'Interest accrued on others': ['Interest accrued on others'],
            'Trade / security deposits received': ['Trade / security deposits received'],
            'Advances from customers': ['Advances from customers'],
            'Other (audit fee)': ['audit fee']
        }
    },
    '10': {
        'title': 'Short term provisions',
        'sub_items': {
            '(a) Provision for employee benefits': {
                'Provision for bonus': ['Provision for bonus'],
                'Provision for compensated absences': ['Provision for compensated absences'],
                'Provision for gratuity (net)': ['Provision for gratuity'],
                'Provision for post-employment medical benefits': ['Provision for post-employment medical benefits'],
                'Provision for other defined benefit plans (net)': ['Provision for other defined benefit plans'],
                'Provision for other employee benefits (give details)': ['Provision for other employee benefits']
            },
            '(b) Provision - Others': {
                'Provision for tax (net)': ['Provision for tax'],
                'Provision for premium payable on redemption of bonds': ['Provision for premium payable on redemption of bonds'],
                'Provision for estimated loss on derivatives': ['Provision for estimated loss on derivatives'],
                'Provision for warranty': ['Provision for warranty'],
                'Provision for estimated losses on onerous contracts': ['Provision for estimated losses on onerous contracts'],
                'Provision for other contingencies': ['Provision for other contingencies'],
                'Provision for proposed equity dividend': ['Provision for proposed equity dividend'],
                'Provision for proposed preference dividend': ['Provision for proposed preference dividend'],
                'Provision for tax on proposed dividends': ['Provision for tax on proposed dividends'],
                'Provision for Audit Fees': ['Provision for Audit Fees'],
                'Provision for Accounting Fee': ['Provision for Accounting Fee']
            }
        }
    },
    '11': {
        'title': 'Fixed Assets (Tangible & Intangible)',
        'sub_items': {
            'Depreciation for the year': ['Depriciation for the year', 'Depreciation', 'Dep as per IT ACT', 'Dep as per Comp'],
            'Opening WDV': ['Opening WDV', 'WDV as on 31-03-2024'],
            'Additions': ['additions before 30.09', 'additions after 30.09', 'Additions'],
            'Deleations': ['Deletions'],
            'Closing WDV': ['W.d.v as on 31/3/2025', 'WDV on 31/03/2025'],
            'Office Interiors': ['Office Interiors'],
            'Air Conditioners': ['Air Conditioners'],
            'Battery': ['Battery'],
            'CCTV Camera': ['CC TV Camera', 'CCTV Camera'],
            'Computers': ['Computers'],
            'Curtains': ['Curtains'],
            'Electronic Items': ['Electronic Items'],
            'Epson Printer': ['Epson Printer'],
            'Fan': ['Fan'],
            'Furniture': ['Furniture'],
            'Inverter': ['Inverter'],
            'Mobile Phone': ['Mobile Phone', 'Mobile phone'],
            'Motor Vehicle': ['Motor Vehicle'],
            'Refrigerator': ['Refridgerator', 'Refrigerator'],
            'Television': ['Television'],
            'Water Dispenser': ['Water Dispenser'],
            'Water Filter': ['Water Filter']
        }
    },
    '12': {
        'title': 'Non-current Investments',
        'sub_items': {
            'A. Trade Investments': {
                '(a) Investment in equity instruments': {
                    'of subsidiaries': ['trade investment in equity of subsidiaries'],
                    'of associates': ['trade investment in equity of associates'],
                    'of joint venture companies': ['trade investment in equity of joint venture companies'],
                    'of controlled special purpose entities': ['trade investment in equity of controlled special purpose entities'],
                    'of other entities': ['trade investment in equity of other entities']
                },
                '(b) Investment in preference shares': {
                    'of subsidiaries ': ['trade investment in preference shares of subsidiaries'],
                    'of associates ': ['trade investment in preference shares of associates'],
                    'of joint venture companies ': ['trade investment in preference shares of joint venture companies'],
                    'of controlled special purpose entities ': ['trade investment in preference shares of controlled special purpose entities'],
                    'of other entities ': ['trade investment in preference shares of other entities']
                },
                '(c) Investment in debentures or bonds': {
                    'of subsidiaries  ': ['trade investment in debentures of subsidiaries', 'trade investment in bonds of subsidiaries'],
                    'of associates  ': ['trade investment in debentures of associates', 'trade investment in bonds of associates'],
                    'of joint venture companies  ': ['trade investment in debentures of joint venture companies', 'trade investment in bonds of joint venture companies'],
                    'of controlled special purpose entities  ': ['trade investment in debentures of controlled special purpose entities', 'trade investment in bonds of controlled special purpose entities'],
                    'of other entities  ': ['trade investment in debentures of other entities', 'trade investment in bonds of other entities']
                },
                '(d) Investment in partnership firms': ['Trade Investment in partnership firms'],
                '(e) Other non-current trade investments': ['Other non-current trade investments']
            },
            'B. Other Investments': {
                '(a) Investment property': ['Investment property'],
                '(b) Investment in equity instruments ': {
                    'of subsidiaries   ': ['other investment in equity of subsidiaries'],
                    'of associates   ': ['other investment in equity of associates'],
                    'of joint venture companies   ': ['other investment in equity of joint venture companies'],
                    'of controlled special purpose entities   ': ['other investment in equity of controlled special purpose entities'],
                    'of other entities   ': ['other investment in equity of other entities']
                },
                '(c) Investment in preference shares ': {
                    'of subsidiaries    ': ['other investment in preference shares of subsidiaries'],
                    'of associates    ': ['other investment in preference shares of associates'],
                    'of joint venture companies    ': ['other investment in preference shares of joint venture companies'],
                    'of controlled special purpose entities    ': ['other investment in preference shares of controlled special purpose entities'],
                    'of other entities    ': ['other investment in preference shares of other entities']
                },
                '(d) Investment in government or trust securities': {
                    'government securities': ['government securities'],
                    'trust securities': ['trust securities']
                },
                '(e) Investment in debentures or bonds ': {
                    'of subsidiaries     ': ['other investment in debentures of subsidiaries', 'other investment in bonds of subsidiaries'],
                    'of associates     ': ['other investment in debentures of associates', 'other investment in bonds of associates'],
                    'of joint venture companies     ': ['other investment in debentures of joint venture companies', 'other investment in bonds of joint venture companies'],
                    'of controlled special purpose entities     ': ['other investment in debentures of controlled special purpose entities', 'other investment in bonds of controlled special purpose entities'],
                    'of other entities     ': ['other investment in debentures of other entities', 'other investment in bonds of other entities']
                },
                '(f) Investment in mutual funds': ['Investment in mutual funds'],
                '(g) Investment in partnership firms ': ['Other Investment in partnership firms'],
                '(h) Other non-current investments ': ['Other non-current investments (specify nature)']
            },
            'Less: Provision for diminution in value of investments': ['Provision for diminution in value of investments'],
            'Aggregate amount of quoted investments': ['Aggregate amount of quoted investments'],
            'Aggregate market value of listed and quoted investments': ['Aggregate market value of listed and quoted investments'],
            'Aggregate value of listed but not quoted investments': ['Aggregate value of listed but not quoted investments'],
            'Aggregate amount of unquoted investments': ['Aggregate amount of unquoted investments']
        }
    },
    '13': {
        'title': 'Long term loans and advances',
        'sub_items': {
            '(a) Capital advances': {
                'Secured, considered good': ['Capital advances secured considered good'],
                'Unsecured, considered good': ['Capital advances unsecured considered good'],
                'Doubtful': ['Capital advances doubtful'],
                'Less: Provision for doubtful advances': ['Provision for doubtful advances']
            },
            '(b) Security deposits': {
                'Secured, considered good ': ['Security deposits secured considered good'],
                'Unsecured, considered good ': ['Security deposits unsecured considered good'],
                'Doubtful ': ['Security deposits doubtful'],
                'Less: Provision for doubtful deposits': ['Provision for doubtful deposits']
            },
            '(c) Loans and advances to related parties': {
                'Secured, considered good  ': ['Loans and advances to related parties secured considered good'],
                'Unsecured, considered good  ': ['Loans and advances to related parties unsecured considered good'],
                'Doubtful  ': ['Loans and advances to related parties doubtful'],
                'Less: Provision for doubtful loans and advances ': ['Provision for doubtful loans and advances related parties']
            },
            '(d) Loans and advances to employees': {
                'Secured, considered good   ': ['Loans and advances to employees secured considered good'],
                'Unsecured, considered good   ': ['Loans and advances to employees unsecured considered good'],
                'Doubtful   ': ['Loans and advances to employees doubtful'],
                'Less: Provision for doubtful loans and advances  ': ['Provision for doubtful loans and advances employees']
            },
            '(e) Prepaid expenses - Unsecured, considered good': ['Prepaid expenses'],
            '(f) Advance income tax (net of provisions)': ['Advance income tax'],
            '(g) MAT credit entitlement - Unsecured, considered good': ['MAT credit entitlement'],
            '(h) Balances with government authorities': {
                'Unsecured, considered good': ['Balances with government authorities unsecured'],
                'CENVAT credit receivable': ['CENVAT credit receivable'],
                'VAT credit receivable': ['VAT credit receivable'],
                'Service Tax credit receivable': ['Service Tax credit receivable']
            },
            '(i) Other loans and advances': {
                'Secured, considered good    ': ['Other loans and advances secured considered good'],
                'Unsecured, considered good    ': ['Other loans and advances unsecured considered good'],
                'Doubtful    ': ['Other loans and advances doubtful'],
                'Less: Provision for other doubtful loans and advances': ['Provision for other doubtful loans and advances']
            },
            'Amounts due from (Disclosure)': {
                'Directors': ['Loans and advances due from Directors'],
                'Other officers of the Company': ['Loans and advances due from Other officers'],
                'Firms in which any director is a partner': ['Loans and advances due from Firms director is partner'],
                'Private companies in which any director is a member': ['Loans and advances due from Private companies director is member']
            }
        }
    },
    '14': {
        'title': 'Other non-current assets',
        'sub_items': {
            '(a) Long-term trade receivables': {
                'Secured, considered good': ['Long-term trade receivables secured'],
                'Unsecured, considered good': ['Long-term trade receivables unsecured'],
                'Doubtful': ['Long-term trade receivables doubtful'],
                'Less: Provision for doubtful trade receivables': ['Provision for doubtful trade receivables']
            },
            '(b) Unamortised expenses': {
                'Ancillary borrowing costs': ['Ancillary borrowing costs'],
                'Share issue expenses': ['Share issue expenses'],
                'Discount on shares': ['Discount on shares']
            },
            '(c) Accruals': {
                'Interest accrued on deposits': ['Interest accrued on deposits'],
                'Interest accrued on investments': ['Interest accrued on investments'],
                'Interest accrued on trade receivables': ['Interest accrued on trade receivables']
            },
            '(d) Others': {
                'Insurance claims': ['Insurance claims'],
                'Receivables on sale of fixed assets': ['Receivables on sale of fixed assets'],
                'Contractually reimbursable expenses': ['Contractually reimbursable expenses'],
                'Others (specify nature)': ['Other non-current assets specify nature']
            },
            'Debts due from (Disclosure)': {
                'Directors': ['Long-term trade receivables from Directors'],
                'Other officers of the Company': ['Long-term trade receivables from Other officers'],
                'Firms in which any director is a partner': ['Long-term trade receivables from Firms director is partner'],
                'Private companies in which any director is a member': ['Long-term trade receivables from Private companies director is member']
            }
        }
    },
    '15': {
        'title': 'Current Investments',
        'sub_items': {
            'A. Current portion of long-term investments': {
                '(a) Investment in preference shares': ['Current portion of long-term investment in preference shares'],
                '(b) Investment in government or trust securities': ['Current portion of long-term investment in government or trust securities'],
                '(c) Investment in debentures or bonds': ['Current portion of long-term investment in debentures or bonds'],
                '(d) Investment in mutual funds': ['Current portion of long-term investment in mutual funds'],
                '(e) Other investments': ['Current portion of other long-term investments'],
                'Less: Provision for diminution': ['Provision for diminution in value of current portion of long-term investments']
            },
            'B. Other current investments': {
                '(a) Investment in equity instruments': {
                    'of subsidiaries': ['Other current investment in equity of subsidiaries'],
                    'of associates': ['Other current investment in equity of associates'],
                    'of joint venture companies': ['Other current investment in equity of joint venture companies'],
                    'of controlled special purpose entities': ['Other current investment in equity of controlled special purpose entities'],
                    'of other entities': ['Other current investment in equity of other entities']
                },
                '(b) Investment in preference shares ': {
                    'of subsidiaries ': ['Other current investment in preference shares of subsidiaries'],
                    'of associates ': ['Other current investment in preference shares of associates'],
                    'of joint venture companies ': ['Other current investment in preference shares of joint venture companies'],
                    'of controlled special purpose entities ': ['Other current investment in preference shares of controlled special purpose entities'],
                    'of other entities ': ['Other current investment in preference shares of other entities']
                },
                '(c) Investment in government or trust securities ': {
                    'government securities': ['Other current investment in government securities'],
                    'trust securities': ['Other current investment in trust securities']
                },
                '(d) Investment in debentures or bonds ': {
                    'of subsidiaries  ': ['Other current investment in debentures or bonds of subsidiaries'],
                    'of associates  ': ['Other current investment in debentures or bonds of associates'],
                    'of joint venture companies  ': ['Other current investment in debentures or bonds of joint venture companies'],
                    'of controlled special purpose entities  ': ['Other current investment in debentures or bonds of controlled special purpose entities'],
                    'of other entities  ': ['Other current investment in debentures or bonds of other entities']
                },
                '(e) Investment in mutual funds ': ['Other current investment in mutual funds'],
                '(f) Investment in partnership firms': ['Other current investment in partnership firms'],
                '(g) Other investments (specify nature)': ['Other current investments specify nature']
            },
            'Aggregate amount of quoted current investments': ['Aggregate amount of quoted current investments'],
            'Aggregate market value of listed and quoted current investments': ['Aggregate market value of listed and quoted current investments'],
            'Aggregate value of listed but not quoted current investments': ['Aggregate value of listed but not quoted current investments'],
            'Aggregate amount of unquoted current investments': ['Aggregate amount of unquoted current investments'],
            'Aggregate provision for diminution (write down) in the value of other current investments': ['Aggregate provision for diminution in value of other current investments']
        }
    },
    '16': {
        'title': 'Inventories',
        'sub_items': {
            '(a) Raw materials': {
                'Raw materials': ['Raw materials'],
                'Goods-in-transit': ['Raw materials goods-in-transit']
            },
            '(b) Work-in-progress': {
                'Product X1': ['Work-in-progress Product X1'],
                'Product Y1': ['Work-in-progress Product Y1'],
                'Product Z1': ['Work-in-progress Product Z1'],
                'Other items': ['Work-in-progress Other items'],
                'Goods-in-transit ': ['Work-in-progress goods-in-transit']
            },
            '(c) Finished goods': {
                'Finished goods': ['Finished goods (other than those acquired for trading)'],
                'Goods-in-transit  ': ['Finished goods goods-in-transit']
            },
            '(d) Stock-in-trade': {
                'Stock-in-trade': ['Stock-in-trade (acquired for trading)'],
                'Goods-in-transit   ': ['Stock-in-trade goods-in-transit']
            },
            '(e) Stores and spares': {
                'Stores and spares': ['Stores and spares'],
                'Goods-in-transit    ': ['Stores and spares goods-in-transit']
            },
            '(f) Loose tools': {
                'Loose tools': ['Loose tools'],
                'Goods-in-transit     ': ['Loose tools goods-in-transit']
            },
            '(g) Others': {
                'Others (Specify nature)': ['Inventories Others'],
                'Goods-in-transit      ': ['Inventories Others goods-in-transit']
            }
        }
    },
    '17': {
        'title': 'Trade Receivables',
        'sub_items': {
            'Trade receivables outstanding > 6 months': {
                'Secured, considered good': ['Outstanding trade receivables secured good'],
                'Unsecured, considered good': ['Outstanding trade receivables unsecured good'],
                'Doubtful': ['Outstanding trade receivables doubtful'],
                'Less: Provision for doubtful trade receivables': ['Provision for outstanding doubtful trade receivables']
            },
            'Other Trade receivables': {
                'Secured, considered good ': ['Other trade receivables secured good'],
                'Unsecured, considered good ': ['Other trade receivables unsecured good'],
                'Doubtful ': ['Other trade receivables doubtful'],
                'Less: Provision for doubtful trade receivables ': ['Provision for other doubtful trade receivables']
            }
        }
    },
    '18': {
        'title': 'Cash and cash equivalents',
        'sub_items': {
            '(a) Cash on hand': ['Cash on hand'],
            '(b) Cheques, drafts on hand': ['Cheques, drafts on hand'],
            '(c) Balances with banks': {
                '(i) In current accounts': ['Balances with banks in current accounts'],
                '(ii) In EEFC accounts': ['Balances with banks in EEFC accounts'],
                '(iii) In deposit accounts': ['Balances with banks in deposit accounts'],
                '(iv) In earmarked accounts': {
                    'Unpaid dividend accounts': ['Unpaid dividend accounts'],
                    'Unpaid matured deposits': ['Unpaid matured deposits'],
                    'Unpaid matured debentures': ['Unpaid matured debentures'],
                    'Share application money for refund': ['Share application money received for allotment of securities and due for refund', 'Share application money for refund'],
                    'Balances held as margin money or security': ['Balances held as margin money or security'],
                    'Other earmarked accounts': ['Other earmarked accounts']
                }
            },
            '(d) Others (specify nature)': ['Cash and cash equivalents Others']
        }
    },
    '19': {
        'title': 'Short term loans and advances',
        'sub_items': {
            '(a) Loans and advances to related parties': {
                'Secured, considered good': ['Short-term loans and advances to related parties secured'],
                'Unsecured, considered good': ['Short-term loans and advances to related parties unsecured'],
                'Doubtful': ['Short-term loans and advances to related parties doubtful'],
                'Less: Provision for doubtful loans and advances': ['Provision for doubtful short-term loans and advances to related parties']
            },
            '(b) Security deposits': {
                'Secured, considered good ': ['Short-term security deposits secured'],
                'Unsecured, considered good ': ['Short-term security deposits unsecured'],
                'Doubtful ': ['Short-term security deposits doubtful'],
                'Less: Provision for doubtful deposits': ['Provision for doubtful short-term security deposits']
            },
            '(c) Loans and advances to employees': {
                'Secured, considered good  ': ['Short-term loans and advances to employees secured'],
                'Unsecured, considered good  ': ['Short-term loans and advances to employees unsecured'],
                'Doubtful  ': ['Short-term loans and advances to employees doubtful'],
                'Less: Provision for doubtful loans and advances ': ['Provision for doubtful short-term loans and advances to employees']
            },
            '(d) Prepaid expenses': ['Short-term Prepaid expenses'],
            '(e) Balances with government authorities': {
                'Unsecured, considered good': ['Short-term balances with government authorities unsecured'],
                'CENVAT credit receivable': ['Short-term CENVAT credit receivable'],
                'VAT credit receivable': ['Short-term VAT credit receivable'],
                'Service Tax credit receivable': ['Short-term Service Tax credit receivable']
            },
            '(f) Inter-corporate deposits': {
                'Secured, considered good   ': ['Inter-corporate deposits secured'],
                'Unsecured, considered good   ': ['Inter-corporate deposits unsecured'],
                'Doubtful   ': ['Inter-corporate deposits doubtful'],
                'Less: Provision for doubtful inter-corporate deposits': ['Provision for doubtful inter-corporate deposits']
            },
            '(g) Others (specify nature)': {
                'Secured, considered good    ': ['Other short-term loans and advances secured'],
                'Unsecured, considered good    ': ['Other short-term loans and advances unsecured'],
                'Doubtful    ': ['Other short-term loans and advances doubtful'],
                'Less: Provision for other doubtful loans and advances': ['Provision for other doubtful short-term loans and advances']
            },
            'Amounts due from (Disclosure)': {
                'Directors': ['Short-term loans and advances from Directors'],
                'Other officers of the Company': ['Short-term loans and advances from Other officers'],
                'Firms in which any director is a partner': ['Short-term loans and advances from Firms where director is partner'],
                'Private companies in which any director is a member': ['Short-term loans and advances from Private companies where director is member']
            }
        }
    },
    '20': {
        'title': 'Other current assets',
        'sub_items': {
            '(a) Unbilled revenue': ['Unbilled revenue'],
            '(b) Unamortised expenses': {
                'Ancillary borrowing costs': ['Unamortised ancillary borrowing costs'],
                'Share issue expenses': ['Unamortised share issue expenses'],
                'Discount on shares': ['Unamortised discount on a shares']
            },
            '(c) Accruals': {
                'Interest accrued on deposits': ['Current Interest accrued on deposits'],
                'Interest accrued on investments': ['Current Interest accrued on investments'],
                'Interest accrued on trade receivables': ['Current Interest accrued on trade receivables']
            },
            '(d) Advance Tax & Other Receivables': {
                'Advance Tax': ['Advance Tax'],
                'Income receivable from services': ['Income receivable from services'],
                'Receivables on sale of fixed assets': ['Current Receivables on sale of fixed assets'],
                'Contractually reimbursable expenses': ['Current Contractually reimbursable expenses'],
                'TDS and other statutory payments': ['TDS and other statutory payments'],
                'Input GST': ['Input GST']
            }
        }
    },
    '21': {
        'title': 'Revenue from Operations',
        'sub_items': {
            'Sale of Services': ['Sale of Services']
        }
    },
    '22': {
        'title': 'Other income',
        'sub_items': {
            'Miscellaneous Income': ['Miscellaneous Income'],
            'Refund on GST': ['Refund on GST']
        }
    },
    '23': {
        'title': 'Cost of Materials Consumed',
        'sub_items': {
            'Purchases': ['Purchases']
        }
    },
    '24': {
        'title': 'Employee benefit expenses',
        'sub_items': {
            'Salaries and Wages': ['Salaries and Wages', 'Salary'],
            'Contribution to provident and other funds': ['Contribution to provident and other funds'],
            'Gratuity Expenses': ['Gratuity Expenses'],
            'Staff welfare Expenses': ['Staff welfare Expenses']
        }
    },
    '25': {
        'title': 'Finance Costs',
        'sub_items': {
            'Interest on borrowings': ['Interest on borrowings'],
            'Other Interest (Interest on Income Tax)': ['Other Interest', 'Interest on Income Tax']
        }
    },
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'Accounting Fee': ['Accounting Fee'],
            'Audit Fees': ['Audit Fees'],
            'Accomodation Charges': ['Accomodation Charges'],
            'Admin expenses': ['Admin expenses'],
            'Bank Charges': ['Bank Charges'],
            'Books and periodicals': ['Books and periodicals'],
            'Business Promotion': ['Business Promotion'],
            'Consultancy charges': ['Consultancy charges'],
            'Donations': ['Donations'],
            'Electrcity charges': ['Electrcity charges', 'Electricity charges'],
            'Entertainment Expenses': ['Entertainment Expenses'],
            'EPFO charges': ['EPFO charges'],
            'Freight charges': ['Freight charges'],
            'GST Charges': ['GST Charges'],
            'Income Tax': ['Income Tax'],
            'Insurance': ['Insurance'],
            'Internet Charges': ['Internet Charges'],
            'Medical Insurance': ['Medical Insurance'],
            'ELD Annual Subscription': ['ELD Annual Subscription'],
            'Office expenses': ['Office expenses'],
            'Recruitment Expenses': ['Recruitment Expenses'],
            'Professional Tax': ['Professional Tax'],
            'Printing and stationary': ['Printing and stationary'],
            'Software Charges': ['Software Charges'],
            'Stamps and Postage': ['Stamps and Postage'],
            'Rent': ['Rent'],
            'Subscription Charges': ['Subscription Charges'],
            'Web Hosting and Domain': ['Web Hosting and Domain'],
            'Vehicle Maintenance': ['Vehicle Maintenance'],
            'Travelling Expense': ['Travelling Expense'],
            'Telephone expenses': ['Telephone expenses'],
            'Repair and maintenance': ['Repair and maintenance'],
            'Water Charges': ['Water Charges'],
            'Registration Fee': ['Registration Fee'],
            'Posters': ['Posters'],
            'Pantry Purchases': ['Pantry Purchases'],
            'Painter Charges': ['Painter Charges'],
            'Office Maintenance': ['Office Maintenance'],
            'Food Expenses': ['Food Expenses'],
            'Education Fee': ['Education Fee'],
            'Visa Charges': ['Visa Charges'],
            'Computers on Rent': ['Computers on Rent'],
            'Computer Expenses': ['ComputerExpenses', 'Computer Expenses'],
            'Commission Charges': ['Commission Charges'],
            'Allowances': ['Allowances'],
            'Other expenses': ['Other expenses'],
            'Vehicle Accessories': ['Vehicle Accessories'],
            'MCA Fee': ['MCA Fee'],
            'Round Off': ['Round Off']
        }
    }
}
