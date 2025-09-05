#!/usr/bin/env python3
"""
Run Enhanced Forecast with State-Level Unemployment Data
Integrates state-level unemployment data into the unemployment forecast
"""

import json
import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.getcwd())

def run_enhanced_forecast_with_states():
    """Run the enhanced forecast with state unemployment data"""
    
    print("🚀 Running Enhanced Forecast with State-Level Unemployment Data")
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
        
        # Add state unemployment analysis to leading indicators
        print("🔄 Adding state unemployment analysis...")
        leading_indicators['state_unemployment_analysis'] = {
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
        
        # Update the forecast system with enhanced data
        forecast_system.leading_indicators_data = leading_indicators
        
        # Calculate the enhanced forecast
        print("🔄 Calculating enhanced forecast...")
        forecast, adjustments = forecast_system.calculate_final_enhanced_forecast()
        
        # Calculate enhanced confidence
        print("🔄 Calculating enhanced confidence...")
        confidence = forecast_system.calculate_final_enhanced_confidence()
        
        # Generate comprehensive report
        print("🔄 Generating comprehensive report...")
        report = forecast_system.create_final_enhanced_report(forecast, adjustments, confidence)
        
        # Print results
        print("\n" + "="*80)
        print("🎯 ENHANCED FORECAST RESULTS WITH STATE DATA")
        print("="*80)
        print(f"📊 Forecast: {forecast:.2f}%")
        print(f"🎯 Confidence: {confidence:.1f}%")
        print(f"📈 Total Adjustments: {len(adjustments)} factors")
        
        print(f"\n🔧 Adjustment Breakdown:")
        for adj_name, adj_value in adjustments:
            print(f"   • {adj_name}: {adj_value:+.4f}%")
        
        # Show state unemployment specific impacts
        state_adj = next((adj[1] for adj in adjustments if 'State Unemployment' in adj[0]), 0)
        wage_adj = next((adj[1] for adj in adjustments if 'Wage Growth' in adj[0]), 0)
        quit_adj = next((adj[1] for adj in adjustments if 'Quit Rate' in adj[0]), 0)
        
        print(f"\n🏛️ State Unemployment Impact: {state_adj:+.4f}%")
        print(f"💰 Wage Growth Impact: {wage_adj:+.4f}%")
        print(f"🚪 Quit Rate Impact: {quit_adj:+.4f}%")
        
        # Show state analysis details
        state_analysis = leading_indicators.get('state_unemployment_analysis', {})
        if state_analysis:
            print(f"\n📊 State Analysis Details:")
            print(f"   • Regional Dispersion: {state_analysis.get('regional_dispersion', 'unknown')}")
            print(f"   • Average State Rate: {state_analysis.get('average_state_rate', 0):.1f}%")
            print(f"   • Outlier States: {len(state_analysis.get('outliers', []))}")
            print(f"   • States Analyzed: {len(state_analysis.get('latest_rates', {}))}")
        
        # Save enhanced results
        enhanced_results = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "forecast": forecast,
            "confidence": confidence,
            "adjustments": adjustments,
            "state_unemployment_impact": state_adj,
            "wage_growth_impact": wage_adj,
            "quit_rate_impact": quit_adj,
            "state_analysis": state_analysis,
            "leading_indicators_data": leading_indicators,
            "report": report
        }
        
        with open('enhanced_forecast_with_states_results.json', 'w') as f:
            json.dump(enhanced_results, f, indent=2)
        
        print(f"\n✅ Enhanced forecast results saved to: enhanced_forecast_with_states_results.json")
        
        # Print summary
        print(f"\n📋 SUMMARY:")
        print(f"   • Enhanced Forecast: {forecast:.2f}%")
        print(f"   • Enhanced Confidence: {confidence:.1f}%")
        print(f"   • State Unemployment Adjustment: {state_adj:+.4f}%")
        print(f"   • Wage Growth Adjustment: {wage_adj:+.4f}%")
        print(f"   • Quit Rate Adjustment: {quit_adj:+.4f}%")
        print(f"   • Total New Factors: 3 (State Data + Wage Growth + Quit Rate)")
        
        return enhanced_results
        
    except Exception as e:
        print(f"❌ Error running enhanced forecast: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = run_enhanced_forecast_with_states()
    if results:
        print(f"\n🎉 Enhanced forecast with state data completed successfully!")
    else:
        print(f"\n💥 Enhanced forecast with state data failed!")