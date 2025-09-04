#!/usr/bin/env python3
"""
Fetch New Claims Data and Update Forecast
Uses FRED API to get latest initial and continuing claims data
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time

class ClaimsDataFetcher:
    def __init__(self):
        self.fred_api_key = "73c6c14c5998dda7efaf106939718f18"
        self.fred_endpoint = "https://api.stlouisfed.org/fred/series/observations"
        
        # Claims Series IDs
        self.claims_series = {
            "ICSA": "Initial Claims",
            "CCSA": "Continuing Claims"
        }
        
    def fetch_claims_data(self):
        """Fetch latest claims data from FRED"""
        print("🔄 Fetching latest claims data from FRED...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        claims_data = {}
        
        for series_id, description in self.claims_series.items():
            try:
                print(f"\n📊 Fetching {description} ({series_id})...")
                
                # FRED API parameters
                params = {
                    'series_id': series_id,
                    'api_key': self.fred_api_key,
                    'file_type': 'json',
                    'limit': 12,  # Last 12 weeks
                    'sort_order': 'desc',
                    'observation_start': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
                    'observation_end': datetime.now().strftime('%Y-%m-%d')
                }
                
                # Create URL
                url = self.fred_endpoint + '?' + urllib.parse.urlencode(params)
                
                # Make request
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
                
                if 'observations' in data:
                    observations = data['observations']
                    
                    # Process the data
                    processed_data = []
                    for obs in observations:
                        if obs['value'] != '.' and obs['value'] is not None:
                            processed_data.append({
                                'date': obs['date'],
                                'value': float(obs['value']),
                                'realtime_start': obs['realtime_start'],
                                'realtime_end': obs['realtime_end']
                            })
                    
                    if processed_data:
                        # Sort by date (most recent first)
                        processed_data.sort(key=lambda x: x['date'], reverse=True)
                        
                        result = {
                            'description': description,
                            'data': processed_data,
                            'latest_value': processed_data[0]['value'],
                            'latest_date': processed_data[0]['date'],
                            'total_observations': len(processed_data)
                        }
                        
                        print(f"✅ {description}: {processed_data[0]['value']:,.0f} ({processed_data[0]['date']})")
                        
                        # Show trend if we have at least 2 data points
                        if len(processed_data) >= 2:
                            current = processed_data[0]['value']
                            previous = processed_data[1]['value']
                            change = current - previous
                            change_pct = (change / previous) * 100 if previous != 0 else 0
                            
                            direction = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                            print(f"   Trend: {direction} {change:+,.0f} ({change_pct:+.1f}%)")
                        
                        claims_data[series_id] = result
                    else:
                        print(f"⚠️ No valid data found for {series_id}")
                else:
                    print(f"⚠️ No observations found for {series_id}")
                    
            except Exception as e:
                print(f"❌ Error fetching {series_id}: {e}")
            
            # Rate limiting for FRED API
            time.sleep(0.5)
        
        return claims_data
    
    def analyze_claims_impact(self, claims_data):
        """Analyze the impact of new claims data on forecast"""
        print("\n" + "=" * 60)
        print("🔍 CLAIMS DATA IMPACT ANALYSIS")
        print("=" * 60)
        
        analysis = {}
        
        # Initial Claims Analysis
        if 'ICSA' in claims_data:
            initial_claims = claims_data['ICSA']
            current_claims = initial_claims['latest_value']
            analysis['initial_claims'] = {
                'current': current_claims,
                'date': initial_claims['latest_date'],
                'trend': self._calculate_trend(initial_claims['data'][:4])  # 4-week trend
            }
            print(f"\n📋 Initial Claims: {current_claims:,.0f} ({initial_claims['latest_date']})")
            print(f"   Trend: {analysis['initial_claims']['trend']}")
        
        # Continuing Claims Analysis
        if 'CCSA' in claims_data:
            continuing_claims = claims_data['CCSA']
            current_continuing = continuing_claims['latest_value']
            analysis['continuing_claims'] = {
                'current': current_continuing,
                'date': continuing_claims['latest_date'],
                'trend': self._calculate_trend(continuing_claims['data'][:4])  # 4-week trend
            }
            print(f"\n📋 Continuing Claims: {current_continuing:,.0f} ({continuing_claims['latest_date']})")
            print(f"   Trend: {analysis['continuing_claims']['trend']}")
        
        # Calculate 4-week averages
        if 'ICSA' in claims_data and 'CCSA' in claims_data:
            initial_4wk_avg = sum(obs['value'] for obs in claims_data['ICSA']['data'][:4]) / 4
            continuing_4wk_avg = sum(obs['value'] for obs in claims_data['CCSA']['data'][:4]) / 4
            
            analysis['four_week_averages'] = {
                'initial_claims': initial_4wk_avg,
                'continuing_claims': continuing_4wk_avg
            }
            
            print(f"\n📊 4-Week Averages:")
            print(f"   Initial Claims: {initial_4wk_avg:,.0f}")
            print(f"   Continuing Claims: {continuing_4wk_avg:,.0f}")
        
        return analysis
    
    def _calculate_trend(self, data_points):
        """Calculate trend from recent data points"""
        if len(data_points) < 2:
            return "Insufficient data"
        
        current = data_points[0]['value']
        previous = data_points[1]['value']
        change = current - previous
        change_pct = (change / previous) * 100 if previous != 0 else 0
        
        if change_pct > 5:
            return f"Strongly Rising (+{change_pct:.1f}%)"
        elif change_pct > 2:
            return f"Rising (+{change_pct:.1f}%)"
        elif change_pct < -5:
            return f"Strongly Falling ({change_pct:.1f}%)"
        elif change_pct < -2:
            return f"Falling ({change_pct:.1f}%)"
        else:
            return f"Stable ({change_pct:+.1f}%)"
    
    def save_claims_data(self, claims_data, analysis):
        """Save claims data and analysis to file"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'data_source': 'FRED API',
            'claims_data': claims_data,
            'analysis': analysis,
            'summary': {
                'total_series': len(claims_data),
                'latest_update': max([data['latest_date'] for data in claims_data.values()]) if claims_data else None
            }
        }
        
        filename = f"new_claims_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"\n💾 Claims data saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving claims data: {e}")

def main():
    """Main function to fetch and analyze new claims data"""
    fetcher = ClaimsDataFetcher()
    
    # Fetch claims data
    claims_data = fetcher.fetch_claims_data()
    
    if claims_data:
        # Analyze the data
        analysis = fetcher.analyze_claims_impact(claims_data)
        
        # Save data
        fetcher.save_claims_data(claims_data, analysis)
        
        print("\n" + "=" * 60)
        print("✅ NEW CLAIMS DATA FETCH COMPLETE")
        print("=" * 60)
        print(f"📊 Fetched {len(claims_data)} claims series")
        print(f"📅 Latest data from: {max([data['latest_date'] for data in claims_data.values()]) if claims_data else 'N/A'}")
        
    else:
        print("\n❌ No claims data was successfully fetched")

if __name__ == "__main__":
    main()