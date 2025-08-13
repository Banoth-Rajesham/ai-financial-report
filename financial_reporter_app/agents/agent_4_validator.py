# ==============================================================================
# FILE: agents/agent_4_validator.py
# ==============================================================================

def data_validation_agent(aggregated_data):
    """Performs automated checks and returns a list of warnings."""
    print("\n--- Agent 4 (Data Validation): Checking data integrity... ---")
    warnings = []
    for year in ['CY', 'PY']:
        year_label = "2025" if year == 'CY' else "2024"
        get_total = lambda key: aggregated_data.get(key, {}).get('total', {}).get(year, 0)
        
        equity_notes = ['1', '2']
        liability_notes = ['3', '5', '6', '7', '8', '9', '10']
        asset_notes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        
        deferred_tax = get_total('4')
        
        total_equity = sum(get_total(n) for n in equity_notes)
        total_liabilities = sum(get_total(n) for n in liability_notes)
        total_assets = sum(get_total(n) for n in asset_notes)

        # Handle DTA/DTL correctly
        final_le = total_equity + total_liabilities + (deferred_tax if deferred_tax > 0 else 0)
        final_a = total_assets + (deferred_tax if deferred_tax < 0 else 0)

        if abs(final_a - final_le) > 100.0:
            warnings.append(f"CRITICAL ({year_label}): Balance Sheet out of balance! Assets ({final_a:,.2f}) != L+E ({final_le:,.2f}) [Diff: {abs(final_a-final_le):,.2f}]")
    
    if not warnings:
        print("✅ Validation PASSED.")
    else:
        print("⚠️  Validation FINISHED with warnings.")
    
    return warnings
