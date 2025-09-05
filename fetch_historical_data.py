#!/usr/bin/env python3
"""
Fetch Historical Data (2010-2025)
Get 15+ years of data for proper econometric modeling
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def fetch_historical_data():
    """Fetch 15+ years of historical data from FRED API"""
    
    print("FETCHING HISTORICAL DATA (2010-2025)")
    print("="*50)
    
    # FRED API Key
    fred_key = "73c6c14c5998dda7efaf106939718f18"
    
    # Date range for historical data
    start_date = "2010-01-01"
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Fetching data from {start_date} to {end_date}")
    print()
    
    # Core labor market indicators
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
    
    historical_data = {}
    
    for series_id, description in fred_series.items():
        print(f"Fetching {description} ({series_id})...")
        data = fetch_fred_data(series_id, fred_key, start_date, end_date)
        if data and 'observations' in data:
            observations = data['observations']
            # Filter out missing values
            valid_obs = [obs for obs in observations if obs['value'] != '.']
            historical_data[series_id] = {
                'description': description,
                'data': valid_obs,
                'count': len(valid_obs),
                'status': 'success',
                'first_date': valid_obs[-1]['date'] if valid_obs else None,
                'last_date': valid_obs[0]['date'] if valid_obs else None
            }
            print(f"  ✓ Success: {len(valid_obs)} observations")
            print(f"    Date range: {valid_obs[-1]['date']} to {valid_obs[0]['date']}")
        else:
            historical_data[series_id] = {
                'description': description,
                'data': [],
                'count': 0,
                'status': 'failed',
                'first_date': None,
                'last_date': None
            }
            print(f"  ✗ Failed")
    
    print()
    
    # Analyze data availability
    print("DATA AVAILABILITY ANALYSIS")
    print("-" * 30)
    
    successful_series = [k for k, v in historical_data.items() if v['status'] == 'success']
    failed_series = [k for k, v in historical_data.items() if v['status'] == 'failed']
    
    print(f"Successful series: {len(successful_series)}/{len(fred_series)}")
    print(f"Failed series: {len(failed_series)}")
    
    if successful_series:
        print(f"\nSuccessful series:")
        for series_id in successful_series:
            data_info = historical_data[series_id]
            print(f"  {series_id}: {data_info['count']} obs ({data_info['first_date']} to {data_info['last_date']})")
    
    if failed_series:
        print(f"\nFailed series:")
        for series_id in failed_series:
            print(f"  {series_id}: {historical_data[series_id]['description']}")
    
    print()
    
    # Check if we have enough data for modeling
    print("MODELING READINESS CHECK")
    print("-" * 30)
    
    # Check for core indicators
    core_indicators = ['UNRATE', 'CIVPART', 'ICSA', 'CCSA']
    core_available = all(series in successful_series for series in core_indicators)
    
    # Check for JOLTS data
    jolts_indicators = ['JTSJOL', 'JTSHIL', 'JTSTSL', 'JTSQUL']
    jolts_available = all(series in successful_series for series in jolts_indicators)
    
    # Check data length
    min_observations = 100  # Need at least 100 observations for reliable modeling
    sufficient_data = all(historical_data[series]['count'] >= min_observations 
                         for series in successful_series)
    
    print(f"Core indicators available: {core_available}")
    print(f"JOLTS data available: {jolts_available}")
    print(f"Sufficient observations: {sufficient_data}")
    
    if core_available and sufficient_data:
        print("✓ Ready for econometric modeling")
        modeling_ready = True
    else:
        print("✗ Not ready for econometric modeling")
        modeling_ready = False
    
    print()
    
    # Sample data analysis
    if modeling_ready:
        print("SAMPLE DATA ANALYSIS")
        print("-" * 30)
        
        # Unemployment rate analysis
        if 'UNRATE' in successful_series:
            unrate_data = historical_data['UNRATE']['data']
            unrate_values = [float(obs['value']) for obs in unrate_data]
            min_unrate = min(unrate_values)
            max_unrate = max(unrate_values)
            avg_unrate = sum(unrate_values) / len(unrate_values)
            print(f"Unemployment Rate:")
            print(f"  Range: {min_unrate:.1f}% to {max_unrate:.1f}%")
            print(f"  Average: {avg_unrate:.1f}%")
            print(f"  Observations: {len(unrate_values)}")
        
        # Labor force participation analysis
        if 'CIVPART' in successful_series:
            lfpr_data = historical_data['CIVPART']['data']
            lfpr_values = [float(obs['value']) for obs in lfpr_data]
            min_lfpr = min(lfpr_values)
            max_lfpr = max(lfpr_values)
            avg_lfpr = sum(lfpr_values) / len(lfpr_values)
            print(f"\nLabor Force Participation Rate:")
            print(f"  Range: {min_lfpr:.1f}% to {max_lfpr:.1f}%")
            print(f"  Average: {avg_lfpr:.1f}%")
            print(f"  Observations: {len(lfpr_values)}")
        
        # Initial claims analysis
        if 'ICSA' in successful_series:
            claims_data = historical_data['ICSA']['data']
            claims_values = [int(obs['value']) for obs in claims_data]
            min_claims = min(claims_values)
            max_claims = max(claims_values)
            avg_claims = sum(claims_values) / len(claims_values)
            print(f"\nInitial Claims:")
            print(f"  Range: {min_claims:,} to {max_claims:,}")
            print(f"  Average: {int(avg_claims):,}")
            print(f"  Observations: {len(claims_values)}")
    
    # Compile results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': {
            'start': start_date,
            'end': end_date
        },
        'historical_data': historical_data,
        'summary': {
            'total_series': len(fred_series),
            'successful_series': len(successful_series),
            'failed_series': len(failed_series),
            'modeling_ready': modeling_ready,
            'core_indicators_available': core_available,
            'jolts_data_available': jolts_available,
            'sufficient_data': sufficient_data
        }
    }
    
    # Save results
    with open('historical_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nHistorical data saved to: historical_data.json")
    
    return results

def fetch_fred_data(series_id, api_key, start_date=None, end_date=None):
    """Fetch data from FRED API"""
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 10000  # Increased limit for historical data
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

if __name__ == "__main__":
    results = fetch_historical_data()
    print(f"\nHistorical data fetch completed!")