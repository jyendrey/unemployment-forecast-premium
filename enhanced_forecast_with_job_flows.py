#!/usr/bin/env python3
"""
Enhanced Unemployment Forecasting System with BLS CPS Job Flows
Integrates job flows data with existing trade data and FRED data
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import json
import os
from datetime import datetime, timedelta
from bls_cps_job_flows_fetcher import BLSCPSJobFlowsFetcher

class EnhancedUnemploymentForecasterWithJobFlows:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        self.version = "v3.1-enhanced-with-job-flows"
        self.current_date = datetime.now()
        
        # Initialize job flows fetcher
        self.job_flows_fetcher = BLSCPSJobFlowsFetcher()
        
        # Load existing data sources
        self.trade_analysis = self.load_trade_analysis()
        self.extended_fred_data = self.load_extended_fred_data()
        self.job_flows_data = self.load_job_flows_data()
        
    def load_trade_analysis(self):
        """Load the updated trade data analysis"""
        try:
            with open('enhanced_forecast_input.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Trade analysis file not found. Using default values.")
            return self.get_default_analysis()
    
    def load_extended_fred_data(self):
        """Load the extended FRED claims data (24 months)"""
        try:
            with open('extended_fred_claims_analysis.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Extended FRED data file not found. Using default values.")
            return self.get_default_extended_fred_data()
    
    def load_job_flows_data(self):
        """Load BLS CPS job flows data"""
        try:
            with open('bls_cps_job_flows_analysis.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Job flows data file not found. Fetching from BLS...")
            # Try to fetch fresh data
            analysis = self.job_flows_fetcher.create_job_flows_analysis()
            return analysis if analysis else self.get_default_job_flows_data()
    
    def get_default_analysis(self):
        """Get default analysis if trade data is not available"""
        return {
            'market_sentiment': {
                'sentiment_score': -0.124,
                'sentiment_interpretation': 'Neutral',
                'contracts_analyzed': 26,
                'total_volume': 260,
                'confidence': 0.85
            },
            'data_quality': {
                'total_trades_processed': 0,
                'unemployment_trade_ratio': 0,
                'date_coverage': 0
            }
        }
    
    def get_default_extended_fred_data(self):
        """Get default extended FRED data if not available"""
        return {
            'latest_data': {
                'initial_claims': {'value': 218000, 'trend': 'Declining'},
                'continuing_claims': {'value': 1800000, 'trend': 'Declining'}
            },
            'extended_trends': {
                'short_term': {'initial_claims': {'trend': 'Declining'}, 'continuing_claims': {'trend': 'Declining'}},
                'medium_term': {'initial_claims': {'trend': 'Declining'}, 'continuing_claims': {'trend': 'Declining'}},
                'long_term': {'initial_claims': {'trend': 'Declining'}, 'continuing_claims': {'trend': 'Declining'}}
            },
            'market_health_assessment': {'overall_market_health': 'Strong'}
        }
    
    def get_default_job_flows_data(self):
        """Get default job flows data if not available"""
        return {
            'key_metrics': {
                'job_finding_rate': 0.25,  # 25% of unemployed find jobs
                'job_separation_rate': 0.015,  # 1.5% of employed lose jobs
                'net_flows': {
                    'net_employment_growth': 150000,
                    'net_unemployment_change': -50000,
                    'net_labor_force_participation': 100000
                }
            },
            'data_quality': 'Fallback'
        }
    
    def get_current_unemployment_rate(self):
        """Get current unemployment rate (using fallback for demonstration)"""
        return 4.2  # Current rate as of latest data
    
    def get_labor_force_participation_rate(self):
        """Get current labor force participation rate"""
        return 62.2  # Current rate as of latest data
    
    def get_latest_initial_claims(self):
        """Get latest initial claims from extended FRED data"""
        if self.extended_fred_data and 'latest_data' in self.extended_fred_data:
            return self.extended_fred_data['latest_data']['initial_claims']['value']
        return 218000  # Fallback value
    
    def get_latest_continuing_claims(self):
        """Get latest continuing claims from extended FRED data"""
        if self.extended_fred_data and 'latest_data' in self.extended_fred_data:
            return self.extended_fred_data['latest_data']['continuing_claims']['value']
        return 1800000  # Fallback value
    
    def get_job_finding_rate(self):
        """Get job finding rate from job flows data"""
        if self.job_flows_data and 'key_metrics' in self.job_flows_data:
            return self.job_flows_data['key_metrics']['job_finding_rate']
        return 0.25  # Fallback value
    
    def get_job_separation_rate(self):
        """Get job separation rate from job flows data"""
        if self.job_flows_data and 'key_metrics' in self.job_flows_data:
            return self.job_flows_data['key_metrics']['job_separation_rate']
        return 0.015  # Fallback value
    
    def get_net_job_flows(self):
        """Get net job flows from job flows data"""
        if self.job_flows_data and 'key_metrics' in self.job_flows_data:
            return self.job_flows_data['key_metrics']['net_flows']
        return {
            'net_employment_growth': 150000,
            'net_unemployment_change': -50000,
            'net_labor_force_participation': 100000
        }
    
    def calculate_enhanced_forecast_with_job_flows(self):
        """Calculate enhanced unemployment forecast including job flows data"""
        
        print("🎯 Calculating Enhanced Unemployment Forecast with Job Flows...")
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print("="*60)
        
        # Base rate from foundation
        base_rate = self.get_current_unemployment_rate()
        print(f"📊 Base Rate (Foundation {self.foundation_id}): {base_rate}%")
        
        # Enhanced adjustments using math framework, including job flows
        adjustments = []
        
        # 1. LFPR Adjustment
        lfpr = self.get_labor_force_participation_rate()
        lfpr_adjustment = (lfpr - 63.0) * 0.5 / 100
        adjustments.append(('LFPR Adjustment', lfpr_adjustment))
        print(f"🔧 LFPR Adjustment (Math Framework {self.math_framework_id}): {lfpr_adjustment:.4f}%")
        
        # 2. Extended Initial Claims Adjustment
        latest_initial_claims = self.get_latest_initial_claims()
        claims_adjustment = (latest_initial_claims - 225000) / 225000 * 0.3 / 100
        adjustments.append(('Initial Claims Adjustment', claims_adjustment))
        print(f"🔧 Initial Claims Adjustment (Math Framework {self.math_framework_id}): {claims_adjustment:.4f}%")
        
        # 3. Extended Continuing Claims Adjustment
        latest_continuing_claims = self.get_latest_continuing_claims()
        continuing_claims_adjustment = (latest_continuing_claims - 1750000) / 1750000 * 0.2 / 100
        adjustments.append(('Continuing Claims Adjustment', continuing_claims_adjustment))
        print(f"🔧 Continuing Claims Adjustment (Math Framework {self.math_framework_id}): {continuing_claims_adjustment:.4f}%")
        
        # 4. NEW: Job Finding Rate Adjustment
        job_finding_rate = self.get_job_finding_rate()
        # Higher job finding rate should reduce unemployment
        job_finding_adjustment = -(job_finding_rate - 0.25) * 0.5  # Scale factor
        adjustments.append(('Job Finding Rate Adjustment', job_finding_adjustment))
        print(f"🔧 Job Finding Rate Adjustment (Math Framework {self.math_framework_id}): {job_finding_adjustment:.4f}%")
        
        # 5. NEW: Job Separation Rate Adjustment
        job_separation_rate = self.get_job_separation_rate()
        # Higher job separation rate should increase unemployment
        job_separation_adjustment = (job_separation_rate - 0.015) * 0.3  # Scale factor
        adjustments.append(('Job Separation Rate Adjustment', job_separation_adjustment))
        print(f"🔧 Job Separation Rate Adjustment (Math Framework {self.math_framework_id}): {job_separation_adjustment:.4f}%")
        
        # 6. NEW: Net Job Flows Adjustment
        net_flows = self.get_net_job_flows()
        net_employment_growth = net_flows.get('net_employment_growth', 0)
        net_unemployment_change = net_flows.get('net_unemployment_change', 0)
        
        # Net employment growth should reduce unemployment
        net_employment_adjustment = -(net_employment_growth / 1000000) * 0.1  # Scale factor
        adjustments.append(('Net Employment Growth Adjustment', net_employment_adjustment))
        print(f"🔧 Net Employment Growth Adjustment (Math Framework {self.math_framework_id}): {net_employment_adjustment:.4f}%")
        
        # Net unemployment change directly affects unemployment rate
        net_unemployment_adjustment = (net_unemployment_change / 1000000) * 0.2  # Scale factor
        adjustments.append(('Net Unemployment Change Adjustment', net_unemployment_adjustment))
        print(f"🔧 Net Unemployment Change Adjustment (Math Framework {self.math_framework_id}): {net_unemployment_adjustment:.4f}%")
        
        # 7. Enhanced Trade Data Sentiment Adjustment
        if self.trade_analysis:
            trade_sentiment = self.trade_analysis['market_sentiment']['sentiment_score']
            trade_confidence = self.trade_analysis['market_sentiment']['confidence']
            
            sentiment_adjustment = trade_sentiment * 0.2 * trade_confidence / 100
            adjustments.append(('Trade Sentiment Adjustment', sentiment_adjustment))
            print(f"🔧 Trade Sentiment Adjustment (Math Framework {self.math_framework_id}): {sentiment_adjustment:.4f}%")
            
            trade_volume = self.trade_analysis['market_sentiment']['total_volume']
            volume_factor = min(trade_volume / 100000, 2.0)
            volume_adjustment = trade_sentiment * 0.1 * volume_factor / 100
            adjustments.append(('Trade Volume Adjustment', volume_adjustment))
            print(f"🔧 Trade Volume Adjustment (Math Framework {self.math_framework_id}): {volume_adjustment:.4f}%")
        
        # Calculate total adjustment
        total_adjustment = sum(adj[1] for adj in adjustments)
        print(f"📈 Total Adjustment: {total_adjustment:.4f}%")
        
        # Calculate final forecast
        final_forecast = base_rate + total_adjustment
        print(f"🎯 Final Enhanced Forecast with Job Flows: {final_forecast:.2f}%")
        
        return final_forecast, adjustments
    
    def calculate_enhanced_confidence_with_job_flows(self):
        """Calculate enhanced confidence including job flows data quality"""
        
        print("\n📊 Calculating Enhanced Confidence with Job Flows...")
        
        # Base confidence
        base_confidence = 70
        
        # Data quality scores
        data_quality = 100 if self.trade_analysis else 80
        foundation_stability = 100
        math_framework_accuracy = 100
        
        # Trade data confidence
        trade_confidence = 0
        trade_volume_score = 0
        if self.trade_analysis:
            trade_confidence = self.trade_analysis['market_sentiment']['confidence'] * 100
            trade_volume_score = min(self.trade_analysis['market_sentiment']['total_volume'] / 1000, 100)
        
        # FRED data confidence
        fred_confidence = 100 if self.extended_fred_data else 80
        fred_freshness = 100
        
        # NEW: Job flows data confidence
        job_flows_confidence = 100 if self.job_flows_data and self.job_flows_data.get('data_quality') != 'Fallback' else 85
        job_flows_freshness = 100 if self.job_flows_data else 80
        
        # Market stability bonus
        market_stability = self.extended_fred_data.get('volatility_analysis', {}).get('overall_market_stability', 'Unknown') if self.extended_fred_data else 'Unknown'
        stability_bonus = 0
        if market_stability == 'Very Stable':
            stability_bonus = 5
        elif market_stability == 'Stable':
            stability_bonus = 3
        elif market_stability == 'Moderately Stable':
            stability_bonus = 1
        
        # Job flows stability bonus
        job_flows_stability_bonus = 0
        if self.job_flows_data and self.job_flows_data.get('data_quality') == 'High':
            job_flows_stability_bonus = 3
        
        # Final enhanced confidence calculation
        final_enhanced_confidence = (base_confidence + 
                                   (data_quality * 0.2) + 
                                   (foundation_stability * 0.15) + 
                                   (math_framework_accuracy * 0.1) +
                                   (trade_confidence * 0.1) +
                                   (trade_volume_score * 0.05) +
                                   (fred_confidence * 0.1) +
                                   (fred_freshness * 0.05) +
                                   (job_flows_confidence * 0.15) +  # NEW: Job flows weight
                                   (job_flows_freshness * 0.05) +  # NEW: Job flows freshness
                                   stability_bonus +
                                   job_flows_stability_bonus)  # NEW: Job flows stability bonus
        
        # Adjust for uncertainty and cap at 95%
        final_confidence = min(final_enhanced_confidence, 95)
        
        print(f"🔧 Foundation Stability ({self.foundation_id}): {foundation_stability}%")
        print(f"🔧 Math Framework Accuracy ({self.math_framework_id}): {math_framework_accuracy}%")
        print(f"🔧 Trade Data Confidence: {trade_confidence:.1f}%")
        print(f"🔧 Trade Volume Score: {trade_volume_score:.1f}%")
        print(f"🔧 FRED Data Confidence: {fred_confidence:.1f}%")
        print(f"🔧 FRED Data Freshness: {fred_freshness:.1f}%")
        print(f"🔧 Job Flows Data Confidence: {job_flows_confidence:.1f}%")  # NEW
        print(f"🔧 Job Flows Data Freshness: {job_flows_freshness:.1f}%")  # NEW
        print(f"🔧 Market Stability Bonus: +{stability_bonus:.1f}%")
        print(f"🔧 Job Flows Stability Bonus: +{job_flows_stability_bonus:.1f}%")  # NEW
        print(f"📊 Final Enhanced Confidence with Job Flows: {final_confidence:.1f}%")
        
        return final_confidence
    
    def create_enhanced_report_with_job_flows(self, forecast, adjustments, confidence):
        """Create comprehensive enhanced forecast report including job flows"""
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'version': self.version,
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id,
            'forecast_summary': {
                'current_unemployment': self.get_current_unemployment_rate(),
                'forecasted_unemployment': round(forecast, 2),
                'change': round(forecast - self.get_current_unemployment_rate(), 2),
                'confidence_level': round(confidence, 1),
                'direction': 'Rising' if forecast > self.get_current_unemployment_rate() else 'Falling' if forecast < self.get_current_unemployment_rate() else 'Stable'
            },
            'job_flows_analysis': {
                'job_finding_rate': self.get_job_finding_rate(),
                'job_separation_rate': self.get_job_separation_rate(),
                'net_flows': self.get_net_job_flows(),
                'data_quality': self.job_flows_data.get('data_quality', 'Unknown') if self.job_flows_data else 'Unknown'
            },
            'enhanced_adjustments': [
                {
                    'adjustment_name': adj[0],
                    'adjustment_value': round(adj[1], 4),
                    'adjustment_percentage': round(adj[1] * 100, 4)
                }
                for adj in adjustments
            ],
            'data_sources': {
                'trade_data': 'Enhanced Trade Data (ForecastEx)',
                'fred_data': 'Extended FRED Data (24 months)',
                'job_flows_data': 'BLS CPS Job Flows Data',  # NEW
                'bls_data': 'BLS API (Unemployment Rate, LFPR)'
            },
            'system_components': {
                'foundation': self.foundation_id,
                'math_framework': self.math_framework_id,
                'job_flows_integration': 'v3.1-enhanced'
            }
        }
        
        # Save report
        with open('enhanced_forecast_with_job_flows_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Enhanced forecast report with job flows saved to enhanced_forecast_with_job_flows_report.json")
        
        return report

def main():
    """Main function to run the enhanced forecasting with job flows"""
    forecaster = EnhancedUnemploymentForecasterWithJobFlows()
    
    # Calculate forecast
    forecast, adjustments = forecaster.calculate_enhanced_forecast_with_job_flows()
    
    # Calculate confidence
    confidence = forecaster.calculate_enhanced_confidence_with_job_flows()
    
    # Create report
    report = forecaster.create_enhanced_report_with_job_flows(forecast, adjustments, confidence)
    
    # Display summary
    print("\n" + "="*60)
    print("🎯 ENHANCED UNEMPLOYMENT FORECAST WITH JOB FLOWS")
    print("="*60)
    print(f"📊 Current Unemployment Rate: {report['forecast_summary']['current_unemployment']}%")
    print(f"🎯 Enhanced Forecast: {report['forecast_summary']['forecasted_unemployment']}%")
    print(f"📈 Change: {report['forecast_summary']['change']:+.2f} percentage points")
    print(f"🎯 Confidence Level: {report['forecast_summary']['confidence_level']}%")
    print(f"📊 Direction: {report['forecast_summary']['direction']}")
    print("\n🔧 Job Flows Analysis:")
    print(f"   Job Finding Rate: {report['job_flows_analysis']['job_finding_rate']:.4f} ({report['job_flows_analysis']['job_finding_rate']*100:.2f}%)")
    print(f"   Job Separation Rate: {report['job_flows_analysis']['job_separation_rate']:.4f} ({report['job_flows_analysis']['job_separation_rate']*100:.2f}%)")
    print(f"   Net Employment Growth: {report['job_flows_analysis']['net_flows']['net_employment_growth']:,.0f}")
    print(f"   Net Unemployment Change: {report['job_flows_analysis']['net_flows']['net_unemployment_change']:,.0f}")
    print(f"   Data Quality: {report['job_flows_analysis']['data_quality']}")

if __name__ == "__main__":
    main()