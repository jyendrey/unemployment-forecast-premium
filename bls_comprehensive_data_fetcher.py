#!/usr/bin/env python3
"""
BLS Comprehensive Data Fetcher
Fetches all BLS Employment Situation data including demographic, establishment, and household survey data
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import urllib.request
import json
from datetime import datetime, timedelta
import statistics

class BLSComprehensiveDataFetcher:
    def __init__(self):
        self.api_key = "7358702e869844db978f304b5079cfb8"  # BLS API key
        self.base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        
        # BLS Series IDs for comprehensive data
        self.series_ids = {
            # Basic unemployment metrics
            'unemployment_rate': 'LNS14000000',
            'unemployed_persons': 'LNS13000000',
            'employed_persons': 'LNS12000000',
            'labor_force': 'LNS11000000',
            'labor_force_participation_rate': 'LNS11300000',
            'employment_population_ratio': 'LNS12300000',
            
            # Demographic unemployment rates
            'unemployment_rate_men': 'LNS14000001',
            'unemployment_rate_women': 'LNS14000002',
            'unemployment_rate_teens': 'LNS14000003',
            'unemployment_rate_white': 'LNS14000004',
            'unemployment_rate_black': 'LNS14000005',
            'unemployment_rate_asian': 'LNS14000006',
            'unemployment_rate_hispanic': 'LNS14000007',
            
            # Underemployment metrics
            'part_time_economic_reasons': 'LNS12032194',  # Part-time for economic reasons
            'marginally_attached': 'LNS15000000',  # Marginally attached to labor force
            'discouraged_workers': 'LNS15000001',  # Discouraged workers
            'new_entrants': 'LNS15000002',  # New entrants
            'long_term_unemployed': 'LNS13025714',  # Long-term unemployed (27+ weeks)
            
            # Establishment survey data
            'nonfarm_payrolls': 'CES0000000001',  # Total nonfarm payroll employment
            'private_payrolls': 'CES0500000001',  # Private sector employment
            'government_payrolls': 'CES9000000001',  # Government employment
            
            # Industry-specific employment
            'health_care_employment': 'CES6562000001',  # Health care
            'manufacturing_employment': 'CES3000000001',  # Manufacturing
            'construction_employment': 'CES2000000001',  # Construction
            'retail_trade_employment': 'CES4244000001',  # Retail trade
            'leisure_hospitality_employment': 'CES7000000001',  # Leisure and hospitality
            
            # Wage and hours data
            'avg_hourly_earnings': 'CES0500000003',  # Average hourly earnings
            'avg_weekly_hours': 'CES0500000002',  # Average weekly hours
            'manufacturing_hours': 'CES3000000002',  # Manufacturing hours
            'manufacturing_overtime': 'CES3000000003',  # Manufacturing overtime
        }
        
    def fetch_bls_data(self, series_ids, start_year=None, end_year=None):
        """Fetch data from BLS API for multiple series"""
        
        if start_year is None:
            start_year = (datetime.now() - timedelta(days=365*2)).year
        if end_year is None:
            end_year = datetime.now().year
            
        # Prepare the request payload
        payload = {
            "seriesid": series_ids,
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": self.api_key
        }
        
        try:
            print(f"📊 Fetching BLS comprehensive data for {len(series_ids)} series...")
            
            # Convert payload to JSON
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                self.base_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Make request
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result['status'] == 'REQUEST_SUCCEEDED':
                    print(f"✅ Successfully fetched BLS comprehensive data")
                    return result['Results']['series']
                else:
                    print(f"❌ BLS API error: {result.get('message', 'Unknown error')}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error fetching BLS comprehensive data: {e}")
            return None
    
    def get_fallback_comprehensive_data(self):
        """Get fallback comprehensive data when BLS API is unavailable"""
        print("⚠️ Using fallback comprehensive BLS data - API unavailable")
        
        current_date = datetime.now()
        fallback_data = {}
        
        # Generate synthetic data based on August 2025 BLS report
        base_data = {
            'unemployment_rate': 4.3,
            'unemployed_persons': 7400000,
            'employed_persons': 165000000,
            'labor_force': 172400000,
            'labor_force_participation_rate': 62.3,
            'employment_population_ratio': 59.6,
            
            # Demographic rates
            'unemployment_rate_men': 4.1,
            'unemployment_rate_women': 3.8,
            'unemployment_rate_teens': 13.9,
            'unemployment_rate_white': 3.7,
            'unemployment_rate_black': 7.5,
            'unemployment_rate_asian': 3.6,
            'unemployment_rate_hispanic': 5.3,
            
            # Underemployment
            'part_time_economic_reasons': 4700000,
            'marginally_attached': 1800000,
            'discouraged_workers': 514000,
            'new_entrants': 786000,
            'long_term_unemployed': 1900000,
            
            # Establishment survey
            'nonfarm_payrolls': 158000000,
            'private_payrolls': 135000000,
            'government_payrolls': 23000000,
            
            # Industry data
            'health_care_employment': 17000000,
            'manufacturing_employment': 13000000,
            'construction_employment': 8000000,
            'retail_trade_employment': 16000000,
            'leisure_hospitality_employment': 17000000,
            
            # Wage and hours
            'avg_hourly_earnings': 36.53,
            'avg_weekly_hours': 34.2,
            'manufacturing_hours': 40.0,
            'manufacturing_overtime': 2.9,
        }
        
        for series_name, base_value in base_data.items():
            data_points = []
            for i in range(24):  # 24 months of data
                date = current_date - timedelta(days=30*i)
                # Add some variation to the base value
                variation = (i % 12 - 6) * 0.02  # Seasonal variation
                value = base_value * (1 + variation)
                
                data_points.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'value': value,
                    'year': date.year,
                    'period': f"M{date.month:02d}"
                })
            
            fallback_data[series_name] = data_points
        
        return fallback_data
    
    def calculate_demographic_analysis(self, data):
        """Calculate demographic unemployment analysis"""
        
        if not data:
            return None
        
        # Get most recent data
        recent_data = {}
        for series_name in ['unemployment_rate_men', 'unemployment_rate_women', 'unemployment_rate_teens',
                           'unemployment_rate_white', 'unemployment_rate_black', 'unemployment_rate_asian', 'unemployment_rate_hispanic']:
            if series_name in data and data[series_name]:
                recent_data[series_name] = data[series_name][0]['value']
            else:
                recent_data[series_name] = 0
        
        # Calculate disparities
        overall_rate = data.get('unemployment_rate', [{}])[0].get('value', 4.3) if data.get('unemployment_rate') else 4.3
        
        disparities = {
            'black_white_gap': recent_data['unemployment_rate_black'] - recent_data['unemployment_rate_white'],
            'hispanic_white_gap': recent_data['unemployment_rate_hispanic'] - recent_data['unemployment_rate_white'],
            'teen_adult_gap': recent_data['unemployment_rate_teens'] - overall_rate,
            'gender_gap': recent_data['unemployment_rate_men'] - recent_data['unemployment_rate_women']
        }
        
        print(f"🔧 Demographic Unemployment Analysis:")
        print(f"   Adult Men: {recent_data['unemployment_rate_men']:.1f}%")
        print(f"   Adult Women: {recent_data['unemployment_rate_women']:.1f}%")
        print(f"   Teenagers: {recent_data['unemployment_rate_teens']:.1f}%")
        print(f"   White: {recent_data['unemployment_rate_white']:.1f}%")
        print(f"   Black: {recent_data['unemployment_rate_black']:.1f}%")
        print(f"   Asian: {recent_data['unemployment_rate_asian']:.1f}%")
        print(f"   Hispanic: {recent_data['unemployment_rate_hispanic']:.1f}%")
        print(f"   Black-White Gap: {disparities['black_white_gap']:.1f} percentage points")
        print(f"   Hispanic-White Gap: {disparities['hispanic_white_gap']:.1f} percentage points")
        
        return {
            'rates': recent_data,
            'disparities': disparities,
            'overall_rate': overall_rate
        }
    
    def calculate_underemployment_analysis(self, data):
        """Calculate underemployment and labor force attachment analysis"""
        
        if not data:
            return None
        
        # Get most recent data
        recent_data = {}
        for series_name in ['part_time_economic_reasons', 'marginally_attached', 'discouraged_workers',
                           'new_entrants', 'long_term_unemployed', 'unemployed_persons']:
            if series_name in data and data[series_name]:
                recent_data[series_name] = data[series_name][0]['value']
            else:
                recent_data[series_name] = 0
        
        # Calculate percentages
        unemployed_total = recent_data['unemployed_persons']
        long_term_pct = (recent_data['long_term_unemployed'] / unemployed_total * 100) if unemployed_total > 0 else 0
        discouraged_pct = (recent_data['discouraged_workers'] / recent_data['marginally_attached'] * 100) if recent_data['marginally_attached'] > 0 else 0
        
        print(f"🔧 Underemployment Analysis:")
        print(f"   Part-time for Economic Reasons: {recent_data['part_time_economic_reasons']:,.0f}")
        print(f"   Marginally Attached: {recent_data['marginally_attached']:,.0f}")
        print(f"   Discouraged Workers: {recent_data['discouraged_workers']:,.0f} ({discouraged_pct:.1f}% of marginally attached)")
        print(f"   New Entrants: {recent_data['new_entrants']:,.0f}")
        print(f"   Long-term Unemployed: {recent_data['long_term_unemployed']:,.0f} ({long_term_pct:.1f}% of unemployed)")
        
        return {
            'counts': recent_data,
            'percentages': {
                'long_term_unemployed_pct': long_term_pct,
                'discouraged_workers_pct': discouraged_pct
            }
        }
    
    def calculate_establishment_analysis(self, data):
        """Calculate establishment survey analysis"""
        
        if not data:
            return None
        
        # Get most recent data
        recent_data = {}
        for series_name in ['nonfarm_payrolls', 'private_payrolls', 'government_payrolls',
                           'health_care_employment', 'manufacturing_employment', 'construction_employment',
                           'retail_trade_employment', 'leisure_hospitality_employment']:
            if series_name in data and data[series_name]:
                recent_data[series_name] = data[series_name][0]['value']
            else:
                recent_data[series_name] = 0
        
        # Calculate month-over-month changes (simplified)
        print(f"🔧 Establishment Survey Analysis:")
        print(f"   Total Nonfarm Payrolls: {recent_data['nonfarm_payrolls']:,.0f}")
        print(f"   Private Sector: {recent_data['private_payrolls']:,.0f}")
        print(f"   Government: {recent_data['government_payrolls']:,.0f}")
        print(f"   Health Care: {recent_data['health_care_employment']:,.0f}")
        print(f"   Manufacturing: {recent_data['manufacturing_employment']:,.0f}")
        print(f"   Construction: {recent_data['construction_employment']:,.0f}")
        print(f"   Retail Trade: {recent_data['retail_trade_employment']:,.0f}")
        print(f"   Leisure & Hospitality: {recent_data['leisure_hospitality_employment']:,.0f}")
        
        return recent_data
    
    def calculate_wage_hours_analysis(self, data):
        """Calculate wage and hours analysis"""
        
        if not data:
            return None
        
        # Get most recent data
        recent_data = {}
        for series_name in ['avg_hourly_earnings', 'avg_weekly_hours', 'manufacturing_hours', 'manufacturing_overtime']:
            if series_name in data and data[series_name]:
                recent_data[series_name] = data[series_name][0]['value']
            else:
                recent_data[series_name] = 0
        
        # Calculate year-over-year growth (simplified)
        print(f"🔧 Wage and Hours Analysis:")
        print(f"   Average Hourly Earnings: ${recent_data['avg_hourly_earnings']:.2f}")
        print(f"   Average Weekly Hours: {recent_data['avg_weekly_hours']:.1f}")
        print(f"   Manufacturing Hours: {recent_data['manufacturing_hours']:.1f}")
        print(f"   Manufacturing Overtime: {recent_data['manufacturing_overtime']:.1f}")
        
        return recent_data
    
    def create_comprehensive_analysis(self):
        """Create comprehensive BLS analysis"""
        
        print("🎯 Creating Comprehensive BLS Analysis...")
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print("="*60)
        
        # Fetch comprehensive data
        all_series = list(self.series_ids.keys())
        bls_data = self.fetch_bls_data(all_series)
        
        if not bls_data:
            print("⚠️ Using fallback comprehensive data")
            data = self.get_fallback_comprehensive_data()
        else:
            # Process BLS data
            data = {}
            for series in bls_data:
                series_id = series['seriesID']
                series_name = None
                
                # Find series name
                for name, sid in self.series_ids.items():
                    if sid == series_id:
                        series_name = name
                        break
                
                if series_name:
                    data_points = []
                    for data_point in series['data']:
                        try:
                            value = float(data_point['value'])
                            date = data_point['year'] + '-' + data_point['period'][1:3] + '-01'
                            data_points.append({
                                'date': date,
                                'value': value,
                                'year': int(data_point['year']),
                                'period': data_point['period']
                            })
                        except (ValueError, KeyError):
                            continue
                    
                    data_points.sort(key=lambda x: x['date'], reverse=True)
                    data[series_name] = data_points
        
        # Calculate analyses
        demographic_analysis = self.calculate_demographic_analysis(data)
        underemployment_analysis = self.calculate_underemployment_analysis(data)
        establishment_analysis = self.calculate_establishment_analysis(data)
        wage_hours_analysis = self.calculate_wage_hours_analysis(data)
        
        # Create comprehensive report
        analysis = {
            'generated_date': datetime.now().isoformat(),
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id,
            'data_source': 'BLS Comprehensive Employment Situation',
            'raw_data': data,
            'demographic_analysis': demographic_analysis,
            'underemployment_analysis': underemployment_analysis,
            'establishment_analysis': establishment_analysis,
            'wage_hours_analysis': wage_hours_analysis,
            'analysis_summary': {
                'total_series_analyzed': len(data),
                'data_quality': 'High' if bls_data else 'Fallback',
                'latest_data_date': data[list(data.keys())[0]][0]['date'] if data else None
            }
        }
        
        # Save analysis to file
        with open('bls_comprehensive_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Comprehensive BLS analysis saved to bls_comprehensive_analysis.json")
        
        return analysis

def main():
    """Main function to run the comprehensive BLS analysis"""
    fetcher = BLSComprehensiveDataFetcher()
    analysis = fetcher.create_comprehensive_analysis()
    
    if analysis:
        print("\n📊 Comprehensive BLS Analysis Summary:")
        if analysis['demographic_analysis']:
            print(f"Overall Unemployment Rate: {analysis['demographic_analysis']['overall_rate']:.1f}%")
            print(f"Black-White Gap: {analysis['demographic_analysis']['disparities']['black_white_gap']:.1f} pp")
        if analysis['underemployment_analysis']:
            print(f"Long-term Unemployed: {analysis['underemployment_analysis']['percentages']['long_term_unemployed_pct']:.1f}% of unemployed")
        if analysis['establishment_analysis']:
            print(f"Total Nonfarm Payrolls: {analysis['establishment_analysis']['nonfarm_payrolls']:,.0f}")
        if analysis['wage_hours_analysis']:
            print(f"Average Hourly Earnings: ${analysis['wage_hours_analysis']['avg_hourly_earnings']:.2f}")

if __name__ == "__main__":
    main()