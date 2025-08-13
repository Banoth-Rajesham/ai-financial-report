# agents/agent_4_validator.py

def data_validation_agent(aggregated_data):
    """
    AGENT 4: Performs automated checks on the aggregated data.
    Returns a list of warning messages. An empty list means success.
    """
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

        # Accounting Equation: Assets = Liabilities + Equity
        final_liabilities_equity = total_equity + total_liabilities + deferred_tax
        final_assets = total_assets + deferred_tax

        # We allow a small tolerance (e.g., 5.0) for rounding differences
        if abs(final_assets - final_liabilities_equity) > 5.0:
            warnings.append(
                f"CRITICAL ({year_label}): Accounting equation out of balance! "
                f"Assets ({final_assets:,.2f}) != Liabilities + Equity ({final_liabilities_equity:,.2f})"
            )

    if not warnings:
        print("✅ Validation PASSED: All checks are clear.")
    else:
        print("⚠️  Validation FINISHED with warnings.")

    return warnings
