#!/usr/bin/env python3
"""
Fetch Current API Data for Unemployment Forecasting
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

def fetch_bls_data(series_id, api_key, start_year, end_year):
    """Fetch data from BLS API"""
    base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    
    payload = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": api_key
    }
    
    try:
        req = urllib.request.Request(
            base_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching BLS data for {series_id}: {e}")
        return None

def fetch_bea_data(api_key, dataset_name, table_name, year):
    """Fetch data from BEA API"""
    base_url = "https://apps.bea.gov/api/data/"
    
    params = {
        'UserID': api_key,
        'method': 'GetData',
        'datasetname': dataset_name,
        'TableName': table_name,
        'Year': str(year),
        'ResultFormat': 'JSON'
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching BEA data: {e}")
        return None

def fetch_current_api_data():
    """Fetch current data from all APIs"""
    
    print("FETCHING CURRENT API DATA")
    print("="*50)
    
    # API Keys
    fred_key = "73c6c14c5998dda7efaf106939718f18"
    bls_key = "7358702e869844db978f304b5079cfb8"
    bea_key = "9CE55341-BAF6-4134-8119-56A1C0BD9BD3"
    
    # Date range for recent data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
    
    print(f"Fetching data from {start_date} to {end_date}")
    print()
    
    # FRED Data
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
        'JTSLDL': 'Layoffs and Discharges',
        'PAYEMS': 'Total Nonfarm Payrolls',
        'UNEMPLOY': 'Unemployed',
        'EMRATIO': 'Employment-Population Ratio',
        'AHE': 'Average Hourly Earnings',
        'ECIWAG': 'Employment Cost Index - Wages',
        'PMI': 'Purchasing Managers Index',
        'LEI': 'Leading Economic Index'
    }
    
    fred_data = {}
    
    for series_id, description in fred_series.items():
        print(f"Fetching {description} ({series_id})...")
        data = fetch_fred_data(series_id, fred_key, start_date, end_date)
        if data and 'observations' in data:
            fred_data[series_id] = {
                'description': description,
                'data': data['observations'][:12],  # Last 12 observations
                'status': 'success'
            }
            print(f"  ✓ Success: {len(data['observations'])} observations")
        else:
            fred_data[series_id] = {
                'description': description,
                'data': [],
                'status': 'failed'
            }
            print(f"  ✗ Failed")
    
    print()
    
    # BLS Data
    print("FETCHING BLS DATA")
    print("-" * 30)
    
    bls_series = {
        'LNS14000000': 'Unemployment Rate',
        'LNS11300000': 'Labor Force Participation Rate',
        'LNS13000000': 'Employment-Population Ratio'
    }
    
    bls_data = {}
    current_year = datetime.now().year
    
    for series_id, description in bls_series.items():
        print(f"Fetching {description} ({series_id})...")
        data = fetch_bls_data(series_id, bls_key, current_year-1, current_year)
        if data and 'Results' in data and 'series' in data['Results']:
            bls_data[series_id] = {
                'description': description,
                'data': data['Results']['series'][0]['data'][:12],  # Last 12 observations
                'status': 'success'
            }
            print(f"  ✓ Success: {len(data['Results']['series'][0]['data'])} observations")
        else:
            bls_data[series_id] = {
                'description': description,
                'data': [],
                'status': 'failed'
            }
            print(f"  ✗ Failed")
    
    print()
    
    # BEA Data
    print("FETCHING BEA DATA")
    print("-" * 30)
    
    bea_data = {}
    current_year = datetime.now().year
    
    print(f"Fetching GDP data for {current_year}...")
    gdp_data = fetch_bea_data(bea_key, 'NIPA', 'T10101', current_year)
    if gdp_data and 'BEAAPI' in gdp_data and 'Results' in gdp_data['BEAAPI']:
        bea_data['GDP'] = {
            'description': 'Gross Domestic Product',
            'data': gdp_data['BEAAPI']['Results']['Data'][:12],  # Last 12 observations
            'status': 'success'
        }
        print(f"  ✓ Success: {len(gdp_data['BEAAPI']['Results']['Data'])} observations")
    else:
        bea_data['GDP'] = {
            'description': 'Gross Domestic Product',
            'data': [],
            'status': 'failed'
        }
        print(f"  ✗ Failed")
    
    print()
    
    # Compile results
    api_results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': {
            'start': start_date,
            'end': end_date
        },
        'fred_data': fred_data,
        'bls_data': bls_data,
        'bea_data': bea_data,
        'summary': {
            'fred_success': sum(1 for v in fred_data.values() if v['status'] == 'success'),
            'fred_total': len(fred_data),
            'bls_success': sum(1 for v in bls_data.values() if v['status'] == 'success'),
            'bls_total': len(bls_data),
            'bea_success': sum(1 for v in bea_data.values() if v['status'] == 'success'),
            'bea_total': len(bea_data)
        }
    }
    
    # Save results
    with open('current_api_data.json', 'w') as f:
        json.dump(api_results, f, indent=2)
    
    print("API DATA FETCH SUMMARY")
    print("-" * 30)
    print(f"FRED: {api_results['summary']['fred_success']}/{api_results['summary']['fred_total']} successful")
    print(f"BLS: {api_results['summary']['bls_success']}/{api_results['summary']['bls_total']} successful")
    print(f"BEA: {api_results['summary']['bea_success']}/{api_results['summary']['bea_total']} successful")
    print()
    print(f"Data saved to: current_api_data.json")
    
    return api_results

if __name__ == "__main__":
    results = fetch_current_api_data()
    print(f"\nAPI data fetch completed!")