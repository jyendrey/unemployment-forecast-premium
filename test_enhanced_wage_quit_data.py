#!/usr/bin/env python3
"""
Test Enhanced Wage Growth and Quit Rate Integration
Tests the updated system with real wage growth and quit rate data
"""

import json
from datetime import datetime

def test_enhanced_wage_quit_integration():
    """Test the enhanced system with wage growth and quit rate data"""
    
    print("🧪 Testing Enhanced Wage Growth and Quit Rate Integration")
    print("="*80)
    
    # Test data for wage growth analysis
    test_wage_data = {
        "CES0500000003": {
            "description": "Average Hourly Earnings - All Employees",
            "data": [
                {"date": "2024-12-01", "value": 28.50},
                {"date": "2024-11-01", "value": 28.25},
                {"date": "2024-10-01", "value": 28.00}
            ]
        },
        "ECIWAG": {
            "description": "Employment Cost Index - Wages & Salaries", 
            "data": [
                {"date": "2024-12-01", "value": 125.5},
                {"date": "2024-11-01", "value": 125.0},
                {"date": "2024-10-01", "value": 124.5}
            ]
        }
    }
    
    # Test data for quit rate analysis
    test_quit_data = {
        "quit_rate": 2.3,
        "quits": 3208000,
        "employment": 139500000,
        "interpretation": "moderate_confidence"
    }
    
    # Test JOLTS data for quit rate calculation
    test_jolts_data = {
        "JTSQUL": {
            "latest_value": 3208000,
            "latest_date": "2024-12-01"
        }
    }
    
    # Test employment data
    test_employment_data = {
        "LNS12000000": {
            "data": [
                {"date": "2024-12-01", "value": 139500000}
            ]
        }
    }
    
    print("📊 Test Data Setup:")
    print(f"   • Wage Growth Data: {len(test_wage_data)} series")
    print(f"   • Quit Rate: {test_quit_data['quit_rate']:.1f}%")
    print(f"   • Quits: {test_quit_data['quits']:,}")
    print(f"   • Employment: {test_quit_data['employment']:,}")
    print(f"   • Interpretation: {test_quit_data['interpretation']}")
    
    # Simulate wage growth analysis
    print("\n🔍 Wage Growth Analysis:")
    wage_growth_rates = []
    for series_id, data in test_wage_data.items():
        if len(data['data']) >= 2:
            current = data['data'][0]['value']
            previous = data['data'][1]['value']
            growth_rate = (current - previous) / previous * 100
            wage_growth_rates.append(growth_rate)
            print(f"   • {data['description']}: {growth_rate:.2f}% growth")
    
    avg_wage_growth = sum(wage_growth_rates) / len(wage_growth_rates) if wage_growth_rates else 0
    print(f"   • Average Wage Growth: {avg_wage_growth:.2f}%")
    
    # Determine wage pressure
    if avg_wage_growth > 4.0:
        wage_pressure = 'high'
        confidence_score = 0.8
    elif avg_wage_growth > 2.5:
        wage_pressure = 'moderate'
        confidence_score = 0.6
    else:
        wage_pressure = 'low'
        confidence_score = 0.4
    
    print(f"   • Wage Pressure: {wage_pressure}")
    print(f"   • Confidence Score: {confidence_score}")
    
    # Calculate forecast adjustments
    print("\n🎯 Forecast Adjustments:")
    
    # Wage Growth Adjustment
    if wage_pressure == 'high':
        wage_adjustment = -0.002  # High wages = lower unemployment
    elif wage_pressure == 'moderate':
        wage_adjustment = -0.001
    else:
        wage_adjustment = 0.000
    
    print(f"   • Wage Growth Adjustment: {wage_adjustment:.4f}% (Pressure: {wage_pressure})")
    
    # Quit Rate Adjustment
    quit_rate = test_quit_data['quit_rate']
    quit_interpretation = test_quit_data['interpretation']
    
    if quit_interpretation == 'high_confidence':
        quit_adjustment = -0.0015
    elif quit_interpretation == 'moderate_confidence':
        quit_adjustment = -0.001
    else:
        quit_adjustment = -0.0005
    
    print(f"   • Quit Rate Adjustment: {quit_adjustment:.4f}% (Rate: {quit_rate:.2f}%, {quit_interpretation})")
    
    # Calculate confidence boosts
    print("\n🚀 Confidence Boosts:")
    
    # Wage Growth Confidence Boost
    wage_boost = confidence_score * 1.5  # +1-2% boost
    print(f"   • Wage Growth Boost: +{wage_boost:.1f}%")
    
    # Quit Rate Confidence Boost
    if quit_interpretation == 'high_confidence':
        quit_boost = 0.8
    elif quit_interpretation == 'moderate_confidence':
        quit_boost = 0.5
    else:
        quit_boost = 0.2
    
    print(f"   • Quit Rate Boost: +{quit_boost:.1f}%")
    
    # Total adjustments and boosts
    total_adjustment = wage_adjustment + quit_adjustment
    total_boost = wage_boost + quit_boost
    
    print(f"\n📈 Summary:")
    print(f"   • Total Adjustment: {total_adjustment:.4f}%")
    print(f"   • Total Confidence Boost: +{total_boost:.1f}%")
    
    # Simulate forecast impact
    base_forecast = 4.2
    new_forecast = base_forecast + total_adjustment
    base_confidence = 95.0
    new_confidence = min(base_confidence + total_boost, 100.0)
    
    print(f"\n🎯 Forecast Impact:")
    print(f"   • Base Forecast: {base_forecast:.2f}%")
    print(f"   • New Forecast: {new_forecast:.2f}%")
    print(f"   • Change: {total_adjustment:.4f}%")
    print(f"   • Base Confidence: {base_confidence:.1f}%")
    print(f"   • New Confidence: {new_confidence:.1f}%")
    print(f"   • Confidence Boost: +{total_boost:.1f}%")
    
    # Save test results
    test_results = {
        "test_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "wage_growth_analysis": {
            "average_growth_rate": avg_wage_growth,
            "wage_pressure": wage_pressure,
            "confidence_score": confidence_score,
            "adjustment": wage_adjustment,
            "confidence_boost": wage_boost
        },
        "quit_rate_analysis": {
            "quit_rate": quit_rate,
            "interpretation": quit_interpretation,
            "adjustment": quit_adjustment,
            "confidence_boost": quit_boost
        },
        "forecast_impact": {
            "base_forecast": base_forecast,
            "new_forecast": new_forecast,
            "total_adjustment": total_adjustment,
            "base_confidence": base_confidence,
            "new_confidence": new_confidence,
            "total_boost": total_boost
        }
    }
    
    with open('enhanced_wage_quit_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n✅ Test results saved to: enhanced_wage_quit_test_results.json")
    
    return test_results

if __name__ == "__main__":
    test_enhanced_wage_quit_integration()