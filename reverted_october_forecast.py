#!/usr/bin/env python3
"""
Reverted October 2025 Unemployment Rate Forecast
Removing trade data and reverting to original labor market-only equation
"""

import json
from datetime import datetime
import math

class RevertedOctober2025Forecaster:
    def __init__(self):
        # September 2025 baseline (from BLS August 2025 report)
        self.september_unemployment_rate = 4.3  # August 2025 rate
        self.september_lfpr = 62.3
        self.september_ep_ratio = 59.6
        self.september_initial_claims = 240000  # 4-week average
        self.september_continuing_claims = 1920000
        self.september_nonfarm_payrolls = 159540000  # 159.54 million
        self.september_avg_hourly_earnings = 36.53
        
        # October 2025 projections (my estimates)
        self.october_initial_claims = 235000  # Slight improvement
        self.october_continuing_claims = 1900000  # Slight improvement
        self.october_nonfarm_payrolls = 159800000  # +260k jobs
        self.october_avg_hourly_earnings = 36.65  # +0.3% growth
        self.october_lfpr = 62.4  # Slight improvement
        self.october_ep_ratio = 59.7  # Slight improvement
        
        # Economic indicators for October
        self.october_consumer_confidence = 108.5  # Slight improvement
        self.october_manufacturing_pmi = 51.2  # Expansion territory
        self.october_services_pmi = 53.8  # Strong expansion
        self.october_job_openings = 8500000  # Slight decrease
        self.october_quits_rate = 2.3  # Slight decrease
        
        # Forecast probability ranges (as provided)
        self.forecast_ranges = {
            "above_3.9": {"yes": 97, "no": 3},   # 97% think it will be above 3.9%
            "above_4.0": {"yes": 93, "no": 5},   # 93% think it will be above 4.0%
            "above_4.1": {"yes": 87, "no": 11},  # 87% think it will be above 4.1%
            "above_4.2": {"yes": 63, "no": 35},  # 63% think it will be above 4.2%
            "above_4.3": {"yes": 40, "no": 58},  # 40% think it will be above 4.3% (flip point)
            "above_4.4": {"yes": 16, "no": 84}   # 16% think it will be above 4.4%
        }
        
    def calculate_october_forecast(self):
        """Calculate October 2025 unemployment rate forecast - LABOR MARKET ONLY"""
        
        # Base rate from September
        base_rate = self.september_unemployment_rate
        
        # Labor market adjustments only (no trade data)
        adjustments = {}
        
        # 1. Initial Claims Adjustment (Higher claims = HIGHER unemployment)
        claims_change = (self.october_initial_claims - self.september_initial_claims) / 1000000
        claims_adjustment = claims_change * 0.25  # +0.25% per 100k increase
        adjustments['initial_claims'] = claims_adjustment
        
        # 2. Continuing Claims Adjustment (Higher claims = HIGHER unemployment)
        continuing_change = (self.october_continuing_claims - self.september_continuing_claims) / 1000000
        continuing_adjustment = continuing_change * 0.15  # +0.15% per 100k increase
        adjustments['continuing_claims'] = continuing_adjustment
        
        # 3. Nonfarm Payrolls Adjustment (Fewer payrolls = HIGHER unemployment)
        payrolls_change = (self.october_nonfarm_payrolls - self.september_nonfarm_payrolls) / 1000000
        payrolls_adjustment = -payrolls_change * 0.3  # -0.3% per 100k jobs (fewer jobs = higher unemployment)
        adjustments['nonfarm_payrolls'] = payrolls_adjustment
        
        # 4. Labor Force Participation Rate Adjustment
        # Higher LFPR = slightly higher unemployment (more people looking)
        lfpr_change = self.october_lfpr - self.september_lfpr
        lfpr_adjustment = lfpr_change * 0.1  # +0.1% per 0.1% LFPR increase
        adjustments['lfpr'] = lfpr_adjustment
        
        # 5. Employment-Population Ratio Adjustment
        # Higher EP ratio = lower unemployment
        ep_change = self.october_ep_ratio - self.september_ep_ratio
        ep_adjustment = -ep_change * 0.2  # -0.2% per 0.1% EP increase
        adjustments['ep_ratio'] = ep_adjustment
        
        # 6. Wage Growth Adjustment
        # Higher wage growth = tighter labor market = lower unemployment
        wage_growth = (self.october_avg_hourly_earnings - self.september_avg_hourly_earnings) / self.september_avg_hourly_earnings
        wage_adjustment = -wage_growth * 0.5  # -0.5% per 1% wage growth
        adjustments['wage_growth'] = wage_adjustment
        
        # 7. Consumer Confidence Adjustment
        # Higher confidence = more job seeking = slightly higher unemployment
        confidence_change = self.october_consumer_confidence - 105.0
        confidence_adjustment = confidence_change * 0.01  # +0.01% per point
        adjustments['consumer_confidence'] = confidence_adjustment
        
        # 8. Manufacturing PMI Adjustment
        # PMI > 50 = expansion = lower unemployment
        pmi_change = self.october_manufacturing_pmi - 50.0
        pmi_adjustment = -pmi_change * 0.02  # -0.02% per PMI point
        adjustments['manufacturing_pmi'] = pmi_adjustment
        
        # 9. Job Openings Adjustment
        # More openings = lower unemployment
        openings_change = (self.october_job_openings - 8500000) / 1000000
        openings_adjustment = -openings_change * 0.1  # -0.1% per 100k openings
        adjustments['job_openings'] = openings_adjustment
        
        # 10. Quits Rate Adjustment
        # Higher quits = more job mobility = lower unemployment
        quits_change = self.october_quits_rate - 2.3
        quits_adjustment = -quits_change * 0.15  # -0.15% per 0.1% quits change
        adjustments['quits_rate'] = quits_adjustment
        
        # Calculate total adjustment
        total_adjustment = sum(adjustments.values())
        
        # Apply adjustment to base rate
        forecast_rate = base_rate + total_adjustment
        
        # Ensure reasonable bounds (3.0% to 8.0%)
        forecast_rate = max(3.0, min(8.0, forecast_rate))
        
        return forecast_rate, adjustments, total_adjustment
    
    def calculate_probability_analysis(self, forecast_rate):
        """Analyze how our forecast aligns with market expectations"""
        analysis = {}
        
        # Determine which side of each threshold our forecast falls on
        for threshold, probs in self.forecast_ranges.items():
            threshold_value = float(threshold.split('_')[1])
            market_yes_prob = probs["yes"]
            
            if forecast_rate >= threshold_value:
                # Our forecast is above the threshold
                analysis[threshold] = {
                    "our_forecast": "ABOVE",
                    "market_yes_probability": market_yes_prob,
                    "market_no_probability": probs["no"],
                    "alignment": "ALIGNED" if market_yes_prob > 50 else "MISALIGNED"
                }
            else:
                # Our forecast is below the threshold
                analysis[threshold] = {
                    "our_forecast": "BELOW", 
                    "market_yes_probability": market_yes_prob,
                    "market_no_probability": probs["no"],
                    "alignment": "MISALIGNED" if market_yes_prob > 50 else "ALIGNED"
                }
        
        return analysis
    
    def calculate_confidence(self):
        """Calculate confidence level for the forecast"""
        
        # Data quality factors
        data_freshness = 0.9  # Recent data available
        data_consistency = 0.85  # Good consistency across indicators
        economic_stability = 0.8  # Moderate stability
        
        # Methodology factors
        model_complexity = 0.75  # Lower complexity without trade data
        historical_accuracy = 0.7  # Estimated accuracy
        
        # External factors
        market_volatility = 0.8  # Moderate volatility
        policy_uncertainty = 0.75  # Some uncertainty
        
        # Calculate weighted confidence
        confidence_factors = {
            'data_quality': (data_freshness + data_consistency + economic_stability) / 3,
            'methodology': (model_complexity + historical_accuracy) / 2,
            'external': (market_volatility + policy_uncertainty) / 2
        }
        
        weights = {
            'data_quality': 0.4,
            'methodology': 0.35,
            'external': 0.25
        }
        
        weighted_confidence = sum(confidence_factors[factor] * weights[factor] 
                                for factor in confidence_factors)
        
        # Convert to percentage
        confidence_percentage = weighted_confidence * 100
        
        return confidence_percentage, confidence_factors
    
    def generate_reverted_report(self, forecast, confidence, adjustments, total_adjustment, probability_analysis):
        """Generate reverted October forecast report"""
        
        print("=" * 70)
        print("🎯 REVERTED OCTOBER 2025 UNEMPLOYMENT FORECAST")
        print("📊 LABOR MARKET ONLY - NO TRADE DATA")
        print("=" * 70)
        print(f"📊 September 2025 Rate: {self.september_unemployment_rate:.1f}%")
        print(f"🎯 October 2025 Forecast: {forecast:.2f}%")
        print(f"📈 Change: {forecast - self.september_unemployment_rate:+.2f} percentage points")
        print(f"🎯 Confidence Level: {confidence:.0f}%")
        
        if forecast > self.september_unemployment_rate:
            print("📊 Direction: Rising")
        elif forecast < self.september_unemployment_rate:
            print("📊 Direction: Falling")
        else:
            print("📊 Direction: Stable")
        
        print(f"📊 Data Source: Labor Market Indicators Only")
        print()
        
        print("🔍 LABOR MARKET ADJUSTMENTS (NO TRADE DATA):")
        print("-" * 50)
        for factor, adjustment in adjustments.items():
            direction = "📈" if adjustment > 0 else "📉" if adjustment < 0 else "➡️"
            print(f"{direction} {factor.replace('_', ' ').title()}: {adjustment:+.3f}%")
        
        print(f"\n📊 Total Adjustment: {total_adjustment:+.3f}%")
        print()
        
        print("🎯 MARKET EXPECTATIONS vs OUR FORECAST:")
        print("-" * 45)
        for threshold, analysis in probability_analysis.items():
            threshold_display = threshold.replace('_', ' ').title()
            status = "✅" if analysis["alignment"] == "ALIGNED" else "❌"
            print(f"{status} {threshold_display}: Market Yes {analysis['market_yes_probability']}% | No {analysis['market_no_probability']}% | Our Forecast: {analysis['our_forecast']}")
        print()
        
        print("🎯 REVERTED FORECAST RATIONALE:")
        print("-" * 35)
        print("• REMOVED: All trade data adjustments")
        print("• FOCUSED: Only on domestic labor market indicators")
        print("• Higher claims correctly increase unemployment")
        print("• Fewer payrolls correctly increase unemployment") 
        print("• Rising labor force participation adds slight upward pressure")
        print("• Strong wage growth indicates tight labor market")
        print("• Manufacturing expansion supports job creation")
        print("• Consumer confidence remains elevated")
        print()
        
        print("⚠️  KEY RISKS:")
        print("-" * 15)
        print("• Federal Reserve policy uncertainty")
        print("• Labor force participation volatility")
        print("• Missing trade policy impacts")
        print("• Missing global economic factors")
        print("• Missing supply chain disruptions")
        print()
        
        print("=" * 70)
        print("🎯 REVERTED OCTOBER 2025 FORECAST: {:.2f}%".format(forecast))
        print("=" * 70)

def main():
    """Main execution function"""
    print("🚀 Starting REVERTED October 2025 Unemployment Forecast...")
    print("📊 Labor Market Only - No Trade Data")
    print()
    
    forecaster = RevertedOctober2025Forecaster()
    
    # Calculate forecast
    forecast, adjustments, total_adjustment = forecaster.calculate_october_forecast()
    
    # Calculate confidence
    confidence, confidence_factors = forecaster.calculate_confidence()
    
    # Calculate probability analysis
    probability_analysis = forecaster.calculate_probability_analysis(forecast)
    
    # Generate report
    forecaster.generate_reverted_report(forecast, confidence, adjustments, total_adjustment, probability_analysis)
    
    # Save results
    results = {
        "forecast_date": datetime.now().isoformat(),
        "target_month": "October 2025",
        "september_rate": forecaster.september_unemployment_rate,
        "october_forecast": forecast,
        "change": forecast - forecaster.september_unemployment_rate,
        "confidence": confidence,
        "adjustments": adjustments,
        "total_adjustment": total_adjustment,
        "probability_analysis": probability_analysis,
        "market_expectations": forecaster.forecast_ranges,
        "confidence_factors": confidence_factors
    }
    
    with open("reverted_october_2025_forecast.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to reverted_october_2025_forecast.json")

if __name__ == "__main__":
    main()