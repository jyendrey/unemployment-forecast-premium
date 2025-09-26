#!/usr/bin/env python3
"""
Historical Data Analyzer for Labor Market Indicators
Fetches historical data and calculates realistic projections
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import statistics

class HistoricalDataAnalyzer:
    def __init__(self):
        self.fred_api_key = "a05f2e75daeca5fb9a47f2aa4ab0fba0"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # Series IDs for the indicators
        self.series_ids = {
            "ICSA": "Initial Claims",
            "CCSA": "Continuing Claims", 
            "PAYEMS": "Nonfarm Payrolls",
            "CES0500000003": "Average Hourly Earnings"
        }

    def fetch_historical_data(self, series_id, start_date="2020-01-01", end_date=None):
        """Fetch historical data from FRED API"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            "series_id": series_id,
            "api_key": self.fred_api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date,
            "sort_order": "desc",
            "limit": 100
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'observations' in data:
                # Filter out null values and convert to float
                valid_observations = []
                for obs in data['observations']:
                    if obs['value'] != '.' and obs['value'] is not None and obs['value'] != '':
                        try:
                            valid_observations.append({
                                'date': obs['date'],
                                'value': float(obs['value'])
                            })
                        except (ValueError, TypeError):
                            continue
                return valid_observations
            else:
                print(f"Error in response for {series_id}: {data}")
                return []
                
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return []

    def calculate_trends(self, data, series_id):
        """Calculate historical trends and projections"""
        if len(data) < 12:  # Need at least 12 months of data
            return None
            
        # Get recent data (last 12 months)
        recent_data = data[:12]
        values = [obs['value'] for obs in recent_data]
        
        # Calculate various trends
        trends = {}
        
        # Current value (most recent)
        trends['current'] = values[0]
        trends['current_date'] = recent_data[0]['date']
        
        # 3-month average
        trends['3_month_avg'] = statistics.mean(values[:3])
        
        # 6-month average
        trends['6_month_avg'] = statistics.mean(values[:6])
        
        # 12-month average
        trends['12_month_avg'] = statistics.mean(values)
        
        # Month-over-month change (average of last 3 months)
        if len(values) >= 4:
            mom_changes = []
            for i in range(3):
                if i + 1 < len(values):
                    change = values[i] - values[i + 1]
                    mom_changes.append(change)
            trends['avg_mom_change'] = statistics.mean(mom_changes)
        else:
            trends['avg_mom_change'] = 0
        
        # Year-over-year change
        if len(values) >= 12:
            trends['yoy_change'] = values[0] - values[11]
        else:
            trends['yoy_change'] = 0
        
        # Calculate projection for next month
        if series_id == "PAYEMS":
            # Payrolls: use average monthly change
            trends['projection'] = trends['current'] + trends['avg_mom_change']
        elif series_id == "CES0500000003":
            # Earnings: use average monthly change
            trends['projection'] = trends['current'] + trends['avg_mom_change']
        else:
            # Claims: use average monthly change
            trends['projection'] = trends['current'] + trends['avg_mom_change']
        
        # Calculate confidence based on data consistency
        if len(values) >= 6:
            recent_std = statistics.stdev(values[:6])
            recent_mean = statistics.mean(values[:6])
            if recent_mean != 0:
                trends['volatility'] = recent_std / abs(recent_mean)
            else:
                trends['volatility'] = 0
        else:
            trends['volatility'] = 0
        
        return trends

    def analyze_all_indicators(self):
        """Analyze all labor market indicators"""
        print("HISTORICAL DATA ANALYSIS")
        print("=" * 80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_trends = {}
        
        for series_id, description in self.series_ids.items():
            print(f"Analyzing {description} ({series_id})")
            print("-" * 50)
            
            # Fetch historical data
            data = self.fetch_historical_data(series_id)
            
            if data:
                print(f"✓ Fetched {len(data)} observations")
                
                # Calculate trends
                trends = self.calculate_trends(data, series_id)
                
                if trends:
                    all_trends[series_id] = trends
                    
                    print(f"Current Value: {trends['current']:,.0f} (as of {trends['current_date']})")
                    print(f"3-Month Average: {trends['3_month_avg']:,.0f}")
                    print(f"6-Month Average: {trends['6_month_avg']:,.0f}")
                    print(f"12-Month Average: {trends['12_month_avg']:,.0f}")
                    print(f"Avg Monthly Change: {trends['avg_mom_change']:+,.0f}")
                    print(f"Year-over-Year Change: {trends['yoy_change']:+,.0f}")
                    print(f"Projected Next Month: {trends['projection']:,.0f}")
                    print(f"Volatility: {trends['volatility']:.2f}")
                else:
                    print("✗ Insufficient data for trend analysis")
            else:
                print("✗ Failed to fetch data")
            
            print()
        
        return all_trends

    def generate_projection_summary(self, all_trends):
        """Generate a summary of projections"""
        print("PROJECTION SUMMARY")
        print("=" * 80)
        
        if not all_trends:
            print("No data available for projections")
            return
        
        print("Current → Projected (Next Month)")
        print("-" * 40)
        
        for series_id, trends in all_trends.items():
            description = self.series_ids[series_id]
            current = trends['current']
            projected = trends['projection']
            change = projected - current
            
            print(f"{description}:")
            print(f"  {current:,.0f} → {projected:,.0f} ({change:+,.0f})")
            print(f"  Confidence: {'High' if trends['volatility'] < 0.1 else 'Medium' if trends['volatility'] < 0.2 else 'Low'}")
            print()
        
        # Save trends to file
        with open('historical_trends.json', 'w') as f:
            json.dump(all_trends, f, indent=2)
        print("Historical trends saved to historical_trends.json")

def main():
    analyzer = HistoricalDataAnalyzer()
    all_trends = analyzer.analyze_all_indicators()
    analyzer.generate_projection_summary(all_trends)

if __name__ == "__main__":
    main()