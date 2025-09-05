#!/usr/bin/env python3
"""
Update Base Rate with Optimized Weights
Incorporates the optimized weights directly into the base forecast calculation
"""

import json
from datetime import datetime

def update_base_rate_with_weights():
    """Update the base rate to incorporate optimized weights"""
    
    print("🔧 Updating Base Rate with Optimized Weights")
    print("="*80)
    
    # Load optimized weights
    try:
        with open('optimized_forecast_weights.json', 'r') as f:
            weight_data = json.load(f)
        optimized_weights = weight_data['optimized_weights']
        print("✅ Loaded optimized weights")
    except FileNotFoundError:
        print("❌ Optimized weights file not found. Run optimize_forecast_weights.py first.")
        return None
    
    # Current base rate
    current_base_rate = 4.2
    print(f"📊 Current Base Rate: {current_base_rate}%")
    
    # Calculate weighted base rate adjustments
    print("\n🔍 Calculating Weighted Base Rate Adjustments:")
    
    # Core Labor Market Factors (most reliable)
    lfpr_weight = optimized_weights['lfpr']
    initial_claims_weight = optimized_weights['initial_claims']
    continuing_claims_weight = optimized_weights['continuing_claims']
    
    # Trade Data Factors (market sentiment)
    trade_sentiment_weight = optimized_weights['trade_sentiment']
    trade_volume_weight = optimized_weights['trade_volume']
    initial_claims_trade_weight = optimized_weights['initial_claims_trade_sentiment']
    initial_claims_volume_weight = optimized_weights['initial_claims_volume']
    weekly_trade_sentiment_weight = optimized_weights['weekly_trade_sentiment']
    weekly_trade_volume_weight = optimized_weights['weekly_trade_volume']
    updated_trade_weight = optimized_weights['updated_trade_data']
    
    # Leading Indicators (forward-looking)
    jolts_weight = optimized_weights['jolts_data']
    business_cycle_weight = optimized_weights['business_cycle_indicators']
    wage_growth_weight = optimized_weights['wage_growth_data']
    sector_employment_weight = optimized_weights['sector_employment_data']
    state_unemployment_weight = optimized_weights['state_unemployment_data']
    
    # Economic Health Factors
    economic_health_weight = optimized_weights['economic_health']
    economic_risk_weight = optimized_weights['economic_risk']
    
    # Technical Factors (least reliable)
    claims_trend_weight = optimized_weights['claims_trend']
    market_stability_weight = optimized_weights['market_stability']
    
    # Calculate weighted base rate
    # Core labor market factors get the highest influence on base rate
    core_labor_influence = (lfpr_weight + initial_claims_weight + continuing_claims_weight) / 3
    trade_influence = (trade_sentiment_weight + trade_volume_weight + initial_claims_trade_weight + 
                     initial_claims_volume_weight + weekly_trade_sentiment_weight + 
                     weekly_trade_volume_weight + updated_trade_weight) / 7
    leading_indicators_influence = (jolts_weight + business_cycle_weight + wage_growth_weight + 
                                  sector_employment_weight + state_unemployment_weight) / 5
    economic_health_influence = (economic_health_weight + economic_risk_weight) / 2
    technical_influence = (claims_trend_weight + market_stability_weight) / 2
    
    print(f"   • Core Labor Market Influence: {core_labor_influence:.3f}")
    print(f"   • Trade Data Influence: {trade_influence:.3f}")
    print(f"   • Leading Indicators Influence: {leading_indicators_influence:.3f}")
    print(f"   • Economic Health Influence: {economic_health_influence:.3f}")
    print(f"   • Technical Influence: {technical_influence:.3f}")
    
    # Calculate weighted base rate adjustment
    # The base rate should reflect the most reliable indicators
    base_rate_adjustment = 0.0
    
    # Core labor market gets primary influence
    base_rate_adjustment += core_labor_influence * 0.1  # 10% of influence
    
    # Trade data gets secondary influence
    base_rate_adjustment += trade_influence * 0.05  # 5% of influence
    
    # Leading indicators get tertiary influence
    base_rate_adjustment += leading_indicators_influence * 0.02  # 2% of influence
    
    # Economic health gets minimal influence
    base_rate_adjustment += economic_health_influence * 0.01  # 1% of influence
    
    # Technical factors get minimal influence
    base_rate_adjustment += technical_influence * 0.005  # 0.5% of influence
    
    # Calculate new weighted base rate
    weighted_base_rate = current_base_rate + base_rate_adjustment
    
    print(f"\n📈 Base Rate Calculation:")
    print(f"   • Current Base Rate: {current_base_rate}%")
    print(f"   • Weighted Adjustment: {base_rate_adjustment:+.4f}%")
    print(f"   • New Weighted Base Rate: {weighted_base_rate:.4f}%")
    
    # Create updated configuration
    updated_config = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "base_rate_update": "v1.0-weighted-base-rate",
        "current_base_rate": current_base_rate,
        "weighted_base_rate": weighted_base_rate,
        "base_rate_adjustment": base_rate_adjustment,
        "influence_weights": {
            "core_labor_market": core_labor_influence,
            "trade_data": trade_influence,
            "leading_indicators": leading_indicators_influence,
            "economic_health": economic_health_influence,
            "technical_factors": technical_influence
        },
        "optimized_weights": optimized_weights
    }
    
    # Save updated configuration
    with open('weighted_base_rate_config.json', 'w') as f:
        json.dump(updated_config, f, indent=2)
    
    print(f"\n✅ Weighted base rate configuration saved to: weighted_base_rate_config.json")
    
    # Print summary
    print(f"\n📋 WEIGHTED BASE RATE SUMMARY:")
    print(f"   • Original Base Rate: {current_base_rate}%")
    print(f"   • Weighted Base Rate: {weighted_base_rate:.4f}%")
    print(f"   • Adjustment: {base_rate_adjustment:+.4f}%")
    print(f"   • Primary Influence: Core Labor Market ({core_labor_influence:.3f})")
    print(f"   • Secondary Influence: Trade Data ({trade_influence:.3f})")
    print(f"   • Tertiary Influence: Leading Indicators ({leading_indicators_influence:.3f})")
    
    return updated_config

if __name__ == "__main__":
    config = update_base_rate_with_weights()
    if config:
        print(f"\n🎉 Base rate update completed successfully!")
    else:
        print(f"\n💥 Base rate update failed!")