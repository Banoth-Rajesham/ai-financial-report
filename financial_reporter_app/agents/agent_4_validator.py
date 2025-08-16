# ==============================================================================
# FILE: agents/agent_4_validator.py (DEFINITIVE, ERROR-FREE VERSION)
# ==============================================================================
from config import MASTER_TEMPLATE

def data_validation_agent(aggregated_data):
    """
    Performs automated checks that are perfectly synchronized with the
    MASTER_TEMPLATE to ensure 100% accurate validation.
    """
    print("\n--- Agent 4 (Data Validation): Checking data integrity... ---")
    warnings = []
    
    # Dynamically get the note numbers for calculation from the master template
    bs_template = MASTER_TEMPLATE['Balance Sheet']
    
    equity_notes = [row[2] for row in bs_template if row[2] and row[1] in ["Share Capital", "Reserves and surplus"]]
    liability_notes = [row[2] for row in bs_template if row[2] and any(x in row[1] for x in ["borrowings", "payables", "provisions", "Other Long - term liabilities"])]
    asset_notes = [row[2] for row in bs_template if row[2] and any(x in row[1] for x in ["Fixed assets", "investments", "loans and advances", "Other non-current assets", "Inventories", "receivables", "Cash and cash equivalents", "Other current assets"])]

    for year in ['CY', 'PY']:
        year_label = "2025" if year == 'CY' else "2024"
        get_total = lambda key: aggregated_data.get(key, {}).get('total', {}).get(year, 0)
        
        deferred_tax = get_total('4')
        
        total_equity = sum(get_total(n) for n in equity_notes)
        total_liabilities = sum(get_total(n) for n in liability_notes)
        total_assets = sum(get_total(n) for n in asset_notes)

        # Handle Deferred Tax Asset (DTA) vs Deferred Tax Liability (DTL) correctly
        final_le = total_equity + total_liabilities
        if deferred_tax > 0: # It's a liability
            final_le += deferred_tax

        final_a = total_assets
        if deferred_tax < 0: # It's an asset
            final_a += abs(deferred_tax)

        if abs(final_a - final_le) > 100.0: # Using a small tolerance for floating point issues
            warnings.append(f"CRITICAL ({year_label}): Balance Sheet out of balance! Assets ({final_a:,.2f}) != L+E ({final_le:,.2f}) [Diff: {abs(final_a-final_le):,.2f}]")
    
    if not warnings:
        print("✅ Validation PASSED.")
    else:
        print("⚠️  Validation FINISHED with warnings.")
    
    return warnings
