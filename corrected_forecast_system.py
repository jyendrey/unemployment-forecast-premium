#!/usr/bin/env python3
"""
Corrected Enhanced Unemployment Forecasting System
Properly accounts for claims data, payrolls revisions, and trade range sentiment
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import json
from datetime import datetime

class CorrectedForecastSystem:
    def __init__(self):
        self.foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.version = "v3.3-corrected-forecast"
        self.current_date = datetime.now()
        
        # Latest economic data
        self.initial_claims = 263000  # Rising +29,000
        self.continuing_claims = 1939000  # Declining -22,000
        self.payrolls_revision = -911000  # -911K since March
        
        # Trade range data (corrected interpretation)
        self.trade_ranges = {
            "Above 3.9%": {"Yes": 97, "No": 3},
            "Above 4.0%": {"Yes": 92, "No": 6},
            "Above 4.1%": {"Yes": 73, "No": 25},
            "Above 4.2%": {"Yes": 50, "No": 48},
            "Above 4.3%": {"Yes": 28, "No": 70},
            "Above 4.4%": {"Yes": 16, "No": 84},
            "Above 4.5%": {"Yes": 8, "No": 92}
        }
    
    def calculate_claims_impact(self):
        """Calculate unemployment impact from claims data (CORRECTED)"""
        
        print("🔍 Calculating Claims Data Impact (CORRECTED)...")
        
        # Initial Claims Impact (CORRECTED: Higher claims = Higher unemployment)
        initial_claims_benchmark = 225000
        initial_claims_change = self.initial_claims - initial_claims_benchmark
        initial_claims_impact = (initial_claims_change / initial_claims_benchmark) * 0.1  # 0.1% per 10% change
        
        print(f"📊 Initial Claims: {self.initial_claims:,} (Benchmark: {initial_claims_benchmark:,})")
        print(f"📊 Initial Claims Change: {initial_claims_change:+,}")
        print(f"📊 Initial Claims Impact: {initial_claims_impact:+.4f}% (Higher claims = Higher unemployment)")
        
        # Continuing Claims Impact (CORRECTED: Higher claims = Higher unemployment)
        continuing_claims_benchmark = 1750000
        continuing_claims_change = self.continuing_claims - continuing_claims_benchmark
        continuing_claims_impact = (continuing_claims_change / continuing_claims_benchmark) * 0.05  # 0.05% per 10% change
        
        print(f"📊 Continuing Claims: {self.continuing_claims:,} (Benchmark: {continuing_claims_benchmark:,})")
        print(f"📊 Continuing Claims Change: {continuing_claims_change:+,}")
        print(f"📊 Continuing Claims Impact: {continuing_claims_impact:+.4f}% (Higher claims = Higher unemployment)")
        
        total_claims_impact = initial_claims_impact + continuing_claims_impact
        print(f"📊 Total Claims Impact: {total_claims_impact:+.4f}%")
        
        return {
            'initial_claims_impact': initial_claims_impact,
            'continuing_claims_impact': continuing_claims_impact,
            'total_claims_impact': total_claims_impact
        }
    
    def calculate_payrolls_impact(self):
        """Calculate unemployment impact from payrolls revisions (CORRECTED)"""
        
        print("\n🔍 Calculating Payrolls Revision Impact (CORRECTED)...")
        
        # Payrolls Impact (CORRECTED: Fewer payrolls = Higher unemployment)
        # Rule of thumb: 100K jobs ≈ 0.1% unemployment rate change
        payrolls_impact = (self.payrolls_revision / 100000) * 0.1
        
        print(f"📊 Payrolls Revision: {self.payrolls_revision:,} jobs since March")
        print(f"📊 Payrolls Impact: {payrolls_impact:+.4f}% (Fewer jobs = Higher unemployment)")
        
        return {
            'payrolls_revision': self.payrolls_revision,
            'payrolls_impact': payrolls_impact
        }
    
    def calculate_trade_sentiment(self):
        """Calculate market sentiment from trade ranges (CORRECTED)"""
        
        print("\n🔍 Calculating Trade Range Sentiment (CORRECTED)...")
        
        # Analyze market expectations
        market_expectations = []
        
        for threshold, data in self.trade_ranges.items():
            threshold_value = float(threshold.split("Above ")[1].replace("%", ""))
            yes_pct = data["Yes"]
            no_pct = data["No"]
            
            # Market expectation: If Yes > 50%, market expects unemployment above this level
            if yes_pct > 50:
                expectation = f"Above {threshold_value}%"
                confidence = yes_pct / 100
            else:
                expectation = f"Below {threshold_value}%"
                confidence = no_pct / 100
            
            market_expectations.append({
                'threshold': threshold_value,
                'expectation': expectation,
                'confidence': confidence,
                'yes_pct': yes_pct,
                'no_pct': no_pct
            })
            
            print(f"📊 {threshold}: {yes_pct}% Yes, {no_pct}% No → {expectation} (Confidence: {confidence:.1%})")
        
        # Determine market's unemployment range expectation
        # Find where market flips from "above" to "below"
        flip_point = None
        for i, exp in enumerate(market_expectations):
            if exp['yes_pct'] < 50:  # Market expects below this level
                flip_point = exp['threshold']
                break
        
        if flip_point:
            print(f"📊 Market Flip Point: {flip_point}% (Market expects unemployment below this level)")
            market_range = f"Above 4.1% but below {flip_point}%"
        else:
            market_range = "Above 4.5%"
        
        print(f"📊 Market Expectation Range: {market_range}")
        
        # Calculate sentiment adjustment based on market expectations vs current rate
        current_rate = 4.2
        if flip_point and current_rate < flip_point:
            # Market expects unemployment above current rate
            sentiment_adjustment = 0.002  # Slight upward pressure
            sentiment_interpretation = "Market expects higher unemployment"
        else:
            # Market expects unemployment below current rate
            sentiment_adjustment = -0.002  # Slight downward pressure
            sentiment_interpretation = "Market expects lower unemployment"
        
        print(f"📊 Market Sentiment Adjustment: {sentiment_adjustment:+.4f}%")
        print(f"📊 Sentiment Interpretation: {sentiment_interpretation}")
        
        return {
            'market_expectations': market_expectations,
            'market_range': market_range,
            'flip_point': flip_point,
            'sentiment_adjustment': sentiment_adjustment,
            'sentiment_interpretation': sentiment_interpretation
        }
    
    def calculate_corrected_forecast(self):
        """Calculate corrected unemployment forecast"""
        
        print("="*60)
        print("CORRECTED UNEMPLOYMENT FORECAST CALCULATION")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        # Base unemployment rate
        base_rate = 4.2
        print(f"📊 Base Unemployment Rate: {base_rate}%")
        
        # Calculate all impacts
        claims_impact = self.calculate_claims_impact()
        payrolls_impact = self.calculate_payrolls_impact()
        trade_sentiment = self.calculate_trade_sentiment()
        
        # Calculate total adjustment
        total_adjustment = (claims_impact['total_claims_impact'] + 
                           payrolls_impact['payrolls_impact'] + 
                           trade_sentiment['sentiment_adjustment'])
        
        print(f"\n📈 TOTAL ADJUSTMENT CALCULATION:")
        print(f"  Claims Impact: {claims_impact['total_claims_impact']:+.4f}%")
        print(f"  Payrolls Impact: {payrolls_impact['payrolls_impact']:+.4f}%")
        print(f"  Trade Sentiment: {trade_sentiment['sentiment_adjustment']:+.4f}%")
        print(f"  Total Adjustment: {total_adjustment:+.4f}%")
        
        # Calculate final forecast
        final_forecast = base_rate + total_adjustment
        
        print(f"\n🎯 CORRECTED FORECAST RESULTS:")
        print(f"  Base Rate: {base_rate}%")
        print(f"  Total Adjustment: {total_adjustment:+.4f}%")
        print(f"  Final Forecast: {final_forecast:.2f}%")
        print(f"  Change from Current: {final_forecast - base_rate:+.2f} percentage points")
        
        if final_forecast > base_rate:
            direction = "Deterioration (Higher Unemployment Expected)"
        elif final_forecast < base_rate:
            direction = "Improvement (Lower Unemployment Expected)"
        else:
            direction = "Stable (No Change Expected)"
        
        print(f"  Direction: {direction}")
        
        return {
            'base_rate': base_rate,
            'final_forecast': final_forecast,
            'total_adjustment': total_adjustment,
            'direction': direction,
            'claims_impact': claims_impact,
            'payrolls_impact': payrolls_impact,
            'trade_sentiment': trade_sentiment
        }
    
    def create_corrected_report(self, forecast_data):
        """Create corrected forecast report"""
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'version': self.version,
            'foundation_id': self.foundation_id,
            'forecast_summary': {
                'current_unemployment': forecast_data['base_rate'],
                'forecasted_unemployment': round(forecast_data['final_forecast'], 2),
                'change': round(forecast_data['final_forecast'] - forecast_data['base_rate'], 2),
                'direction': forecast_data['direction']
            },
            'data_analysis': {
                'initial_claims': {
                    'value': self.initial_claims,
                    'trend': 'Rising (+29,000)',
                    'impact': forecast_data['claims_impact']['initial_claims_impact']
                },
                'continuing_claims': {
                    'value': self.continuing_claims,
                    'trend': 'Declining (-22,000)',
                    'impact': forecast_data['claims_impact']['continuing_claims_impact']
                },
                'payrolls_revision': {
                    'revision': self.payrolls_revision,
                    'period': 'March 2025 to September 2025',
                    'impact': forecast_data['payrolls_impact']['payrolls_impact']
                }
            },
            'market_sentiment': {
                'market_range': forecast_data['trade_sentiment']['market_range'],
                'flip_point': forecast_data['trade_sentiment']['flip_point'],
                'sentiment_interpretation': forecast_data['trade_sentiment']['sentiment_interpretation'],
                'sentiment_adjustment': forecast_data['trade_sentiment']['sentiment_adjustment']
            },
            'trade_range_analysis': self.trade_ranges
        }
        
        return report
    
    def save_corrected_report(self, report, filename="corrected_forecast_report.json"):
        """Save corrected forecast report"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Corrected forecast report saved to: {filename}")
        return filename
    
    def print_corrected_summary(self, report):
        """Print corrected forecast summary"""
        
        print("\n" + "="*60)
        print("CORRECTED FORECAST SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        forecast = report['forecast_summary']
        print(f"\n📊 FORECAST RESULTS:")
        print(f"  Current Unemployment Rate: {forecast['current_unemployment']}%")
        print(f"  Corrected Forecast: {forecast['forecasted_unemployment']}%")
        print(f"  Change: {forecast['change']:+.2f} percentage points")
        print(f"  Direction: {forecast['direction']}")
        
        data = report['data_analysis']
        print(f"\n📊 DATA IMPACT ANALYSIS:")
        print(f"  Initial Claims: {data['initial_claims']['value']:,} ({data['initial_claims']['trend']}) → {data['initial_claims']['impact']:+.4f}%")
        print(f"  Continuing Claims: {data['continuing_claims']['value']:,} ({data['continuing_claims']['trend']}) → {data['continuing_claims']['impact']:+.4f}%")
        print(f"  Payrolls Revision: {data['payrolls_revision']['revision']:,} jobs → {data['payrolls_revision']['impact']:+.4f}%")
        
        sentiment = report['market_sentiment']
        print(f"\n📊 MARKET SENTIMENT:")
        print(f"  Market Range Expectation: {sentiment['market_range']}")
        print(f"  Flip Point: {sentiment['flip_point']}%")
        print(f"  Interpretation: {sentiment['sentiment_interpretation']}")
        print(f"  Sentiment Adjustment: {sentiment['sentiment_adjustment']:+.4f}%")
        
        print("\n" + "="*60)
    
    def run_corrected_forecast(self):
        """Run the complete corrected forecasting process"""
        
        # Calculate corrected forecast
        forecast_data = self.calculate_corrected_forecast()
        
        # Create corrected report
        report = self.create_corrected_report(forecast_data)
        
        # Save report
        report_file = self.save_corrected_report(report)
        
        # Print summary
        self.print_corrected_summary(report)
        
        print(f"\n🎯 Corrected forecasting complete!")
        print(f"📁 Report saved to: {report_file}")
        print(f"🔧 Foundation System: {self.foundation_id}")
        print("="*60)
        
        return report

def main():
    """Main execution function"""
    forecaster = CorrectedForecastSystem()
    forecaster.run_corrected_forecast()

if __name__ == "__main__":
    main()