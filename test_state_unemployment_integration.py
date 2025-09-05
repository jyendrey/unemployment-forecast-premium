#!/usr/bin/env python3
"""
Test State Unemployment Data Integration
Tests the state-level unemployment data integration into the forecast system
"""

import json
from datetime import datetime

def test_state_unemployment_integration():
    """Test state unemployment data integration"""
    
    print("🧪 Testing State Unemployment Data Integration")
    print("="*80)
    
    # Test data for state unemployment analysis
    test_state_data = {
        "CAUR": {
            "description": "California Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 5.2},
                {"date": "2024-11-01", "value": 5.1},
                {"date": "2024-10-01", "value": 5.0}
            ]
        },
        "TXUR": {
            "description": "Texas Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.1},
                {"date": "2024-11-01", "value": 4.0},
                {"date": "2024-10-01", "value": 3.9}
            ]
        },
        "FLUR": {
            "description": "Florida Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 3.8},
                {"date": "2024-11-01", "value": 3.7},
                {"date": "2024-10-01", "value": 3.6}
            ]
        },
        "NYUR": {
            "description": "New York Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.5},
                {"date": "2024-11-01", "value": 4.4},
                {"date": "2024-10-01", "value": 4.3}
            ]
        },
        "PAUR": {
            "description": "Pennsylvania Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.8},
                {"date": "2024-11-01", "value": 4.7},
                {"date": "2024-10-01", "value": 4.6}
            ]
        },
        "ILUR": {
            "description": "Illinois Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.9},
                {"date": "2024-11-01", "value": 4.8},
                {"date": "2024-10-01", "value": 4.7}
            ]
        },
        "OHUR": {
            "description": "Ohio Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.2},
                {"date": "2024-11-01", "value": 4.1},
                {"date": "2024-10-01", "value": 4.0}
            ]
        },
        "GAUR": {
            "description": "Georgia Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 3.9},
                {"date": "2024-11-01", "value": 3.8},
                {"date": "2024-10-01", "value": 3.7}
            ]
        },
        "NCUR": {
            "description": "North Carolina Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.0},
                {"date": "2024-11-01", "value": 3.9},
                {"date": "2024-10-01", "value": 3.8}
            ]
        },
        "MIUR": {
            "description": "Michigan Unemployment Rate",
            "data": [
                {"date": "2024-12-01", "value": 4.6},
                {"date": "2024-11-01", "value": 4.5},
                {"date": "2024-10-01", "value": 4.4}
            ]
        }
    }
    
    print("📊 Test State Data Setup:")
    print(f"   • States: {len(test_state_data)}")
    
    # Simulate state unemployment analysis
    print("\n🔍 State Unemployment Analysis:")
    
    # Get latest unemployment rates for all states
    latest_rates = {}
    for state_id, data in test_state_data.items():
        if data['data']:
            latest_rates[state_id] = data['data'][0]['value']
    
    print(f"   • Latest rates collected: {len(latest_rates)} states")
    
    # Calculate statistics
    rates = list(latest_rates.values())
    avg_state_rate = sum(rates) / len(rates)
    min_rate = min(rates)
    max_rate = max(rates)
    rate_std = (sum((x - avg_state_rate) ** 2 for x in rates) / len(rates)) ** 0.5
    
    print(f"   • Average State Rate: {avg_state_rate:.2f}%")
    print(f"   • Min Rate: {min_rate:.2f}%")
    print(f"   • Max Rate: {max_rate:.2f}%")
    print(f"   • Standard Deviation: {rate_std:.2f}%")
    
    # Calculate coefficient of variation (dispersion measure)
    cv = rate_std / avg_state_rate if avg_state_rate > 0 else 0
    print(f"   • Coefficient of Variation: {cv:.3f}")
    
    # Determine regional dispersion level
    if cv > 0.3:
        dispersion_level = 'high'
        confidence_score = 0.8
    elif cv > 0.2:
        dispersion_level = 'moderate'
        confidence_score = 0.6
    else:
        dispersion_level = 'low'
        confidence_score = 0.4
    
    print(f"   • Regional Dispersion: {dispersion_level}")
    print(f"   • Confidence Score: {confidence_score}")
    
    # Identify outlier states
    outliers = []
    for state_id, rate in latest_rates.items():
        if abs(rate - avg_state_rate) > 2 * rate_std:
            outliers.append({
                'state': state_id,
                'rate': rate,
                'deviation': rate - avg_state_rate
            })
    
    print(f"   • Outlier States: {len(outliers)}")
    for outlier in outliers:
        print(f"     - {outlier['state']}: {outlier['rate']:.1f}% (deviation: {outlier['deviation']:+.1f}%)")
    
    # Calculate forecast adjustments
    print("\n🎯 Forecast Adjustments:")
    
    # State Unemployment Adjustment
    state_adjustment = 0.0
    
    # High dispersion suggests economic stress
    if dispersion_level == 'high':
        state_adjustment += 0.0005
    elif dispersion_level == 'moderate':
        state_adjustment += 0.0002
    
    # Outlier states with high unemployment suggest problems
    high_unemployment_outliers = [o for o in outliers if o['deviation'] > 1.0]
    if len(high_unemployment_outliers) > 3:  # More than 3 states significantly above average
        state_adjustment += 0.0003
    
    # Average state rate vs national rate comparison
    if avg_state_rate > 4.5:  # States averaging higher than 4.5%
        state_adjustment += 0.0002
    elif avg_state_rate < 3.8:  # States averaging lower than 3.8%
        state_adjustment -= 0.0002
    
    print(f"   • State Unemployment Adjustment: {state_adjustment:.4f}%")
    print(f"     - Dispersion Factor: {dispersion_level}")
    print(f"     - Outlier Factor: {len(high_unemployment_outliers)} high outliers")
    print(f"     - Average Rate Factor: {avg_state_rate:.1f}% vs 4.2% national")
    
    # Calculate confidence boost
    print("\n🚀 Confidence Boost:")
    
    # Base boost from state data availability
    state_boost = confidence_score * 0.6  # +0.2-0.5% boost
    
    # Additional boost for high dispersion (more informative)
    if dispersion_level == 'high':
        state_boost += 0.3
    elif dispersion_level == 'moderate':
        state_boost += 0.1
    
    print(f"   • State Data Boost: +{state_boost:.1f}%")
    print(f"     - Base Boost: {confidence_score * 0.6:.1f}%")
    print(f"     - Dispersion Bonus: {0.3 if dispersion_level == 'high' else 0.1 if dispersion_level == 'moderate' else 0:.1f}%")
    
    # Simulate forecast impact
    base_forecast = 4.2
    new_forecast = base_forecast + state_adjustment
    base_confidence = 95.0
    new_confidence = min(base_confidence + state_boost, 100.0)
    
    print(f"\n🎯 Forecast Impact:")
    print(f"   • Base Forecast: {base_forecast:.2f}%")
    print(f"   • New Forecast: {new_forecast:.2f}%")
    print(f"   • Change: {state_adjustment:+.4f}%")
    print(f"   • Base Confidence: {base_confidence:.1f}%")
    print(f"   • New Confidence: {new_confidence:.1f}%")
    print(f"   • Confidence Boost: +{state_boost:.1f}%")
    
    # Save test results
    test_results = {
        "test_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "state_analysis": {
            "states_analyzed": len(test_state_data),
            "average_state_rate": avg_state_rate,
            "rate_std": rate_std,
            "coefficient_variation": cv,
            "regional_dispersion": dispersion_level,
            "outliers": outliers,
            "confidence_score": confidence_score
        },
        "forecast_impact": {
            "adjustment": state_adjustment,
            "confidence_boost": state_boost,
            "base_forecast": base_forecast,
            "new_forecast": new_forecast,
            "base_confidence": base_confidence,
            "new_confidence": new_confidence
        }
    }
    
    with open('state_unemployment_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n✅ Test results saved to: state_unemployment_test_results.json")
    
    return test_results

if __name__ == "__main__":
    test_state_unemployment_integration()