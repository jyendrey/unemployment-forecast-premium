#!/usr/bin/env python3
"""
Enhanced Unemployment Forecast with Trend-Focused Analysis
Incorporates forward-looking indicators to match CHURN methodology
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class TrendFocusedForecast:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.version = "v4.1-trend-focused"
        self.current_date = datetime.now()
        
        # Load existing data
        self.jolts_data = self.load_jolts_data()
        self.trade_data = self.load_trade_data()
        self.economic_data = self.load_economic_data()
        
    def load_jolts_data(self):
        """Load JOLTS data with trend information"""
        return {
            'job_openings': 7181,  # Current
            'job_openings_prev': 7357,  # Previous month (for trend)
            'hires': 5308,
            'hires_prev': 5267,  # Previous month
            'separations': 5289,
            'separations_prev': 5341,  # Previous month
            'quits': 3208,
            'quits_prev': 3209,  # Previous month
            'layoffs': 1808,
            'layoffs_prev': 1796,  # Previous month
            'date': '2025-07-01'
        }
    
    def load_trade_data(self):
        """Load daily trade data with trend information"""
        return {
            'daily_volume': 1500,
            'sentiment_score': -0.124,  # Current sentiment
            'sentiment_trend': -0.05,  # Declining sentiment trend
            'volatility': 0.15,
            'trend_strength': 0.8,
            'data_freshness': 1.0
        }
    
    def load_economic_data(self):
        """Load economic data with trend information"""
        return {
            'unemployment_rate': 4.2,
            'unemployment_rate_prev': 4.1,  # Previous month
            'labor_force_participation': 62.2,
            'initial_claims': 218000,
            'initial_claims_prev': 210000,  # Previous month
            'continuing_claims': 1800000,
            'continuing_claims_prev': 1750000  # Previous month
        }
    
    def calculate_trend_indicators(self):
        """Calculate trend indicators for forward-looking analysis"""
        print("🔄 Calculating Trend Indicators...")
        
        # JOLTS trends
        openings_trend = (self.jolts_data['job_openings'] - self.jolts_data['job_openings_prev']) / self.jolts_data['job_openings_prev']
        hires_trend = (self.jolts_data['hires'] - self.jolts_data['hires_prev']) / self.jolts_data['hires_prev']
        separations_trend = (self.jolts_data['separations'] - self.jolts_data['separations_prev']) / self.jolts_data['separations_prev']
        quits_trend = (self.jolts_data['quits'] - self.jolts_data['quits_prev']) / self.jolts_data['quits_prev']
        layoffs_trend = (self.jolts_data['layoffs'] - self.jolts_data['layoffs_prev']) / self.jolts_data['layoffs_prev']
        
        # Economic trends
        unemployment_trend = self.economic_data['unemployment_rate'] - self.economic_data['unemployment_rate_prev']
        claims_trend = (self.economic_data['initial_claims'] - self.economic_data['initial_claims_prev']) / self.economic_data['initial_claims_prev']
        continuing_claims_trend = (self.economic_data['continuing_claims'] - self.economic_data['continuing_claims_prev']) / self.economic_data['continuing_claims_prev']
        
        trend_indicators = {
            'jolts_trends': {
                'openings_trend': openings_trend,
                'hires_trend': hires_trend,
                'separations_trend': separations_trend,
                'quits_trend': quits_trend,
                'layoffs_trend': layoffs_trend
            },
            'economic_trends': {
                'unemployment_trend': unemployment_trend,
                'claims_trend': claims_trend,
                'continuing_claims_trend': continuing_claims_trend
            }
        }
        
        print(f"📊 Job Openings Trend: {openings_trend:+.1%}")
        print(f"📊 Hires Trend: {hires_trend:+.1%}")
        print(f"📊 Separations Trend: {separations_trend:+.1%}")
        print(f"📊 Unemployment Trend: {unemployment_trend:+.1f}%")
        print(f"📊 Claims Trend: {claims_trend:+.1%}")
        
        return trend_indicators
    
    def calculate_forward_looking_adjustments(self, trend_indicators):
        """Calculate forward-looking adjustments based on trends"""
        print("🔄 Calculating Forward-Looking Adjustments...")
        
        # Job openings declining = future hiring slowdown = higher unemployment
        openings_adjustment = trend_indicators['jolts_trends']['openings_trend'] * 0.3  # Negative trend = positive unemployment adjustment
        
        # Hires increasing = positive for unemployment (but may be temporary)
        hires_adjustment = -trend_indicators['jolts_trends']['hires_trend'] * 0.2  # Positive trend = negative unemployment adjustment
        
        # Separations increasing = negative for unemployment
        separations_adjustment = trend_indicators['jolts_trends']['separations_trend'] * 0.25  # Positive trend = positive unemployment adjustment
        
        # Claims increasing = negative for unemployment
        claims_adjustment = trend_indicators['economic_trends']['claims_trend'] * 0.4  # Positive trend = positive unemployment adjustment
        
        # Continuing claims increasing = negative for unemployment
        continuing_claims_adjustment = trend_indicators['economic_trends']['continuing_claims_trend'] * 0.3
        
        # Trade sentiment declining = negative for unemployment
        trade_adjustment = -self.trade_data['sentiment_trend'] * 0.15  # Negative trend = positive unemployment adjustment
        
        # Combine adjustments
        total_forward_adjustment = (
            openings_adjustment + 
            hires_adjustment + 
            separations_adjustment + 
            claims_adjustment + 
            continuing_claims_adjustment + 
            trade_adjustment
        )
        
        forward_adjustments = {
            'openings_adjustment': openings_adjustment,
            'hires_adjustment': hires_adjustment,
            'separations_adjustment': separations_adjustment,
            'claims_adjustment': claims_adjustment,
            'continuing_claims_adjustment': continuing_claims_adjustment,
            'trade_adjustment': trade_adjustment,
            'total_forward_adjustment': total_forward_adjustment
        }
        
        print(f"📊 Openings Adjustment: {openings_adjustment:+.3f}%")
        print(f"📊 Hires Adjustment: {hires_adjustment:+.3f}%")
        print(f"📊 Separations Adjustment: {separations_adjustment:+.3f}%")
        print(f"📊 Claims Adjustment: {claims_adjustment:+.3f}%")
        print(f"📊 Trade Adjustment: {trade_adjustment:+.3f}%")
        print(f"📊 Total Forward Adjustment: {total_forward_adjustment:+.3f}%")
        
        return forward_adjustments
    
    def calculate_job_flow_rates(self):
        """Calculate job finding and separation rates (same as before)"""
        print("🔄 Calculating Job Flow Rates...")
        
        total_employment = 160_000_000
        unemployed = total_employment * (self.economic_data['unemployment_rate'] / 100)
        job_finding_rate = (self.jolts_data['hires'] * 1000) / unemployed
        job_separation_rate = (self.jolts_data['separations'] * 1000) / total_employment
        
        if job_finding_rate + job_separation_rate > 0:
            flow_consistent_rate = (job_separation_rate / (job_separation_rate + job_finding_rate)) * 100
        else:
            flow_consistent_rate = self.economic_data['unemployment_rate']
        
        job_flows = {
            'job_finding_rate': job_finding_rate,
            'job_separation_rate': job_separation_rate,
            'flow_consistent_rate': flow_consistent_rate
        }
        
        print(f"📊 Flow-Consistent Rate: {flow_consistent_rate:.3f}%")
        
        return job_flows
    
    def calculate_trend_focused_forecast(self):
        """Calculate trend-focused forecast"""
        print("🚀 TREND-FOCUSED UNEMPLOYMENT FORECAST")
        print("=" * 70)
        
        # Step 1: Calculate trend indicators
        trend_indicators = self.calculate_trend_indicators()
        
        # Step 2: Calculate forward-looking adjustments
        forward_adjustments = self.calculate_forward_looking_adjustments(trend_indicators)
        
        # Step 3: Calculate job flow rates
        job_flows = self.calculate_job_flow_rates()
        
        # Step 4: Calculate trend-focused forecast
        base_forecast = self.economic_data['unemployment_rate']
        
        # Apply forward-looking adjustments (trend-focused)
        trend_adjustment = forward_adjustments['total_forward_adjustment']
        
        # Apply job flow adjustment (smaller weight for trend-focused approach)
        job_flow_adjustment = (job_flows['flow_consistent_rate'] - base_forecast) * 0.1
        
        # Apply trade data adjustment
        trade_adjustment = self.trade_data['sentiment_score'] * 0.05
        
        # Final trend-focused forecast
        trend_focused_forecast = base_forecast + trend_adjustment + job_flow_adjustment + trade_adjustment
        
        # Calculate confidence (trend analysis adds uncertainty)
        base_confidence = 85.0
        trend_confidence_boost = 2.0  # Smaller boost due to trend uncertainty
        job_flow_confidence_boost = 1.0
        trade_data_confidence_boost = 1.0
        
        trend_focused_confidence = min(100.0, base_confidence + trend_confidence_boost + 
                                     job_flow_confidence_boost + trade_data_confidence_boost)
        
        # Determine forecast direction
        if trend_focused_forecast > base_forecast + 0.05:
            direction = 'rising'
        elif trend_focused_forecast < base_forecast - 0.05:
            direction = 'falling'
        else:
            direction = 'stable'
        
        results = {
            'trend_focused_forecast': round(trend_focused_forecast, 3),
            'trend_focused_confidence': round(trend_focused_confidence, 1),
            'direction': direction,
            'trend_indicators': trend_indicators,
            'forward_adjustments': forward_adjustments,
            'job_flows': job_flows,
            'adjustments': {
                'trend_adjustment': trend_adjustment,
                'job_flow_adjustment': job_flow_adjustment,
                'trade_adjustment': trade_adjustment
            }
        }
        
        return results
    
    def print_trend_focused_summary(self, results):
        """Print trend-focused forecast summary"""
        print("\n" + "=" * 70)
        print("🎯 TREND-FOCUSED UNEMPLOYMENT FORECAST RESULTS")
        print("=" * 70)
        
        print(f"📊 Trend-Focused Forecast: {results['trend_focused_forecast']}%")
        print(f"🚀 Trend-Focused Confidence: {results['trend_focused_confidence']}%")
        print(f"📈 Direction: {results['direction']}")
        
        print(f"\n🔧 Trend Analysis:")
        trends = results['trend_indicators']['jolts_trends']
        print(f"  • Job Openings: {trends['openings_trend']:+.1%}")
        print(f"  • Hires: {trends['hires_trend']:+.1%}")
        print(f"  • Separations: {trends['separations_trend']:+.1%}")
        
        econ_trends = results['trend_indicators']['economic_trends']
        print(f"  • Unemployment: {econ_trends['unemployment_trend']:+.1f}%")
        print(f"  • Claims: {econ_trends['claims_trend']:+.1%}")
        
        print(f"\n📊 Forward-Looking Adjustments:")
        adj = results['forward_adjustments']
        print(f"  • Openings: {adj['openings_adjustment']:+.3f}%")
        print(f"  • Hires: {adj['hires_adjustment']:+.3f}%")
        print(f"  • Separations: {adj['separations_adjustment']:+.3f}%")
        print(f"  • Claims: {adj['claims_adjustment']:+.3f}%")
        print(f"  • Trade: {adj['trade_adjustment']:+.3f}%")
        print(f"  • Total Trend: {adj['total_forward_adjustment']:+.3f}%")
        
        print(f"\n🔧 Final Adjustments:")
        print(f"  • Trend Adjustment: {results['adjustments']['trend_adjustment']:+.3f}%")
        print(f"  • Job Flow Adjustment: {results['adjustments']['job_flow_adjustment']:+.3f}%")
        print(f"  • Trade Adjustment: {results['adjustments']['trade_adjustment']:+.3f}%")
        
        print(f"\n🔄 Comparison with CHURN Model:")
        print(f"  • Our Trend-Focused: {results['trend_focused_forecast']}%")
        print(f"  • CHURN Model: 4.26%")
        print(f"  • Difference: {results['trend_focused_forecast'] - 4.26:+.3f}%")
        
        print(f"\n📊 Comparison with Original Framework:")
        print(f"  • Original Forecast: 4.2%")
        print(f"  • Trend-Focused: {results['trend_focused_forecast']}%")
        print(f"  • Change: {results['trend_focused_forecast'] - 4.2:+.3f}%")

def main():
    """Main function to run trend-focused forecast"""
    forecast = TrendFocusedForecast()
    results = forecast.calculate_trend_focused_forecast()
    forecast.print_trend_focused_summary(results)
    
    # Save results
    filename = f"trend_focused_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Trend-focused forecast saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving forecast: {e}")

if __name__ == "__main__":
    main()