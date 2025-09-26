#!/usr/bin/env python3
"""
Latest Data Fetcher - Get most recent data up to September 25, 2025
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

class LatestDataFetcher:
    def __init__(self):
        self.fred_api_key = "a05f2e75daeca5fb9a47f2aa4ab0fba0"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # Series IDs
        self.series_ids = {
            "UNRATE": "Unemployment Rate",
            "ICSA": "Initial Claims",
            "CCSA": "Continuing Claims", 
            "PAYEMS": "Nonfarm Payrolls",
            "CES0500000003": "Average Hourly Earnings",
            "JTSJOL": "Job Openings",
            "JTSHIL": "Hires",
            "JTSQUL": "Quits",
            "JTSLDL": "Layoffs and Discharges"
        }

    def fetch_latest_data(self, series_id, end_date="2025-09-25"):
        """Fetch the most recent data up to specified end date"""
        params = {
            "series_id": series_id,
            "api_key": self.fred_api_key,
            "file_type": "json",
            "observation_start": "2025-01-01",
            "observation_end": end_date,
            "sort_order": "desc",
            "limit": 20
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'observations' in data:
                # Get the most recent non-null observation
                for obs in data['observations']:
                    if obs['value'] != '.' and obs['value'] is not None and obs['value'] != '':
                        try:
                            return {
                                'value': float(obs['value']),
                                'date': obs['date'],
                                'realtime_start': obs.get('realtime_start', ''),
                                'realtime_end': obs.get('realtime_end', '')
                            }
                        except (ValueError, TypeError):
                            continue
                return None
            else:
                print(f"Error in response for {series_id}: {data}")
                return None
                
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return None

    def get_all_latest_data(self):
        """Get the most recent data for all series"""
        print("FETCHING LATEST DATA UP TO SEPTEMBER 25, 2025")
        print("=" * 60)
        print(f"Fetch Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        latest_data = {}
        
        for series_id, description in self.series_ids.items():
            print(f"Fetching {description} ({series_id})...")
            
            data = self.fetch_latest_data(series_id)
            
            if data:
                latest_data[series_id] = data
                print(f"  ✓ {data['value']:,.2f} (as of {data['date']})")
                print(f"    Realtime: {data['realtime_start']} to {data['realtime_end']}")
            else:
                print(f"  ✗ No data available")
            
            print()
        
        return latest_data

    def save_latest_data(self, latest_data, filename="latest_data_sept25.json"):
        """Save latest data to JSON file"""
        combined_data = {
            'latest_data': latest_data,
            'fetched_at': datetime.now().isoformat(),
            'data_source': 'FRED API',
            'end_date': '2025-09-25'
        }
        
        with open(filename, 'w') as f:
            json.dump(combined_data, f, indent=2)
        print(f"Latest data saved to {filename}")

    def create_latest_analysis(self):
        """Create analysis of latest data"""
        latest_data = self.get_all_latest_data()
        
        if not latest_data:
            print("No data available")
            return
        
        print("LATEST DATA ANALYSIS")
        print("=" * 60)
        
        # Group by data type
        print("LABOR MARKET INDICATORS:")
        print("-" * 30)
        for series_id in ["UNRATE", "ICSA", "CCSA", "PAYEMS", "CES0500000003"]:
            if series_id in latest_data:
                data = latest_data[series_id]
                description = self.series_ids[series_id]
                print(f"{description}: {data['value']:,.2f} (as of {data['date']})")
        print()
        
        print("JOLTS DATA:")
        print("-" * 30)
        for series_id in ["JTSJOL", "JTSHIL", "JTSQUL", "JTSLDL"]:
            if series_id in latest_data:
                data = latest_data[series_id]
                description = self.series_ids[series_id]
                print(f"{description}: {data['value']:,.0f} (as of {data['date']})")
        print()
        
        # Save data
        self.save_latest_data(latest_data)
        
        return latest_data

def main():
    fetcher = LatestDataFetcher()
    latest_data = fetcher.create_latest_analysis()
    
    if latest_data:
        print("✓ Latest data successfully fetched!")
        print("This data can now be used for the most current forecast.")
    else:
        print("✗ Failed to fetch latest data")

if __name__ == "__main__":
    main()