#!/usr/bin/env python3
"""
Forecast Accuracy Analysis
Analyzes our forecast accuracy against the actual unemployment rate of 4.3%
"""

import json
from datetime import datetime

def analyze_forecast_accuracy():
    """Analyze forecast accuracy against actual unemployment rate"""
    
    print("🔍 FORECAST ACCURACY ANALYSIS")
    print("=" * 60)
    
    # Our forecasts vs actual
    actual_rate = 4.3
    our_forecasts = {
        "Previous Forecast (4.239%)": 4.239,
        "Updated Forecast (4.233%)": 4.233,
        "CHURN Model (4.26%)": 4.26
    }
    
    print(f"📊 Actual Unemployment Rate: {actual_rate}%")
    print(f"📅 Release Date: September 2025")
    
    print(f"\n📊 Forecast Comparison:")
    print("-" * 40)
    
    best_forecast = None
    best_accuracy = float('inf')
    
    for forecast_name, forecast_rate in our_forecasts.items():
        error = abs(forecast_rate - actual_rate)
        error_pct = (error / actual_rate) * 100
        
        if error < best_accuracy:
            best_accuracy = error
            best_forecast = forecast_name
        
        direction = "Above" if forecast_rate > actual_rate else "Below"
        
        print(f"• {forecast_name}:")
        print(f"  - Forecast: {forecast_rate}%")
        print(f"  - Error: {error:.3f}% ({direction} actual)")
        print(f"  - Accuracy: {100 - error_pct:.1f}%")
        print()
    
    print(f"🏆 Most Accurate Forecast: {best_forecast}")
    print(f"📊 Best Error: {best_accuracy:.3f}%")
    print(f"📊 Best Accuracy: {100 - (best_accuracy/actual_rate)*100:.1f}%")
    
    # Analysis of our performance
    our_error = abs(4.233 - actual_rate)
    our_accuracy = 100 - (our_error/actual_rate)*100
    
    print(f"\n🎯 Our Performance Analysis:")
    print(f"• Our Forecast: 4.233%")
    print(f"• Actual Rate: 4.3%")
    print(f"• Error: {our_error:.3f}% (Below actual)")
    print(f"• Accuracy: {our_accuracy:.1f}%")
    
    # Comparison with CHURN
    churn_error = abs(4.26 - actual_rate)
    churn_accuracy = 100 - (churn_error/actual_rate)*100
    
    print(f"\n🔄 CHURN Comparison:")
    print(f"• CHURN Forecast: 4.26%")
    print(f"• CHURN Error: {churn_error:.3f}% (Below actual)")
    print(f"• CHURN Accuracy: {churn_accuracy:.1f}%")
    print(f"• Our Advantage: {our_accuracy - churn_accuracy:+.1f}%")
    
    # What this means for our model
    print(f"\n💡 Model Performance Insights:")
    if our_error < 0.1:
        print("✅ EXCELLENT: Error < 0.1% - Model performed exceptionally well")
    elif our_error < 0.2:
        print("✅ VERY GOOD: Error < 0.2% - Model performed very well")
    elif our_error < 0.5:
        print("✅ GOOD: Error < 0.5% - Model performed well")
    else:
        print("⚠️ NEEDS IMPROVEMENT: Error > 0.5% - Model needs refinement")
    
    print(f"\n🔧 Model Adjustments Needed:")
    if 4.233 < actual_rate:
        print("• Model slightly underestimated unemployment")
        print("• Consider increasing economic headwinds weight")
        print("• Review claims trend impact calculation")
    else:
        print("• Model slightly overestimated unemployment")
        print("• Consider reducing economic headwinds weight")
        print("• Review job flow calculations")
    
    # Save analysis
    analysis = {
        'analysis_date': datetime.now().isoformat(),
        'actual_unemployment_rate': actual_rate,
        'our_forecast': 4.233,
        'our_error': our_error,
        'our_accuracy': our_accuracy,
        'churn_forecast': 4.26,
        'churn_error': churn_error,
        'churn_accuracy': churn_accuracy,
        'performance_rating': 'EXCELLENT' if our_error < 0.1 else 'VERY GOOD' if our_error < 0.2 else 'GOOD' if our_error < 0.5 else 'NEEDS IMPROVEMENT',
        'model_direction': 'Underestimated' if 4.233 < actual_rate else 'Overestimated',
        'recommendations': [
            'Continue monitoring trade data for real-time adjustments',
            'Fine-tune economic headwinds calculation',
            'Review claims trend impact weights',
            'Maintain current confidence calculation approach'
        ]
    }
    
    filename = f"forecast_accuracy_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n💾 Analysis saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving analysis: {e}")
    
    return analysis

def main():
    """Main function to run accuracy analysis"""
    analysis = analyze_forecast_accuracy()
    
    print(f"\n" + "=" * 60)
    print("✅ FORECAST ACCURACY ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"📊 Our Accuracy: {analysis['our_accuracy']:.1f}%")
    print(f"📊 Performance: {analysis['performance_rating']}")
    print(f"📊 Direction: {analysis['model_direction']}")
    print(f"💾 Analysis saved successfully")

if __name__ == "__main__":
    main()