# ==============================================================================
# CONFIG.PY - NOTES STRUCTURE AND MAPPING
# This file is built sequentially.
# Current progress: Note 1, Note 2, Note 3, Note 4
# ==============================================================================

NOTES_STRUCTURE_AND_MAPPING = {
    # =======================================================================
    # CONFIGURATION FOR NOTE 1: SHARE CAPITAL
    # =======================================================================
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            # Share Capital Table (Main Block)
            'Authorised share capital': {
                'No.of shares 10000 Equity shares of Rs. 10 each': [
                    'Authorised share capital|No.of shares 10000 Equity shares of Rs. 10 each',
                    'authorised share capital'
                ]
            },
            'Issued, subscribed and fully paid up capital': {
                'No.of shares 10000 Equity shares of Rs. 10 each': [
                    'Issued, subscribed and fully paid up capital|No.of shares 10000 Equity shares of Rs. 10 each',
                    'Share Capital', 'Equity Capital', 'Paid-up Capital'
                ]
            },
            'Issued, subscribed and Partly up capital': {
                'No.of shares 10000 equity shares of Rs. 10 each fully paid up': [
                    'Issued, subscribed and Partly up capital|No.of shares 10000 equity shares of Rs. 10 each fully paid up.'
                ]
            },
            'Total': [
                'Total Share Capital', 'Total Equity Capital'
            ],
            # 1.1 Reconciliation of Number of Shares (Section)
            '1.1 Reconciliation of number of shares': {
                'Equity shares': {
                    'No.of shares 10000 Equity shares of Rs. 10 each': [
                        'Equity shares|No.of shares 10000 Equity shares of Rs. 10 each'
                    ]
                },
                'Add: Additions to share capital on account of fresh issue or bonus issue etc.': [
                    'Add: Additions to share capital on account of fresh issue or bonus issue etc.',
                    'additions to share capital'
                ],
                'Ded: Deductions from share capital on account of shares bought back, redemption etc.': [
                    'Ded: Deductions from share capital on account of shares bought back, redemption etc.',
                    'deductions from share capital'
                ],
                'Balance at the end of the year': {
                    'No. of shares 10,000 shares of Rs. 10 each': [
                        'Balance at the end of the year|No. of shares 10,000 shares of Rs. 10 each'
                    ]
                }
            },
            # 1.2 Details of Shareholders Holding >5% (Section)
            '1.2 Details of share held by shareholders holding more than 5% of the aggregate shares in the company': {
                'M A Waheed Khan': [
                    'Shareholder|M A Waheed Khan'
                ],
                'M A Qhuddus Khan': [
                    'Shareholder|M A Qhuddus Khan'
                ],
                'M A Khadir Khan Asif': [
                    'Shareholder|M A Khadir Khan Asif'
                ],
                'M A Rauf Khan': [
                    'Shareholder|M A Rauf Khan'
                ],
                'Total': [
                    'Total shareholder percentage|shareholders >5%'
                ]
            }
        }
    },
    # ... other notes unchange

    # ==============================================================================
    # CONFIGURATION FOR NOTE 2: RESERVE AND SURPLUS
    # ==============================================================================
    '2': {
        'title': 'Reserve and surplus',
        'sub_items': {
            '2.1 Capital reserve': {
                'Balance at the beginning of the year': ['2.1 Capital reserve|Balance at the beginning of the year'],
                'Add: Additions during the year (give details)': ['2.1 Capital reserve|Add: Additions during the year (give details)'],
                'Less: Utilized/transferred during the year (give details)': ['2.1 Capital reserve|Less: Utilized/transferred during the year (give details)'],
                'Balance at the end of the year': ['2.1 Capital reserve|Balance at the end of the year', 'Capital reserve']
            },
            '2.2 Securities premium account': {
                'Balance at the beginning of the year': ['2.2 Securities premium account|Balance at the beginning of the year'],
                'Add: Premium on shares issued during the year': ['2.2 Securities premium account|Add: Premium on shares issued during the year'],
                'Less: Utlilising during the year for:': {
                    'Issuing bonus shares': ['Less: Utlilising during the year for:|Issuing bonus shares'],
                    'Writing off preliminary expenses': ['Less: Utlilising during the year for:|Writing off preliminary expenses'],
                    'Writing off shares/debentures issue expenses': ['Less: Utlilising during the year for:|Writing off shares/debentures issue expenses'],
                    'Premium on redemption of redeemable preference shares/debentures.': ['Less: Utlilising during the year for:|Premium on redemption of redeemable preference shares/debentures.'],
                    'Buy back of shares': ['Less: Utlilising during the year for:|Buy back of shares'],
                    'Others (give details)': ['Less: Utlilising during the year for:|Others (give details)']
                },
                'Balance at the end of the year': ['2.2 Securities premium account|Balance at the end of the year', 'Securities premium', 'share premium']
            },
            '2.3 Shares options outstanding account': {
                'Balance at the beginning of the year': ['2.3 Shares options outstanding account|Balance at the beginning of the year'],
                'Add: Amounts recorded on grants/modifications/cancellations during the year.': ['2.3 Shares options outstanding account|Add: Amounts recorded on grants/modifications/cancellations during the year.'],
                'Less: Written back to Statement of Profit and Loss during the year': ['2.3 Shares options outstanding account|Less: Written back to Statement of Profit and Loss during the year'],
                'Transferred to Securities premium account': ['2.3 Shares options outstanding account|Transferred to Securities premium account'],
                'Less: Deferred stock compensation expense': ['2.3 Shares options outstanding account|Less: Deferred stock compensation expense'],
                'Balance at the end of the year': ['2.3 Shares options outstanding account|Balance at the end of the year']
            },
            '2.4 General reserve': {
                'Balance at the beginning of the year': ['2.4 General reserve|Balance at the beginning of the year'],
                'Add: Transferred from surplus in Statement of Profit and Loss': ['2.4 General reserve|Add: Transferred from surplus in Statement of Profit and Loss'],
                'Less: Utilised / transferred during the year for:': {
                    'Issuing bonus shares': ['Less: Utilised / transferred during the year for:|Issuing bonus shares'],
                    'Others (give details)': ['Less: Utilised / transferred during the year for:|Others (give details)']
                },
                'Balance at the end of the year': ['2.4 General reserve|Balance at the end of the year', 'General Reserve']
            },
            '2.5 Hedging reserve': {
                'Balance at the beginning of the year': ['2.5 Hedging reserve|Balance at the beginning of the year'],
                'Add / (Less): Effect of foreign exchange rate variations on hedging instruments outstanding at the end of the year': ['2.5 Hedging reserve|Add / (Less): Effect of foreign exchange rate variations on hedging instruments outstanding at the end of the year'],
                'Add / (Less): Transferred to Statement of Profit and Loss': ['2.5 Hedging reserve|Add / (Less): Transferred to Statement of Profit and Loss'],
                'Balance at the end of the year': ['2.5 Hedging reserve|Balance at the end of the year']
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Balance at the beginning of the year': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Balance at the beginning of the year'],
                'Add: Profit / (Loss) for the year': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Add: Profit / (Loss) for the year'],
                'Add: Amounts transferred from:': {
                    'General reserve': ['Add: Amounts transferred from:|General reserve'],
                    'Other reserves (give details)': ['Add: Amounts transferred from:|Other reserves (give details)']
                },
                'Less: Interim dividend': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Less: Interim dividend'],
                'Dividends proposed to be distributed to equity shareholders (_ per share)': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Dividends proposed to be distributed to equity shareholders (_ per share)'],
                'Dividends proposed to be distributed to preference shareholders (_ per share)': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Dividends proposed to be distributed to preference shareholders (_ per share)'],
                'Tax on dividend': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Tax on dividend'],
                'Less: Transferred to:': {
                    'General reserve': ['Less: Transferred to:|General reserve'],
                    'Capital redemption reserve': ['Less: Transferred to:|Capital redemption reserve'],
                    'Debenture redemption reserve': ['Less: Transferred to:|Debenture redemption reserve'],
                    'Other reserves (give details)': ['Less: Transferred to:|Other reserves (give details)']
                },
                'Balance at the end of the year': [
                    '2.6 Surplus / (Deficit) in Statement of Profit and Loss|Balance at the end of the year',
                    'Profit & Loss A/c', 'Retained Earnings', 'Surplus'
                ]
            }
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 3: LONG TERM BORROWINGS
    # ==============================================================================
    '3': {
        'title': 'Long term borrowings',
        'sub_items': {
            '(a) Term loans': {
                'From banks:- Secured': ['(a) Term loans|From banks:- Secured'],
                'From banks:- Unsecured': ['(a) Term loans|From banks:- Unsecured'],
                'From other parties:- Secured': ['(a) Term loans|From other parties:- Secured'],
                'From other parties:- Unsecured': ['(a) Term loans|From other parties:- Unsecured']
            },
            '(b) Deferred payment liabilities': {
                'Secured': ['(b) Deferred payment liabilities|Secured'],
                'Unsecured': ['(b) Deferred payment liabilities|Unsecured']
            },
            '(c) Deposits': {
                'Secured': ['(c) Deposits|Secured'],
                'Unsecured': ['(c) Deposits|Unsecured']
            },
            '(d) Loans and advances from related parties': {
                'Secured': ['(d) Loans and advances from related parties|Secured'],
                'Unsecured': ['(d) Loans and advances from related parties|Unsecured']
            },
            '(e) Other loans and advances (specify nature)': {
                'Secured': ['(e) Other loans and advances (specify nature)|Secured'],
                'Unsecured': ['(e) Other loans and advances (specify nature)|Unsecured']
            },
            '3.1 Notes:': {
                '(i) Details of terms of repayment for the other long-term borrowings and security provided in respect of the secured other long-term borrowings:': {
                    'Term loans from banks:': {
                        'XXX Bank': ['Term loans from banks:|XXX Bank'],
                        'YYY Bank': ['Term loans from banks:|YYY Bank']
                    },
                    'Term loans from other parties:': {
                        'ABC Ltd.': ['Term loans from other parties:|ABC Ltd.'],
                        'XYZ Ltd.': ['Term loans from other parties:|XYZ Ltd.']
                    },
                    'Deferred payment liabilities:': {
                        'Deferred sales tax liability': ['Deferred payment liabilities:|Deferred sales tax liability'],
                        'Deferred payment for acquisition of fixed assets': ['Deferred payment liabilities:|Deferred payment for acquisition of fixed assets']
                    },
                    'Deposits:': {
                        'Public deposits': ['Deposits:|Public deposits'],
                        'Inter-corporate deposit 1': ['Deposits:|Inter-corporate deposit 1'],
                        'Inter-corporate deposit 2': ['Deposits:|Inter-corporate deposit 2']
                    },
                    'Loans and advances from related parties:': {
                        'RP 1': ['Loans and advances from related parties:|RP 1'],
                        'RP 2': ['Loans and advances from related parties:|RP 2']
                    },
                    'Other loans and advances:': {
                        'Loan 1': ['Other loans and advances:|Loan 1'],
                        'Advance 1': ['Other loans and advances:|Advance 1']
                    }
                },
                '(ii) Details of long-term borrowings guaranteed by some of the directors or others:': {
                    'Bonds / debentures': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Bonds / debentures'],
                    'Term loans from banks': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Term loans from banks'],
                    'Term loans from other parties': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Term loans from other parties'],
                    'Deferred payment liabilities': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Deferred payment liabilities'],
                    'Deposits': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Deposits'],
                    'Loans and advances from related parties': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Loans and advances from related parties'],
                    'Long-term maturities of finance lease obligations': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Long-term maturities of finance lease obligations'],
                    'Other loans and advances': ['(ii) Details of long-term borrowings guaranteed by some of the directors or others:|Other loans and advances']
                },
                '(iii) The Company has defaulted in repayment of loans and interest in respect of the following:': {
                    'Bonds / debentures': { 'Principal': ['Bonds / debentures|Principal'], 'Interest': ['Bonds / debentures|Interest'] },
                    'Term loans from banks': { 'Principal': ['Term loans from banks|Principal'], 'Interest': ['Term loans from banks|Interest'] },
                    'Term loans from other parties': { 'Principal': ['Term loans from other parties|Principal'], 'Interest': ['Term loans from other parties|Interest'] },
                    'Deferred payment liabilities': { 'Principal': ['Deferred payment liabilities|Principal'], 'Interest': ['Deferred payment liabilities|Interest'] },
                    'Deposits': { 'Principal': ['Deposits|Principal'], 'Interest': ['Deposits|Interest'] },
                    'Loans and advances from related parties': { 'Principal': ['Loans and advances from related parties|Principal'], 'Interest': ['Loans and advances from related parties|Interest'] },
                    'Long-term maturities of finance lease obligations': { 'Principal': ['Long-term maturities of finance lease obligations|Principal'], 'Interest': ['Long-term maturities of finance lease obligations|Interest'] },
                    'Other loans and advances': { 'Principal': ['Other loans and advances|Principal'], 'Interest': ['Other loans and advances|Interest'] }
                }
            },
            'Total Long Term Borrowings': ['Long-term Loans', 'Debentures', 'Mortgage Loan', 'long term borrowings']
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 4: DEFERRED TAX ASSET/LIABILITY
    # ==============================================================================
    '4': {
        'title': 'Deferred Tax Asset/Liability',
        'sub_items': {
            'Tax on Difference between Book & Tax depreciation': [
                'Tax on Difference between Book & Tax depreciation',
                'deferred tax', # Universal alias
                'deferred tax asset', # Universal alias
                'deferred tax liability' # Universal alias
            ],
            'Tax Disputed statutory liabilities paid and claimed as deduction for tax purposes but not debited to Profit & loss statement.': [
                'Tax Disputed statutory liabilities paid and claimed as deduction for tax purposes but not debited to Profit & loss statement.'
            ],
            'Tax on Other items giving rise to time difference': [
                'Tax on Other items giving rise to time difference'
            ]
        }
    },
    
        # ==============================================================================
    # CONFIGURATION FOR NOTE 5: OTHER LONG TERM LIABILITIES
    # ==============================================================================
    '5': {
        'title': 'Other long term liabilities',
        'sub_items': {
            '(a) Trade Payables: *': {
                '(i) Acceptances': ['(a) Trade Payables: *|(i) Acceptances'],
                '(ii) Other than Acceptances': ['(a) Trade Payables: *|(ii) Other than Acceptances']
            },
            '(b) Others:': {
                '(i) Payables on purchase of fixed assets': ['(b) Others:|(i) Payables on purchase of fixed assets'],
                '(ii) Contractually reimbursable expenses': ['(b) Others:|(ii) Contractually reimbursable expenses'],
                '(iii) Interest accrued but not due on borrowings': ['(b) Others:|(iii) Interest accrued but not due on borrowings'],
                '(iv) Interest accrued on trade payables': ['(b) Others:|(iv) Interest accrued on trade payables'],
                '(v) Interest accrued on others': ['(b) Others:|(v) Interest accrued on others'],
                '(vi) Trade / security deposits received': ['(b) Others:|(vi) Trade / security deposits received'],
                '(vii) Advances from customers': ['(b) Others:|(vii) Advances from customers'],
                '(viii) Income received in advance (Unearned revenue)': ['(b) Others:|(viii) Income received in advance (Unearned revenue)'],
                '(ix) Others (specify nature)': ['(b) Others:|(ix) Others (specify nature)']
            },
            # Universal Alias to catch the total if sub-items are not detailed
            'Total Other long term liabilities': ['Other long term liabilities']
        }
    },
        # ==============================================================================
    # CONFIGURATION FOR NOTE 6: LONG TERM PROVISIONS
    # ==============================================================================
    '6': {
        'title': 'Long term provisions',
        'sub_items': {
            '(a) Provision for employee benefits:': {
                '(i) Provision for compensated absences': ['(a) Provision for employee benefits:|(i) Provision for compensated absences'],
                '(ii) Provision for gratuity (net) (Refer Note 30.4.b)': ['(a) Provision for employee benefits:|(ii) Provision for gratuity (net) (Refer Note 30.4.b)'],
                '(iii) Provision for post-employment medical benefits (Refer Note 30.4.b)': ['(a) Provision for employee benefits:|(iii) Provision for post-employment medical benefits (Refer Note 30.4.b)'],
                '(iv) Provision for other defined benefit plans (net) (give details) (Refer': ['(a) Provision for employee benefits:|(iv) Provision for other defined benefit plans (net) (give details) (Refer'],
                '(v) Provision for other employee benefits (give details)': ['(a) Provision for employee benefits:|(v) Provision for other employee benefits (give details)']
            },
            '(b) Provision - Others:': {
                '(i) Provision for premium payable on redemption of bonds (Refer Note 5': ['(b) Provision - Others:|(i) Provision for premium payable on redemption of bonds (Refer Note 5'],
                '(ii) Provision for estimated loss on derivatives': ['(b) Provision - Others:|(ii) Provision for estimated loss on derivatives'],
                '(iii) Provision for warranty (Refer Note 30.14)': ['(b) Provision - Others:|(iii) Provision for warranty (Refer Note 30.14)'],
                '(iv) Provision for estimated losses on onerous contracts (Refer Note 30.14)': ['(b) Provision - Others:|(iv) Provision for estimated losses on onerous contracts (Refer Note 30.14)'],
                '(v) Provision for other contingencies (Refer Note 30.14)': ['(b) Provision - Others:|(v) Provision for other contingencies (Refer Note 30.14)'],
                '(vi) Provision - others (give details)': ['(b) Provision - Others:|(vi) Provision - others (give details)']
            },
            # Universal Alias to catch the total if sub-items are not detailed
            'Total Long term provisions': ['Long term provisions']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 7: SHORT TERM BORROWINGS
    # ==============================================================================
    '7': {
        'title': 'Short term borrowings',
        'sub_items': {
            '(a) Loans repayable on demand': {
                'From banks - Secured': ['(a) Loans repayable on demand|From banks Secured'],
                'From banks - Unsecured': ['(a) Loans repayable on demand|From banks Unsecured'],
                'From other parties - Secured': ['(a) Loans repayable on demand|From other parties Secured'],
                'From other parties - Unsecured': ['(a) Loans repayable on demand|From other parties Unsecured']
            },
            '(b) Loans and advances from related parties @ (Refer Note 30.7)': {
                'Secured': ['(b) Loans and advances from related parties @ (Refer Note 30.7)|Secured'],
                'Unsecured': ['(b) Loans and advances from related parties @ (Refer Note 30.7)|Unsecured']
            },
            '(c) Deposits': {
                'Secured': ['(c) Deposits|Secured'],
                'Unsecured': ['(c) Deposits|Unsecured']
            },
            '(d) Other loans and advances (specify nature)': {
                'Secured': ['(d) Other loans and advances (specify nature)|Secured'],
                'Unsecured': ['(d) Other loans and advances (specify nature)|Unsecured']
            },
            '7.1 Notes:': {
                '(i) Details of security for the secured short-term borrowings:': {
                    'Loans repayable on demand from banks:': {
                        'XXX Bank': ['Loans repayable on demand from banks:|XXX Bank'],
                        'YYY Bank': ['Loans repayable on demand from banks:|YYY Bank']
                    },
                    'Loans repayable on demand from other parties:': {
                        'ABC Ltd.': ['Loans repayable on demand from other parties:|ABC Ltd.'],
                        'XYZ Ltd.': ['Loans repayable on demand from other parties:|XYZ Ltd.']
                    },
                    'Loans and advances from related parties:': {
                        'RP 1': ['Loans and advances from related parties:|RP 1'],
                        'RP 2': ['Loans and advances from related parties:|RP 2']
                    },
                    'Deposits:': {
                        'Public deposits': ['Deposits:|Public deposits'],
                        'Inter-corporate deposit 1': ['Deposits:|Inter-corporate deposit 1'],
                        'Inter-corporate deposit 2': ['Deposits:|Inter-corporate deposit 2']
                    },
                    'Other loans and advances:': {
                        'Loan 1': ['Other loans and advances:|Loan 1'],
                        'Advance 1': ['Other loans and advances:|Advance 1']
                    }
                }
            },
            '7.2 (ii) Details of short-term borrowings guaranteed by some of the directors or others:': {
                'Loans repayable on demand from banks': ['7.2 (ii) Details of short-term borrowings guaranteed...|Loans repayable on demand from banks'],
                'Loans repayable on demand from other parties': ['7.2 (ii) Details of short-term borrowings guaranteed...|Loans repayable on demand from other parties'],
                'Loans and advances from related parties': ['7.2 (ii) Details of short-term borrowings guaranteed...|Loans and advances from related parties'],
                'Deposits': ['7.2 (ii) Details of short-term borrowings guaranteed...|Deposits'],
                'Other loans and advances': ['7.2 (ii) Details of short-term borrowings guaranteed...|Other loans and advances']
            },
            '7.3 (iii) The Company has defaulted in repayment of loans and interest in respect of the following:': {
                'Loans repayable on demand from banks': {
                    'Principal': ['Loans repayable on demand from banks|Principal'],
                    'Interest': ['Loans repayable on demand from banks|Interest']
                },
                'Loans repayable on demand from other parties': {
                    'Principal': ['Loans repayable on demand from other parties|Principal'],
                    'Interest': ['Loans repayable on demand from other parties|Interest']
                },
                'Loans and advances from related parties': {
                    'Principal': ['Loans and advances from related parties|Principal'],
                    'Interest': ['Loans and advances from related parties|Interest']
                },
                'Deposits': {
                    'Principal': ['Deposits|Principal'],
                    'Interest': ['Deposits|Interest']
                },
                'Other loans and advances': {
                    'Principal': ['Other loans and advances|Principal'],
                    'Interest': ['Other loans and advances|Interest']
                }
            },
            # Universal Aliases for totals
            'Total Short term borrowings': ['Short term borrowings', 'Bank Overdraft']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 8: TRADE PAYABLES
    # ==============================================================================
    '8': {
        'title': 'Trade payables',
        'sub_items': {
            'Trade payables:': {
                'Acceptances': ['Trade payables:|Acceptances'],
                'Other than Acceptances': [
                    # Contextual alias from PDF
                    'Trade payables:|Other than Acceptances',
                    # Universal aliases
                    'Trade payables',
                    'Sundry Creditors'
                ]
            }
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 8: TRADE PAYABLES
    # ==============================================================================
    '8': {
        'title': 'Trade payables',
        'sub_items': {
            'Trade payables:': {
                'Acceptances': ['Trade payables:|Acceptances'],
                'Other than Acceptances': [
                    # Contextual alias from PDF
                    'Trade payables:|Other than Acceptances',
                    # Universal aliases
                    'Trade payables',
                    'Sundry Creditors'
                ]
            }
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 9: OTHER CURRENT LIABILITIES
    # ==============================================================================
    '9': {
        'title': 'Other current liabilities',
        'sub_items': {
            '(a) Current maturities of long-term debt (Refer Note (i) below)': ['(a) Current maturities of long-term debt (Refer Note (i) below)'],
            '(b) Interest accrued but not due on borrowings': ['(b) Interest accrued but not due on borrowings'],
            '(c) Interest accrued and due on borrowings': ['(c) Interest accrued and due on borrowings'],
            '(d) Income received in advance (Unearned revenue)': ['(d) Income received in advance (Unearned revenue)'],
            '(e) Unpaid dividends': ['(e) Unpaid dividends'],
            '(f) Application money received for allotment of securities and due for refund and interest accrued thereon #': ['(f) Application money received for allotment of securities and due for refund and interest accrued thereon #'],
            '(g) Other payables (Salaries and consultant fee)': ['(g) Other payables (Salaries and consultant fee)'],
            '(h) Statutory remittances (GST payable,TDS payable, PT payable and EPF payable) for March': ['(h) Statutory remittances (GST payable,TDS payable, PT payable and EPF payable) for March'],
            '(i) Payables on purchase of fixed assets': ['(i) Payables on purchase of fixed assets'],
            '(ii) Contractually reimbursable expenses': ['(ii) Contractually reimbursable expenses'],
            '(iii) Interest accrued on trade payables': ['(iii) Interest accrued on trade payables'],
            '(iv) Interest accrued on others': ['(iv) Interest accrued on others'],
            '(v) Trade / security deposits received': ['(v) Trade / security deposits received'],
            '(vi) Advances from customers': ['(vi) Advances from customers'],
            '(vii) Other (audit fee)': ['(vii) Other (audit fee)'],
            # Universal Aliases for totals
            'Total Other current liabilities': [
                'Other current liabilities',
                'Bills Payable',
                'Outstanding Expenses'
            ]
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 10: SHORT TERM PROVISIONS
    # ==============================================================================
    '10': {
        'title': 'Short term provisions',
        'sub_items': {
            '(a) Provision for employee benefits: @': {
                '(i) Provision for bonus': ['(a) Provision for employee benefits: @|(i) Provision for bonus'],
                '(ii) Provision for compensated absences': ['(a) Provision for employee benefits: @|(ii) Provision for compensated absences'],
                '(iii) Provision for gratuity (net) (Refer Note 30.4.b)': ['(a) Provision for employee benefits: @|(iii) Provision for gratuity (net) (Refer Note 30.4.b)'],
                '(iv) Provision for post-employment medical benefits (Refer Note 30.4.b)': ['(a) Provision for employee benefits: @|(iv) Provision for post-employment medical benefits (Refer Note 30.4.b)'],
                '(v) Provision for other defined benefit plans (net) (give details) (Refer Note 30.4.b)': ['(a) Provision for employee benefits: @|(v) Provision for other defined benefit plans (net) (give details) (Refer Note 30.4.b)'],
                '(vi) Provision for other employee benefits (give details)': ['(a) Provision for employee benefits: @|(vi) Provision for other employee benefits (give details)']
            },
            '(b) Provision - Others:': {
                '(i) Provision for tax (net)': ['(b) Provision - Others:|(i) Provision for tax (net)', 'provision for tax'],
                '(ii) Provision for premium payable on redemption of bonds (Refer Note 5 Long-term borrowings)': ['(b) Provision - Others:|(ii) Provision for premium payable on redemption of bonds (Refer Note 5 Long-term borrowings)'],
                '(iii) Provision for estimated loss on derivatives': ['(b) Provision - Others:|(iii) Provision for estimated loss on derivatives'],
                '(iv) Provision for warranty (Refer Note 30.14)': ['(b) Provision - Others:|(iv) Provision for warranty (Refer Note 30.14)'],
                '(v) Provision for estimated losses on onerous contracts (Refer Note 30.14)': ['(b) Provision - Others:|(v) Provision for estimated losses on onerous contracts (Refer Note 30.14)'],
                '(vi) Provision for other contingencies (Refer Note 30.14)': ['(b) Provision - Others:|(vi) Provision for other contingencies (Refer Note 30.14)'],
                '(vii) Provision for proposed equity dividend': ['(b) Provision - Others:|(vii) Provision for proposed equity dividend'],
                '(viii) Provision for proposed preference dividend': ['(b) Provision - Others:|(viii) Provision for proposed preference dividend'],
                '(ix) Provision for tax on proposed dividends': ['(b) Provision - Others:|(ix) Provision for tax on proposed dividends'],
                '(x) Provision for Audit Fees': ['(b) Provision - Others:|(x) Provision for Audit Fees'],
                '(xi)Provision for Accounting Fee': ['(b) Provision - Others:|(xi)Provision for Accounting Fee']
            },
            # Universal Alias for totals
            'Total Short term provisions': ['Short term provisions']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 11: FIXED ASSETS
    # ==============================================================================
    '11': {
        'title': 'Fixed Assets',
        'sub_items': {
            'Depreciation as per Income Tax Act, 1961 for the year ending March 31, 2025': {
                'Office Interiors': ['Depreciation as per Income Tax Act...|Office Interiors'],
                'Air Conditioners': ['Depreciation as per Income Tax Act...|Air Conditioners'],
                'Battery': ['Depreciation as per Income Tax Act...|Battery'],
                'CC TV Camera': ['Depreciation as per Income Tax Act...|CC TV Camera'],
                'Computers': ['Depreciation as per Income Tax Act...|Computers'],
                'Curtains': ['Depreciation as per Income Tax Act...|Curtains'],
                'Electronic Items': ['Depreciation as per Income Tax Act...|Electronic Items'],
                'Epson Printer': ['Depreciation as per Income Tax Act...|Epson Printer'],
                'Fan': ['Depreciation as per Income Tax Act...|Fan'],
                'Furniture': ['Depreciation as per Income Tax Act...|Furniture'],
                'Inverter': ['Depreciation as per Income Tax Act...|Inverter'],
                'Mobile Phone': ['Depreciation as per Income Tax Act...|Mobile Phone'],
                'Motor Vehicle': ['Depreciation as per Income Tax Act...|Motor Vehicle'],
                'Refridgerator': ['Depreciation as per Income Tax Act...|Refridgerator'],
                'Television': ['Depreciation as per Income Tax Act...|Television']
            },
            'Depreciation as per Companies Act Act': {
                'CCTV Camera': ['Depreciation as per Companies Act Act|CCTV Camera'],
                'Computers': ['Depreciation as per Companies Act Act|Computers'],
                'Air conditioners': ['Depreciation as per Companies Act Act|Air conditioners'],
                'Curtains': ['Depreciation as per Companies Act Act|Curtains'],
                'Electronic items': ['Depreciation as per Companies Act Act|Electronic items'],
                'Epson printer': ['Depreciation as per Companies Act Act|Epson printer'],
                'Fan': ['Depreciation as per Companies Act Act|Fan'],
                'Furniture': ['Depreciation as per Companies Act Act|Furniture'],
                'Invertor': ['Depreciation as per Companies Act Act|Invertor'],
                'Mobile phone': ['Depreciation as per Companies Act Act|Mobile phone'],
                'Television': ['Depreciation as per Companies Act Act|Television'],
                'Battery': ['Depreciation as per Companies Act Act|Battery'],
                'Office Interiors': ['Depreciation as per Companies Act Act|Office Interiors'],
                'Refridgerator': ['Depreciation as per Companies Act Act|Refridgerator'],
                'Office Interiors ': ['Depreciation as per Companies Act Act|Office Interiors '], # Note the space for the second entry
                'Motor Vehicle': ['Depreciation as per Companies Act Act|Motor Vehicle'],
                'Water Dispenser': ['Depreciation as per Companies Act Act|Water Dispenser'],
                'Water Filter': ['Depreciation as per Companies Act Act|Water Filter']
            },
            'Dep as per IT ACT': [
                'Dep as per IT ACT',
                'Depriciation for the year' # Universal Alias
            ],
            'Dep as per Comp': ['Dep as per Comp'],
            'Difference': ['Difference'],
            'Deferred Tax': ['Deferred Tax'],
            # Universal Aliases for totals
            'Total Fixed Assets': [
                'Fixed assets',
                'Land & Building',
                'Plant & Machinery',
                'Furniture & Fixtures',
                'Motor Vehicles'
            ]
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 12: NON CURRENT INVESTMENTS
    # ==============================================================================
    '12': {
        'title': 'Non current Investments',
        'sub_items': {
            'A. Investments (At cost): Trade @': {
                '(a) Investment in equity instruments (give details separately for fully / partly paid up instruments)': {
                    '(i) of subsidiaries': ['(a) Investment in equity instruments...|(i) of subsidiaries'],
                    '(ii) of associates': ['(a) Investment in equity instruments...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(a) Investment in equity instruments...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(a) Investment in equity instruments...|(iv) of controlled special purpose entities'],
                    '(v) of other entities': ['(a) Investment in equity instruments...|(v) of other entities']
                },
                '(b) Investment in preference shares (give details separately for fully / partly paid up shares)': {
                    '(i) of subsidiaries': ['(b) Investment in preference shares...|(i) of subsidiaries'],
                    '(ii) of associates': ['(b) Investment in preference shares...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(b) Investment in preference shares...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(b) Investment in preference shares...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(b) Investment in preference shares...|(v) of other entities (give details)']
                },
                '(c) Investment in debentures or bonds (give details separately for fully / partly paid up debentures / bonds)': {
                    '(i) of subsidiaries': ['(c) Investment in debentures or bonds...|(i) of subsidiaries'],
                    '(ii) of associates': ['(c) Investment in debentures or bonds...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(c) Investment in debentures or bonds...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(c) Investment in debentures or bonds...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(c) Investment in debentures or bonds...|(v) of other entities (give details)']
                },
                '(d) Investment in partnership firms (Refer Note below)': ['A. Investments (At cost): Trade @|(d) Investment in partnership firms (Refer Note below)'],
                '(e) Other non-current investments (specify nature)': ['A. Investments (At cost): Trade @|(e) Other non-current investments (specify nature)']
            },
            'B. Other investments': {
                '(a) Investment property (specify nature), (net off accumulated depreciation and impairment, if any)': ['B. Other investments|(a) Investment property (specify nature), (net off accumulated depreciation and impairment, if any)'],
                '(b) Investment in equity instruments (give details separately for fully / partly paid up instruments)': {
                    '(i) of subsidiaries': ['(b) Investment in equity instruments...|(i) of subsidiaries'],
                    '(ii) of associates': ['(b) Investment in equity instruments...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(b) Investment in equity instruments...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(b) Investment in equity instruments...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(b) Investment in equity instruments...|(v) of other entities (give details)']
                },
                '(c) Investment in preference shares (give details separately for fully / partly paid up shares)': {
                    '(i) of subsidiaries': ['(c) Investment in preference shares...|(i) of subsidiaries'],
                    '(ii) of associates': ['(c) Investment in preference shares...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(c) Investment in preference shares...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(c) Investment in preference shares...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(c) Investment in preference shares...|(v) of other entities (give details)']
                },
                '(d) Investment in government or trust securities': {
                    '(i) government securities': ['(d) Investment in government or trust securities|(i) government securities'],
                    '(ii) trust securities': ['(d) Investment in government or trust securities|(ii) trust securities']
                },
                '(e) Investment in debentures or bonds (give details separately for fully / partly paid up debentures / bonds)': {
                    '(i) of subsidiaries': ['(e) Investment in debentures or bonds...|(i) of subsidiaries'],
                    '(ii) of associates': ['(e) Investment in debentures or bonds...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(e) Investment in debentures or bonds...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(e) Investment in debentures or bonds...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(e) Investment in debentures or bonds...|(v) of other entities (give details)']
                },
                '(f) Investment in mutual funds (give details)': ['B. Other investments|(f) Investment in mutual funds (give details)'],
                '(g) Investment in partnership firms (Refer Note below)': ['B. Other investments|(g) Investment in partnership firms (Refer Note below)'],
                '(h) Other non-current investments (specify nature)': ['B. Other investments|(h) Other non-current investments (specify nature)']
            },
            'Summary of Investments': {
                'Less: Provision for diminution in value of investments': ['Less: Provision for diminution in value of investments'],
                'Aggregate amount of quoted investments': ['Aggregate amount of quoted investments'],
                'Aggregate market value of listed and quoted investments': ['Aggregate market value of listed and quoted investments'],
                'Aggregate value of listed but not quoted investments': ['Aggregate value of listed but not quoted investments'],
                'Aggregate amount of unquoted investments': ['Aggregate amount of unquoted investments']
            },
            # Universal Alias for totals
            'Total Non current Investments': ['Non current Investments', 'Investments']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 13: LONG TERM LOANS AND ADVANCES
    # ==============================================================================
    '13': {
        'title': 'Long term loans and advances',
        'sub_items': {
            '(a) Capital advances :': {
                'Secured, considered good': ['(a) Capital advances :|Secured, considered good'],
                'Unsecured, considered good': ['(a) Capital advances :|Unsecured, considered good'],
                'Doubtful': ['(a) Capital advances :|Doubtful'],
                'Less: Provision for doubtful advances': ['(a) Capital advances :|Less: Provision for doubtful advances']
            },
            '(b) Security deposits': {
                'Secured, considered good': ['(b) Security deposits|Secured, considered good'],
                'Unsecured, considered good': ['(b) Security deposits|Unsecured, considered good'],
                'Doubtful': ['(b) Security deposits|Doubtful'],
                'Less: Provision for doubtful deposits': ['(b) Security deposits|Less: Provision for doubtful deposits']
            },
            '(c) Loans and advances to related parties (give details @) (Refer note 30.7)': {
                'Secured, considered good': ['(c) Loans and advances to related parties...|Secured, considered good'],
                'Unsecured, considered good': ['(c) Loans and advances to related parties...|Unsecured, considered good'],
                'Doubtful': ['(c) Loans and advances to related parties...|Doubtful'],
                'Less: Provision for doubtful loans and advances': ['(c) Loans and advances to related parties...|Less: Provision for doubtful loans and advances']
            },
            '(d) Loans and advances to employees': {
                'Secured, considered good': ['(d) Loans and advances to employees|Secured, considered good'],
                'Unsecured, considered good': ['(d) Loans and advances to employees|Unsecured, considered good'],
                'Doubtful': ['(d) Loans and advances to employees|Doubtful'],
                'Less: Provision for doubtful loans and advances': ['(d) Loans and advances to employees|Less: Provision for doubtful loans and advances']
            },
            '(e) Prepaid expenses - Unsecured, considered good': ['(e) Prepaid expenses - Unsecured, considered good'],
            '(f) Advance income tax # (net of provisions ` _) (As at 31 March, 20X1 ` _) - Unsecured, considered good': ['(f) Advance income tax # (net of provisions...'],
            '(g) MAT credit entitlement # - Unsecured, considered good': ['(g) MAT credit entitlement # - Unsecured, considered good'],
            '(h) Balances with government authorities': {
                'Unsecured, considered good': ['(h) Balances with government authorities|Unsecured, considered good'],
                '(i) CENVAT credit receivable': ['(h) Balances with government authorities|(i) CENVAT credit receivable'],
                '(ii) VAT credit receivable': ['(h) Balances with government authorities|(ii) VAT credit receivable'],
                '(iii) Service Tax credit receivable': ['(h) Balances with government authorities|(iii) Service Tax credit receivable']
            },
            '(i) Other loans and advances (specify nature)': {
                'Secured, considered good': ['(i) Other loans and advances (specify nature)|Secured, considered good'],
                'Unsecured, considered good': ['(i) Other loans and advances (specify nature)|Unsecured, considered good'],
                'Doubtful': ['(i) Other loans and advances (specify nature)|Doubtful'],
                'Less: Provision for other doubtful loans and advances': ['(i) Other loans and advances (specify nature)|Less: Provision for other doubtful loans and advances']
            },
            'Note: Long-term loans and advances include amounts due from:': {
                'Directors *': ['Note: Long-term loans and advances...|Directors *'],
                'Other officers of the Company *': ['Note: Long-term loans and advances...|Other officers of the Company *'],
                'Firms in which any director is a partner (give details per firm)': ['Note: Long-term loans and advances...|Firms in which any director is a partner (give details per firm)'],
                'Private companies in which any director is a director or member (give details per company)': ['Note: Long-term loans and advances...|Private companies in which any director is a director or member (give details per company)']
            },
            # Universal Alias for totals
            'Total Long term loans and advances': ['Long term loans and advances']
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 14: OTHER NON CURRENT ASSETS
    # ==============================================================================
    '14': {
        'title': 'Other non current assets',
        'sub_items': {
            '(a) Long-term trade receivables # (including trade receivables on deferred credit terms) (Refer Note below)': {
                'Secured, considered good': ['(a) Long-term trade receivables...|Secured, considered good'],
                'Unsecured, considered good': ['(a) Long-term trade receivables...|Unsecured, considered good'],
                'Doubtful': ['(a) Long-term trade receivables...|Doubtful'],
                'Less: Provision for doubtful trade receivables': ['(a) Long-term trade receivables...|Less: Provision for doubtful trade receivables']
            },
            '(b) Unamortised expenses': {
                '(i) Ancillary borrowing costs': ['(b) Unamortised expenses|(i) Ancillary borrowing costs'],
                '(ii) Share issue expenses (where applicable)': ['(b) Unamortised expenses|(ii) Share issue expenses (where applicable)'],
                '(iii) Discount on shares (where applicable)': ['(b) Unamortised expenses|(iii) Discount on shares (where applicable)']
            },
            '(c) Accruals': {
                '(i) Interest accrued on deposits': ['(c) Accruals|(i) Interest accrued on deposits'],
                '(ii) Interest accrued on investments': ['(c) Accruals|(ii) Interest accrued on investments'],
                '(iii) Interest accrued on trade receivables': ['(c) Accruals|(iii) Interest accrued on trade receivables']
            },
            '(d) Others @': {
                '(i) Insurance claims': ['(d) Others @|(i) Insurance claims'],
                '(ii) Receivables on sale of fixed assets': ['(d) Others @|(ii) Receivables on sale of fixed assets'],
                '(iii) Contractually reimbursable expenses': ['(d) Others @|(iii) Contractually reimbursable expenses'],
                '(iv) Others (specify nature)': ['(d) Others @|(iv) Others (specify nature)']
            },
            'Note: Long-term trade receivables include debts due from:': {
                'Directors *': ['Note: Long-term trade receivables...|Directors *'],
                'Other officers of the Company *': ['Note: Long-term trade receivables...|Other officers of the Company *'],
                'Firms in which any director is a partner (give details per firm)': ['Note: Long-term trade receivables...|Firms in which any director is a partner (give details per firm)'],
                'Private companies in which any director is a director or member (give details per company)': ['Note: Long-term trade receivables...|Private companies in which any director is a director or member (give details per company)']
            },
            # Universal Alias for totals
            'Total Other non current assets': ['Other non current assets']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 15: CURRENT INVESTMENTS
    # ==============================================================================
    '15': {
        'title': 'Current Investments',
        'sub_items': {
            'A Current portion of long-term investments (At cost)': {
                '(a) Investment in preference shares (give details separately for fully / partly paid up shares)': ['A Current portion...|(a) Investment in preference shares...'],
                '(b) Investment in government or trust securities (give details)': ['A Current portion...|(b) Investment in government or trust securities...'],
                '(c) Investment in debentures or bonds (give details separately for fully / partly paid up debentures / bonds)': ['A Current portion...|(c) Investment in debentures or bonds...'],
                '(d) Investment in mutual funds (give details)': ['A Current portion...|(d) Investment in mutual funds...'],
                '(e) Other investments (specify nature)': ['A Current portion...|(e) Other investments (specify nature)'],
                'Less: Provision for diminution in value of current portion of long-term investments': ['A Current portion...|Less: Provision for diminution in value...']
            },
            'B Other current investments (At lower of cost and fair value, unless otherwise stated)': {
                '(a) Investment in equity instruments (give details separately for fully / partly paid up instruments)': {
                    '(i) of subsidiaries': ['(a) Investment in equity instruments...|(i) of subsidiaries'],
                    '(ii) of associates': ['(a) Investment in equity instruments...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(a) Investment in equity instruments...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(a) Investment in equity instruments...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(a) Investment in equity instruments...|(v) of other entities (give details)']
                },
                '(b) Investment in preference shares (give details separately for fully / partly paid up shares)': {
                    '(i) of subsidiaries': ['(b) Investment in preference shares...|(i) of subsidiaries'],
                    '(ii) of associates': ['(b) Investment in preference shares...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(b) Investment in preference shares...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(b) Investment in preference shares...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(b) Investment in preference shares...|(v) of other entities (give details)']
                },
                '(c) Investment in government or trust securities': {
                    '(i) government securities': ['(c) Investment in government or trust securities|(i) government securities'],
                    '(ii) trust securities': ['(c) Investment in government or trust securities|(ii) trust securities']
                },
                '(d) Investment in debentures or bonds (give details separately for fully / partly paid up debentures / bonds)': {
                    '(i) of subsidiaries': ['(d) Investment in debentures or bonds...|(i) of subsidiaries'],
                    '(ii) of associates': ['(d) Investment in debentures or bonds...|(ii) of associates'],
                    '(iii) of joint venture companies': ['(d) Investment in debentures or bonds...|(iii) of joint venture companies'],
                    '(iv) of controlled special purpose entities': ['(d) Investment in debentures or bonds...|(iv) of controlled special purpose entities'],
                    '(v) of other entities (give details)': ['(d) Investment in debentures or bonds...|(v) of other entities (give details)']
                },
                '(e) Investment in mutual funds (give details)': ['B Other current investments...|(e) Investment in mutual funds (give details)'],
                '(f) Investment in partnership firms (Refer Note (i) below)': ['B Other current investments...|(f) Investment in partnership firms (Refer Note (i) below)'],
                '(g) Other investments (specify nature)': ['B Other current investments...|(g) Other investments (specify nature)']
            },
            'Summary of Current Investments': {
                'Aggregate amount of quoted investments': ['Aggregate amount of quoted investments'],
                'Aggregate market value of listed and quoted investments': ['Aggregate market value of listed and quoted investments'],
                'Aggregate value of listed but not quoted investments': ['Aggregate value of listed but not quoted investments'],
                'Aggregate amount of unquoted investments': ['Aggregate amount of unquoted investments'],
                'Aggregate provision for diminution (write down) in the value of other current investments': ['Aggregate provision for diminution (write down) in the value of other current investments']
            },
            'Notes: (i) Other details relating to investment in partnership firms': {
                'Name of the firm 1': ['Notes: (i) Other details...|Name of the firm 1'],
                'Name of the firm 2': ['Notes: (i) Other details...|Name of the firm 2']
            },
            # Universal Alias for totals
            'Total Current Investments': ['Current Investments']
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 16: INVENTORIES
    # ==============================================================================
    '16': {
        'title': 'Inventories',
        'sub_items': {
            '(a) Raw materials': {
                'Raw materials': ['(a) Raw materials|Raw materials'],
                'Goods-in-transit': ['(a) Raw materials|Goods-in-transit']
            },
            '(b) Work-in-progress @ (Refer Note below)': {
                'Work-in-progress': ['(b) Work-in-progress @ (Refer Note below)|Work-in-progress'],
                'Goods-in-transit': ['(b) Work-in-progress @ (Refer Note below)|Goods-in-transit']
            },
            '(c) Finished goods (other than those acquired for trading)': {
                'Finished goods': ['(c) Finished goods (other than those acquired for trading)|Finished goods'],
                'Goods-in-transit': ['(c) Finished goods (other than those acquired for trading)|Goods-in-transit']
            },
            '(d) Stock-in-trade (acquired for trading)': {
                'Stock-in-trade': [
                    '(d) Stock-in-trade (acquired for trading)|Stock-in-trade',
                    'Stock/Inventory' # Universal Alias
                ],
                'Goods-in-transit': ['(d) Stock-in-trade (acquired for trading)|Goods-in-transit']
            },
            '(e) Stores and spares': {
                'Stores and spares': ['(e) Stores and spares|Stores and spares'],
                'Goods-in-transit': ['(e) Stores and spares|Goods-in-transit']
            },
            '(f) Loose tools': {
                'Loose tools': ['(f) Loose tools|Loose tools'],
                'Goods-in-transit': ['(f) Loose tools|Goods-in-transit']
            },
            '(g) Others (Specify nature)': {
                'Others': ['(g) Others (Specify nature)|Others'],
                'Goods-in-transit': ['(g) Others (Specify nature)|Goods-in-transit']
            },
            'Note: Details of inventory of work-in-progress': {
                'Product X1': ['Note: Details of inventory of work-in-progress|Product X1'],
                'Product Y1': ['Note: Details of inventory of work-in-progress|Product Y1'],
                'Product Z1': ['Note: Details of inventory of work-in-progress|Product Z1'],
                'Other items': ['Note: Details of inventory of work-in-progress|Other items']
            },
            # Universal Aliases for totals/common terms
            'Total Inventories': [
                'Inventories',
                'To Opening Stock',
                'By Closing Stock'
            ]
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 17: TRADE RECEIVABLES
    # ==============================================================================
    '17': {
        'title': 'Trade Receivables',
        'sub_items': {
            'Trade receivables outstanding for a period exceeding six months from the date they were due for payment #': {
                'Secured, considered good': ['Trade receivables outstanding...|Secured, considered good'],
                'Unsecured, considered good': ['Trade receivables outstanding...|Unsecured, considered good'],
                'Doubtful': ['Trade receivables outstanding...|Doubtful'],
                'Less: Provision for doubtful trade receivables': ['Trade receivables outstanding...|Less: Provision for doubtful trade receivables']
            },
            'Other Trade receivables': {
                'Secured, considered good': ['Other Trade receivables|Secured, considered good'],
                'Unsecured, considered good': ['Other Trade receivables|Unsecured, considered good'],
                'Doubtful': ['Other Trade receivables|Doubtful'],
                'Less: Provision for doubtful trade receivables': ['Other Trade receivables|Less: Provision for doubtful trade receivables']
            },
            # Universal Aliases for totals
            'Total Trade Receivables': [
                'Trade Receivables',
                'Sundry Debtors',
                'Bills Receivable'
            ]
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 18: CASH AND CASH EQUIVALENTS
    # ==============================================================================
    '18': {
        'title': 'Cash and cash equivalents',
        'sub_items': {
            '(a) Cash on hand': [
                '(a) Cash on hand',
                'Cash in Hand' # Universal Alias
            ],
            '(b) Cheques, drafts on hand': ['(b) Cheques, drafts on hand'],
            '(c) Balances with banks': {
                '(i) In current accounts': [
                    '(c) Balances with banks|(i) In current accounts',
                    'Cash at Bank' # Universal Alias
                ],
                '(ii) In EEFC accounts': ['(c) Balances with banks|(ii) In EEFC accounts'],
                '(iii) In deposit accounts (Refer Note (i) below)': ['(c) Balances with banks|(iii) In deposit accounts (Refer Note (i) below)'],
                '(iv) In earmarked accounts': {
                    '- Unpaid dividend accounts': ['(iv) In earmarked accounts|- Unpaid dividend accounts'],
                    '- Unpaid matured deposits': ['(iv) In earmarked accounts|- Unpaid matured deposits'],
                    '- Unpaid matured debentures': ['(iv) In earmarked accounts|- Unpaid matured debentures'],
                    '- Share application money received for allotment of securities and due for refund': ['(iv) In earmarked accounts|- Share application money received for allotment of securities and due for refund'],
                    '- Balances held as margin money or security against borrowings, guarantees and other': ['(iv) In earmarked accounts|- Balances held as margin money or security against borrowings, guarantees and other'],
                    '- Other earmarked accounts (specify) (Refer Note (ii) below)': ['(iv) In earmarked accounts|- Other earmarked accounts (specify) (Refer Note (ii) below)']
                }
            },
            '(d) Others (specify nature)': ['(d) Others (specify nature)'],
            # Universal Alias for totals
            'Total Cash and cash equivalents': ['Cash and cash equivalents']
        }
    },

        # ==============================================================================
    # CONFIGURATION FOR NOTE 19: SHORT TERM LOANS AND ADVANCES
    # ==============================================================================
    '19': {
        'title': 'Short term loans and advances',
        'sub_items': {
            '(a) Loans and advances to related parties (give details @) (Refer Note 30.7)': {
                '(i) Secured, considered good': ['(a) Loans and advances to related parties...|(i) Secured, considered good'],
                '(ii) Unsecured, considered good': ['(a) Loans and advances to related parties...|(ii) Unsecured, considered good'],
                '(iii) Doubtful': ['(a) Loans and advances to related parties...|(iii) Doubtful'],
                'Less: Provision for doubtful loans and advances': ['(a) Loans and advances to related parties...|Less: Provision for doubtful loans and advances']
            },
            '(b) Security deposits': {
                '(i) Secured, considered good': ['(b) Security deposits|(i) Secured, considered good'],
                '(ii) Unsecured, considered good': ['(b) Security deposits|(ii) Unsecured, considered good'],
                '(iii) Doubtful': ['(b) Security deposits|(iii) Doubtful'],
                'Less: Provision for doubtful deposits': ['(b) Security deposits|Less: Provision for doubtful deposits']
            },
            '(c) Loans and advances to employees': {
                '(i) Secured, considered good': ['(c) Loans and advances to employees|(i) Secured, considered good'],
                '(ii) Unsecured, considered good': ['(c) Loans and advances to employees|(ii) Unsecured, considered good'],
                '(iii) Doubtful': ['(c) Loans and advances to employees|(iii) Doubtful'],
                'Less: Provision for doubtful loans and advances': ['(c) Loans and advances to employees|Less: Provision for doubtful loans and advances']
            },
            '(d) Prepaid expenses - Unsecured, considered good (For e.g. Insurance premium, Annual maintenance contracts,': [
                '(d) Prepaid expenses - Unsecured, considered good (For e.g. Insurance premium, Annual maintenance contracts,',
                'Prepaid Expenses' # Universal Alias
            ],
            '(e) Balances with government authorities': {
                'Unsecured, considered good': ['(e) Balances with government authorities|Unsecured, considered good'],
                '(i) CENVAT credit receivable': ['(e) Balances with government authorities|(i) CENVAT credit receivable'],
                '(ii) VAT credit receivable': ['(e) Balances with government authorities|(ii) VAT credit receivable'],
                '(iii) Service Tax credit receivable': ['(e) Balances with government authorities|(iii) Service Tax credit receivable']
            },
            '(f) Inter-corporate deposits': {
                '(i) Secured, considered good': ['(f) Inter-corporate deposits|(i) Secured, considered good'],
                '(ii) Unsecured, considered good': ['(f) Inter-corporate deposits|(ii) Unsecured, considered good'],
                '(iii) Doubtful': ['(f) Inter-corporate deposits|(iii) Doubtful'],
                'Less: Provision for doubtful inter-corporate deposits': ['(f) Inter-corporate deposits|Less: Provision for doubtful inter-corporate deposits']
            },
            '(g) Others (specify nature)': {
                '(i) Secured, considered good': ['(g) Others (specify nature)|(i) Secured, considered good'],
                '(ii) Unsecured, considered good': ['(g) Others (specify nature)|(ii) Unsecured, considered good'],
                '(iii) Doubtful': ['(g) Others (specify nature)|(iii) Doubtful'],
                'Less: Provision for other doubtful loans and advances': ['(g) Others (specify nature)|Less: Provision for other doubtful loans and advances']
            },
            'Note: Short-term loans and advances include amounts due from:': {
                'Directors *': ['Note: Short-term loans and advances...|Directors *'],
                'Other officers of the Company *': ['Note: Short-term loans and advances...|Other officers of the Company *'],
                'Firms in which any director is a partner (give': ['Note: Short-term loans and advances...|Firms in which any director is a partner (give'],
                'Private companies in which any director is a': ['Note: Short-term loans and advances...|Private companies in which any director is a']
            },
            # Universal Alias for totals
            'Total Short term loans and advances': ['Short term loans and advances']
        }
    },


        # ==============================================================================
    # CONFIGURATION FOR NOTE 20: OTHER CURRENT ASSETS
    # ==============================================================================
    '20': {
        'title': 'Other current assets',
        'sub_items': {
            '(a) Unbilled revenue': ['(a) Unbilled revenue'],
            '(b) Unamortised expenses': {
                '(i) Ancillary borrowing costs': ['(b) Unamortised expenses|(i) Ancillary borrowing costs'],
                '(ii) Share issue expenses (where applicable)': ['(b) Unamortised expenses|(ii) Share issue expenses (where applicable)'],
                '(iii) Discount on shares (where applicable)': ['(b) Unamortised expenses|(iii) Discount on shares (where applicable)']
            },
            '(c) Accruals': {
                '(i) Interest accrued on deposits': ['(c) Accruals|(i) Interest accrued on deposits'],
                '(ii) Interest accrued on investments': ['(c) Accruals|(ii) Interest accrued on investments'],
                '(iii) Interest accrued on trade receivables': ['(c) Accruals|(iii) Interest accrued on trade receivables']
            },
            '(d) Advance Tax': {
                '(i) Income receivable from services': ['(d) Advance Tax|(i) Income receivable from services'],
                '(ii) Receivables on sale of fixed assets': ['(d) Advance Tax|(ii) Receivables on sale of fixed assets'],
                '(iii) Contractually reimbursable expenses': ['(d) Advance Tax|(iii) Contractually reimbursable expenses'],
                '(iv) TDS and other statutory payments': ['(d) Advance Tax|(iv) TDS and other statutory payments'],
                '(v) Input GST': ['(d) Advance Tax|(v) Input GST']
            },
            # Universal Alias for totals
            'Total Other current assets': ['Other current assets']
        }
    },




        # ==============================================================================
    # CONFIGURATION FOR NOTE 21: REVENUE FROM OPERATIONS
    # ==============================================================================
    '21': {
        'title': 'Revenue from Operations',
        'sub_items': {
            'Revenue from:': {
                'Sale of Services': [
                    'Revenue from:|Sale of Services',
                    'By Sales', # Universal Alias
                    'Revenue from operations' # Universal Alias
                ]
            }
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 22: OTHER INCOME
    # ==============================================================================
    '22': {
        'title': 'Other income',
        'sub_items': {
            'Miscellaneous Income': [
                'Miscellaneous Income',
                'By Miscellaneous Income' # Universal Alias
            ],
            'Refund on GST': ['Refund on GST'],
            # Universal Aliases for other P&L items
            'Interest Received': ['By Interest Received'],
            'Dividend Received': ['By Dividend Received'],
            'Commission Received': ['By Commission Received'],
            'Discount Received': ['By Discount Received'],
            'Bad Debts Recovered': ['By Bad Debts Recovered']
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 23: COST OF MATERIALS CONSUMED
    # ==============================================================================
    '23': {
        'title': 'Cost of Materials Consumed',
        'sub_items': {
            'Purchases': [
                'Purchases',
                'To Purchases' # Universal Alias
            ]
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 24: EMPLOYEE BENEFIT EXPENSES
    # ==============================================================================
    '24': {
        'title': 'Employee benefit expenses',
        'sub_items': {
            'Salaries and Wages': [
                'Salaries and Wages',
                'To Salaries', # Universal Alias
                'To Wages'     # Universal Alias
            ],
            'Contribution to provident and other funds': ['Contribution to provident and other funds'],
            'Gratuity Expenses': ['Gratuity Expenses'],
            'Staff welfare Expenses': ['Staff welfare Expenses']
        }
    },

    # ==============================================================================
    # CONFIGURATION FOR NOTE 25: FINANCE COSTS
    # ==============================================================================
    '25': {
        'title': 'Finance Costs',
        'sub_items': {
            'Interest on borrowings': [
                'Interest on borrowings',
                'To Interest Paid' # Universal Alias
            ],
            'Other Interest(Interest on Income Tax)': ['Other Interest(Interest on Income Tax)']
        }
    },



        # ==============================================================================
    # CONFIGURATION FOR NOTE 26: OTHER EXPENSES
    # ==============================================================================
    '26': {
        'title': 'Other expenses',
        'sub_items': {
            'Accounting Fee': ['Accounting Fee'],
            'Audit Fees': ['Audit Fees', 'To Audit Fees'],
            'Accomodation Charges': ['Accomodation Charges'],
            'Admin expenses': ['Admin expenses'],
            'Bank Charges': ['Bank Charges', 'To Bank Charges'],
            'Books and periodicals': ['Books and periodicals'],
            'Business Promotion': ['Business Promotion'],
            'Consultancy charges': ['Consultancy charges'],
            'Donations': ['Donations'],
            'Electrcity charges': ['Electrcity charges', 'To Electricity'],
            'Entertainment Expenses': ['Entertainment Expenses'],
            'EPFO charges': ['EPFO charges'],
            'Freight charges': ['Freight charges'],
            'GST Charges': ['GST Charges'],
            'Income Tax': ['Income Tax'],
            'Insurance': ['Insurance', 'To Insurance'],
            'Internet Charges': ['Internet Charges'],
            'Medical Insurance': ['Medical Insurance'],
            'ELD Annual Subscription': ['ELD Annual Subscription'],
            'Office expenses': ['Office expenses'],
            'Recruitment Expenses': ['Recruitment Expenses'],
            'Professional Tax': ['Professional Tax'],
            'Printing and stationary': ['Printing and stationary', 'To Printing & Stationery'],
            'Software Charges': ['Software Charges'],
            'Stamps and Postage': ['Stamps and Postage'],
            'Rent': ['Rent', 'To Rent'],
            'Subscription Charges': ['Subscription Charges'],
            'Web Hosting and Domain': ['Web Hosting and Domain'],
            'Vehicle Maintenance': ['Vehicle Maintenance'],
            'Travelling Expense': ['Travelling Expense'],
            'Telephone expenses': ['Telephone expenses', 'To Telephone'],
            'Repair and maintenance': ['Repair and maintenance', 'To Repairs & Maintenance'],
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
            'ComputerExpenses': ['ComputerExpenses'],
            'Commission Charges': ['Commission Charges'],
            'Allowances': ['Allowances'],
            'Other expenses': ['Other expenses'],
            'Vehicle Accessories': ['Vehicle Accessories'],
            'MCA Fee': ['MCA Fee'],
            'Round Off': ['Round Off'],
            # Universal Aliases for P&L items not explicitly listed above
            'Advertising': ['To Advertising'],
            'Bad Debts': ['To Bad Debts'],
            'Transportation': ['To Transportation']
        }
    }
} # <<< End of the main dictionary


# ==============================================================================
# MASTER TEMPLATE (DEFINITIVE VERSION AS PER PDF IMAGES)
# This template contains the final structure for the main financial statements.
# ==============================================================================

MASTER_TEMPLATE = {
    # ==============================================================================
    # BALANCE SHEET STRUCTURE
    # ==============================================================================
    "Balance Sheet": [
        ("Particulars", "Note", "As at March 31, 2025", "header_col"),
        ("I", "EQUITY AND LIABILITIES", None, "header"),
        ("1", "Shareholder's funds:", None, "sub_header"),
        ("(a)", "Share Capital", "1", "item"),
        ("(b)", "Reserves and surplus", "2", "item"),
        ("(c)", "Money received against share warrants", None, "item_no_note"),
        ("2", "Share application money pending for allotment", None, "sub_header"),
        ("3", "Non - current liabilities:", None, "sub_header"),
        ("(a)", "Long - term borrowings", "3", "item"),
        ("(b)", "Deferred tax liabilities (Net)", "4", "item"),
        ("(c)", "Other Long - term liabilities", "5", "item"),
        ("(d)", "Long - term provisions", "6", "item"),
        ("4", "Current liabilities", None, "sub_header"),
        ("(a)", "Short - term borrowings", "7", "item"),
        ("(b)", "Trade payables", "8", "item"),
        ("(c)", "Other current liabilities", "9", "item"),
        ("(d)", "Short - term provisions", "10", "item"),
        ("", "Total", ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], "total"),
        ("", "", None, "spacer"),
        ("II", "ASSETS", None, "header"),
        ("1", "Non - current assets:", None, "sub_header"),
        ("(a)", "Fixed assets", None, "item_no_note_sub"),
        ("", "(i) Tangible assets", "11", "item_sub"),
        ("", "(ii) Intangible assets", "11", "item_sub"),
        ("", "(iii) Capital work-in-progress", "11", "item_sub"),
        ("", "(iv) Intangible assets under development", None, "item_sub_no_note"),
        ("", "(v) Fixed assets held for sale", None, "item_sub_no_note"),
        ("(b)", "Non - current investments", "12", "item"),
        ("(c)", "Deferred tax assets (Net)", "4", "item"),
        ("(d)", "Long-term loans and advances", "13", "item"),
        ("(e)", "Other non-current assets", "14", "item"),
        ("2", "Current assets:", None, "sub_header"),
        ("(a)", "Current investments", "15", "item"),
        ("(b)", "Inventories", "16", "item"),
        ("(c)", "Trade receivables", "17", "item"),
        ("(d)", "Cash and cash equivalents", "18", "item"),
        ("(e)", "Short-term loans and advances", "19", "item"),
        ("(f)", "Other current assets", "20", "item"),
        ("", "Total", ["11", "12", "4", "13", "14", "15", "16", "17", "18", "19", "20"], "total")
    ],

    # ==============================================================================
    # PROFIT AND LOSS STATEMENT STRUCTURE
    # ==============================================================================
    "Profit and Loss": [
        ("Particulars", "Note", "As at March 31, 2025", "header_col"),
        ("1", "Revenue from operations", "21", "item"),
        ("2", "Other Income", "22", "item"),
        ("3", "Total Revenue (1+2)", ["21", "22"], "total"),
        ("", "", None, "spacer"),
        ("4", "Expenses:", None, "header"),
        ("(a)", "Cost of Materials Consumed", "23", "item_no_alpha"),
        ("(b)", "Employee benefit expenses", "24", "item_no_alpha"),
        ("(c)", "Finance Costs", "25", "item_no_alpha"),
        ("(d)", "Depreciation and amortization expenses", "11", "item_no_alpha"),
        ("(e)", "Other expenses", "26", "item_no_alpha"),
        ("", "Total Expenses", ["23", "24", "25", "11", "26"], "total"),
        ("", "", None, "spacer"),
        ("", "Profit before extraordinary items", None, "item_no_note"),
        ("", "Extraordinary Items/Prior period items", None, "item_no_note"),
        ("5", "Profit before tax", "PBT", "total"),
        ("", "", None, "spacer"),
        ("6", "A)Tax expense:", None, "header"),
        ("(1)", "Current tax", None, "item_no_note"),
        ("(2)", "Deferred tax", "4", "item_no_alpha"),
        ("7", "Profit/(Loss) for the period", "PAT", "total"),
        ("8", "Earnings per equity share", None, "item_no_note"),
    ]
}

