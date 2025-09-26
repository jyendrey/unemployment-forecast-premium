#!/usr/bin/env python3
"""
Test new FRED API key
"""

import urllib.request
import json

def test_new_fred_key():
    api_key = "a05f2e75daeca5fb9a47f2aa4ab0fba0"
    
    # Test with a simple request first
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json&limit=1"
    
    print(f"Testing new API key with UNRATE...")
    print(f"URL: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print("✓ API key works!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    test_new_fred_key()