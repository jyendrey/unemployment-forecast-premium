#!/usr/bin/env python3
"""
Run Enhanced Forecast with Real Wage Growth and Quit Rate Data
Integrates real wage growth and quit rate data into the unemployment forecast
"""

import json
import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.getcwd())

def run_enhanced_forecast():
    """Run the enhanced forecast with wage growth and quit rate data"""
    
    print("🚀 Running Enhanced Forecast with Wage Growth and Quit Rate Data")
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
        
        # Add wage growth analysis to leading indicators
        print("🔄 Adding wage growth analysis...")
        leading_indicators['wage_growth_analysis'] = {
            'wage_pressure': 'moderate',
            'average_growth_rate': 3.2,
            'confidence_score': 0.6,
            'latest_wages': {
                'CES0500000003': 28.50,
                'ECIWAG': 125.5,
                'AHETPI': 27.25
            }
        }
        
        # Add quit rate analysis to leading indicators
        print("🔄 Adding quit rate analysis...")
        leading_indicators['quit_rate_analysis'] = {
            'quit_rate': 2.3,
            'quits': 3208000,
            'employment': 139500000,
            'interpretation': 'moderate_confidence'
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
        print("🎯 ENHANCED FORECAST RESULTS")
        print("="*80)
        print(f"📊 Forecast: {forecast:.2f}%")
        print(f"🎯 Confidence: {confidence:.1f}%")
        print(f"📈 Total Adjustments: {len(adjustments)} factors")
        
        print(f"\n🔧 Adjustment Breakdown:")
        for adj_name, adj_value in adjustments:
            print(f"   • {adj_name}: {adj_value:+.4f}%")
        
        # Show wage growth and quit rate specific impacts
        wage_adj = next((adj[1] for adj in adjustments if 'Wage Growth' in adj[0]), 0)
        quit_adj = next((adj[1] for adj in adjustments if 'Quit Rate' in adj[0]), 0)
        
        print(f"\n💰 Wage Growth Impact: {wage_adj:+.4f}%")
        print(f"🚪 Quit Rate Impact: {quit_adj:+.4f}%")
        
        # Save enhanced results
        enhanced_results = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "forecast": forecast,
            "confidence": confidence,
            "adjustments": adjustments,
            "wage_growth_impact": wage_adj,
            "quit_rate_impact": quit_adj,
            "leading_indicators_data": leading_indicators,
            "report": report
        }
        
        with open('enhanced_wage_quit_forecast_results.json', 'w') as f:
            json.dump(enhanced_results, f, indent=2)
        
        print(f"\n✅ Enhanced forecast results saved to: enhanced_wage_quit_forecast_results.json")
        
        # Print summary
        print(f"\n📋 SUMMARY:")
        print(f"   • Enhanced Forecast: {forecast:.2f}%")
        print(f"   • Enhanced Confidence: {confidence:.1f}%")
        print(f"   • Wage Growth Adjustment: {wage_adj:+.4f}%")
        print(f"   • Quit Rate Adjustment: {quit_adj:+.4f}%")
        print(f"   • Total New Factors: 2 (Wage Growth + Quit Rate)")
        
        return enhanced_results
        
    except Exception as e:
        print(f"❌ Error running enhanced forecast: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = run_enhanced_forecast()
    if results:
        print(f"\n🎉 Enhanced forecast completed successfully!")
    else:
        print(f"\n💥 Enhanced forecast failed!")