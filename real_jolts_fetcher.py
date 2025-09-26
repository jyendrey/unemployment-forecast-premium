#!/usr/bin/env python3
"""
Real JOLTS Data Fetcher using working FRED API key
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

class RealJOLTSFetcher:
    def __init__(self):
        self.fred_api_key = "a05f2e75daeca5fb9a47f2aa4ab0fba0"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # JOLTS series IDs
        self.jolts_series = {
            "JTSJOL": "Job Openings",
            "JTSHIL": "Hires", 
            "JTSQUL": "Quits",
            "JTSLDL": "Layoffs and Discharges"
        }

    def fetch_series_data(self, series_id, start_date="2020-01-01", end_date=None):
        """Fetch data from FRED API for a specific series"""
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
                print(f"Error in response for {series_id}: {data}")
                return []
                
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return []

    def get_latest_jolts_data(self):
        """Get the latest JOLTS data for all series"""
        jolts_data = {}
        
        print("Fetching REAL JOLTS data from FRED API...")
        print("=" * 60)
        
        for series_id, description in self.jolts_series.items():
            print(f"Fetching {series_id}: {description}")
            
            observations = self.fetch_series_data(series_id)
            
            if observations:
                # Get the most recent non-null observation
                latest_value = None
                latest_date = None
                
                for obs in observations:
                    if obs['value'] != '.' and obs['value'] is not None and obs['value'] != '':
                        try:
                            latest_value = float(obs['value'])
                            latest_date = obs['date']
                            break
                        except (ValueError, TypeError):
                            continue
                
                if latest_value is not None:
                    jolts_data[series_id] = {
                        'value': latest_value,
                        'date': latest_date,
                        'description': description
                    }
                    print(f"  ✓ Latest: {latest_value:,.0f} (as of {latest_date})")
                else:
                    print(f"  ✗ No valid data found")
            else:
                print(f"  ✗ Failed to fetch data")
            
            print()
        
        return jolts_data

    def calculate_rates(self, jolts_data):
        """Calculate JOLTS rates from raw data"""
        if not jolts_data:
            return {}
        
        # Get current employment level from FRED
        employment_data = self.fetch_series_data("PAYEMS", "2024-01-01")
        employment_level = 159540000  # Default fallback
        
        if employment_data:
            for obs in employment_data:
                if obs['value'] != '.' and obs['value'] is not None:
                    employment_level = float(obs['value']) * 1000  # PAYEMS is in thousands
                    break
        
        rates = {}
        
        for series_id, data in jolts_data.items():
            if series_id == "JTSJOL":
                # Job openings rate = job openings / (employment + job openings)
                rate = (data['value'] / (employment_level + data['value'])) * 100
                rates[f"{series_id}_rate"] = {
                    'value': rate,
                    'date': data['date'],
                    'description': f"{data['description']} Rate"
                }
            else:
                # Other rates = rate / employment * 100
                rate = (data['value'] / employment_level) * 100
                rates[f"{series_id}_rate"] = {
                    'value': rate,
                    'date': data['date'],
                    'description': f"{data['description']} Rate"
                }
        
        return rates

    def save_jolts_data(self, jolts_data, rates_data, filename="real_jolts_data.json"):
        """Save JOLTS data to JSON file"""
        combined_data = {
            'raw_data': jolts_data,
            'rates': rates_data,
            'fetched_at': datetime.now().isoformat(),
            'data_source': 'FRED API'
        }
        
        with open(filename, 'w') as f:
            json.dump(combined_data, f, indent=2)
        print(f"JOLTS data saved to {filename}")

    def create_jolts_analysis(self):
        """Create comprehensive JOLTS analysis"""
        jolts_data = self.get_latest_jolts_data()
        
        if not jolts_data:
            print("No JOLTS data available")
            return None, None
        
        print("REAL JOLTS DATA ANALYSIS")
        print("=" * 60)
        
        # Show raw data
        print("Raw JOLTS Data:")
        for series_id, data in jolts_data.items():
            print(f"{data['description']} ({series_id})")
            print(f"  Value: {data['value']:,.0f}")
            print(f"  Date: {data['date']}")
            print()
        
        # Calculate rates
        rates_data = self.calculate_rates(jolts_data)
        
        if rates_data:
            print("Calculated JOLTS Rates:")
            for series_id, data in rates_data.items():
                print(f"{data['description']} ({series_id})")
                print(f"  Rate: {data['value']:.2f}%")
                print(f"  Date: {data['date']}")
                print()
        
        # Save data
        self.save_jolts_data(jolts_data, rates_data)
        
        return jolts_data, rates_data

def main():
    fetcher = RealJOLTSFetcher()
    jolts_data, rates_data = fetcher.create_jolts_analysis()
    
    if jolts_data:
        print("✓ REAL JOLTS data successfully fetched and saved!")
        print("This data can now be used in the forecasting model.")
    else:
        print("✗ Failed to fetch JOLTS data")

if __name__ == "__main__":
    main()