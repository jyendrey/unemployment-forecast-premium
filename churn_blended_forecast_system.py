#!/usr/bin/env python3
"""
CHURN-Blended Unemployment Forecasting System
Integrates Chicago Fed CHURN model elements with trade data and percent ranges
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import json
from datetime import datetime
import statistics

class CHURNBlendedForecastSystem:
    def __init__(self):
        self.foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.version = "v3.0-churn-blended"
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
        
        # Market Sentiment Data (Our Trade Data)
        self.market_sentiment = {
            "Above 3.9%": {"Yes": 97, "No": 3},
            "Above 4.0%": {"Yes": 92, "No": 6},
            "Above 4.1%": {"Yes": 73, "No": 25},
            "Above 4.2%": {"Yes": 50, "No": 48},
            "Above 4.3%": {"Yes": 28, "No": 70},
            "Above 4.4%": {"Yes": 16, "No": 84},
            "Above 4.5%": {"Yes": 8, "No": 92}
        }
        
        # CHURN Model Weights (based on Fed methodology)
        self.churn_weights = {
            'traditional_data': 0.4,  # 40% weight to traditional data
            'alternative_data': 0.3,  # 30% weight to alternative data
            'market_sentiment': 0.3   # 30% weight to market sentiment
        }
    
    def estimate_job_postings(self):
        """Estimate online job postings trend (alternative data)"""
        # Based on current labor market conditions
        # Rising unemployment typically correlates with declining job postings
        base_job_postings = 100  # Index base
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -5  # -5 points per 0.1% unemployment
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.1  # Negative impact from rising claims
        
        job_postings_index = base_job_postings + unemployment_impact + claims_impact
        return max(job_postings_index, 50)  # Floor at 50
    
    def estimate_social_sentiment(self):
        """Estimate social media employment sentiment (alternative data)"""
        # Based on unemployment rate and claims data
        # Higher unemployment typically correlates with negative sentiment
        base_sentiment = 50  # Neutral
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -10  # -10 points per 0.1% unemployment
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.2  # Negative impact from rising claims
        
        sentiment_index = base_sentiment + unemployment_impact + claims_impact
        return max(min(sentiment_index, 100), 0)  # Clamp between 0-100
    
    def estimate_mobility_data(self):
        """Estimate mobility/commuting data (alternative data)"""
        # Based on unemployment and claims data
        # Higher unemployment typically correlates with reduced mobility
        base_mobility = 100  # Normal mobility
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -15  # -15 points per 0.1% unemployment
        claims_impact = (self.traditional_data['initial_claims'] - 225000) / 1000 * -0.3  # Negative impact from rising claims
        
        mobility_index = base_mobility + unemployment_impact + claims_impact
        return max(mobility_index, 20)  # Floor at 20
    
    def estimate_real_time_payroll(self):
        """Estimate real-time payroll data (alternative data)"""
        # Based on payrolls revision and current conditions
        # Negative revision suggests weaker real-time payroll growth
        base_payroll_growth = 2.0  # 2% annual growth
        revision_impact = self.traditional_data['payrolls_revision'] / 1000000 * -0.5  # -0.5% per 1M revision
        unemployment_impact = (self.current_unemployment_rate - 4.0) * -0.2  # -0.2% per 0.1% unemployment
        
        payroll_growth = base_payroll_growth + revision_impact + unemployment_impact
        return max(payroll_growth, -2.0)  # Floor at -2%
    
    def calculate_traditional_data_score(self):
        """Calculate traditional data component score (CHURN methodology)"""
        
        print("🔍 CALCULATING TRADITIONAL DATA SCORE (CHURN Component 1)")
        print("="*60)
        
        # Unemployment rate component (40% of traditional score)
        unemployment_score = max(0, 100 - (self.traditional_data['unemployment_rate'] - 3.5) * 20)
        print(f"📊 Unemployment Rate: {self.traditional_data['unemployment_rate']}% → Score: {unemployment_score:.1f}")
        
        # Initial claims component (30% of traditional score)
        claims_normalized = max(0, 100 - (self.traditional_data['initial_claims'] - 200000) / 1000)
        print(f"📊 Initial Claims: {self.traditional_data['initial_claims']:,} → Score: {claims_normalized:.1f}")
        
        # Continuing claims component (20% of traditional score)
        continuing_normalized = max(0, 100 - (self.traditional_data['continuing_claims'] - 1500000) / 10000)
        print(f"📊 Continuing Claims: {self.traditional_data['continuing_claims']:,} → Score: {continuing_normalized:.1f}")
        
        # Labor force participation component (10% of traditional score)
        lfpr_score = max(0, (self.traditional_data['labor_force_participation'] - 60) * 2)
        print(f"📊 Labor Force Participation: {self.traditional_data['labor_force_participation']}% → Score: {lfpr_score:.1f}")
        
        # Weighted traditional data score
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
        
        # Online job postings component (30% of alternative score)
        job_postings_score = self.alternative_data['online_job_postings']
        print(f"📊 Online Job Postings Index: {job_postings_score:.1f}")
        
        # Social media sentiment component (25% of alternative score)
        social_sentiment_score = self.alternative_data['social_media_sentiment']
        print(f"📊 Social Media Sentiment: {social_sentiment_score:.1f}")
        
        # Mobility data component (25% of alternative score)
        mobility_score = self.alternative_data['mobility_data']
        print(f"📊 Mobility/Commuting Index: {mobility_score:.1f}")
        
        # Real-time payroll component (20% of alternative score)
        payroll_growth = self.alternative_data['real_time_payroll']
        payroll_score = max(0, min(100, 50 + payroll_growth * 10))  # Convert to 0-100 scale
        print(f"📊 Real-time Payroll Growth: {payroll_growth:.1f}% → Score: {payroll_score:.1f}")
        
        # Weighted alternative data score
        alternative_score = (job_postings_score * 0.30 + 
                           social_sentiment_score * 0.25 + 
                           mobility_score * 0.25 + 
                           payroll_score * 0.20)
        
        print(f"\n📈 Alternative Data Score: {alternative_score:.1f}/100")
        return alternative_score
    
    def calculate_market_sentiment_score(self):
        """Calculate market sentiment component score (Our Trade Data)"""
        
        print("\n🔍 CALCULATING MARKET SENTIMENT SCORE (Trade Data Component)")
        print("="*60)
        
        # Analyze market expectations
        current_rate = self.current_unemployment_rate
        market_expectations = []
        
        for threshold, data in self.market_sentiment.items():
            threshold_value = float(threshold.split("Above ")[1].replace("%", ""))
            yes_pct = data["Yes"]
            no_pct = data["No"]
            
            if threshold_value == current_rate:
                # Current rate analysis
                below_current = no_pct
                above_current = yes_pct
                print(f"📊 At Current Rate ({threshold_value}%): {yes_pct}% expect above, {no_pct}% expect below")
            elif threshold_value < current_rate:
                if yes_pct > 50:
                    market_expectations.append(('above', threshold_value, yes_pct))
            else:
                if no_pct > 50:
                    market_expectations.append(('below', threshold_value, no_pct))
        
        # Calculate market sentiment score
        # Higher score = market expects lower unemployment
        # Lower score = market expects higher unemployment
        
        # Base score from current rate expectations
        if current_rate in [float(t.split("Above ")[1].replace("%", "")) for t in self.market_sentiment.keys()]:
            # Market is split on current rate
            sentiment_score = 50  # Neutral
        else:
            # Calculate based on market expectations
            sentiment_score = 50  # Default neutral
        
        # Adjust based on market expectations
        for expectation, threshold, confidence in market_expectations:
            if expectation == 'below':
                # Market expects unemployment below this threshold
                if threshold > current_rate:
                    # Market expects unemployment to decline
                    sentiment_score += confidence * 0.1
            elif expectation == 'above':
                # Market expects unemployment above this threshold
                if threshold < current_rate:
                    # Market expects unemployment to rise
                    sentiment_score -= confidence * 0.1
        
        sentiment_score = max(0, min(100, sentiment_score))
        
        print(f"\n📈 Market Sentiment Score: {sentiment_score:.1f}/100")
        return sentiment_score
    
    def calculate_churn_blended_forecast(self):
        """Calculate CHURN-blended unemployment forecast"""
        
        print("\n🎯 CALCULATING CHURN-BLENDED FORECAST")
        print("="*60)
        
        # Calculate component scores
        traditional_score = self.calculate_traditional_data_score()
        alternative_score = self.calculate_alternative_data_score()
        sentiment_score = self.calculate_market_sentiment_score()
        
        # Calculate weighted CHURN score
        churn_score = (traditional_score * self.churn_weights['traditional_data'] + 
                      alternative_score * self.churn_weights['alternative_data'] + 
                      sentiment_score * self.churn_weights['market_sentiment'])
        
        print(f"\n📊 CHURN COMPONENT SCORES:")
        print(f"  Traditional Data: {traditional_score:.1f} (Weight: {self.churn_weights['traditional_data']:.1%})")
        print(f"  Alternative Data: {alternative_score:.1f} (Weight: {self.churn_weights['alternative_data']:.1%})")
        print(f"  Market Sentiment: {sentiment_score:.1f} (Weight: {self.churn_weights['market_sentiment']:.1%})")
        print(f"  CHURN Blended Score: {churn_score:.1f}/100")
        
        # Convert CHURN score to unemployment rate forecast
        # Higher CHURN score = lower unemployment rate
        # Lower CHURN score = higher unemployment rate
        
        # Base unemployment rate
        base_rate = self.current_unemployment_rate
        
        # Convert score to unemployment rate change
        # Score of 100 = -0.5% unemployment change
        # Score of 0 = +0.5% unemployment change
        # Score of 50 = no change
        
        unemployment_change = (churn_score - 50) / 100 * 0.5
        forecast_rate = base_rate - unemployment_change
        
        print(f"\n🎯 CHURN-BLENDED FORECAST:")
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
    
    def create_churn_report(self, forecast_data):
        """Create CHURN-blended forecast report"""
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'version': self.version,
            'foundation_id': self.foundation_id,
            'methodology': {
                'model': 'CHURN-Blended Forecasting System',
                'components': ['Traditional Data', 'Alternative Data', 'Market Sentiment'],
                'weights': self.churn_weights,
                'data_sources': {
                    'traditional': 'BLS unemployment, claims, payrolls data',
                    'alternative': 'Estimated job postings, social sentiment, mobility, real-time payroll',
                    'market_sentiment': 'Trade range data with percent distributions'
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
            'data_inputs': {
                'traditional_data': self.traditional_data,
                'alternative_data': self.alternative_data,
                'market_sentiment': self.market_sentiment
            }
        }
        
        return report
    
    def save_churn_report(self, report, filename="churn_blended_forecast_report.json"):
        """Save CHURN-blended forecast report"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ CHURN-blended forecast report saved to: {filename}")
        return filename
    
    def print_churn_summary(self, report):
        """Print CHURN-blended forecast summary"""
        
        print("\n" + "="*60)
        print("CHURN-BLENDED FORECAST SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        forecast = report['forecast_summary']
        print(f"\n📊 FORECAST RESULTS:")
        print(f"  Current Unemployment Rate: {forecast['current_unemployment']}%")
        print(f"  CHURN Forecast: {forecast['forecasted_unemployment']}%")
        print(f"  Change: {forecast['change']:+.3f} percentage points")
        print(f"  CHURN Score: {forecast['churn_score']}/100")
        print(f"  Direction: {forecast['direction']}")
        
        components = report['component_analysis']
        print(f"\n📊 CHURN COMPONENT BREAKDOWN:")
        print(f"  Traditional Data: {components['traditional_data']['score']:.1f} (Weight: {components['traditional_data']['weight']:.1%})")
        print(f"  Alternative Data: {components['alternative_data']['score']:.1f} (Weight: {components['alternative_data']['weight']:.1%})")
        print(f"  Market Sentiment: {components['market_sentiment']['score']:.1f} (Weight: {components['market_sentiment']['weight']:.1%})")
        
        methodology = report['methodology']
        print(f"\n📋 METHODOLOGY:")
        print(f"  Model: {methodology['model']}")
        print(f"  Components: {', '.join(methodology['components'])}")
        print(f"  Weights: Traditional {methodology['weights']['traditional_data']:.1%}, Alternative {methodology['weights']['alternative_data']:.1%}, Sentiment {methodology['weights']['market_sentiment']:.1%}")
        
        print("\n" + "="*60)
    
    def run_churn_forecast(self):
        """Run the complete CHURN-blended forecasting process"""
        
        print("="*60)
        print("CHURN-BLENDED UNEMPLOYMENT FORECASTING SYSTEM")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        # Calculate CHURN-blended forecast
        forecast_data = self.calculate_churn_blended_forecast()
        
        # Create CHURN report
        report = self.create_churn_report(forecast_data)
        
        # Save report
        report_file = self.save_churn_report(report)
        
        # Print summary
        self.print_churn_summary(report)
        
        print(f"\n🎯 CHURN-blended forecasting complete!")
        print(f"📁 Report saved to: {report_file}")
        print(f"🔧 Foundation System: {self.foundation_id}")
        print("="*60)
        
        return report

def main():
    """Main execution function"""
    forecaster = CHURNBlendedForecastSystem()
    forecaster.run_churn_forecast()

if __name__ == "__main__":
    main()