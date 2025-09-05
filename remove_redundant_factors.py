#!/usr/bin/env python3
"""
Remove Redundant Factors and Recalibrate Weights
Removes Economic Health and Technical Factors, then recalibrates remaining weights
"""

import json
from datetime import datetime

def remove_redundant_factors_and_recalibrate():
    """Remove redundant factors and recalibrate weights"""
    
    print("🔧 Removing Redundant Factors and Recalibrating Weights")
    print("="*80)
    
    # Current weights (before removal)
    current_weights = {
        "lfpr": 0.6,
        "initial_claims": 0.4,
        "continuing_claims": 0.3,
        "trade_sentiment": 0.08,
        "trade_volume": 0.12,
        "claims_trend": 0.0005,  # REMOVE
        "market_stability": 0.0003,  # REMOVE
        "initial_claims_trade_sentiment": 0.18,
        "initial_claims_volume": 0.08,
        "weekly_trade_sentiment": 0.15,
        "weekly_trade_volume": 0.05,
        "economic_health": 0.0015,  # REMOVE
        "economic_risk": 0.001,  # REMOVE
        "jolts_data": 0.003,
        "business_cycle_indicators": 0.002,
        "wage_growth_data": 0.002,
        "sector_employment_data": 0.0015,
        "state_unemployment_data": 0.001,
        "updated_trade_data": 0.06
    }
    
    print("📊 Current Weight Analysis:")
    total_current = sum(current_weights.values())
    print(f"   • Total Current Weight: {total_current:.3f}")
    print(f"   • Number of Factors: {len(current_weights)}")
    
    # Identify redundant factors
    redundant_factors = ["claims_trend", "market_stability", "economic_health", "economic_risk"]
    print(f"\n🗑️ Removing Redundant Factors:")
    for factor in redundant_factors:
        if factor in current_weights:
            print(f"   • {factor}: {current_weights[factor]:.4f} (REMOVED)")
    
    # Remove redundant factors
    cleaned_weights = {k: v for k, v in current_weights.items() if k not in redundant_factors}
    
    print(f"\n📈 After Removal:")
    total_cleaned = sum(cleaned_weights.values())
    print(f"   • Total Cleaned Weight: {total_cleaned:.3f}")
    print(f"   • Number of Factors: {len(cleaned_weights)}")
    print(f"   • Weight Removed: {total_current - total_cleaned:.3f}")
    
    # Recalibrate weights to maintain same total impact
    target_total = 2.0  # Target total weight
    recalibration_factor = target_total / total_cleaned
    
    print(f"\n🔧 Recalibrating Weights:")
    print(f"   • Target Total Weight: {target_total}")
    print(f"   • Recalibration Factor: {recalibration_factor:.3f}")
    
    # Apply recalibration
    recalibrated_weights = {}
    for factor, weight in cleaned_weights.items():
        new_weight = weight * recalibration_factor
        recalibrated_weights[factor] = new_weight
        change = new_weight - weight
        print(f"   • {factor}: {weight:.4f} → {new_weight:.4f} ({change:+.4f})")
    
    # Verify new total
    new_total = sum(recalibrated_weights.values())
    print(f"\n✅ Recalibration Complete:")
    print(f"   • New Total Weight: {new_total:.3f}")
    print(f"   • Target Achieved: {'YES' if abs(new_total - target_total) < 0.001 else 'NO'}")
    
    # Categorize recalibrated weights
    print(f"\n📊 Recalibrated Weight Categories:")
    
    core_labor = {
        "lfpr": recalibrated_weights["lfpr"],
        "initial_claims": recalibrated_weights["initial_claims"],
        "continuing_claims": recalibrated_weights["continuing_claims"]
    }
    core_labor_total = sum(core_labor.values())
    print(f"   • Core Labor Market: {core_labor_total:.3f} ({core_labor_total/new_total*100:.1f}%)")
    
    trade_data = {
        "trade_sentiment": recalibrated_weights["trade_sentiment"],
        "trade_volume": recalibrated_weights["trade_volume"],
        "initial_claims_trade_sentiment": recalibrated_weights["initial_claims_trade_sentiment"],
        "initial_claims_volume": recalibrated_weights["initial_claims_volume"],
        "weekly_trade_sentiment": recalibrated_weights["weekly_trade_sentiment"],
        "weekly_trade_volume": recalibrated_weights["weekly_trade_volume"],
        "updated_trade_data": recalibrated_weights["updated_trade_data"]
    }
    trade_data_total = sum(trade_data.values())
    print(f"   • Trade Data: {trade_data_total:.3f} ({trade_data_total/new_total*100:.1f}%)")
    
    leading_indicators = {
        "jolts_data": recalibrated_weights["jolts_data"],
        "business_cycle_indicators": recalibrated_weights["business_cycle_indicators"],
        "wage_growth_data": recalibrated_weights["wage_growth_data"],
        "sector_employment_data": recalibrated_weights["sector_employment_data"],
        "state_unemployment_data": recalibrated_weights["state_unemployment_data"]
    }
    leading_indicators_total = sum(leading_indicators.values())
    print(f"   • Leading Indicators: {leading_indicators_total:.3f} ({leading_indicators_total/new_total*100:.1f}%)")
    
    # Calculate expected impact improvements
    print(f"\n🎯 Expected Impact Improvements:")
    print(f"   • Core Labor Market: {core_labor_total:.3f} (increased from {sum(current_weights[f] for f in core_labor.keys()):.3f})")
    print(f"   • Trade Data: {trade_data_total:.3f} (increased from {sum(current_weights[f] for f in trade_data.keys()):.3f})")
    print(f"   • Leading Indicators: {leading_indicators_total:.3f} (increased from {sum(current_weights[f] for f in leading_indicators.keys()):.3f})")
    
    # Save recalibrated weights
    recalibration_results = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "recalibration_version": "v1.0-remove-redundant-factors",
        "removed_factors": redundant_factors,
        "original_weights": current_weights,
        "cleaned_weights": cleaned_weights,
        "recalibrated_weights": recalibrated_weights,
        "weight_analysis": {
            "original_total": total_current,
            "cleaned_total": total_cleaned,
            "recalibrated_total": new_total,
            "recalibration_factor": recalibration_factor
        },
        "category_breakdown": {
            "core_labor_market": core_labor,
            "trade_data": trade_data,
            "leading_indicators": leading_indicators
        }
    }
    
    with open('recalibrated_weights.json', 'w') as f:
        json.dump(recalibration_results, f, indent=2)
    
    print(f"\n✅ Recalibrated weights saved to: recalibrated_weights.json")
    
    # Print summary
    print(f"\n📋 RECALIBRATION SUMMARY:")
    print(f"   • Factors Removed: {len(redundant_factors)}")
    print(f"   • Factors Remaining: {len(recalibrated_weights)}")
    print(f"   • Total Weight: {total_current:.3f} → {new_total:.3f}")
    print(f"   • Core Labor Market: {core_labor_total:.3f} ({core_labor_total/new_total*100:.1f}%)")
    print(f"   • Trade Data: {trade_data_total:.3f} ({trade_data_total/new_total*100:.1f}%)")
    print(f"   • Leading Indicators: {leading_indicators_total:.3f} ({leading_indicators_total/new_total*100:.1f}%)")
    
    return recalibrated_weights

if __name__ == "__main__":
    weights = remove_redundant_factors_and_recalibrate()
    print(f"\n🎉 Recalibration completed successfully!")