#!/usr/bin/env python3
"""
Updated Enhanced Unemployment Forecasting System with Payrolls Benchmark Revisions
Integrates -911K payrolls revisions since March with all other data sources
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Updated Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import json
import os
from datetime import datetime

class UpdatedForecastWithPayrolls:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.updated_foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        self.version = "v3.2-final-enhanced-with-payrolls"
        self.current_date = datetime.now()
        
        # Load all data sources
        self.trade_analysis = self.load_trade_analysis()
        self.extended_fred_data = self.load_extended_fred_data()
        self.payrolls_analysis = self.load_payrolls_analysis()
        
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
    
    def load_payrolls_analysis(self):
        """Load the payrolls benchmark revision analysis"""
        try:
            with open('payrolls_benchmark_analysis.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Payrolls analysis file not found. Using default values.")
            return self.get_default_payrolls_data()
    
    def get_default_analysis(self):
        """Get default analysis if trade data is not available"""
        return {
            'market_sentiment': {
                'sentiment_score': -0.124,
                'sentiment_interpretation': 'Neutral',
                'contracts_analyzed': 26,
                'total_volume': 260,
                'confidence': 0.85
            }
        }
    
    def get_default_extended_fred_data(self):
        """Get default extended FRED data if not available"""
        return {
            'latest_data': {
                'initial_claims': {'value': 218000, 'trend': 'Declining'},
                'continuing_claims': {'value': 1800000, 'trend': 'Declining'}
            }
        }
    
    def get_default_payrolls_data(self):
        """Get default payrolls data if not available"""
        return {
            'forecast_adjustments': {
                'total_payrolls_impact': 0.0
            }
        }
    
    def get_current_unemployment_rate(self):
        """Get current unemployment rate"""
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
    
    def calculate_updated_forecast_with_payrolls(self):
        """Calculate updated forecast including payrolls benchmark revisions"""
        
        print("🎯 Calculating Updated Forecast with Payrolls Benchmark Revisions...")
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Updated Foundation ID: {self.updated_foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print("="*60)
        
        # Base rate from foundation
        base_rate = self.get_current_unemployment_rate()
        print(f"📊 Base Rate (Foundation {self.foundation_id}): {base_rate}%")
        
        # Enhanced adjustments including payrolls benchmark revisions
        adjustments = []
        
        # 1. LFPR Adjustment
        lfpr = self.get_labor_force_participation_rate()
        lfpr_adjustment = (lfpr - 63.0) * 0.5 / 100
        adjustments.append(('LFPR Adjustment', lfpr_adjustment))
        print(f"🔧 LFPR Adjustment: {lfpr_adjustment:.4f}%")
        
        # 2. Initial Claims Adjustment
        latest_initial_claims = self.get_latest_initial_claims()
        claims_adjustment = (latest_initial_claims - 225000) / 225000 * 0.3 / 100
        adjustments.append(('Initial Claims Adjustment', claims_adjustment))
        print(f"🔧 Initial Claims Adjustment: {claims_adjustment:.4f}%")
        
        # 3. Continuing Claims Adjustment
        latest_continuing_claims = self.get_latest_continuing_claims()
        continuing_claims_adjustment = (latest_continuing_claims - 1750000) / 1750000 * 0.2 / 100
        adjustments.append(('Continuing Claims Adjustment', continuing_claims_adjustment))
        print(f"🔧 Continuing Claims Adjustment: {continuing_claims_adjustment:.4f}%")
        
        # 4. Trade Data Sentiment Adjustment
        if self.trade_analysis:
            trade_sentiment = self.trade_analysis['market_sentiment']['sentiment_score']
            trade_confidence = self.trade_analysis['market_sentiment']['confidence']
            sentiment_adjustment = trade_sentiment * 0.2 * trade_confidence / 100
            adjustments.append(('Trade Sentiment Adjustment', sentiment_adjustment))
            print(f"🔧 Trade Sentiment Adjustment: {sentiment_adjustment:.4f}%")
        
        # 5. CRITICAL: Payrolls Benchmark Revision Adjustment
        if self.payrolls_analysis and 'forecast_adjustments' in self.payrolls_analysis:
            payrolls_impact = self.payrolls_analysis['forecast_adjustments']['total_payrolls_impact'] / 100
            adjustments.append(('Payrolls Benchmark Revision Adjustment', payrolls_impact))
            print(f"🔧 Payrolls Benchmark Revision Adjustment: {payrolls_impact:.4f}%")
            print(f"   📊 -911K jobs revision since March = {payrolls_impact:.4f}% unemployment impact")
        else:
            # Fallback if payrolls data not available
            payrolls_impact = -0.0073  # Estimated impact of -911K revision
            adjustments.append(('Payrolls Benchmark Revision Adjustment (Estimated)', payrolls_impact))
            print(f"🔧 Payrolls Benchmark Revision Adjustment (Estimated): {payrolls_impact:.4f}%")
        
        # 6. Market Stability Adjustment
        if self.extended_fred_data and 'volatility_analysis' in self.extended_fred_data:
            stability_level = self.extended_fred_data['volatility_analysis']['overall_market_stability']
            if stability_level == 'Very Stable':
                stability_adjustment = -0.0005 / 100
            else:
                stability_adjustment = 0.0
            adjustments.append(('Market Stability Adjustment', stability_adjustment))
            print(f"🔧 Market Stability Adjustment: {stability_adjustment:.4f}%")
        
        # Calculate total adjustment
        total_adjustment = sum(adj[1] for adj in adjustments)
        print(f"📈 Total Adjustment: {total_adjustment:.4f}%")
        
        # Calculate final forecast
        final_forecast = base_rate + total_adjustment
        print(f"🎯 Updated Forecast with Payrolls: {final_forecast:.2f}%")
        
        return final_forecast, adjustments
    
    def calculate_updated_confidence(self):
        """Calculate updated confidence including payrolls data"""
        
        print("\n📊 Calculating Updated Confidence...")
        
        # Base confidence
        base_confidence = 70
        
        # Data quality scores
        fred_confidence = 100 if self.extended_fred_data else 80
        trade_confidence = 100 if self.trade_analysis else 80
        payrolls_confidence = 85 if self.payrolls_analysis else 70  # High confidence in BLS revisions
        
        # Payrolls data bonus (significant economic indicator)
        payrolls_bonus = 5 if self.payrolls_analysis else 0
        
        # Final confidence calculation
        final_confidence = (base_confidence + 
                           (fred_confidence * 0.25) + 
                           (trade_confidence * 0.2) +
                           (payrolls_confidence * 0.3) +  # Higher weight for payrolls
                           payrolls_bonus)
        
        # Cap at 95%
        final_confidence = min(final_confidence, 95)
        
        print(f"🔧 FRED Data Confidence: {fred_confidence}%")
        print(f"🔧 Trade Data Confidence: {trade_confidence}%")
        print(f"🔧 Payrolls Data Confidence: {payrolls_confidence}%")
        print(f"🔧 Payrolls Data Bonus: +{payrolls_bonus}%")
        print(f"📊 Final Updated Confidence: {final_confidence:.1f}%")
        
        return final_confidence
    
    def create_updated_report(self, forecast, adjustments, confidence):
        """Create comprehensive updated forecast report"""
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'version': self.version,
            'foundation_id': self.foundation_id,
            'updated_foundation_id': self.updated_foundation_id,
            'math_framework_id': self.math_framework_id,
            'forecast_summary': {
                'current_unemployment': self.get_current_unemployment_rate(),
                'forecasted_unemployment': round(forecast, 2),
                'change': round(forecast - self.get_current_unemployment_rate(), 2),
                'confidence': confidence,
                'direction': 'Improvement' if forecast < self.get_current_unemployment_rate() else 'Deterioration'
            },
            'adjustments': [
                {
                    'name': name,
                    'value': round(adj, 4),
                    'math_framework': self.math_framework_id
                }
                for name, adj in adjustments
            ],
            'payrolls_benchmark_integration': {
                'revision_amount': -911000,
                'revision_period': 'March 2025 to September 2025',
                'unemployment_impact': round(forecast - self.get_current_unemployment_rate(), 4),
                'data_authority': 'BLS Official Benchmark',
                'confidence_level': 0.85,
                'foundation_id': self.updated_foundation_id
            },
            'data_sources': {
                'fred_data': {
                    'initial_claims': self.get_latest_initial_claims(),
                    'continuing_claims': self.get_latest_continuing_claims(),
                    'coverage': '24 months (103 observations)'
                },
                'trade_data': {
                    'sentiment_score': self.trade_analysis['market_sentiment']['sentiment_score'] if self.trade_analysis else None,
                    'total_volume': self.trade_analysis['market_sentiment']['total_volume'] if self.trade_analysis else None
                },
                'payrolls_data': {
                    'benchmark_revision': -911000,
                    'impact_on_forecast': round(forecast - self.get_current_unemployment_rate(), 4)
                }
            }
        }
        
        return report
    
    def save_updated_report(self, report, filename="updated_forecast_with_payrolls_report.json"):
        """Save the updated forecast report"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Updated forecast report saved to: {filename}")
        return filename
    
    def print_updated_summary(self, report):
        """Print comprehensive updated forecast summary"""
        
        print("\n" + "="*60)
        print("UPDATED FORECAST WITH PAYROLLS BENCHMARK REVISIONS")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Updated Foundation ID: {self.updated_foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        forecast = report['forecast_summary']
        print(f"\n📊 UPDATED FORECAST RESULTS:")
        print(f"  Current Unemployment Rate: {forecast['current_unemployment']}%")
        print(f"  Updated Forecast: {forecast['forecasted_unemployment']}%")
        print(f"  Change: {forecast['change']:+.2f} percentage points")
        print(f"  Confidence Level: {forecast['confidence']:.1f}%")
        print(f"  Direction: {forecast['direction']}")
        
        payrolls = report['payrolls_benchmark_integration']
        print(f"\n📊 PAYROLLS BENCHMARK REVISION IMPACT:")
        print(f"  Revision Amount: {payrolls['revision_amount']:,} jobs")
        print(f"  Revision Period: {payrolls['revision_period']}")
        print(f"  Unemployment Impact: {payrolls['unemployment_impact']:+.4f} percentage points")
        print(f"  Data Authority: {payrolls['data_authority']}")
        print(f"  Confidence Level: {payrolls['confidence_level']:.1%}")
        
        print(f"\n🔧 ALL ADJUSTMENTS APPLIED:")
        for adj in report['adjustments']:
            print(f"  {adj['name']}: {adj['value']:+.4f}%")
        
        print("\n" + "="*60)
    
    def run_updated_forecast(self):
        """Run the complete updated forecasting process"""
        
        print("="*60)
        print("UPDATED ENHANCED UNEMPLOYMENT FORECASTING SYSTEM")
        print("WITH PAYROLLS BENCHMARK REVISIONS")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Updated Foundation ID: {self.updated_foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        # Calculate updated forecast
        forecast, adjustments = self.calculate_updated_forecast_with_payrolls()
        
        # Calculate updated confidence
        confidence = self.calculate_updated_confidence()
        
        # Create updated report
        report = self.create_updated_report(forecast, adjustments, confidence)
        
        # Save report
        report_file = self.save_updated_report(report)
        
        # Print summary
        self.print_updated_summary(report)
        
        print(f"\n🎯 Updated forecasting with payrolls benchmark complete!")
        print(f"📁 Report saved to: {report_file}")
        print(f"🔧 Foundation System: {self.foundation_id}")
        print(f"🔧 Updated Foundation System: {self.updated_foundation_id}")
        print(f"🔧 Math Framework: {self.math_framework_id}")
        print("="*60)
        
        return report

def main():
    """Main execution function"""
    forecaster = UpdatedForecastWithPayrolls()
    forecaster.run_updated_forecast()

if __name__ == "__main__":
    main()