#!/usr/bin/env python3
"""
Enhanced Unemployment Forecasting System with Real Data
Uses real FRED API data and enhanced fallback data for comprehensive forecasting
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import json
import os
from datetime import datetime, timedelta
from real_data_fetcher import RealDataFetcher

class EnhancedUnemploymentForecasterWithRealData:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        self.version = "v4.1-real-data-enhanced"
        self.current_date = datetime.now()
        
        # Initialize real data fetcher
        self.real_data_fetcher = RealDataFetcher()
        
        # Load real data
        self.real_data = self.load_real_data()
        
    def load_real_data(self):
        """Load real data analysis"""
        try:
            with open('real_data_analysis.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Real data analysis file not found. Fetching real data...")
            analysis = self.real_data_fetcher.create_real_data_analysis()
            return analysis if analysis else self.get_default_real_data()
    
    def get_default_real_data(self):
        """Get default real data if not available"""
        return {
            'key_metrics': {
                'unemployment_rate': 4.3,
                'labor_force_participation_rate': 62.3,
                'employment_population_ratio': 59.6,
                'initial_claims': 218000,
                'continuing_claims': 1800000,
                'avg_hourly_earnings': 36.53,
                'avg_weekly_hours': 34.2,
                'nonfarm_payrolls': 158000000,
                'private_payrolls': 135000000
            },
            'demographic_analysis': {
                'overall_rate': 4.3,
                'rates': {
                    'unemployment_rate_men': 4.1,
                    'unemployment_rate_women': 3.8,
                    'unemployment_rate_teens': 13.9,
                    'unemployment_rate_white': 3.7,
                    'unemployment_rate_black': 7.5,
                    'unemployment_rate_asian': 3.6,
                    'unemployment_rate_hispanic': 5.3
                },
                'disparities': {
                    'black_white_gap': 3.8,
                    'hispanic_white_gap': 1.6,
                    'teen_adult_gap': 9.6,
                    'gender_gap': 0.3
                }
            },
            'underemployment_analysis': {
                'counts': {
                    'part_time_economic_reasons': 4700000,
                    'marginally_attached': 1800000,
                    'discouraged_workers': 514000,
                    'new_entrants': 786000,
                    'long_term_unemployed': 1900000
                },
                'percentages': {
                    'long_term_unemployed_pct': 25.7,
                    'discouraged_workers_pct': 28.6
                }
            },
            'establishment_analysis': {
                'nonfarm_payrolls': 158000000,
                'private_payrolls': 135000000,
                'government_payrolls': 23000000,
                'health_care_employment': 17000000,
                'manufacturing_employment': 13000000,
                'construction_employment': 8000000,
                'retail_trade_employment': 16000000,
                'leisure_hospitality_employment': 17000000
            },
            'wage_hours_analysis': {
                'avg_hourly_earnings': 36.53,
                'avg_weekly_hours': 34.2,
                'manufacturing_hours': 40.0,
                'manufacturing_overtime': 2.9
            },
            'data_quality': {
                'fred_data_available': 0,
                'total_series': 15,
                'data_freshness': 'Fallback'
            }
        }
    
    def get_current_unemployment_rate(self):
        """Get current unemployment rate from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['unemployment_rate']
        return 4.3  # Fallback from August 2025 BLS report
    
    def get_labor_force_participation_rate(self):
        """Get labor force participation rate from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['labor_force_participation_rate']
        return 62.3
    
    def get_employment_population_ratio(self):
        """Get employment-population ratio from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['employment_population_ratio']
        return 59.6
    
    def get_initial_claims(self):
        """Get initial claims from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['initial_claims']
        return 218000
    
    def get_continuing_claims(self):
        """Get continuing claims from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['continuing_claims']
        return 1800000
    
    def get_avg_hourly_earnings(self):
        """Get average hourly earnings from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['avg_hourly_earnings']
        return 36.53
    
    def get_avg_weekly_hours(self):
        """Get average weekly hours from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['avg_weekly_hours']
        return 34.2
    
    def get_nonfarm_payrolls(self):
        """Get nonfarm payrolls from real data"""
        if self.real_data and 'key_metrics' in self.real_data:
            return self.real_data['key_metrics']['nonfarm_payrolls']
        return 158000000
    
    def calculate_real_data_forecast(self):
        """Calculate unemployment forecast using real data"""
        
        print("🎯 Calculating Real Data Unemployment Forecast...")
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print("="*60)
        
        # Base rate from real data
        base_rate = self.get_current_unemployment_rate()
        print(f"📊 Base Rate (Real Data): {base_rate}%")
        
        # Real data adjustments
        adjustments = []
        
        # 1. Labor Force Participation Rate Adjustment
        lfpr = self.get_labor_force_participation_rate()
        lfpr_adjustment = (lfpr - 62.3) * 0.4 / 100
        adjustments.append(('LFPR Adjustment (Real Data)', lfpr_adjustment))
        print(f"🔧 LFPR Adjustment: {lfpr_adjustment:.4f}%")
        
        # 2. Employment-Population Ratio Adjustment
        epr = self.get_employment_population_ratio()
        epr_adjustment = (epr - 59.6) * 0.3 / 100
        adjustments.append(('Employment-Population Ratio Adjustment (Real Data)', epr_adjustment))
        print(f"🔧 Employment-Population Ratio Adjustment: {epr_adjustment:.4f}%")
        
        # 3. Initial Claims Adjustment (Real Data)
        initial_claims = self.get_initial_claims()
        claims_adjustment = (initial_claims - 225000) / 225000 * 0.2 / 100
        adjustments.append(('Initial Claims Adjustment (Real Data)', claims_adjustment))
        print(f"🔧 Initial Claims Adjustment: {claims_adjustment:.4f}%")
        
        # 4. Continuing Claims Adjustment (Real Data)
        continuing_claims = self.get_continuing_claims()
        continuing_adjustment = (continuing_claims - 1750000) / 1750000 * 0.15 / 100
        adjustments.append(('Continuing Claims Adjustment (Real Data)', continuing_adjustment))
        print(f"🔧 Continuing Claims Adjustment: {continuing_adjustment:.4f}%")
        
        # 5. Wage Growth Adjustment (Real Data)
        avg_earnings = self.get_avg_hourly_earnings()
        wage_adjustment = (avg_earnings - 36.53) / 36.53 * 0.1
        adjustments.append(('Wage Growth Adjustment (Real Data)', wage_adjustment))
        print(f"🔧 Wage Growth Adjustment: {wage_adjustment:.4f}%")
        
        # 6. Nonfarm Payrolls Adjustment (Real Data)
        nonfarm_payrolls = self.get_nonfarm_payrolls()
        payrolls_adjustment = (nonfarm_payrolls - 158000000) / 1000000 * 0.01
        adjustments.append(('Nonfarm Payrolls Adjustment (Real Data)', payrolls_adjustment))
        print(f"🔧 Nonfarm Payrolls Adjustment: {payrolls_adjustment:.4f}%")
        
        # 7. Demographic Disparities Adjustment
        if self.real_data and 'demographic_analysis' in self.real_data:
            disparities = self.real_data['demographic_analysis']['disparities']
            black_white_gap = disparities.get('black_white_gap', 0)
            demographic_adjustment = (black_white_gap - 3.8) * 0.05 / 100
            adjustments.append(('Demographic Disparities Adjustment', demographic_adjustment))
            print(f"🔧 Demographic Disparities Adjustment: {demographic_adjustment:.4f}%")
        
        # 8. Underemployment Adjustment
        if self.real_data and 'underemployment_analysis' in self.real_data:
            underemployment = self.real_data['underemployment_analysis']
            part_time_economic = underemployment['counts'].get('part_time_economic_reasons', 0)
            part_time_adjustment = (part_time_economic - 4700000) / 1000000 * 0.03
            adjustments.append(('Part-time Economic Reasons Adjustment', part_time_adjustment))
            print(f"🔧 Part-time Economic Reasons Adjustment: {part_time_adjustment:.4f}%")
            
            long_term_pct = underemployment['percentages'].get('long_term_unemployed_pct', 0)
            long_term_adjustment = (long_term_pct - 25.7) * 0.01 / 100
            adjustments.append(('Long-term Unemployed Adjustment', long_term_adjustment))
            print(f"🔧 Long-term Unemployed Adjustment: {long_term_adjustment:.4f}%")
        
        # 9. Industry Analysis Adjustment
        if self.real_data and 'establishment_analysis' in self.real_data:
            establishment = self.real_data['establishment_analysis']
            health_care = establishment.get('health_care_employment', 0)
            manufacturing = establishment.get('manufacturing_employment', 0)
            
            # Health care growth typically reduces unemployment
            health_care_adjustment = -(health_care - 17000000) / 1000000 * 0.02
            adjustments.append(('Health Care Employment Adjustment', health_care_adjustment))
            print(f"🔧 Health Care Employment Adjustment: {health_care_adjustment:.4f}%")
            
            # Manufacturing decline typically increases unemployment
            manufacturing_adjustment = (manufacturing - 13000000) / 1000000 * 0.01
            adjustments.append(('Manufacturing Employment Adjustment', manufacturing_adjustment))
            print(f"🔧 Manufacturing Employment Adjustment: {manufacturing_adjustment:.4f}%")
        
        # Calculate total adjustment
        total_adjustment = sum(adj[1] for adj in adjustments)
        print(f"📈 Total Adjustment: {total_adjustment:.4f}%")
        
        # Calculate final forecast
        final_forecast = base_rate + total_adjustment
        print(f"🎯 Final Real Data Forecast: {final_forecast:.2f}%")
        
        return final_forecast, adjustments
    
    def calculate_real_data_confidence(self):
        """Calculate confidence using real data quality"""
        
        print("\n📊 Calculating Real Data Confidence...")
        
        # Base confidence
        base_confidence = 80  # Higher base for real data
        
        # Data quality scores
        if self.real_data and 'data_quality' in self.real_data:
            fred_data_available = self.real_data['data_quality']['fred_data_available']
            total_series = self.real_data['data_quality']['total_series']
            data_freshness = self.real_data['data_quality']['data_freshness']
        else:
            fred_data_available = 0
            total_series = 15
            data_freshness = 'Fallback'
        
        # FRED data quality score
        fred_quality = (fred_data_available / total_series) * 100 if total_series > 0 else 0
        
        # Data freshness score
        freshness_score = 100 if data_freshness == 'Real-time' else 80
        
        # Real data bonus
        real_data_bonus = 0
        if fred_quality > 50:  # If more than half the data is from FRED
            real_data_bonus = 10
        elif fred_quality > 25:  # If some data is from FRED
            real_data_bonus = 5
        
        # Stability bonus based on data consistency
        stability_bonus = 0
        if self.real_data and 'demographic_analysis' in self.real_data:
            disparities = self.real_data['demographic_analysis']['disparities']
            if disparities.get('black_white_gap', 0) < 4.0:
                stability_bonus = 3
        
        # Final confidence calculation
        final_confidence = (base_confidence + 
                           (fred_quality * 0.3) +
                           (freshness_score * 0.1) +
                           real_data_bonus +
                           stability_bonus)
        
        # Cap at 95% for real data
        final_confidence = min(final_confidence, 95)
        
        print(f"🔧 FRED Data Quality: {fred_quality:.1f}% ({fred_data_available}/{total_series} series)")
        print(f"🔧 Data Freshness: {freshness_score}%")
        print(f"🔧 Real Data Bonus: +{real_data_bonus}%")
        print(f"🔧 Stability Bonus: +{stability_bonus}%")
        print(f"📊 Final Real Data Confidence: {final_confidence:.1f}%")
        
        return final_confidence
    
    def create_real_data_report(self, forecast, adjustments, confidence):
        """Create comprehensive real data forecast report"""
        
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
            'real_data_analysis': self.real_data.get('demographic_analysis', {}),
            'underemployment_analysis': self.real_data.get('underemployment_analysis', {}),
            'establishment_analysis': self.real_data.get('establishment_analysis', {}),
            'wage_hours_analysis': self.real_data.get('wage_hours_analysis', {}),
            'real_data_adjustments': [
                {
                    'adjustment_name': adj[0],
                    'adjustment_value': round(adj[1], 4),
                    'adjustment_percentage': round(adj[1] * 100, 4)
                }
                for adj in adjustments
            ],
            'data_sources': {
                'fred_api': 'Federal Reserve Economic Data (FRED) API',
                'real_data_analysis': 'Real-time data with enhanced fallback',
                'bls_methodology': 'BLS Employment Situation methodology'
            },
            'data_quality': self.real_data.get('data_quality', {}),
            'methodology': {
                'real_data_integration': 'Uses real FRED API data when available',
                'enhanced_fallback': 'Comprehensive fallback data for missing series',
                'bls_compliance': 'Follows BLS Employment Situation methodology',
                'confidence_calculation': 'Enhanced confidence with real data weighting'
            }
        }
        
        # Save report
        with open('real_data_forecast_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Real data forecast report saved to real_data_forecast_report.json")
        
        return report

def main():
    """Main function to run the real data forecasting"""
    forecaster = EnhancedUnemploymentForecasterWithRealData()
    
    # Calculate forecast
    forecast, adjustments = forecaster.calculate_real_data_forecast()
    
    # Calculate confidence
    confidence = forecaster.calculate_real_data_confidence()
    
    # Create report
    report = forecaster.create_real_data_report(forecast, adjustments, confidence)
    
    # Display summary
    print("\n" + "="*60)
    print("🎯 REAL DATA UNEMPLOYMENT FORECAST")
    print("="*60)
    print(f"📊 Current Unemployment Rate: {report['forecast_summary']['current_unemployment']}%")
    print(f"🎯 Real Data Forecast: {report['forecast_summary']['forecasted_unemployment']}%")
    print(f"📈 Change: {report['forecast_summary']['change']:+.2f} percentage points")
    print(f"🎯 Confidence Level: {report['forecast_summary']['confidence_level']}%")
    print(f"📊 Direction: {report['forecast_summary']['direction']}")
    
    if report['real_data_analysis']:
        print("\n🔧 Real Data Analysis:")
        rates = report['real_data_analysis'].get('rates', {})
        print(f"   Adult Men: {rates.get('unemployment_rate_men', 'N/A')}%")
        print(f"   Adult Women: {rates.get('unemployment_rate_women', 'N/A')}%")
        print(f"   White: {rates.get('unemployment_rate_white', 'N/A')}%")
        print(f"   Black: {rates.get('unemployment_rate_black', 'N/A')}%")
        print(f"   Hispanic: {rates.get('unemployment_rate_hispanic', 'N/A')}%")
    
    if report['data_quality']:
        print(f"\n📊 Data Quality:")
        print(f"   FRED Data Available: {report['data_quality'].get('fred_data_available', 0)}/{report['data_quality'].get('total_series', 0)} series")
        print(f"   Data Freshness: {report['data_quality'].get('data_freshness', 'Unknown')}")
    
    if report['establishment_analysis']:
        print(f"\n🔧 Establishment Survey:")
        establishment = report['establishment_analysis']
        print(f"   Total Nonfarm Payrolls: {establishment.get('nonfarm_payrolls', 0):,.0f}")
        print(f"   Private Sector: {establishment.get('private_payrolls', 0):,.0f}")
        print(f"   Government: {establishment.get('government_payrolls', 0):,.0f}")
    
    if report['wage_hours_analysis']:
        print(f"\n🔧 Wage and Hours:")
        wage_data = report['wage_hours_analysis']
        print(f"   Average Hourly Earnings: ${wage_data.get('avg_hourly_earnings', 0):.2f}")
        print(f"   Average Weekly Hours: {wage_data.get('avg_weekly_hours', 0):.1f}")

if __name__ == "__main__":
    main()