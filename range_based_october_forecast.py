#!/usr/bin/env python3
"""
Range-Based October 2025 Unemployment Rate Forecast
Using trade data to create a range around the labor market forecast
"""

import json
from datetime import datetime
import math

class RangeBasedOctober2025Forecaster:
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
        
        # Trade-related indicators for October 2025 (for range calculation)
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
        
        # Forecast probability ranges (as provided)
        self.forecast_ranges = {
            "above_3.9": {"yes": 97, "no": 3},   # 97% think it will be above 3.9%
            "above_4.0": {"yes": 93, "no": 5},   # 93% think it will be above 4.0%
            "above_4.1": {"yes": 87, "no": 11},  # 87% think it will be above 4.1%
            "above_4.2": {"yes": 63, "no": 35},  # 63% think it will be above 4.2%
            "above_4.3": {"yes": 40, "no": 58},  # 40% think it will be above 4.3% (flip point)
            "above_4.4": {"yes": 16, "no": 84}   # 16% think it will be above 4.4%
        }
        
    def calculate_labor_market_forecast(self):
        """Calculate base forecast using only labor market data"""
        
        # Base rate from September
        base_rate = self.september_unemployment_rate
        
        # Labor market adjustments only
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
        base_forecast = base_rate + total_adjustment
        
        # Ensure reasonable bounds (3.0% to 8.0%)
        base_forecast = max(3.0, min(8.0, base_forecast))
        
        return base_forecast, adjustments, total_adjustment
    
    def calculate_trade_range(self, base_forecast):
        """Calculate range based on trade data scenarios"""
        
        # Calculate trade impact scenarios
        trade_scenarios = {}
        
        # Optimistic Trade Scenario (all trade factors positive)
        optimistic_trade_impact = -0.25  # -0.25% from trade improvements
        trade_scenarios['optimistic'] = {
            'forecast': base_forecast + optimistic_trade_impact,
            'description': 'Strong trade improvements',
            'factors': [
                'Better trade balance (-$85B vs -$90B)',
                'Export growth (+1.8%)',
                'Manufacturing export growth (+3.7%)',
                'Supply chain improvements (52.5)',
                'Global expansion (51.8 PMI)',
                'China expansion (50.5 PMI)'
            ]
        }
        
        # Base Trade Scenario (modest trade improvements)
        base_trade_impact = -0.10  # -0.10% from modest trade improvements
        trade_scenarios['base'] = {
            'forecast': base_forecast + base_trade_impact,
            'description': 'Modest trade improvements',
            'factors': [
                'Slight trade balance improvement',
                'Modest export growth',
                'Stable supply chains',
                'Mixed global PMI signals'
            ]
        }
        
        # Pessimistic Trade Scenario (trade headwinds)
        pessimistic_trade_impact = +0.15  # +0.15% from trade headwinds
        trade_scenarios['pessimistic'] = {
            'forecast': base_forecast + pessimistic_trade_impact,
            'description': 'Trade headwinds',
            'factors': [
                'EU contraction (49.8 PMI)',
                'Trade policy uncertainty',
                'Supply chain disruptions',
                'China economic slowdown',
                'Global economic headwinds'
            ]
        }
        
        # Calculate range
        forecasts = [scenario['forecast'] for scenario in trade_scenarios.values()]
        min_forecast = min(forecasts)
        max_forecast = max(forecasts)
        range_width = max_forecast - min_forecast
        
        return trade_scenarios, min_forecast, max_forecast, range_width
    
    def calculate_probability_analysis(self, base_forecast, min_forecast, max_forecast):
        """Analyze how our forecast range aligns with market expectations"""
        analysis = {}
        
        # Analyze both base forecast and range
        forecasts_to_analyze = {
            'base': base_forecast,
            'optimistic': min_forecast,
            'pessimistic': max_forecast
        }
        
        for forecast_type, forecast_rate in forecasts_to_analyze.items():
            analysis[forecast_type] = {}
            
            for threshold, probs in self.forecast_ranges.items():
                threshold_value = float(threshold.split('_')[1])
                market_yes_prob = probs["yes"]
                
                if forecast_rate >= threshold_value:
                    # Our forecast is above the threshold
                    analysis[forecast_type][threshold] = {
                        "our_forecast": "ABOVE",
                        "market_yes_probability": market_yes_prob,
                        "market_no_probability": probs["no"],
                        "alignment": "ALIGNED" if market_yes_prob > 50 else "MISALIGNED"
                    }
                else:
                    # Our forecast is below the threshold
                    analysis[forecast_type][threshold] = {
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
        model_complexity = 0.8  # Higher complexity with range analysis
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
    
    def generate_range_report(self, base_forecast, trade_scenarios, min_forecast, max_forecast, 
                            range_width, adjustments, total_adjustment, probability_analysis, confidence):
        """Generate comprehensive range-based forecast report"""
        
        print("=" * 70)
        print("🎯 RANGE-BASED OCTOBER 2025 UNEMPLOYMENT FORECAST")
        print("📊 LABOR MARKET BASE + TRADE DATA RANGE")
        print("=" * 70)
        print(f"📊 September 2025 Rate: {self.september_unemployment_rate:.1f}%")
        print(f"🎯 Base Forecast (Labor Market): {base_forecast:.2f}%")
        print(f"📈 Change: {base_forecast - self.september_unemployment_rate:+.2f} percentage points")
        print(f"🎯 Confidence Level: {confidence:.0f}%")
        print()
        
        print("📊 FORECAST RANGE (Including Trade Scenarios):")
        print("-" * 50)
        print(f"🔵 Optimistic (Strong Trade): {min_forecast:.2f}%")
        print(f"🟡 Base (Labor Market): {base_forecast:.2f}%")
        print(f"🔴 Pessimistic (Trade Headwinds): {max_forecast:.2f}%")
        print(f"📏 Range Width: {range_width:.2f} percentage points")
        print()
        
        print("🔍 LABOR MARKET ADJUSTMENTS:")
        print("-" * 35)
        for factor, adjustment in adjustments.items():
            direction = "📈" if adjustment > 0 else "📉" if adjustment < 0 else "➡️"
            print(f"{direction} {factor.replace('_', ' ').title()}: {adjustment:+.3f}%")
        print(f"\n📊 Total Labor Market Adjustment: {total_adjustment:+.3f}%")
        print()
        
        print("🌍 TRADE SCENARIOS:")
        print("-" * 25)
        for scenario_name, scenario in trade_scenarios.items():
            print(f"\n{scenario_name.upper()} SCENARIO: {scenario['forecast']:.2f}%")
            print(f"Description: {scenario['description']}")
            for factor in scenario['factors']:
                print(f"  • {factor}")
        print()
        
        print("🎯 MARKET EXPECTATIONS vs FORECAST RANGE:")
        print("-" * 50)
        for threshold, probs in self.forecast_ranges.items():
            threshold_display = threshold.replace('_', ' ').title()
            threshold_value = float(threshold.split('_')[1])
            market_yes = probs["yes"]
            market_no = probs["no"]
            
            print(f"\n{threshold_display} (≥{threshold_value}%):")
            print(f"  Market: Yes {market_yes}% | No {market_no}%")
            
            # Check where each scenario falls
            if min_forecast >= threshold_value:
                print(f"  🔵 Optimistic: ABOVE ✅")
            else:
                print(f"  🔵 Optimistic: BELOW {'❌' if market_yes > 50 else '✅'}")
                
            if base_forecast >= threshold_value:
                print(f"  🟡 Base: ABOVE ✅")
            else:
                print(f"  🟡 Base: BELOW {'❌' if market_yes > 50 else '✅'}")
                
            if max_forecast >= threshold_value:
                print(f"  🔴 Pessimistic: ABOVE ✅")
            else:
                print(f"  🔴 Pessimistic: BELOW {'❌' if market_yes > 50 else '✅'}")
        print()
        
        print("🎯 RANGE-BASED FORECAST RATIONALE:")
        print("-" * 40)
        print("• Base forecast uses only labor market indicators")
        print("• Trade data creates range of possible outcomes")
        print("• Optimistic scenario: Strong trade improvements")
        print("• Pessimistic scenario: Trade headwinds and uncertainty")
        print("• Range captures uncertainty in trade policy and global conditions")
        print("• Market expectations help validate scenario probabilities")
        print()
        
        print("⚠️  KEY RISKS BY SCENARIO:")
        print("-" * 35)
        print("🔵 OPTIMISTIC RISKS:")
        print("  • Trade policy reversals")
        print("  • Global economic slowdown")
        print("  • Supply chain disruptions")
        print()
        print("🟡 BASE RISKS:")
        print("  • Federal Reserve policy uncertainty")
        print("  • Labor force participation volatility")
        print("  • Missing trade impacts")
        print()
        print("🔴 PESSIMISTIC RISKS:")
        print("  • Trade war escalation")
        print("  • Global recession")
        print("  • Supply chain collapse")
        print("  • China economic crisis")
        print()
        
        print("=" * 70)
        print("🎯 RANGE-BASED OCTOBER 2025 FORECAST: {:.2f}% - {:.2f}%".format(min_forecast, max_forecast))
        print("🎯 BASE FORECAST: {:.2f}%".format(base_forecast))
        print("=" * 70)

def main():
    """Main execution function"""
    print("🚀 Starting Range-Based October 2025 Unemployment Forecast...")
    print("📊 Labor Market Base + Trade Data Range")
    print()
    
    forecaster = RangeBasedOctober2025Forecaster()
    
    # Calculate base labor market forecast
    base_forecast, adjustments, total_adjustment = forecaster.calculate_labor_market_forecast()
    
    # Calculate trade range
    trade_scenarios, min_forecast, max_forecast, range_width = forecaster.calculate_trade_range(base_forecast)
    
    # Calculate confidence
    confidence, confidence_factors = forecaster.calculate_confidence()
    
    # Calculate probability analysis
    probability_analysis = forecaster.calculate_probability_analysis(base_forecast, min_forecast, max_forecast)
    
    # Generate report
    forecaster.generate_range_report(base_forecast, trade_scenarios, min_forecast, max_forecast, 
                                   range_width, adjustments, total_adjustment, probability_analysis, confidence)
    
    # Save results
    results = {
        "forecast_date": datetime.now().isoformat(),
        "target_month": "October 2025",
        "september_rate": forecaster.september_unemployment_rate,
        "base_forecast": base_forecast,
        "forecast_range": {
            "min": min_forecast,
            "max": max_forecast,
            "width": range_width
        },
        "trade_scenarios": trade_scenarios,
        "labor_market_adjustments": adjustments,
        "total_labor_market_adjustment": total_adjustment,
        "probability_analysis": probability_analysis,
        "market_expectations": forecaster.forecast_ranges,
        "confidence": confidence,
        "confidence_factors": confidence_factors
    }
    
    with open("range_based_october_2025_forecast.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to range_based_october_2025_forecast.json")

if __name__ == "__main__":
    main()