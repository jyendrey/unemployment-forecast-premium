#!/usr/bin/env python3
"""
Search for JOLTS series IDs in FRED
"""

import json
import urllib.request
import urllib.parse

class JOLTSSeriesSearcher:
    def __init__(self):
        self.fred_api_key = "7358702e869844db978f304b5079cfb8"
        self.search_url = "https://api.stlouisfed.org/fred/series/search"

    def search_jolts_series(self):
        """Search for JOLTS-related series"""
        params = {
            "search_text": "JOLTS",
            "api_key": self.fred_api_key,
            "file_type": "json",
            "limit": 50
        }
        
        url = f"{self.search_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'seriess' in data:
                print("JOLTS Series Found:")
                print("=" * 50)
                for series in data['seriess']:
                    print(f"ID: {series['id']}")
                    print(f"Title: {series['title']}")
                    print(f"Units: {series['units']}")
                    print(f"Frequency: {series['frequency']}")
                    print("-" * 30)
                return data['seriess']
            else:
                print(f"Error: {data}")
                return []
                
        except Exception as e:
            print(f"Error searching JOLTS series: {e}")
            return []

    def search_job_openings(self):
        """Search for job openings series"""
        params = {
            "search_text": "job openings",
            "api_key": self.fred_api_key,
            "file_type": "json",
            "limit": 20
        }
        
        url = f"{self.search_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'seriess' in data:
                print("\nJob Openings Series Found:")
                print("=" * 50)
                for series in data['seriess']:
                    print(f"ID: {series['id']}")
                    print(f"Title: {series['title']}")
                    print(f"Units: {series['units']}")
                    print("-" * 30)
                return data['seriess']
            else:
                print(f"Error: {data}")
                return []
                
        except Exception as e:
            print(f"Error searching job openings: {e}")
            return []

def main():
    searcher = JOLTSSeriesSearcher()
    
    # Search for JOLTS series
    jolts_series = searcher.search_jolts_series()
    
    # Search for job openings
    job_openings = searcher.search_job_openings()

if __name__ == "__main__":
    main()