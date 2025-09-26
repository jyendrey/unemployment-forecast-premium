#!/usr/bin/env python3
"""
CORRECTED October 2025 Unemployment Rate Forecast
Fixing calculation errors and probability interpretation
"""

import json
from datetime import datetime
import math

class CorrectedOctober2025Forecaster:
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
        
        # Trade-related indicators for October 2025
        self.october_trade_balance = -85000  # -$85B deficit (slight improvement from -$90B)
        self.october_exports = 280000000000  # $280B (slight increase)
        self.october_imports = 365000000000  # $365B (slight decrease)
        self.october_manufacturing_exports = 85000000000  # $85B
        self.october_services_exports = 95000000000  # $95B
        self.october_agricultural_exports = 18000000000  # $18B
        self.october_energy_exports = 12000000000  # $12B
        self.october_supply_chain_index = 52.5  # Above 50 = improvement
        self.october_global_pmi = 51.8  # Global expansion
        self.october_china_pmi = 50.5  # Slight expansion
        self.october_eu_pmi = 49.8  # Slight contraction
        
        # CORRECTED Forecast probability ranges
        # These represent probability that unemployment will be ABOVE each threshold
        self.forecast_ranges = {
            "above_3.9": {"yes": 97, "no": 3},   # 97% think it will be above 3.9%
            "above_4.0": {"yes": 93, "no": 5},   # 93% think it will be above 4.0%
            "above_4.1": {"yes": 87, "no": 11},  # 87% think it will be above 4.1%
            "above_4.2": {"yes": 63, "no": 35},  # 63% think it will be above 4.2%
            "above_4.3": {"yes": 40, "no": 58},  # 40% think it will be above 4.3% (flip point)
            "above_4.4": {"yes": 16, "no": 84}   # 16% think it will be above 4.4%
        }
        
    def calculate_trade_adjustments(self):
        """Calculate unemployment adjustments based on trade data"""
        adjustments = {}
        
        # 1. Trade Balance Adjustment
        # Better trade balance (less negative) = more export jobs = LOWER unemployment
        trade_balance_change = (self.october_trade_balance - (-90000)) / 1000  # Billions
        trade_balance_adjustment = -trade_balance_change * 0.01  # -0.01% per $1B improvement
        adjustments['trade_balance'] = trade_balance_adjustment
        
        # 2. Export Growth Adjustment
        # More exports = more jobs = LOWER unemployment
        export_growth = (self.october_exports - 275000000000) / 275000000000  # % change
        export_adjustment = -export_growth * 0.3  # -0.3% per 1% export growth
        adjustments['export_growth'] = export_adjustment
        
        # 3. Manufacturing Export Adjustment
        # Manufacturing exports create high-value jobs = LOWER unemployment
        mfg_export_growth = (self.october_manufacturing_exports - 82000000000) / 82000000000
        mfg_export_adjustment = -mfg_export_growth * 0.4  # -0.4% per 1% growth
        adjustments['manufacturing_exports'] = mfg_export_adjustment
        
        # 4. Services Export Adjustment
        # Services exports create jobs = LOWER unemployment
        services_export_growth = (self.october_services_exports - 92000000000) / 92000000000
        services_export_adjustment = -services_export_growth * 0.2  # -0.2% per 1% growth
        adjustments['services_exports'] = services_export_adjustment
        
        # 5. Supply Chain Index Adjustment
        # Better supply chains = more manufacturing = LOWER unemployment
        supply_chain_change = self.october_supply_chain_index - 50.0
        supply_chain_adjustment = -supply_chain_change * 0.05  # -0.05% per point
        adjustments['supply_chain'] = supply_chain_adjustment
        
        # 6. Global PMI Adjustment
        # Global expansion = more demand for US exports = LOWER unemployment
        global_pmi_change = self.october_global_pmi - 50.0
        global_pmi_adjustment = -global_pmi_change * 0.03  # -0.03% per point
        adjustments['global_pmi'] = global_pmi_adjustment
        
        # 7. China PMI Adjustment
        # China expansion = more demand for US goods = LOWER unemployment
        china_pmi_change = self.october_china_pmi - 50.0
        china_pmi_adjustment = -china_pmi_change * 0.02  # -0.02% per point
        adjustments['china_pmi'] = china_pmi_adjustment
        
        # 8. EU PMI Adjustment
        # EU contraction = less demand for US exports = HIGHER unemployment
        eu_pmi_change = self.october_eu_pmi - 50.0
        eu_pmi_adjustment = -eu_pmi_change * 0.02  # -0.02% per point
        adjustments['eu_pmi'] = eu_pmi_adjustment
        
        return adjustments
    
    def calculate_october_forecast(self):
        """Calculate October 2025 unemployment rate forecast with CORRECTED logic"""
        
        # Base rate from September
        base_rate = self.september_unemployment_rate
        
        # CORRECTED labor market adjustments
        adjustments = {}
        
        # 1. Initial Claims Adjustment (CORRECTED: Higher claims = HIGHER unemployment)
        claims_change = (self.october_initial_claims - self.september_initial_claims) / 1000000
        claims_adjustment = claims_change * 0.25  # +0.25% per 100k increase
        adjustments['initial_claims'] = claims_adjustment
        
        # 2. Continuing Claims Adjustment (CORRECTED: Higher claims = HIGHER unemployment)
        continuing_change = (self.october_continuing_claims - self.september_continuing_claims) / 1000000
        continuing_adjustment = continuing_change * 0.15  # +0.15% per 100k increase
        adjustments['continuing_claims'] = continuing_adjustment
        
        # 3. Nonfarm Payrolls Adjustment (CORRECTED: Fewer payrolls = HIGHER unemployment)
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
        
        # Add trade-related adjustments
        trade_adjustments = self.calculate_trade_adjustments()
        adjustments.update(trade_adjustments)
        
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
        model_complexity = 0.8  # Higher complexity with trade data
        historical_accuracy = 0.7  # Estimated accuracy
        
        # External factors
        market_volatility = 0.8  # Moderate volatility
        policy_uncertainty = 0.75  # Some uncertainty
        trade_uncertainty = 0.7  # Trade policy uncertainty
        
        # Calculate weighted confidence
        confidence_factors = {
            'data_quality': (data_freshness + data_consistency + economic_stability) / 3,
            'methodology': (model_complexity + historical_accuracy) / 2,
            'external': (market_volatility + policy_uncertainty + trade_uncertainty) / 3
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
    
    def generate_corrected_report(self, forecast, confidence, adjustments, total_adjustment, probability_analysis):
        """Generate corrected October forecast report"""
        
        print("=" * 70)
        print("🎯 CORRECTED OCTOBER 2025 UNEMPLOYMENT FORECAST")
        print("📊 FIXED CALCULATION ERRORS & PROBABILITY INTERPRETATION")
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
        
        print(f"📊 Data Source: Labor Market + Trade Indicators (CORRECTED)")
        print()
        
        print("🔍 CORRECTED LABOR MARKET ADJUSTMENTS:")
        print("-" * 45)
        labor_factors = ['initial_claims', 'continuing_claims', 'nonfarm_payrolls', 
                        'lfpr', 'ep_ratio', 'wage_growth', 'consumer_confidence', 
                        'manufacturing_pmi', 'job_openings', 'quits_rate']
        for factor in labor_factors:
            if factor in adjustments:
                direction = "📈" if adjustments[factor] > 0 else "📉" if adjustments[factor] < 0 else "➡️"
                print(f"{direction} {factor.replace('_', ' ').title()}: {adjustments[factor]:+.3f}%")
        
        print("\n🌍 TRADE DATA ADJUSTMENTS:")
        print("-" * 30)
        trade_factors = ['trade_balance', 'export_growth', 'manufacturing_exports', 
                        'services_exports', 'supply_chain', 'global_pmi', 'china_pmi', 'eu_pmi']
        for factor in trade_factors:
            if factor in adjustments:
                direction = "📈" if adjustments[factor] > 0 else "📉" if adjustments[factor] < 0 else "➡️"
                print(f"{direction} {factor.replace('_', ' ').title()}: {adjustments[factor]:+.3f}%")
        
        print(f"\n📊 Total Adjustment: {total_adjustment:+.3f}%")
        print()
        
        print("🎯 MARKET EXPECTATIONS vs OUR FORECAST:")
        print("-" * 45)
        for threshold, analysis in probability_analysis.items():
            threshold_display = threshold.replace('_', ' ').title()
            status = "✅" if analysis["alignment"] == "ALIGNED" else "❌"
            print(f"{status} {threshold_display}: Market Yes {analysis['market_yes_probability']}% | No {analysis['market_no_probability']}% | Our Forecast: {analysis['our_forecast']}")
        print()
        
        print("🎯 CORRECTED FORECAST RATIONALE:")
        print("-" * 35)
        print("• FIXED: Higher claims now correctly increase unemployment")
        print("• FIXED: Fewer payrolls now correctly increase unemployment") 
        print("• Improved trade balance supports export-related employment")
        print("• Manufacturing export growth creates high-value jobs")
        print("• Better supply chain conditions support manufacturing")
        print("• Global economic expansion increases export demand")
        print("• Strong domestic labor market indicators remain supportive")
        print()
        
        print("⚠️  KEY RISKS:")
        print("-" * 15)
        print("• Trade policy uncertainty and potential tariffs")
        print("• Global supply chain disruptions")
        print("• China economic slowdown risks")
        print("• EU economic weakness")
        print("• Federal Reserve policy uncertainty")
        print("• Labor force participation volatility")
        print()
        
        print("=" * 70)
        print("🎯 CORRECTED OCTOBER 2025 FORECAST: {:.2f}%".format(forecast))
        print("=" * 70)

def main():
    """Main execution function"""
    print("🚀 Starting CORRECTED October 2025 Unemployment Forecast...")
    print("📊 Fixing calculation errors and probability interpretation")
    print()
    
    forecaster = CorrectedOctober2025Forecaster()
    
    # Calculate forecast
    forecast, adjustments, total_adjustment = forecaster.calculate_october_forecast()
    
    # Calculate confidence
    confidence, confidence_factors = forecaster.calculate_confidence()
    
    # Calculate probability analysis
    probability_analysis = forecaster.calculate_probability_analysis(forecast)
    
    # Generate report
    forecaster.generate_corrected_report(forecast, confidence, adjustments, total_adjustment, probability_analysis)
    
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
    
    with open("corrected_october_2025_forecast.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to corrected_october_2025_forecast.json")

if __name__ == "__main__":
    main()