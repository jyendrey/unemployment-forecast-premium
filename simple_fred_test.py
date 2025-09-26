#!/usr/bin/env python3
"""
Simple FRED API test
"""

import urllib.request
import json

def test_simple_fred():
    api_key = "7358702e869844db978f304b5079cfb8"
    
    # Test with a simple request
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json&limit=1"
    
    print(f"Testing URL: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print("Success!")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_simple_fred()