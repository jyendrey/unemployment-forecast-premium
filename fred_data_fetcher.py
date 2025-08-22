#!/usr/bin/env python3
"""
FRED Data Fetcher
Pulls latest initial and continuing claims data from FRED API
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import urllib.request
import json
from datetime import datetime, timedelta

class FREDDataFetcher:
    def __init__(self):
        self.api_key = "73c6c14c5998dda7efaf106939718f18"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        
    def fetch_series_data(self, series_id, limit=10):
        """Fetch data for a specific FRED series"""
        
        url = f"{self.base_url}?series_id={series_id}&api_key={self.api_key}&file_type=json&sort_order=desc&limit={limit}"
        
        try:
            print(f"📊 Fetching {series_id} data from FRED...")
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if 'observations' in data and data['observations']:
                    print(f"✅ Successfully fetched {len(data['observations'])} observations for {series_id}")
                    return data['observations']
                else:
                    print(f"⚠️ No data found for series {series_id}")
                    return []
                    
        except Exception as e:
            print(f"❌ Error fetching {series_id}: {e}")
            return []
    
    def fetch_initial_claims(self):
        """Fetch initial jobless claims data (ICSA)"""
        return self.fetch_series_data("ICSA", limit=20)
    
    def fetch_continuing_claims(self):
        """Fetch continuing jobless claims data (CCSA)"""
        return self.fetch_series_data("CCSA", limit=20)
    
    def fetch_unemployment_rate(self):
        """Fetch unemployment rate data (UNRATE)"""
        return self.fetch_series_data("UNRATE", limit=20)
    
    def fetch_labor_force_participation(self):
        """Fetch labor force participation rate (CIVPART)"""
        return self.fetch_series_data("CIVPART", limit=20)
    
    def analyze_claims_data(self, initial_claims, continuing_claims):
        """Analyze the claims data for trends and insights"""
        
        if not initial_claims or not continuing_claims:
            print("⚠️ Insufficient data for analysis")
            return None
        
        print(f"\n🔍 Analyzing claims data...")
        
        # Get latest values
        latest_initial = initial_claims[0]
        latest_continuing = continuing_claims[0]
        
        # Get previous values for trend analysis
        if len(initial_claims) > 1:
            prev_initial = initial_claims[1]
        else:
            prev_initial = latest_initial
            
        if len(continuing_claims) > 1:
            prev_continuing = continuing_claims[1]
        else:
            prev_continuing = latest_continuing
        
        # Calculate trends
        initial_change = float(latest_initial['value']) - float(prev_initial['value'])
        continuing_change = float(latest_continuing['value']) - float(prev_continuing['value'])
        
        # Determine trend direction
        initial_trend = "Declining" if initial_change < 0 else "Rising" if initial_change > 0 else "Stable"
        continuing_trend = "Declining" if continuing_change < 0 else "Rising" if continuing_change > 0 else "Stable"
        
        analysis = {
            'latest_data': {
                'initial_claims': {
                    'value': int(float(latest_initial['value'])),
                    'date': latest_initial['date'],
                    'trend': initial_trend,
                    'change': int(initial_change)
                },
                'continuing_claims': {
                    'value': int(float(latest_continuing['value'])),
                    'date': latest_continuing['date'],
                    'trend': continuing_trend,
                    'change': int(continuing_change)
                }
            },
            'trend_analysis': {
                'initial_claims_trend': initial_trend,
                'continuing_claims_trend': continuing_trend,
                'market_health': self.assess_market_health(float(latest_initial['value']), float(latest_continuing['value']))
            },
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id,
            'fetched_at': datetime.now().isoformat()
        }
        
        return analysis
    
    def assess_market_health(self, initial_claims, continuing_claims):
        """Assess labor market health based on claims data"""
        
        # Historical benchmarks
        initial_normal_range = (200000, 250000)
        continuing_normal_range = (1500000, 2000000)
        
        # Assess initial claims
        if initial_claims < initial_normal_range[0]:
            initial_health = "Excellent"
        elif initial_claims < initial_normal_range[1]:
            initial_health = "Good"
        else:
            initial_health = "Concerning"
        
        # Assess continuing claims
        if continuing_claims < continuing_normal_range[0]:
            continuing_health = "Excellent"
        elif continuing_claims < continuing_normal_range[1]:
            continuing_health = "Good"
        else:
            continuing_health = "Concerning"
        
        # Overall assessment
        if initial_health == "Excellent" and continuing_health == "Excellent":
            overall_health = "Very Strong"
        elif initial_health in ["Excellent", "Good"] and continuing_health in ["Excellent", "Good"]:
            overall_health = "Strong"
        elif initial_health == "Concerning" or continuing_health == "Concerning":
            overall_health = "Moderate"
        else:
            overall_health = "Weak"
        
        return {
            'initial_claims_health': initial_health,
            'continuing_claims_health': continuing_health,
            'overall_market_health': overall_health,
            'initial_claims_benchmark': f"{initial_normal_range[0]:,} - {initial_normal_range[1]:,}",
            'continuing_claims_benchmark': f"{continuing_normal_range[0]:,} - {continuing_normal_range[1]:,}"
        }
    
    def print_claims_summary(self, analysis):
        """Print a comprehensive summary of the claims data"""
        
        if not analysis:
            print("❌ No analysis data available")
            return
        
        print("\n" + "="*60)
        print("FRED CLAIMS DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print(f"Data Fetched: {analysis['fetched_at']}")
        print("="*60)
        
        latest = analysis['latest_data']
        
        print(f"\n📊 INITIAL CLAIMS:")
        print(f"  Latest Value: {latest['initial_claims']['value']:,}")
        print(f"  Date: {latest['initial_claims']['date']}")
        print(f"  Trend: {latest['initial_claims']['trend']}")
        print(f"  Change: {latest['initial_claims']['change']:+,}")
        
        print(f"\n📊 CONTINUING CLAIMS:")
        print(f"  Latest Value: {latest['continuing_claims']['value']:,}")
        print(f"  Date: {latest['continuing_claims']['date']}")
        print(f"  Trend: {latest['continuing_claims']['trend']}")
        print(f"  Change: {latest['continuing_claims']['change']:+,}")
        
        trend = analysis['trend_analysis']
        print(f"\n📈 TREND ANALYSIS:")
        print(f"  Initial Claims Trend: {trend['initial_claims_trend']}")
        print(f"  Continuing Claims Trend: {trend['continuing_claims_trend']}")
        print(f"  Overall Market Health: {trend['market_health']['overall_market_health']}")
        
        health = trend['market_health']
        print(f"\n🏥 MARKET HEALTH ASSESSMENT:")
        print(f"  Initial Claims Health: {health['initial_claims_health']}")
        print(f"  Continuing Claims Health: {health['continuing_claims_health']}")
        print(f"  Initial Claims Benchmark: {health['initial_claims_benchmark']}")
        print(f"  Continuing Claims Benchmark: {health['continuing_claims_benchmark']}")
        
        print("\n" + "="*60)
    
    def save_analysis(self, analysis, filename="fred_claims_analysis.json"):
        """Save the analysis results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Claims analysis saved to: {filename}")
        return filename
    
    def fetch_all_data(self):
        """Fetch all relevant FRED data series"""
        
        print("="*60)
        print("FRED DATA FETCHER")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print("="*60)
        
        # Fetch initial claims
        initial_claims = self.fetch_initial_claims()
        
        # Fetch continuing claims
        continuing_claims = self.fetch_continuing_claims()
        
        # Fetch unemployment rate
        unemployment_rate = self.fetch_unemployment_rate()
        
        # Fetch labor force participation
        labor_force_participation = self.fetch_labor_force_participation()
        
        # Analyze claims data
        claims_analysis = self.analyze_claims_data(initial_claims, continuing_claims)
        
        if claims_analysis:
            # Print summary
            self.print_claims_summary(claims_analysis)
            
            # Save analysis
            analysis_file = self.save_analysis(claims_analysis)
            
            print(f"\n🎯 FRED data fetching complete!")
            print(f"📁 Analysis saved to: {analysis_file}")
            print(f"🔧 Foundation System: {self.foundation_id}")
            print(f"🔧 Math Framework: {self.math_framework_id}")
            print("="*60)
            
            return claims_analysis
        else:
            print("❌ Failed to analyze claims data")
            return None

def main():
    """Main execution function"""
    fetcher = FREDDataFetcher()
    fetcher.fetch_all_data()

if __name__ == "__main__":
    main()