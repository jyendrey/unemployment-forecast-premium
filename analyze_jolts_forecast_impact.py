#!/usr/bin/env python3
"""
Analyze JOLTS Data Impact on Forecast
Compares current default JOLTS data with new real JOLTS data
"""

import json
from datetime import datetime

def analyze_jolts_impact():
    """Analyze how new JOLTS data impacts the forecast"""
    
    print("🔍 JOLTS DATA FORECAST IMPACT ANALYSIS")
    print("=" * 60)
    
    # Current default JOLTS data (from forecast system)
    current_default = {
        'labor_market_tightness': 'balanced',
        'hiring_activity': 'moderate', 
        'confidence_score': 0.3
    }
    
    # New real JOLTS data (from our fetch)
    new_jolts_data = {
        'labor_market_tightness': 'very_tight',  # 1.35 ratio
        'hiring_activity': 'increasing',  # +0.8% trend
        'confidence_score': 0.85,  # High confidence due to very tight market
        'job_openings_ratio': 1.35,
        'hires_trend': '+0.8%',
        'openings_trend': '-2.4%',
        'quits_trend': 'stable'
    }
    
    print("📊 CURRENT vs NEW JOLTS DATA COMPARISON:")
    print("-" * 40)
    print(f"Labor Market Tightness:")
    print(f"  Current: {current_default['labor_market_tightness']}")
    print(f"  New:     {new_jolts_data['labor_market_tightness']} (1.35 ratio)")
    print()
    print(f"Hiring Activity:")
    print(f"  Current: {current_default['hiring_activity']}")
    print(f"  New:     {new_jolts_data['hiring_activity']} ({new_jolts_data['hires_trend']})")
    print()
    print(f"Confidence Score:")
    print(f"  Current: {current_default['confidence_score']}")
    print(f"  New:     {new_jolts_data['confidence_score']}")
    
    # Calculate forecast adjustments
    print("\n🔧 FORECAST ADJUSTMENT CALCULATIONS:")
    print("-" * 40)
    
    # Current adjustment calculation
    current_adjustment = current_default['confidence_score'] * 0.002 / 100
    print(f"Current JOLTS Adjustment: {current_adjustment:.6f}%")
    
    # New adjustment calculation  
    new_adjustment = new_jolts_data['confidence_score'] * 0.002 / 100
    print(f"New JOLTS Adjustment: {new_adjustment:.6f}%")
    
    adjustment_change = new_adjustment - current_adjustment
    print(f"Adjustment Change: {adjustment_change:+.6f}%")
    
    # Calculate confidence boost changes
    print("\n🚀 CONFIDENCE BOOST CALCULATIONS:")
    print("-" * 40)
    
    # Current confidence boost
    current_boost = current_default['confidence_score'] * 3.5
    print(f"Current JOLTS Confidence Boost: +{current_boost:.1f}%")
    
    # New confidence boost
    new_boost = new_jolts_data['confidence_score'] * 3.5
    print(f"New JOLTS Confidence Boost: +{new_boost:.1f}%")
    
    boost_change = new_boost - current_boost
    print(f"Confidence Boost Change: +{boost_change:.1f}%")
    
    # Interpret the impact
    print("\n📈 FORECAST IMPACT INTERPRETATION:")
    print("-" * 40)
    
    if new_jolts_data['job_openings_ratio'] > 1.2:
        market_interpretation = "Very tight labor market - supports lower unemployment"
        unemployment_direction = "DOWNWARD pressure"
    elif new_jolts_data['job_openings_ratio'] > 1.0:
        market_interpretation = "Tight labor market - supports lower unemployment"
        unemployment_direction = "DOWNWARD pressure"
    else:
        market_interpretation = "Balanced/loose labor market - neutral to higher unemployment"
        unemployment_direction = "NEUTRAL to UPWARD pressure"
    
    print(f"Labor Market Interpretation: {market_interpretation}")
    print(f"Unemployment Direction: {unemployment_direction}")
    
    # Analyze the mixed signals
    print(f"\nMixed Signals Analysis:")
    print(f"  • Job Openings: {new_jolts_data['openings_trend']} (potentially negative for unemployment)")
    print(f"  • Hires: {new_jolts_data['hires_trend']} (positive for unemployment)")
    print(f"  • Quits: {new_jolts_data['quits_trend']} (neutral)")
    
    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    print("-" * 40)
    
    if new_jolts_data['job_openings_ratio'] > 1.2 and new_jolts_data['hires_trend'].startswith('+'):
        assessment = "POSITIVE for unemployment forecast - tight market with increasing hires"
        impact_magnitude = "MODERATE"
    elif new_jolts_data['job_openings_ratio'] > 1.0:
        assessment = "SLIGHTLY POSITIVE for unemployment forecast - still tight market"
        impact_magnitude = "SMALL"
    else:
        assessment = "NEUTRAL to NEGATIVE for unemployment forecast - market loosening"
        impact_magnitude = "SMALL to MODERATE"
    
    print(f"Assessment: {assessment}")
    print(f"Impact Magnitude: {impact_magnitude}")
    print(f"Confidence Improvement: +{boost_change:.1f}%")
    
    # Specific forecast implications
    print(f"\n📊 SPECIFIC FORECAST IMPLICATIONS:")
    print("-" * 40)
    
    print(f"1. Unemployment Rate Direction:")
    if new_jolts_data['job_openings_ratio'] > 1.2:
        print(f"   → DOWNWARD pressure due to very tight labor market")
    else:
        print(f"   → NEUTRAL to slight upward pressure")
    
    print(f"\n2. Forecast Confidence:")
    print(f"   → INCREASES by +{boost_change:.1f}% due to high-quality JOLTS data")
    
    print(f"\n3. Labor Market Health:")
    if new_jolts_data['hires_trend'].startswith('+'):
        print(f"   → POSITIVE - hiring activity increasing")
    else:
        print(f"   → NEGATIVE - hiring activity declining")
    
    print(f"\n4. Worker Behavior:")
    if new_jolts_data['quits_trend'] == 'stable':
        print(f"   → CAUTIOUS - workers not changing jobs frequently")
    else:
        print(f"   → ACTIVE - workers changing jobs")
    
    return {
        'adjustment_change': adjustment_change,
        'confidence_boost_change': boost_change,
        'unemployment_direction': unemployment_direction,
        'assessment': assessment,
        'impact_magnitude': impact_magnitude
    }

def main():
    """Main analysis function"""
    impact = analyze_jolts_impact()
    
    print(f"\n" + "=" * 60)
    print(f"✅ JOLTS FORECAST IMPACT ANALYSIS COMPLETE")
    print(f"=" * 60)
    print(f"📈 Key Takeaway: {impact['assessment']}")
    print(f"🎯 Impact: {impact['impact_magnitude']} with {impact['confidence_boost_change']:+.1f}% confidence boost")
    print(f"📊 Unemployment Direction: {impact['unemployment_direction']}")

if __name__ == "__main__":
    main()