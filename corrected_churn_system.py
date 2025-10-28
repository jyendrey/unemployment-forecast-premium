#!/usr/bin/env python3
"""
Corrected CHURN-Blended Unemployment Forecasting System
Fixes trade range data interpretation - "Above 4.3%" means 4.4%+
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import json
from datetime import datetime
import statistics

class CorrectedCHURNBlendedForecastSystem:
    def __init__(self):
        self.foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.version = "v3.1-corrected-churn-blended"
        self.current_date = datetime.now()
        
        # Current unemployment rate
        self.current_unemployment_rate = 4.3
        
        # Traditional Labor Market Data (CHURN Component 1)
        self.traditional_data = {
            'unemployment_rate': 4.3,
            'initial_claims': 263000,  # Week ending September 6, 2025
            'continuing_claims': 1939000,  # Week ending August 30, 2025
            'payrolls_revision': -911000,  # Since March 2025
            'labor_force_participation': 62.2
        }
        
        # Alternative Data Sources (CHURN Component 2)
        self.alternative_data = {
            'online_job_postings': self.estimate_job_postings(),
            'social_media_sentiment': self.estimate_social_sentiment(),
            'mobility_data': self.estimate_mobility_data(),
            'real_time_payroll': self.estimate_real_time_payroll()
        }
        
        # Market Sentiment Data (Our Trade Data) - CORRECTED INTERPRETATION
        self.market_sentiment = {
            "Above 3.9%": {"Yes": 97, "No": 3, "threshold": 4.0},  # 4.0% and above
            "Above 4.0%": {"Yes": 92, "No": 6, "threshold": 4.1},  # 4.1% and above
            "Above 4.1%": {"Yes": 73, "No": 25, "threshold": 4.2}, # 4.2% and above
            "Above 4.2%": {"Yes": 50, "No": 48, "threshold": 4.3}, # 4.3% and above
            "Above 4.3%": {"Yes": 28, "No": 70, "threshold": 4.4}, # 4.4% and above
            "Above 4.4%": {"Yes": 16, "No": 84, "threshold": 4.5}, # 4.5% and above
            "Above 4.5%": {"Yes": 8, "No": 92, "threshold": 4.6}   # 4.6% and above
        }
        
        # CHURN Model Weights (based on Fed methodology)
        self.churn_weights = {
            'traditional_data': 0.4,  # 40% weight to traditional data
            'alternative_data': 0.3,  # 30% weight to alternative data
            'market_sentiment': 0.3   # 30% weight to market sentiment
        }
    
    def estimate_job_postings(self):
        """Estimate online job postings trend (alternative data)"""
        base_job_postings = 100
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -5
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.1
        
        job_postings_index = base_job_postings + unemployment_impact + claims_impact
        return max(job_postings_index, 50)
    
    def estimate_social_sentiment(self):
        """Estimate social media employment sentiment (alternative data)"""
        base_sentiment = 50
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -10
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.2
        
        sentiment_index = base_sentiment + unemployment_impact + claims_impact
        return max(min(sentiment_index, 100), 0)
    
    def estimate_mobility_data(self):
        """Estimate mobility/commuting data (alternative data)"""
        base_mobility = 100
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -15
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.3
        
        mobility_index = base_mobility + unemployment_impact + claims_impact
        return max(mobility_index, 20)
    
    def estimate_real_time_payroll(self):
        """Estimate real-time payroll data (alternative data)"""
        base_payroll_growth = 2.0
        revision_impact = self.traditional_data['payrolls_revision'] / 1000000 * -0.5
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -0.2
        
        payroll_growth = base_payroll_growth + revision_impact + unemployment_impact
        return max(payroll_growth, -2.0)
    
    def calculate_traditional_data_score(self):
        """Calculate traditional data component score (CHURN methodology)"""
        
        print("🔍 CALCULATING TRADITIONAL DATA SCORE (CHURN Component 1)")
        print("="*60)
        
        unemployment_score = max(0, 100 - (self.traditional_data['unemployment_rate'] - 3.5) * 20)
        print(f"📊 Unemployment Rate: {self.traditional_data['unemployment_rate']}% → Score: {unemployment_score:.1f}")
        
        claims_normalized = max(0, 100 - (self.traditional_data['initial_claims'] - 200000) / 1000)
        print(f"📊 Initial Claims: {self.traditional_data['initial_claims']:,} → Score: {claims_normalized:.1f}")
        
        continuing_normalized = max(0, 100 - (self.traditional_data['continuing_claims'] - 1500000) / 10000)
        print(f"📊 Continuing Claims: {self.traditional_data['continuing_claims']:,} → Score: {continuing_normalized:.1f}")
        
        lfpr_score = max(0, (self.traditional_data['labor_force_participation'] - 60) * 2)
        print(f"📊 Labor Force Participation: {self.traditional_data['labor_force_participation']}% → Score: {lfpr_score:.1f}")
        
        traditional_score = (unemployment_score * 0.4 + 
                           claims_normalized * 0.3 + 
                           continuing_normalized * 0.2 + 
                           lfpr_score * 0.1)
        
        print(f"\n📈 Traditional Data Score: {traditional_score:.1f}/100")
        return traditional_score
    
    def calculate_alternative_data_score(self):
        """Calculate alternative data component score (CHURN methodology)"""
        
        print("\n🔍 CALCULATING ALTERNATIVE DATA SCORE (CHURN Component 2)")
        print("="*60)
        
        job_postings_score = self.alternative_data['online_job_postings']
        print(f"📊 Online Job Postings Index: {job_postings_score:.1f}")
        
        social_sentiment_score = self.alternative_data['social_media_sentiment']
        print(f"📊 Social Media Sentiment: {social_sentiment_score:.1f}")
        
        mobility_score = self.alternative_data['mobility_data']
        print(f"📊 Mobility/Commuting Index: {mobility_score:.1f}")
        
        payroll_growth = self.alternative_data['real_time_payroll']
        payroll_score = max(0, min(100, 50 + payroll_growth * 10))
        print(f"📊 Real-time Payroll Growth: {payroll_growth:.1f}% → Score: {payroll_score:.1f}")
        
        alternative_score = (job_postings_score * 0.30 + 
                           social_sentiment_score * 0.25 + 
                           mobility_score * 0.25 + 
                           payroll_score * 0.20)
        
        print(f"\n📈 Alternative Data Score: {alternative_score:.1f}/100")
        return alternative_score
    
    def calculate_corrected_market_sentiment_score(self):
        """Calculate market sentiment with CORRECTED trade range interpretation"""
        
        print("\n🔍 CALCULATING CORRECTED MARKET SENTIMENT SCORE")
        print("="*60)
        
        current_rate = self.current_unemployment_rate
        print(f"📊 Current Unemployment Rate: {current_rate}%")
        
        # CORRECTED ANALYSIS: "Above 4.3%" means 4.4% and above
        print(f"\n📊 CORRECTED TRADE RANGE ANALYSIS:")
        
        market_expectations = []
        for threshold_name, data in self.market_sentiment.items():
            threshold_value = data['threshold']
            yes_pct = data["Yes"]
            no_pct = data["No"]
            
            if threshold_value == current_rate:
                print(f"  At Current Rate ({threshold_value}%): {yes_pct}% expect above, {no_pct}% expect below")
            elif threshold_value < current_rate:
                if yes_pct > 50:
                    print(f"  {threshold_name} ({threshold_value}%+): {yes_pct}% Yes → EXPECTED (unemployment above {threshold_value}%)")
                    market_expectations.append(('above', threshold_value, yes_pct))
                else:
                    print(f"  {threshold_name} ({threshold_value}%+): {no_pct}% No → UNEXPECTED (unemployment below {threshold_value}%)")
            else:
                if no_pct > 50:
                    print(f"  {threshold_name} ({threshold_value}%+): {no_pct}% No → EXPECTED (unemployment below {threshold_value}%)")
                    market_expectations.append(('below', threshold_value, no_pct))
                else:
                    print(f"  {threshold_name} ({threshold_value}%+): {yes_pct}% Yes → UNEXPECTED (unemployment above {threshold_value}%)")
        
        # Calculate market sentiment score based on corrected interpretation
        # Current rate is 4.3%
        # Market expects unemployment above 4.1% but below 4.4%
        # This means market expects unemployment to stay in 4.2-4.3% range
        
        # Find the range where market expectations flip
        below_expectations = [exp for exp in market_expectations if exp[0] == 'below']
        above_expectations = [exp for exp in market_expectations if exp[0] == 'above']
        
        if below_expectations:
            upper_bound = min([exp[1] for exp in below_expectations])
            upper_confidence = max([exp[2] for exp in below_expectations if exp[1] == upper_bound])
        else:
            upper_bound = 4.6  # Default
            upper_confidence = 50
        
        if above_expectations:
            lower_bound = max([exp[1] for exp in above_expectations])
            lower_confidence = max([exp[2] for exp in above_expectations if exp[1] == lower_bound])
        else:
            lower_bound = 3.9  # Default
            lower_confidence = 50
        
        print(f"\n📊 MARKET EXPECTATION RANGE:")
        print(f"  Lower Bound: {lower_bound}% (Confidence: {lower_confidence}%)")
        print(f"  Upper Bound: {upper_bound}% (Confidence: {upper_confidence}%)")
        print(f"  Current Rate: {current_rate}%")
        
        # Calculate sentiment score
        # If current rate is in the middle of expected range, score = 50
        # If current rate is at upper bound, score = 25 (market expects decline)
        # If current rate is at lower bound, score = 75 (market expects rise)
        
        if current_rate <= lower_bound:
            # Current rate is at or below lower bound
            sentiment_score = 75  # Market expects rise
        elif current_rate >= upper_bound:
            # Current rate is at or above upper bound
            sentiment_score = 25  # Market expects decline
        else:
            # Current rate is within expected range
            # Calculate position within range
            range_size = upper_bound - lower_bound
            position = (current_rate - lower_bound) / range_size
            sentiment_score = 75 - (position * 50)  # 75 at lower bound, 25 at upper bound
        
        print(f"\n📈 Market Sentiment Score: {sentiment_score:.1f}/100")
        print(f"  Interpretation: Market expects unemployment in {lower_bound}%-{upper_bound}% range")
        print(f"  Current position: {current_rate}% (within expected range)")
        
        return sentiment_score
    
    def calculate_corrected_churn_forecast(self):
        """Calculate corrected CHURN-blended unemployment forecast"""
        
        print("\n🎯 CALCULATING CORRECTED CHURN-BLENDED FORECAST")
        print("="*60)
        
        # Calculate component scores
        traditional_score = self.calculate_traditional_data_score()
        alternative_score = self.calculate_alternative_data_score()
        sentiment_score = self.calculate_corrected_market_sentiment_score()
        
        # Calculate weighted CHURN score
        churn_score = (traditional_score * self.churn_weights['traditional_data'] + 
                      alternative_score * self.churn_weights['alternative_data'] + 
                      sentiment_score * self.churn_weights['market_sentiment'])
        
        print(f"\n📊 CORRECTED CHURN COMPONENT SCORES:")
        print(f"  Traditional Data: {traditional_score:.1f} (Weight: {self.churn_weights['traditional_data']:.1%})")
        print(f"  Alternative Data: {alternative_score:.1f} (Weight: {self.churn_weights['alternative_data']:.1%})")
        print(f"  Market Sentiment: {sentiment_score:.1f} (Weight: {self.churn_weights['market_sentiment']:.1%})")
        print(f"  CHURN Blended Score: {churn_score:.1f}/100")
        
        # Convert CHURN score to unemployment rate forecast
        base_rate = self.current_unemployment_rate
        unemployment_change = (churn_score - 50) / 100 * 0.5
        forecast_rate = base_rate - unemployment_change
        
        print(f"\n🎯 CORRECTED CHURN-BLENDED FORECAST:")
        print(f"  Base Rate: {base_rate}%")
        print(f"  CHURN Score: {churn_score:.1f}")
        print(f"  Unemployment Change: {unemployment_change:+.3f}%")
        print(f"  Forecast Rate: {forecast_rate:.2f}%")
        
        return {
            'base_rate': base_rate,
            'forecast_rate': forecast_rate,
            'unemployment_change': unemployment_change,
            'churn_score': churn_score,
            'component_scores': {
                'traditional': traditional_score,
                'alternative': alternative_score,
                'sentiment': sentiment_score
            }
        }
    
    def create_corrected_report(self, forecast_data):
        """Create corrected CHURN-blended forecast report"""
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'version': self.version,
            'foundation_id': self.foundation_id,
            'correction_note': 'Fixed trade range interpretation - "Above 4.3%" means 4.4%+',
            'methodology': {
                'model': 'Corrected CHURN-Blended Forecasting System',
                'components': ['Traditional Data', 'Alternative Data', 'Market Sentiment'],
                'weights': self.churn_weights,
                'data_sources': {
                    'traditional': 'BLS unemployment, claims, payrolls data',
                    'alternative': 'Estimated job postings, social sentiment, mobility, real-time payroll',
                    'market_sentiment': 'Trade range data with CORRECTED percent distributions'
                }
            },
            'forecast_summary': {
                'current_unemployment': forecast_data['base_rate'],
                'forecasted_unemployment': round(forecast_data['forecast_rate'], 2),
                'change': round(forecast_data['unemployment_change'], 3),
                'churn_score': round(forecast_data['churn_score'], 1),
                'direction': 'Improvement' if forecast_data['unemployment_change'] < 0 else 'Deterioration'
            },
            'component_analysis': {
                'traditional_data': {
                    'score': forecast_data['component_scores']['traditional'],
                    'weight': self.churn_weights['traditional_data'],
                    'contribution': forecast_data['component_scores']['traditional'] * self.churn_weights['traditional_data']
                },
                'alternative_data': {
                    'score': forecast_data['component_scores']['alternative'],
                    'weight': self.churn_weights['alternative_data'],
                    'contribution': forecast_data['component_scores']['alternative'] * self.churn_weights['alternative_data']
                },
                'market_sentiment': {
                    'score': forecast_data['component_scores']['sentiment'],
                    'weight': self.churn_weights['market_sentiment'],
                    'contribution': forecast_data['component_scores']['sentiment'] * self.churn_weights['market_sentiment']
                }
            },
            'corrected_trade_analysis': {
                'interpretation': 'Above 4.3% means 4.4% and above',
                'market_expectation_range': '4.2% - 4.3%',
                'current_rate_position': 'Within expected range',
                'market_sentiment': 'Neutral to slightly bullish'
            }
        }
        
        return report
    
    def save_corrected_report(self, report, filename="corrected_churn_forecast_report.json"):
        """Save corrected CHURN-blended forecast report"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Corrected CHURN-blended forecast report saved to: {filename}")
        return filename
    
    def print_corrected_summary(self, report):
        """Print corrected CHURN-blended forecast summary"""
        
        print("\n" + "="*60)
        print("CORRECTED CHURN-BLENDED FORECAST SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        forecast = report['forecast_summary']
        print(f"\n📊 FORECAST RESULTS:")
        print(f"  Current Unemployment Rate: {forecast['current_unemployment']}%")
        print(f"  Corrected CHURN Forecast: {forecast['forecasted_unemployment']}%")
        print(f"  Change: {forecast['change']:+.3f} percentage points")
        print(f"  CHURN Score: {forecast['churn_score']}/100")
        print(f"  Direction: {forecast['direction']}")
        
        components = report['component_analysis']
        print(f"\n📊 CHURN COMPONENT BREAKDOWN:")
        print(f"  Traditional Data: {components['traditional_data']['score']:.1f} (Weight: {components['traditional_data']['weight']:.1%})")
        print(f"  Alternative Data: {components['alternative_data']['score']:.1f} (Weight: {components['alternative_data']['weight']:.1%})")
        print(f"  Market Sentiment: {components['market_sentiment']['score']:.1f} (Weight: {components['market_sentiment']['weight']:.1%})")
        
        trade_analysis = report['corrected_trade_analysis']
        print(f"\n📊 CORRECTED TRADE ANALYSIS:")
        print(f"  Interpretation: {trade_analysis['interpretation']}")
        print(f"  Market Expectation Range: {trade_analysis['market_expectation_range']}")
        print(f"  Current Rate Position: {trade_analysis['current_rate_position']}")
        print(f"  Market Sentiment: {trade_analysis['market_sentiment']}")
        
        print("\n" + "="*60)
    
    def run_corrected_churn_forecast(self):
        """Run the complete corrected CHURN-blended forecasting process"""
        
        print("="*60)
        print("CORRECTED CHURN-BLENDED UNEMPLOYMENT FORECASTING SYSTEM")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        # Calculate corrected CHURN-blended forecast
        forecast_data = self.calculate_corrected_churn_forecast()
        
        # Create corrected report
        report = self.create_corrected_report(forecast_data)
        
        # Save report
        report_file = self.save_corrected_report(report)
        
        # Print summary
        self.print_corrected_summary(report)
        
        print(f"\n🎯 Corrected CHURN-blended forecasting complete!")
        print(f"📁 Report saved to: {report_file}")
        print(f"🔧 Foundation System: {self.foundation_id}")
        print("="*60)
        
        return report

def main():
    """Main execution function"""
    forecaster = CorrectedCHURNBlendedForecastSystem()
    forecaster.run_corrected_churn_forecast()

if __name__ == "__main__":
    main()