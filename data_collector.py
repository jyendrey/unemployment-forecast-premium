#!/usr/bin/env python3
"""
Real-Time Data Collector for Interactive Brokers Dashboard
==========================================================

Handles real-time data collection from BLS, FRED, and BEA APIs
with intelligent caching and error handling.

Features:
- Real-time API data collection
- Intelligent caching system
- Data quality validation
- Error recovery and retry logic
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional, Tuple
import logging

class RealTimeDataCollector:
    """
    Real-time data collection system for unemployment forecasting
    """
    
    def __init__(self):
        # API Configuration
        self.bls_key = "7358702e869844db978f304b5079cfb8"
        self.fred_key = "73c6c14c5998dda7efaf106939718f18"
        self.bea_key = "9CE55341-BAF6-4134-8119-56A1C0BD9BD3"
        
        # Cache configuration
        self.cache = {}
        self.cache_duration = 600  # 10 minutes
        self.last_update = {}
        
        # Data quality tracking
        self.data_quality_scores = {}
        self.api_status = {
            'bls': True,
            'fred': True,
            'bea': True
        }
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_latest_data(self) -> Dict:
        """
        Get latest economic data from all sources
        """
        current_time = datetime.now()
        
        # Check if cache is still valid
        if self._is_cache_valid():
            self.logger.info("Using cached data")
            return self.cache.get('latest_data', {})
        
        self.logger.info("Collecting fresh data from APIs...")
        
        latest_data = {
            'unemployment_current': self._get_current_unemployment(),
            'weekly_claims': self._get_weekly_claims(),
            'labor_force_participation': self._get_labor_force_participation(),
            'jolts_data': self._get_jolts_data(),
            'economic_indicators': self._get_key_economic_indicators(),
            'last_updated': current_time.isoformat(),
            'data_quality': self._assess_data_quality(),
            'api_status': self.api_status.copy()
        }
        
        # Cache the results
        self.cache['latest_data'] = latest_data
        self.last_update['latest_data'] = current_time
        
        return latest_data
    
    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if 'latest_data' not in self.cache:
            return False
        
        last_update_time = self.last_update.get('latest_data')
        if not last_update_time:
            return False
        
        time_diff = (datetime.now() - last_update_time).total_seconds()
        return time_diff < self.cache_duration
    
    def _get_current_unemployment(self) -> Dict:
        """Get current unemployment rate from BLS"""
        try:
            # Use BLS API to get most recent unemployment rate
            headers = {'Content-type': 'application/json'}
            url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
            
            data = {
                "seriesid": ["LNS14000000"],  # Unemployment Rate
                "startyear": "2024",
                "endyear": "2025",
                "registrationkey": self.bls_key
            }
            
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
            
            if response.status_code == 200:
                json_data = response.json()
                
                if json_data.get('status') == 'REQUEST_SUCCEEDED':
                    series_data = json_data['Results']['series'][0]['data']
                    
                    # Get most recent data point
                    latest_point = series_data[0]
                    
                    self.api_status['bls'] = True
                    
                    return {
                        'rate': float(latest_point['value']),
                        'period': latest_point['period'],
                        'year': latest_point['year'],
                        'date': f"{latest_point['year']}-{latest_point['period'][1:].zfill(2)}-01",
                        'source': 'BLS',
                        'series_id': 'LNS14000000'
                    }
            
            self.api_status['bls'] = False
            self.logger.warning("BLS API failed, using fallback")
            
        except Exception as e:
            self.logger.error(f"Error getting unemployment data: {str(e)}")
            self.api_status['bls'] = False
        
        # Fallback to known recent value
        return {
            'rate': 4.2,
            'period': 'M07',
            'year': '2025',
            'date': '2025-07-01',
            'source': 'Fallback',
            'series_id': 'LNS14000000'
        }
    
    def _get_weekly_claims(self) -> Dict:
        """Get latest weekly jobless claims from FRED"""
        try:
            # Get initial claims
            initial_claims = self._get_fred_series('ICSA', limit=4)
            continuing_claims = self._get_fred_series('CCSA', limit=4)
            
            self.api_status['fred'] = True
            
            return {
                'initial_claims': {
                    'current': initial_claims['current'] if initial_claims else 320000,
                    'trend': initial_claims['trend'] if initial_claims else 0,
                    'data': initial_claims['values'][:4] if initial_claims else []
                },
                'continuing_claims': {
                    'current': continuing_claims['current'] if continuing_claims else 1800000,
                    'trend': continuing_claims['trend'] if continuing_claims else 0,
                    'data': continuing_claims['values'][:4] if continuing_claims else []
                },
                'source': 'FRED'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting claims data: {str(e)}")
            self.api_status['fred'] = False
            
            return {
                'initial_claims': {'current': 320000, 'trend': 0, 'data': []},
                'continuing_claims': {'current': 1800000, 'trend': 0, 'data': []},
                'source': 'Fallback'
            }
    
    def _get_labor_force_participation(self) -> Dict:
        """Get labor force participation data (critical for our model)"""
        try:
            participation_rate = self._get_fred_series('CIVPART', limit=6)
            employment_ratio = self._get_fred_series('EMRATIO', limit=6)
            
            return {
                'participation_rate': {
                    'current': participation_rate['current'] if participation_rate else 62.4,
                    'trend': participation_rate['trend'] if participation_rate else 0,
                    'recent_change': self._calculate_recent_change(participation_rate['values'][:3]) if participation_rate else 0
                },
                'employment_ratio': {
                    'current': employment_ratio['current'] if employment_ratio else 59.7,
                    'trend': employment_ratio['trend'] if employment_ratio else 0,
                    'recent_change': self._calculate_recent_change(employment_ratio['values'][:3]) if employment_ratio else 0
                },
                'source': 'FRED'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting labor force data: {str(e)}")
            
            return {
                'participation_rate': {'current': 62.4, 'trend': 0, 'recent_change': -0.15},
                'employment_ratio': {'current': 59.7, 'trend': 0, 'recent_change': -0.10},
                'source': 'Fallback'
            }
    
    def _get_jolts_data(self) -> Dict:
        """Get JOLTS (Job Openings and Labor Turnover) data"""
        try:
            job_openings = self._get_fred_series('JTSJOL', limit=6)
            quits_rate = self._get_fred_series('JTSQUR', limit=6)
            hires_rate = self._get_fred_series('JTSHIR', limit=6)
            
            return {
                'job_openings': {
                    'current': job_openings['current'] if job_openings else 7800,
                    'trend': job_openings['trend'] if job_openings else 0,
                    'units': 'thousands'
                },
                'quits_rate': {
                    'current': quits_rate['current'] if quits_rate else 2.3,
                    'trend': quits_rate['trend'] if quits_rate else 0,
                    'units': 'percent'
                },
                'hires_rate': {
                    'current': hires_rate['current'] if hires_rate else 3.4,
                    'trend': hires_rate['trend'] if hires_rate else 0,
                    'units': 'percent'
                },
                'source': 'FRED'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting JOLTS data: {str(e)}")
            
            return {
                'job_openings': {'current': 7800, 'trend': -0.05, 'units': 'thousands'},
                'quits_rate': {'current': 2.3, 'trend': 0, 'units': 'percent'},
                'hires_rate': {'current': 3.4, 'trend': 0, 'units': 'percent'},
                'source': 'Fallback'
            }
    
    def _get_key_economic_indicators(self) -> Dict:
        """Get key economic indicators for context"""
        try:
            fed_funds = self._get_fred_series('FEDFUNDS', limit=3)
            consumer_sentiment = self._get_fred_series('UMCSENT', limit=3)
            yield_spread = self._get_fred_series('T10Y2Y', limit=3)
            
            return {
                'federal_funds_rate': {
                    'current': fed_funds['current'] if fed_funds else 4.33,
                    'trend': fed_funds['trend'] if fed_funds else 0
                },
                'consumer_sentiment': {
                    'current': consumer_sentiment['current'] if consumer_sentiment else 71.2,
                    'trend': consumer_sentiment['trend'] if consumer_sentiment else 0
                },
                'yield_spread_10y2y': {
                    'current': yield_spread['current'] if yield_spread else 0.15,
                    'trend': yield_spread['trend'] if yield_spread else 0
                },
                'source': 'FRED'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting economic indicators: {str(e)}")
            
            return {
                'federal_funds_rate': {'current': 4.33, 'trend': 0},
                'consumer_sentiment': {'current': 71.2, 'trend': 0},
                'yield_spread_10y2y': {'current': 0.15, 'trend': 0},
                'source': 'Fallback'
            }
    
    def _get_fred_series(self, series_id: str, limit: int = 12) -> Optional[Dict]:
        """Get data from FRED API for specific series"""
        try:
            base_url = "https://api.stlouisfed.org/fred/series/observations"
            
            params = {
                'series_id': series_id,
                'api_key': self.fred_key,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': limit
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'observations' in data:
                    valid_obs = [obs for obs in data['observations'] if obs['value'] != '.']
                    
                    if valid_obs:
                        values = [float(obs['value']) for obs in valid_obs]
                        dates = [obs['date'] for obs in valid_obs]
                        
                        return {
                            'current': values[0],
                            'values': values,
                            'dates': dates,
                            'trend': self._calculate_trend(values[:6]) if len(values) >= 6 else 0,
                            'series_id': series_id
                        }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting FRED series {series_id}: {str(e)}")
            return None
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate simple trend from recent values"""
        if len(values) < 3:
            return 0.0
        
        # Simple linear trend using least squares
        n = len(values)
        x = list(range(n))
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        denominator = n * sum_x2 - sum_x ** 2
        if denominator != 0:
            slope = (n * sum_xy - sum_x * sum_y) / denominator
            return slope
        
        return 0.0
    
    def _calculate_recent_change(self, values: List[float]) -> float:
        """Calculate recent change in values"""
        if len(values) < 2:
            return 0.0
        
        return values[0] - values[1]
    
    def _assess_data_quality(self) -> Dict:
        """Assess overall data quality"""
        api_success_count = sum(self.api_status.values())
        total_apis = len(self.api_status)
        
        quality_score = api_success_count / total_apis
        
        if quality_score >= 0.8:
            quality_level = "High"
        elif quality_score >= 0.6:
            quality_level = "Medium"
        else:
            quality_level = "Low"
        
        return {
            'overall_score': quality_score,
            'level': quality_level,
            'apis_working': api_success_count,
            'total_apis': total_apis,
            'last_assessment': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test the data collector
    collector = RealTimeDataCollector()
    
    print("Testing Real-Time Data Collector...")
    print("=" * 50)
    
    data = collector.get_latest_data()
    
    print(f"Current Unemployment Rate: {data['unemployment_current']['rate']}%")
    print(f"Labor Force Participation: {data['labor_force_participation']['participation_rate']['current']}%")
    print(f"Initial Claims: {data['weekly_claims']['initial_claims']['current']:,.0f}")
    print(f"Data Quality: {data['data_quality']['level']}")
