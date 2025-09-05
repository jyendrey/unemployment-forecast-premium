#!/usr/bin/env python3
"""
Fetch Current API Data for Unemployment Forecasting (Fixed)
Pull real data from FRED, BLS, and BEA APIs
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def fetch_fred_data(series_id, api_key, start_date=None, end_date=None):
    """Fetch data from FRED API"""
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1000
    }
    
    if start_date:
        params['observation_start'] = start_date
    if end_date:
        params['observation_end'] = end_date
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching FRED data for {series_id}: {e}")
        return None

def fetch_current_api_data():
    """Fetch current data from FRED API"""
    
    print("FETCHING CURRENT API DATA")
    print("="*50)
    
    # FRED API Key
    fred_key = "73c6c14c5998dda7efaf106939718f18"
    
    # Date range for recent data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
    
    print(f"Fetching data from {start_date} to {end_date}")
    print()
    
    # FRED Data - Core Labor Market Indicators
    print("FETCHING FRED DATA")
    print("-" * 30)
    
    fred_series = {
        'UNRATE': 'Unemployment Rate',
        'CIVPART': 'Labor Force Participation Rate',
        'ICSA': 'Initial Claims',
        'CCSA': 'Continuing Claims',
        'JTSJOL': 'Job Openings',
        'JTSHIL': 'Hires',
        'JTSTSL': 'Total Separations',
        'JTSQUL': 'Quits',
        'PAYEMS': 'Total Nonfarm Payrolls',
        'UNEMPLOY': 'Unemployed',
        'EMRATIO': 'Employment-Population Ratio'
    }
    
    fred_data = {}
    
    for series_id, description in fred_series.items():
        print(f"Fetching {description} ({series_id})...")
        data = fetch_fred_data(series_id, fred_key, start_date, end_date)
        if data and 'observations' in data:
            # Get the most recent 12 observations
            recent_data = data['observations'][:12]
            fred_data[series_id] = {
                'description': description,
                'data': recent_data,
                'status': 'success',
                'count': len(recent_data)
            }
            print(f"  ✓ Success: {len(recent_data)} observations")
            
            # Show latest value
            if recent_data:
                latest = recent_data[0]
                print(f"    Latest: {latest['value']} ({latest['date']})")
        else:
            fred_data[series_id] = {
                'description': description,
                'data': [],
                'status': 'failed',
                'count': 0
            }
            print(f"  ✗ Failed")
    
    print()
    
    # Analyze the data
    print("DATA ANALYSIS")
    print("-" * 30)
    
    # Get latest unemployment rate
    if fred_data['UNRATE']['status'] == 'success' and fred_data['UNRATE']['data']:
        latest_unrate = fred_data['UNRATE']['data'][0]['value']
        print(f"Latest Unemployment Rate: {latest_unrate}% ({fred_data['UNRATE']['data'][0]['date']})")
    
    # Get latest labor force participation
    if fred_data['CIVPART']['status'] == 'success' and fred_data['CIVPART']['data']:
        latest_lfpr = fred_data['CIVPART']['data'][0]['value']
        print(f"Latest Labor Force Participation: {latest_lfpr}% ({fred_data['CIVPART']['data'][0]['date']})")
    
    # Get latest initial claims
    if fred_data['ICSA']['status'] == 'success' and fred_data['ICSA']['data']:
        latest_claims = int(fred_data['ICSA']['data'][0]['value'])
        print(f"Latest Initial Claims: {latest_claims:,} ({fred_data['ICSA']['data'][0]['date']})")
    
    # Get latest continuing claims
    if fred_data['CCSA']['status'] == 'success' and fred_data['CCSA']['data']:
        latest_continuing = int(fred_data['CCSA']['data'][0]['value'])
        print(f"Latest Continuing Claims: {latest_continuing:,} ({fred_data['CCSA']['data'][0]['date']})")
    
    # Get latest JOLTS data
    if fred_data['JTSJOL']['status'] == 'success' and fred_data['JTSJOL']['data']:
        latest_openings = int(fred_data['JTSJOL']['data'][0]['value'])
        print(f"Latest Job Openings: {latest_openings:,} ({fred_data['JTSJOL']['data'][0]['date']})")
    
    if fred_data['JTSHIL']['status'] == 'success' and fred_data['JTSHIL']['data']:
        latest_hires = int(fred_data['JTSHIL']['data'][0]['value'])
        print(f"Latest Hires: {latest_hires:,} ({fred_data['JTSHIL']['data'][0]['date']})")
    
    if fred_data['JTSQUL']['status'] == 'success' and fred_data['JTSQUL']['data']:
        latest_quits = int(fred_data['JTSQUL']['data'][0]['value'])
        print(f"Latest Quits: {latest_quits:,} ({fred_data['JTSQUL']['data'][0]['date']})")
    
    print()
    
    # Calculate trends
    print("TREND ANALYSIS")
    print("-" * 30)
    
    # Unemployment rate trend
    if fred_data['UNRATE']['status'] == 'success' and len(fred_data['UNRATE']['data']) >= 2:
        current_rate = float(fred_data['UNRATE']['data'][0]['value'])
        prev_rate = float(fred_data['UNRATE']['data'][1]['value'])
        trend = current_rate - prev_rate
        print(f"Unemployment Rate Trend: {trend:+.2f} percentage points")
    
    # Initial claims trend
    if fred_data['ICSA']['status'] == 'success' and len(fred_data['ICSA']['data']) >= 4:
        recent_claims = [float(d['value']) for d in fred_data['ICSA']['data'][:4]]
        avg_claims = sum(recent_claims) / len(recent_claims)
        print(f"4-Week Average Initial Claims: {int(avg_claims):,}")
    
    # Labor force participation trend
    if fred_data['CIVPART']['status'] == 'success' and len(fred_data['CIVPART']['data']) >= 2:
        current_lfpr = float(fred_data['CIVPART']['data'][0]['value'])
        prev_lfpr = float(fred_data['CIVPART']['data'][1]['value'])
        trend = current_lfpr - prev_lfpr
        print(f"Labor Force Participation Trend: {trend:+.2f} percentage points")
    
    print()
    
    # Compile results
    api_results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': {
            'start': start_date,
            'end': end_date
        },
        'fred_data': fred_data,
        'summary': {
            'fred_success': sum(1 for v in fred_data.values() if v['status'] == 'success'),
            'fred_total': len(fred_data),
            'total_observations': sum(v['count'] for v in fred_data.values())
        }
    }
    
    # Save results
    with open('current_api_data.json', 'w') as f:
        json.dump(api_results, f, indent=2)
    
    print("API DATA FETCH SUMMARY")
    print("-" * 30)
    print(f"FRED: {api_results['summary']['fred_success']}/{api_results['summary']['fred_total']} successful")
    print(f"Total observations: {api_results['summary']['total_observations']}")
    print()
    print(f"Data saved to: current_api_data.json")
    
    return api_results

if __name__ == "__main__":
    results = fetch_current_api_data()
    print(f"\nAPI data fetch completed!")