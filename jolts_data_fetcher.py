#!/usr/bin/env python3
"""
JOLTS Data Fetcher using FRED API
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

class JOLTSDataFetcher:
    def __init__(self):
        self.fred_api_key = "7358702e869844db978f304b5079cfb8"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # JOLTS series IDs
        self.jolts_series = {
            "JTSJOL": "Job Openings Rate",
            "JTSHIL": "Hires Rate", 
            "JTSQUL": "Quits Rate",
            "JTSLDL": "Layoffs and Discharges Rate"
        }

    def fetch_jolts_data(self, series_id, start_date="2020-01-01", end_date=None):
        """Fetch JOLTS data from FRED API"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            "series_id": series_id,
            "api_key": self.fred_api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date,
            "sort_order": "desc",
            "limit": 50
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'observations' in data:
                return data['observations']
            else:
                print(f"Error fetching {series_id}: {data}")
                return []
                
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return []

    def get_latest_jolts_data(self):
        """Get the latest JOLTS data for all series"""
        jolts_data = {}
        
        print("Fetching JOLTS data from FRED API...")
        print("=" * 50)
        
        for series_id, description in self.jolts_series.items():
            print(f"Fetching {series_id}: {description}")
            
            observations = self.fetch_jolts_data(series_id)
            
            if observations:
                # Get the most recent non-null observation
                latest_value = None
                latest_date = None
                
                for obs in observations:
                    if obs['value'] != '.' and obs['value'] is not None:
                        latest_value = float(obs['value'])
                        latest_date = obs['date']
                        break
                
                if latest_value is not None:
                    jolts_data[series_id] = {
                        'value': latest_value,
                        'date': latest_date,
                        'description': description
                    }
                    print(f"  Latest: {latest_value:.2f}% (as of {latest_date})")
                else:
                    print(f"  No valid data found")
            else:
                print(f"  Failed to fetch data")
            
            print()
        
        return jolts_data

    def save_jolts_data(self, jolts_data, filename="jolts_data.json"):
        """Save JOLTS data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(jolts_data, f, indent=2)
        print(f"JOLTS data saved to {filename}")

    def create_jolts_analysis(self):
        """Create comprehensive JOLTS analysis"""
        jolts_data = self.get_latest_jolts_data()
        
        if not jolts_data:
            print("No JOLTS data available")
            return
        
        print("JOLTS DATA ANALYSIS")
        print("=" * 50)
        
        for series_id, data in jolts_data.items():
            print(f"{data['description']} ({series_id})")
            print(f"  Value: {data['value']:.2f}%")
            print(f"  Date: {data['date']}")
            print()
        
        # Save data
        self.save_jolts_data(jolts_data)
        
        return jolts_data

def main():
    fetcher = JOLTSDataFetcher()
    jolts_data = fetcher.create_jolts_analysis()
    
    if jolts_data:
        print("JOLTS data successfully fetched and saved!")
    else:
        print("Failed to fetch JOLTS data")

if __name__ == "__main__":
    main()