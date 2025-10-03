#!/usr/bin/env python3
"""
Test FRED API with known working series
"""

import json
import urllib.request
import urllib.parse

def test_fred_api():
    fred_api_key = "7358702e869844db978f304b5079cfb8"
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    # Test with a known working series
    test_series = "UNRATE"  # Unemployment rate
    
    params = {
        "series_id": test_series,
        "api_key": fred_api_key,
        "file_type": "json",
        "observation_start": "2024-01-01",
        "observation_end": "2024-12-31",
        "sort_order": "desc",
        "limit": 5
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        print("FRED API Test - UNRATE series:")
        print("=" * 40)
        print(f"URL: {url}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if 'observations' in data:
            print(f"Found {len(data['observations'])} observations")
        else:
            print("No observations found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fred_api()