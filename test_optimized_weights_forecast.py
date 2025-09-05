#!/usr/bin/env python3
"""
Test Optimized Weights Forecast
Tests the forecast with the newly optimized weights
"""

import json
import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.getcwd())

def test_optimized_weights_forecast():
    """Test the forecast with optimized weights"""
    
    print("🧪 Testing Optimized Weights Forecast")
    print("="*80)
    
    try:
        # Import our enhanced forecast system
        from final_enhanced_forecast import FinalEnhancedUnemploymentForecaster
        
        # Initialize the forecast system
        print("🔄 Initializing Enhanced Unemployment Forecast System...")
        forecast_system = FinalEnhancedUnemploymentForecaster()
        
        # Load current leading indicators data
        print("🔄 Loading current leading indicators data...")
        try:
            with open('comprehensive_economic_analysis.json', 'r') as f:
                leading_indicators = json.load(f)
            print("   ✅ Loaded existing leading indicators data")
        except FileNotFoundError:
            print("   ⚠️ No existing leading indicators data found, using defaults")
            leading_indicators = forecast_system.get_default_leading_indicators_data()
        
        # Add comprehensive leading indicators data
        print("🔄 Adding comprehensive leading indicators data...")
        leading_indicators.update({
            'wage_growth_analysis': {
                'wage_pressure': 'moderate',
                'average_growth_rate': 3.2,
                'confidence_score': 0.6,
                'latest_wages': {
                    'CES0500000003': 28.50,
                    'ECIWAG': 125.5,
                    'AHETPI': 27.25
                }
            },
            'quit_rate_analysis': {
                'quit_rate': 2.3,
                'quits': 3208000,
                'employment': 139500000,
                'interpretation': 'moderate_confidence'
            },
            'state_unemployment_analysis': {
                'regional_dispersion': 'moderate',
                'average_state_rate': 4.3,
                'rate_std': 0.6,
                'coefficient_variation': 0.14,
                'min_rate': 3.2,
                'max_rate': 5.8,
                'outliers': [
                    {'state': 'CAUR', 'rate': 5.8, 'deviation': 1.5},
                    {'state': 'NYUR', 'rate': 4.9, 'deviation': 0.6}
                ],
                'confidence_score': 0.6,
                'latest_rates': {
                    'CAUR': 5.8, 'TXUR': 4.1, 'FLUR': 3.8, 'NYUR': 4.9,
                    'PAUR': 4.2, 'ILUR': 4.5, 'OHUR': 4.0, 'GAUR': 3.9,
                    'NCUR': 4.1, 'MIUR': 4.3
                }
            }
        })
        
        # Update the forecast system with enhanced data
        forecast_system.leading_indicators_data = leading_indicators
        
        # Calculate the enhanced forecast
        print("🔄 Calculating enhanced forecast with optimized weights...")
        forecast, adjustments = forecast_system.calculate_final_enhanced_forecast()
        
        # Calculate enhanced confidence
        print("🔄 Calculating enhanced confidence...")
        confidence = forecast_system.calculate_final_enhanced_confidence()
        
        # Generate comprehensive report
        print("🔄 Generating comprehensive report...")
        report = forecast_system.create_final_enhanced_report(forecast, adjustments, confidence)
        
        # Print results
        print("\n" + "="*80)
        print("🎯 OPTIMIZED WEIGHTS FORECAST RESULTS")
        print("="*80)
        print(f"📊 Forecast: {forecast:.2f}%")
        print(f"🎯 Confidence: {confidence:.1f}%")
        print(f"📈 Total Adjustments: {len(adjustments)} factors")
        
        print(f"\n🔧 Adjustment Breakdown:")
        for adj_name, adj_value in adjustments:
            print(f"   • {adj_name}: {adj_value:+.4f}%")
        
        # Show key factor impacts
        lfpr_adj = next((adj[1] for adj in adjustments if 'LFPR' in adj[0]), 0)
        claims_adj = next((adj[1] for adj in adjustments if 'Claims' in adj[0] and 'Trade' not in adj[0]), 0)
        trade_adj = next((adj[1] for adj in adjustments if 'Trade' in adj[0]), 0)
        state_adj = next((adj[1] for adj in adjustments if 'State' in adj[0]), 0)
        wage_adj = next((adj[1] for adj in adjustments if 'Wage' in adj[0]), 0)
        quit_adj = next((adj[1] for adj in adjustments if 'Quit' in adj[0]), 0)
        
        print(f"\n📊 Key Factor Impacts:")
        print(f"   • Labor Force Participation: {lfpr_adj:+.4f}%")
        print(f"   • Claims Data: {claims_adj:+.4f}%")
        print(f"   • Trade Data: {trade_adj:+.4f}%")
        print(f"   • State Unemployment: {state_adj:+.4f}%")
        print(f"   • Wage Growth: {wage_adj:+.4f}%")
        print(f"   • Quit Rate: {quit_adj:+.4f}%")
        
        # Calculate total impact by category
        core_labor_impact = lfpr_adj + claims_adj
        trade_impact = trade_adj
        leading_indicators_impact = state_adj + wage_adj + quit_adj
        
        print(f"\n📈 Category Impacts:")
        print(f"   • Core Labor Market: {core_labor_impact:+.4f}%")
        print(f"   • Trade Data: {trade_impact:+.4f}%")
        print(f"   • Leading Indicators: {leading_indicators_impact:+.4f}%")
        
        # Save test results
        test_results = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "forecast": forecast,
            "confidence": confidence,
            "adjustments": adjustments,
            "factor_impacts": {
                "lfpr": lfpr_adj,
                "claims": claims_adj,
                "trade": trade_adj,
                "state": state_adj,
                "wage": wage_adj,
                "quit": quit_adj
            },
            "category_impacts": {
                "core_labor": core_labor_impact,
                "trade_data": trade_impact,
                "leading_indicators": leading_indicators_impact
            },
            "leading_indicators_data": leading_indicators,
            "report": report
        }
        
        with open('optimized_weights_forecast_results.json', 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n✅ Test results saved to: optimized_weights_forecast_results.json")
        
        # Print summary
        print(f"\n📋 OPTIMIZED WEIGHTS SUMMARY:")
        print(f"   • Enhanced Forecast: {forecast:.2f}%")
        print(f"   • Enhanced Confidence: {confidence:.1f}%")
        print(f"   • Core Labor Impact: {core_labor_impact:+.4f}%")
        print(f"   • Trade Data Impact: {trade_impact:+.4f}%")
        print(f"   • Leading Indicators Impact: {leading_indicators_impact:+.4f}%")
        print(f"   • Total Adjustment Factors: {len(adjustments)}")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Error running optimized weights forecast: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = test_optimized_weights_forecast()
    if results:
        print(f"\n🎉 Optimized weights forecast completed successfully!")
    else:
        print(f"\n💥 Optimized weights forecast failed!")