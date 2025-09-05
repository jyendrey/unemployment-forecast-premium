#!/usr/bin/env python3
"""
Comprehensive Economic Data Fetcher
Fetches economic data from BLS, BEA, and FRED using provided API keys
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time
import os

class EconomicDataFetcher:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.version = "v3.3-economic-data-integrated"
        self.current_date = datetime.now()
        
        # API Keys
        self.bls_api_key = "7358702e869844db978f304b5079cfb8"
        self.bea_api_key = "9CE55341-BAF6-4134-8119-56A1C0BD9BD3"
        self.fred_api_key = "73c6c14c5998dda7efaf106939718f18"
        
        # API Endpoints
        self.bls_endpoint = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        self.bea_endpoint = "https://apps.bea.gov/api/data/"
        self.fred_endpoint = "https://api.stlouisfed.org/fred/series/observations"
        
        # Data storage
        self.bls_data = {}
        self.bea_data = {}
        self.fred_data = {}
        self.combined_analysis = {}
        
    def fetch_bls_data(self) -> Dict:
        """Fetch data from Bureau of Labor Statistics (BLS)"""
        print("🔄 Fetching BLS data...")
        
        # BLS Series IDs for unemployment and labor data
        bls_series = {
            "LNS14000000": "Unemployment Rate",
            "LNS11300000": "Labor Force Participation Rate",
            "LNS13000000": "Employment-Population Ratio",
            "LNS12000000": "Employment Level"
        }
        
        bls_data = {}
        
        for series_id, description in bls_series.items():
            try:
                # BLS API v2 requires JSON payload
                payload = {
                    "seriesid": [series_id],
                    "startyear": str(datetime.now().year - 2),
                    "endyear": str(datetime.now().year),
                    "registrationkey": self.bls_api_key
                }
                
                response = requests.post(self.bls_endpoint, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'Results' in data and data['Results']:
                        series_data = data['Results']['series'][0]['data']
                        
                        # Process the data
                        processed_data = []
                        for item in series_data:
                            processed_data.append({
                                'date': f"{item['year']}-{item['period']:0>2}-01",
                                'value': float(item['value']),
                                'footnotes': item.get('footnotes', [])
                            })
                        
                        bls_data[series_id] = {
                            'description': description,
                            'data': processed_data,
                            'latest_value': processed_data[0]['value'] if processed_data else None,
                            'latest_date': processed_data[0]['date'] if processed_data else None
                        }
                        
                        print(f"✅ Fetched {description}: {processed_data[0]['value'] if processed_data else 'N/A'}")
                        
                else:
                    print(f"⚠️ BLS API error for {series_id}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error fetching BLS data for {series_id}: {e}")
            
            # Rate limiting for BLS API
            time.sleep(0.5)
        
        self.bls_data = bls_data
        return bls_data
    
    def fetch_bea_data(self) -> Dict:
        """Fetch data from Bureau of Economic Analysis (BEA)"""
        print("🔄 Fetching BEA data...")
        
        # BEA data sets and parameters
        bea_datasets = {
            "NIPA": {
                "TableID": "T10101",  # Gross Domestic Product
                "Frequency": "Q",
                "Year": str(datetime.now().year)
            },
            "NIPA": {
                "TableID": "T20301",  # Personal Consumption Expenditures
                "Frequency": "Q",
                "Year": str(datetime.now().year)
            }
        }
        
        bea_data = {}
        
        for dataset, params in bea_datasets.items():
            try:
                # Build BEA API URL
                url = f"{self.bea_endpoint}?UserID={self.bea_api_key}&Method=GetData&DataSetName={dataset}&TableName={params['TableID']}&Frequency={params['Frequency']}&Year={params['Year']}&ResultFormat=JSON"
                
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
                        results = data['BEAAPI']['Results']
                        
                        if 'Data' in results:
                            bea_data[params['TableID']] = {
                                'dataset': dataset,
                                'table_id': params['TableID'],
                                'data': results['Data'],
                                'metadata': results.get('Notes', [])
                            }
                            
                            print(f"✅ Fetched BEA {dataset} data for table {params['TableID']}")
                
                else:
                    print(f"⚠️ BEA API error for {params['TableID']}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error fetching BEA data for {params['TableID']}: {e}")
            
            # Rate limiting for BEA API
            time.sleep(0.5)
        
        self.bea_data = bea_data
        return bea_data
    
    def fetch_fred_data(self) -> Dict:
        """Fetch data from Federal Reserve Economic Data (FRED)"""
        print("🔄 Fetching FRED data...")
        
        # FRED Series IDs for economic indicators
        fred_series = {
            "ICSA": "Initial Claims",
            "CCSA": "Continuing Claims",
            "UNRATE": "Unemployment Rate",
            "CIVPART": "Labor Force Participation Rate",
            "GDP": "Gross Domestic Product",
            "PCE": "Personal Consumption Expenditures",
            "INDPROD": "Industrial Production",
            "PAYEMS": "Total Nonfarm Payrolls"
        }
        
        fred_data = {}
        
        for series_id, description in fred_series.items():
            try:
                # Build FRED API URL
                url = f"{self.fred_endpoint}?series_id={series_id}&api_key={self.fred_api_key}&file_type=json&observation_start={datetime.now().date() - timedelta(days=730)}"
                
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'observations' in data:
                        observations = data['observations']
                        
                        # Process the data
                        processed_data = []
                        for obs in observations:
                            if obs['value'] != '.':
                                processed_data.append({
                                    'date': obs['date'],
                                    'value': float(obs['value']),
                                    'realtime_start': obs.get('realtime_start'),
                                    'realtime_end': obs.get('realtime_end')
                                })
                        
                        if processed_data:
                            fred_data[series_id] = {
                                'description': description,
                                'data': processed_data,
                                'latest_value': processed_data[0]['value'],
                                'latest_date': processed_data[0]['date'],
                                'total_observations': len(processed_data)
                            }
                            
                            print(f"✅ Fetched {description}: {processed_data[0]['value']} ({processed_data[0]['date']})")
                
                else:
                    print(f"⚠️ FRED API error for {series_id}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error fetching FRED data for {series_id}: {e}")
            
            # Rate limiting for FRED API
            time.sleep(0.5)
        
        self.fred_data = fred_data
        return fred_data
    
    def analyze_economic_indicators(self) -> Dict:
        """Analyze economic indicators and generate insights"""
        print("🔄 Analyzing economic indicators...")
        
        analysis = {
            'unemployment_analysis': {},
            'labor_market_analysis': {},
            'economic_growth_analysis': {},
            'market_health_assessment': {},
            'trend_analysis': {},
            'risk_assessment': {}
        }
        
        # Unemployment Analysis
        if 'UNRATE' in self.fred_data:
            unrate_data = self.fred_data['UNRATE']['data']
            if len(unrate_data) >= 2:
                current_rate = unrate_data[0]['value']
                previous_rate = unrate_data[1]['value']
                change = current_rate - previous_rate
                
                analysis['unemployment_analysis'] = {
                    'current_rate': current_rate,
                    'previous_rate': previous_rate,
                    'change': round(change, 3),
                    'direction': 'Rising' if change > 0 else 'Falling' if change < 0 else 'Stable',
                    'trend_strength': abs(change)
                }
        
        # Labor Market Analysis
        if 'CIVPART' in self.fred_data:
            civpart_data = self.fred_data['CIVPART']['data']
            if len(civpart_data) >= 2:
                current_participation = civpart_data[0]['value']
                previous_participation = civpart_data[1]['value']
                participation_change = current_participation - previous_participation
                
                analysis['labor_market_analysis'] = {
                    'current_participation': current_participation,
                    'previous_participation': previous_participation,
                    'change': round(participation_change, 3),
                    'direction': 'Rising' if participation_change > 0 else 'Falling' if participation_change < 0 else 'Stable'
                }
        
        # Initial Claims Analysis
        if 'ICSA' in self.fred_data:
            icsa_data = self.fred_data['ICSA']['data']
            if len(icsa_data) >= 4:
                current_claims = icsa_data[0]['value']
                four_week_avg = sum(obs['value'] for obs in icsa_data[:4]) / 4
                
                analysis['unemployment_analysis']['initial_claims'] = {
                    'current': current_claims,
                    'four_week_average': round(four_week_avg, 0),
                    'trend': 'Improving' if current_claims < four_week_avg else 'Deteriorating'
                }
        
        # Economic Growth Analysis
        if 'GDP' in self.fred_data:
            gdp_data = self.fred_data['GDP']['data']
            if len(gdp_data) >= 2:
                current_gdp = gdp_data[0]['value']
                previous_gdp = gdp_data[1]['value']
                gdp_growth = ((current_gdp - previous_gdp) / previous_gdp) * 100
                
                analysis['economic_growth_analysis'] = {
                    'current_gdp': current_gdp,
                    'previous_gdp': previous_gdp,
                    'growth_rate': round(gdp_growth, 2),
                    'growth_direction': 'Positive' if gdp_growth > 0 else 'Negative'
                }
        
        # Market Health Assessment
        health_score = 0
        health_factors = []
        
        # Unemployment rate health (lower is better)
        if 'unemployment_analysis' in analysis and 'current_rate' in analysis['unemployment_analysis']:
            current_unrate = analysis['unemployment_analysis']['current_rate']
            if current_unrate < 4.0:
                health_score += 25
                health_factors.append("Low unemployment rate")
            elif current_unrate < 5.0:
                health_score += 15
                health_factors.append("Moderate unemployment rate")
            else:
                health_score += 5
                health_factors.append("High unemployment rate")
        
        # Labor participation health (higher is better)
        if 'labor_market_analysis' in analysis and 'current_participation' in analysis['labor_market_analysis']:
            current_participation = analysis['labor_market_analysis']['current_participation']
            if current_participation > 63.0:
                health_score += 25
                health_factors.append("Strong labor participation")
            elif current_participation > 62.0:
                health_score += 15
                health_factors.append("Moderate labor participation")
            else:
                health_score += 5
                health_factors.append("Low labor participation")
        
        # Initial claims health (lower is better)
        if 'unemployment_analysis' in analysis and 'initial_claims' in analysis['unemployment_analysis']:
            current_claims = analysis['unemployment_analysis']['initial_claims']['current']
            if current_claims < 200000:
                health_score += 25
                health_factors.append("Low initial claims")
            elif current_claims < 250000:
                health_score += 15
                health_factors.append("Moderate initial claims")
            else:
                health_score += 5
                health_factors.append("High initial claims")
        
        # Economic growth health
        if 'economic_growth_analysis' in analysis and 'growth_rate' in analysis['economic_growth_analysis']:
            growth_rate = analysis['economic_growth_analysis']['growth_rate']
            if growth_rate > 2.0:
                health_score += 25
                health_factors.append("Strong economic growth")
            elif growth_rate > 0.0:
                health_score += 15
                health_factors.append("Positive economic growth")
            else:
                health_score += 5
                health_factors.append("Negative economic growth")
        
        analysis['market_health_assessment'] = {
            'overall_health_score': health_score,
            'health_level': 'Excellent' if health_score >= 80 else 'Good' if health_score >= 60 else 'Fair' if health_score >= 40 else 'Poor',
            'health_factors': health_factors
        }
        
        # Trend Analysis
        analysis['trend_analysis'] = {
            'unemployment_trend': analysis.get('unemployment_analysis', {}).get('direction', 'Unknown'),
            'labor_market_trend': analysis.get('labor_market_analysis', {}).get('direction', 'Unknown'),
            'economic_growth_trend': analysis.get('economic_growth_analysis', {}).get('growth_direction', 'Unknown'),
            'overall_market_trend': 'Bullish' if health_score >= 60 else 'Bearish' if health_score <= 40 else 'Neutral'
        }
        
        # Risk Assessment
        risk_factors = []
        risk_level = 'Low'
        
        if analysis.get('unemployment_analysis', {}).get('current_rate', 0) > 5.0:
            risk_factors.append("High unemployment rate")
            risk_level = 'High'
        
        if analysis.get('unemployment_analysis', {}).get('initial_claims', {}).get('current', 0) > 300000:
            risk_factors.append("Elevated initial claims")
            risk_level = 'Medium' if risk_level == 'Low' else risk_level
        
        if analysis.get('economic_growth_analysis', {}).get('growth_rate', 0) < 0:
            risk_factors.append("Negative economic growth")
            risk_level = 'High'
        
        analysis['risk_assessment'] = {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'risk_score': 100 - health_score
        }
        
        return analysis
    
    def generate_economic_report(self) -> Dict:
        """Generate comprehensive economic data report"""
        print("🔄 Generating economic report...")
        
        report = {
            'generated_date': self.current_date.isoformat(),
            'foundation_id': self.foundation_id,
            'version': self.version,
            'data_sources': {
                'bls': {
                    'enabled': True,
                    'api_key': self.bls_api_key,
                    'series_fetched': list(self.bls_data.keys()),
                    'total_series': len(self.bls_data)
                },
                'bea': {
                    'enabled': True,
                    'api_key': self.bea_api_key,
                    'datasets_fetched': list(self.bea_data.keys()),
                    'total_datasets': len(self.bea_data)
                },
                'fred': {
                    'enabled': True,
                    'api_key': self.fred_api_key,
                    'series_fetched': list(self.fred_data.keys()),
                    'total_series': len(self.fred_data)
                }
            },
            'economic_analysis': self.combined_analysis,
            'data_summary': {
                'total_data_points': sum(len(self.fred_data.get(series, {}).get('data', [])) for series in self.fred_data),
                'latest_update': self.current_date.strftime('%Y-%m-%d %H:%M:%S'),
                'data_coverage': f"BLS: {len(self.bls_data)} series, BEA: {len(self.bea_data)} datasets, FRED: {len(self.fred_data)} series"
            }
        }
        
        return report
    
    def save_economic_data(self, filename: str = "economic_data_analysis.json") -> str:
        """Save the economic data analysis to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.combined_analysis, f, indent=2)
            
            print(f"✅ Economic data analysis saved to: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ Error saving economic data: {e}")
            return ""
    
    def save_economic_report(self, filename: str = "economic_data_report.json") -> str:
        """Save the economic data report to a JSON file"""
        try:
            report = self.generate_economic_report()
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Economic data report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ Error saving economic report: {e}")
            return ""
    
    def print_economic_summary(self):
        """Print a summary of the fetched economic data"""
        print("\n" + "="*80)
        print("ECONOMIC DATA FETCHING SUMMARY")
        print("="*80)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print(f"Fetch Date: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # BLS Data Summary
        print(f"\n📊 BLS DATA:")
        print(f"  Series Fetched: {len(self.bls_data)}")
        for series_id, data in self.bls_data.items():
            if data['latest_value'] is not None:
                print(f"    {data['description']}: {data['latest_value']} ({data['latest_date']})")
        
        # BEA Data Summary
        print(f"\n📊 BEA DATA:")
        print(f"  Datasets Fetched: {len(self.bea_data)}")
        for table_id, data in self.bea_data.items():
            print(f"    Table {table_id}: {data['dataset']} data")
        
        # FRED Data Summary
        print(f"\n📊 FRED DATA:")
        print(f"  Series Fetched: {len(self.fred_data)}")
        for series_id, data in self.fred_data.items():
            if data['latest_value'] is not None:
                print(f"    {data['description']}: {data['latest_value']} ({data['latest_date']})")
        
        # Economic Analysis Summary
        if self.combined_analysis:
            print(f"\n📈 ECONOMIC ANALYSIS:")
            
            # Unemployment Analysis
            if 'unemployment_analysis' in self.combined_analysis:
                unemp = self.combined_analysis['unemployment_analysis']
                if 'current_rate' in unemp:
                    print(f"  Unemployment Rate: {unemp['current_rate']}% ({unemp.get('direction', 'Unknown')})")
                if 'initial_claims' in unemp:
                    claims = unemp['initial_claims']
                    print(f"  Initial Claims: {claims['current']:,} ({claims['trend']})")
            
            # Labor Market Analysis
            if 'labor_market_analysis' in self.combined_analysis:
                labor = self.combined_analysis['labor_market_analysis']
                if 'current_participation' in labor:
                    print(f"  Labor Participation: {labor['current_participation']}% ({labor.get('direction', 'Unknown')})")
            
            # Market Health
            if 'market_health_assessment' in self.combined_analysis:
                health = self.combined_analysis['market_health_assessment']
                print(f"  Market Health: {health['health_level']} (Score: {health['overall_health_score']}/100)")
            
            # Risk Assessment
            if 'risk_assessment' in self.combined_analysis:
                risk = self.combined_analysis['risk_assessment']
                print(f"  Risk Level: {risk['risk_level']} (Score: {risk['risk_score']}/100)")
        
        print("\n" + "="*80)
    
    def fetch_wage_growth_data(self) -> Dict:
        """Fetch wage growth data from FRED"""
        print("🔄 Fetching wage growth data...")
        
        # Wage growth series
        wage_series = {
            "CES0500000003": "Average Hourly Earnings - All Employees",
            "ECIWAG": "Employment Cost Index - Wages & Salaries",
            "AHETPI": "Average Hourly Earnings -Production Workers"
        }
        
        wage_data = {}
        for series_id, description in wage_series.items():
            try:
                data = self.fetch_fred_data(series_id, 24)
                if data:
                    wage_data[series_id] = {
                        'description': description,
                        'data': data
                    }
                    print(f"   ✅ {description}: {len(data)} months")
                else:
                    print(f"   ❌ Failed to fetch {description}")
            except Exception as e:
                print(f"   ❌ Error fetching {description}: {e}")
        
        return wage_data

    def fetch_state_unemployment_data(self) -> Dict:
        """Fetch state-level unemployment data from FRED"""
        print("🔄 Fetching state-level unemployment data...")
        
        # Key states for unemployment analysis (largest economies + diverse regions)
        state_series = {
            "CAUR": "California Unemployment Rate",
            "TXUR": "Texas Unemployment Rate", 
            "FLUR": "Florida Unemployment Rate",
            "NYUR": "New York Unemployment Rate",
            "PAUR": "Pennsylvania Unemployment Rate",
            "ILUR": "Illinois Unemployment Rate",
            "OHUR": "Ohio Unemployment Rate",
            "GAUR": "Georgia Unemployment Rate",
            "NCUR": "North Carolina Unemployment Rate",
            "MIUR": "Michigan Unemployment Rate",
            "NJUR": "New Jersey Unemployment Rate",
            "VAUR": "Virginia Unemployment Rate",
            "WAUR": "Washington Unemployment Rate",
            "AZUR": "Arizona Unemployment Rate",
            "MAUR": "Massachusetts Unemployment Rate",
            "TNUR": "Tennessee Unemployment Rate",
            "INUR": "Indiana Unemployment Rate",
            "MOUR": "Missouri Unemployment Rate",
            "MDUR": "Maryland Unemployment Rate",
            "WIUR": "Wisconsin Unemployment Rate"
        }
        
        state_data = {}
        for series_id, description in state_series.items():
            try:
                data = self.fetch_fred_data(series_id, 24)
                if data:
                    state_data[series_id] = {
                        'description': description,
                        'data': data
                    }
                    print(f"   ✅ {description}: {len(data)} months")
                else:
                    print(f"   ❌ Failed to fetch {description}")
            except Exception as e:
                print(f"   ❌ Error fetching {description}: {e}")
        
        return state_data

    def analyze_wage_growth_indicators(self, wage_data: Dict) -> Dict:
        """Analyze wage growth indicators"""
        if not wage_data:
            return {'wage_pressure': 'unknown', 'confidence_score': 0.1}
        
        try:
            # Get latest wage data
            latest_wages = {}
            for series_id, data in wage_data.items():
                if data['data']:
                    latest_wages[series_id] = data['data'][0]['value']
            
            # Calculate wage growth trends
            wage_growth_rates = []
            for series_id, data in wage_data.items():
                if len(data['data']) >= 2:
                    current = data['data'][0]['value']
                    previous = data['data'][1]['value']
                    growth_rate = (current - previous) / previous * 100
                    wage_growth_rates.append(growth_rate)
            
            avg_wage_growth = sum(wage_growth_rates) / len(wage_growth_rates) if wage_growth_rates else 0
            
            # Determine wage pressure
            if avg_wage_growth > 4.0:
                wage_pressure = 'high'
                confidence_score = 0.8
            elif avg_wage_growth > 2.5:
                wage_pressure = 'moderate'
                confidence_score = 0.6
            else:
                wage_pressure = 'low'
                confidence_score = 0.4
            
            return {
                'wage_pressure': wage_pressure,
                'average_growth_rate': avg_wage_growth,
                'confidence_score': confidence_score,
                'latest_wages': latest_wages
            }
            
        except Exception as e:
            print(f"⚠️ Error analyzing wage growth: {e}")
            return {'wage_pressure': 'unknown', 'confidence_score': 0.1}

    def calculate_quit_rate(self, jolts_data: Dict) -> Dict:
        """Calculate quit rate from JOLTS data"""
        try:
            if 'JTSQUL' in jolts_data and 'LNS12000000' in self.fred_data:
                quits = jolts_data['JTSQUL']['latest_value']
                employment = self.fred_data['LNS12000000']['data'][0]['value']
                quit_rate = (quits / employment) * 100
                
                return {
                    'quit_rate': quit_rate,
                    'quits': quits,
                    'employment': employment,
                    'interpretation': self._interpret_quit_rate(quit_rate)
                }
            else:
                return {'quit_rate': None, 'interpretation': 'insufficient_data'}
        except Exception as e:
            print(f"⚠️ Error calculating quit rate: {e}")
            return {'quit_rate': None, 'interpretation': 'error'}

    def _interpret_quit_rate(self, rate: float) -> str:
        """Interpret quit rate"""
        if rate > 2.5:
            return 'high_confidence'
        elif rate > 2.0:
            return 'moderate_confidence'
        else:
            return 'low_confidence'

    def analyze_state_unemployment_indicators(self, state_data: Dict) -> Dict:
        """Analyze state-level unemployment indicators"""
        if not state_data:
            return {'regional_dispersion': 'unknown', 'confidence_score': 0.1}
        
        try:
            # Get latest unemployment rates for all states
            latest_rates = {}
            for state_id, data in state_data.items():
                if data['data']:
                    latest_rates[state_id] = data['data'][0]['value']
            
            if not latest_rates:
                return {'regional_dispersion': 'unknown', 'confidence_score': 0.1}
            
            # Calculate statistics
            rates = list(latest_rates.values())
            avg_state_rate = sum(rates) / len(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            rate_std = (sum((x - avg_state_rate) ** 2 for x in rates) / len(rates)) ** 0.5
            
            # Calculate coefficient of variation (dispersion measure)
            cv = rate_std / avg_state_rate if avg_state_rate > 0 else 0
            
            # Determine regional dispersion level
            if cv > 0.3:
                dispersion_level = 'high'
                confidence_score = 0.8
            elif cv > 0.2:
                dispersion_level = 'moderate'
                confidence_score = 0.6
            else:
                dispersion_level = 'low'
                confidence_score = 0.4
            
            # Identify outlier states
            outliers = []
            for state_id, rate in latest_rates.items():
                if abs(rate - avg_state_rate) > 2 * rate_std:
                    outliers.append({
                        'state': state_id,
                        'rate': rate,
                        'deviation': rate - avg_state_rate
                    })
            
            # Calculate trend analysis (comparing latest vs 3 months ago)
            trend_analysis = {}
            for state_id, data in state_data.items():
                if len(data['data']) >= 3:
                    current = data['data'][0]['value']
                    previous = data['data'][2]['value']
                    change = current - previous
                    trend_analysis[state_id] = {
                        'current': current,
                        'change': change,
                        'trend': 'improving' if change < -0.1 else 'worsening' if change > 0.1 else 'stable'
                    }
            
            return {
                'regional_dispersion': dispersion_level,
                'average_state_rate': avg_state_rate,
                'rate_std': rate_std,
                'coefficient_variation': cv,
                'min_rate': min_rate,
                'max_rate': max_rate,
                'outliers': outliers,
                'trend_analysis': trend_analysis,
                'confidence_score': confidence_score,
                'latest_rates': latest_rates
            }
            
        except Exception as e:
            print(f"⚠️ Error analyzing state unemployment: {e}")
            return {'regional_dispersion': 'unknown', 'confidence_score': 0.1}

    def fetch_all_economic_data(self) -> Dict:
        """Fetch all economic data from all sources"""
        print("🔄 Starting comprehensive economic data fetch...")
        print(f"Foundation ID: {self.foundation_id}")
        print("="*80)
        
        # Fetch data from all sources
        self.fetch_bls_data()
        self.fetch_bea_data()
        self.fetch_fred_data()
        
        # Fetch additional wage growth data
        wage_data = self.fetch_wage_growth_data()
        
        # Fetch state-level unemployment data
        state_data = self.fetch_state_unemployment_data()
        
        # Analyze the data
        self.combined_analysis = self.analyze_economic_indicators()
        
        # Add wage growth analysis
        if wage_data:
            self.combined_analysis['wage_growth_analysis'] = self.analyze_wage_growth_indicators(wage_data)
        
        # Add quit rate calculation if we have JOLTS data
        if 'jolts_analysis' in self.combined_analysis:
            quit_rate_data = self.calculate_quit_rate(self.combined_analysis.get('jolts_analysis', {}))
            self.combined_analysis['quit_rate_analysis'] = quit_rate_data
        
        # Add state unemployment analysis
        if state_data:
            self.combined_analysis['state_unemployment_analysis'] = self.analyze_state_unemployment_indicators(state_data)
        
        print("✅ Economic data fetching complete!")
        
        return self.combined_analysis

def main():
    """Main execution function"""
    fetcher = EconomicDataFetcher()
    
    # Fetch all economic data
    analysis = fetcher.fetch_all_economic_data()
    
    # Save analysis and report
    fetcher.save_economic_data()
    fetcher.save_economic_report()
    
    # Print summary
    fetcher.print_economic_summary()
    
    return analysis

if __name__ == "__main__":
    main()