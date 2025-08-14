# ==============================================================================
# FILE: config.py (DEFINITIVE, FULLY CORRECTED VERSION)
# ==============================================================================

# This version has been fully updated with explicit contextual keys ("Header|Particular")
# for every item to ensure an exact match with the data from Agent 1.

NOTES_STRUCTURE_AND_MAPPING = {
    '1': {
        'title': 'Share Capital',
        'sub_items': {
            'Authorised share capital': {
                'Number of shares': ['Authorised share capital|Number of shares'],
                'Equity shares of Rs. 10 each': ['Authorised share capital|Equity shares of Rs. 10 each']
            },
            'Issued, subscribed and fully paid up capital': {
                'Number of shares': ['Issued, subscribed and fully paid up capital|Number of shares'],
                'Equity shares of Rs. 10 each': ['Issued, subscribed and fully paid up capital|Equity shares of Rs. 10 each']
            },
            'Issued, subscribed and Partly up capital': {
                'Number of shares': ['Issued, subscribed and Partly up capital|Number of shares'],
                'Equity shares of Rs.10 each fully paid up.': ['Issued, subscribed and Partly up capital|Equity shares of Rs.10 each fully paid up.']
            },
            '1.1 Reconciliation of number of shares': {
                'Equity shares at the beginning of the year': ['1.1 Reconciliation of number of shares|Equity shares at the beginning of the year'],
                'Add: Additions during the year': ['1.1 Reconciliation of number of shares|Add: Additions during the year'],
                'Ded: Deductions during the year': ['1.1 Reconciliation of number of shares|Ded: Deductions during the year'],
                'Balance at the end of the year': ['1.1 Reconciliation of number of shares|Balance at the end of the year']
            },
            '1.2 Details of share held by shareholders holding more than 5%': {
                'M A Waheed Khan': ['1.2 Details of share held by shareholders holding more than 5%|M A Waheed Khan'],
                'M A Qhuddus Khan': ['1.2 Details of share held by shareholders holding more than 5%|M A Qhuddus Khan'],
                'M A Khadir Khan Asif': ['1.2 Details of share held by shareholders holding more than 5%|M A Khadir Khan Asif'],
                'M A Rauf Khan': ['1.2 Details of share held by shareholders holding more than 5%|M A Rauf Khan']
            }
        }
    },
    '2': {
        'title': 'Reserve and surplus',
        'sub_items': {
            '2.1 Capital reserve': {
                'Balance at the beginning of the year': ['2.1 Capital reserve|Balance at the beginning of the year'],
                'Add: Additions during the year': ['2.1 Capital reserve|Add: Additions during the year'],
                'Less: Utilized/transferred during the year': ['2.1 Capital reserve|Less: Utilized/transferred during the year'],
                'Balance at the end of the year': ['2.1 Capital reserve|Balance at the end of the year']
            },
            '2.2 Securities premium account': {
                'Balance at the beginning of the year': ['2.2 Securities premium account|Balance at the beginning of the year'],
                'Add: Premium on shares issued during the year': ['2.2 Securities premium account|Add: Premium on shares issued during the year'],
                'Less: Utilising during the year for': {
                    'Issuing bonus shares': ['Less: Utilising during the year for|Issuing bonus shares'],
                    'Writing off preliminary expenses': ['Less: Utilising during the year for|Writing off preliminary expenses'],
                    'Writing off shares/debentures issue expenses': ['Less: Utilising during the year for|Writing off shares/debentures issue expenses'],
                    'Premium on redemption of redeemable preference shares/debentures': ['Less: Utilising during the year for|Premium on redemption of redeemable preference shares/debentures'],
                    'Buy back of shares': ['Less: Utilising during the year for|Buy back of shares'],
                    'Others': ['Less: Utilising during the year for|Others']
                },
                'Balance at the end of the year': ['2.2 Securities premium account|Balance at the end of the year']
            },
            '2.3 Shares options outstanding account': {
                'Balance at the beginning of the year': ['2.3 Shares options outstanding account|Balance at the beginning of the year'],
                'Add: Amounts recorded on grants/modifications/cancellations': ['2.3 Shares options outstanding account|Add: Amounts recorded on grants/modifications/cancellations'],
                'Less: Written back to Statement of Profit and Loss': ['2.3 Shares options outstanding account|Less: Written back to Statement of Profit and Loss'],
                'Transferred to Securities premium account': ['2.3 Shares options outstanding account|Transferred to Securities premium account'],
                'Less: Deferred stock compensation expense': ['2.3 Shares options outstanding account|Less: Deferred stock compensation expense'],
                'Balance at the end of the year': ['2.3 Shares options outstanding account|Balance at the end of the year']
            },
            '2.4 General reserve': {
                'Balance at the beginning of the year': ['2.4 General reserve|Balance at the beginning of the year'],
                'Add: Transferred from surplus in Statement of Profit and Loss': ['2.4 General reserve|Add: Transferred from surplus in Statement of Profit and Loss'],
                'Less: Utilised / transferred during the year for': {
                    'Issuing bonus shares': ['Less: Utilised / transferred during the year for|Issuing bonus shares'],
                    'Others': ['Less: Utilised / transferred during the year for|Others']
                },
                'Balance at the end of the year': ['2.4 General reserve|Balance at the end of the year']
            },
            '2.5 Hedging reserve': {
                'Balance at the beginning of the year': ['2.5 Hedging reserve|Balance at the beginning of the year'],
                'Add / (Less): Effect of foreign exchange rate variations': ['2.5 Hedging reserve|Add / (Less): Effect of foreign exchange rate variations'],
                'Add / (Less): Transferred to Statement of Profit and Loss': ['2.5 Hedging reserve|Add / (Less): Transferred to Statement of Profit and Loss'],
                'Balance at the end of the year': ['2.5 Hedging reserve|Balance at the end of the year']
            },
            '2.6 Surplus / (Deficit) in Statement of Profit and Loss': {
                'Balance at the beginning of the year': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Balance at the beginning of the year'],
                'Add: Profit / (Loss) for the year': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Add: Profit / (Loss) for the year'],
                'Add: Amounts transferred from': {
                    'General reserve': ['Add: Amounts transferred from|General reserve'],
                    'Other reserves': ['Add: Amounts transferred from|Other reserves']
                },
                'Less: Interim dividend': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Less: Interim dividend'],
                'Dividends proposed to be distributed': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Dividends proposed to be distributed'],
                'Tax on dividend': ['2.6 Surplus / (Deficit) in Statement of Profit and Loss|Tax on dividend'],
                'Less: Transferred to': {
                    'General reserve': ['Less: Transferred to|General reserve'],
                    'Capital redemption reserve': ['Less: Transferred to|Capital redemption reserve'],
                    'Debenture redemption reserve': ['Less: Transferred to|Debenture redemption reserv
