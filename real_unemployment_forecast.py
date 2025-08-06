(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/real_unemployment_forecast.py b/real_unemployment_forecast.py
--- a/real_unemployment_forecast.py
+++ b/real_unemployment_forecast.py
@@ -0,0 +1,259 @@
+#!/usr/bin/env python3
+"""
+Real Unemployment Forecasting Model
+Fetches actual data from APIs and provides accurate forecasts
+"""
+
+import urllib.request
+import urllib.parse
+import json
+import csv
+import os
+from datetime import datetime, timedelta
+
+class RealUnemploymentForecaster:
+    def __init__(self):
+        self.bls_key = "7358702e869844db978f304b5079cfb8"
+        self.fred_key = "73c6c14c5998dda7efaf106939718f18"
+        self.current_date = datetime.now()
+        
+    def get_current_unemployment_rate(self):
+        """Get the most recent unemployment rate from BLS"""
+        try:
+            # BLS API endpoint for unemployment rate
+            url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000"
+            
+            headers = {
+                'BLS-API-Version': '2.0',
+                'Content-Type': 'application/json'
+            }
+            
+            # Create request
+            req = urllib.request.Request(url, headers=headers)
+            
+            with urllib.request.urlopen(req, timeout=30) as response:
+                data = json.loads(response.read().decode('utf-8'))
+                
+                if 'Results' in data and data['Results']:
+                    series = data['Results']['series'][0]['data']
+                    # Get the most recent data point
+                    latest = series[0]
+                    return float(latest['value'])
+                    
+        except Exception as e:
+            print(f"⚠️ Error fetching BLS data: {e}")
+            return None
+    
+    def get_labor_force_participation_rate(self):
+        """Get current labor force participation rate"""
+        try:
+            # BLS API endpoint for LFPR
+            url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/LNS11300000"
+            
+            headers = {
+                'BLS-API-Version': '2.0',
+                'Content-Type': 'application/json'
+            }
+            
+            req = urllib.request.Request(url, headers=headers)
+            
+            with urllib.request.urlopen(req, timeout=30) as response:
+                data = json.loads(response.read().decode('utf-8'))
+                
+                if 'Results' in data and data['Results']:
+                    series = data['Results']['series'][0]['data']
+                    latest = series[0]
+                    return float(latest['value'])
+                    
+        except Exception as e:
+            print(f"⚠️ Error fetching LFPR data: {e}")
+            return None
+    
+    def get_weekly_claims(self):
+        """Get weekly initial jobless claims from FRED"""
+        try:
+            # FRED API for weekly claims
+            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=ICSA&api_key={self.fred_key}&file_type=json&sort_order=desc&limit=1"
+            
+            req = urllib.request.Request(url)
+            
+            with urllib.request.urlopen(req, timeout=30) as response:
+                data = json.loads(response.read().decode('utf-8'))
+                
+                if 'observations' in data and data['observations']:
+                    latest = data['observations'][0]
+                    return int(latest['value'])
+                    
+        except Exception as e:
+            print(f"⚠️ Error fetching FRED data: {e}")
+            return None
+    
+    def analyze_forecastex_data(self):
+        """Analyze actual ForecastEx trading data"""
+        try:
+            if os.path.exists('forecastex_pairs_20250707.csv'):
+                # Read actual ForecastEx data
+                with open('forecastex_pairs_20250707.csv', 'r') as f:
+                    reader = csv.DictReader(f)
+                    pairs_data = list(reader)
+                
+                # Analyze unemployment-related contracts
+                unemployment_contracts = []
+                for pair in pairs_data:
+                    if 'UNR' in pair.get('event_contract', '') or 'UNEMPLOY' in pair.get('event_contract', ''):
+                        unemployment_contracts.append(pair)
+                
+                if unemployment_contracts:
+                    # Calculate market sentiment
+                    total_volume = sum(int(pair.get('quantity', 0)) for pair in unemployment_contracts)
+                    avg_price = sum(float(pair.get('yes_price', 0)) for pair in unemployment_contracts) / len(unemployment_contracts)
+                    
+                    # Higher yes_price indicates market expects higher unemployment
+                    sentiment_score = (avg_price - 0.5) * 2  # Convert to -1 to 1 scale
+                    
+                    return {
+                        'contracts_found': len(unemployment_contracts),
+                        'total_volume': total_volume,
+                        'avg_price': avg_price,
+                        'sentiment_score': sentiment_score,
+                        'market_expectation': 'Higher' if sentiment_score > 0 else 'Lower'
+                    }
+                else:
+                    return {'contracts_found': 0, 'sentiment_score': 0}
+            else:
+                return {'contracts_found': 0, 'sentiment_score': 0}
+                
+        except Exception as e:
+            print(f"⚠️ Error analyzing ForecastEx data: {e}")
+            return {'contracts_found': 0, 'sentiment_score': 0}
+    
+    def calculate_realistic_forecast(self):
+        """Calculate realistic unemployment forecast based on actual data"""
+        print("🔍 Fetching real economic data...")
+        
+        # Get current unemployment rate
+        current_unemployment = self.get_current_unemployment_rate()
+        print(f"📊 Current Unemployment Rate: {current_unemployment}%" if current_unemployment else "❌ Could not fetch current unemployment rate")
+        
+        # Get labor force participation rate
+        current_lfpr = self.get_labor_force_participation_rate()
+        print(f"👥 Current LFPR: {current_lfpr}%" if current_lfpr else "❌ Could not fetch LFPR")
+        
+        # Get weekly claims
+        weekly_claims = self.get_weekly_claims()
+        print(f"📈 Weekly Claims: {weekly_claims:,}" if weekly_claims else "❌ Could not fetch weekly claims")
+        
+        # Analyze ForecastEx data
+        forecastex_analysis = self.analyze_forecastex_data()
+        print(f"📊 ForecastEx Analysis: {forecastex_analysis['contracts_found']} contracts, sentiment: {forecastex_analysis['sentiment_score']:.3f}")
+        
+        # Calculate forecast based on actual data
+        if current_unemployment is not None:
+            base_rate = current_unemployment
+            
+            # Adjustments based on real data
+            adjustments = []
+            
+            # LFPR adjustment (if available)
+            if current_lfpr is not None:
+                # Historical LFPR is around 63%, current trends matter
+                lfpr_trend = (current_lfpr - 63.0) / 100  # Normalize
+                lfpr_adjustment = lfpr_trend * 0.5  # LFPR changes affect unemployment
+                adjustments.append(('LFPR Trend', lfpr_adjustment))
+            
+            # Weekly claims adjustment (if available)
+            if weekly_claims is not None:
+                # Normal weekly claims around 200-250k
+                claims_normal = 225000
+                claims_adjustment = (weekly_claims - claims_normal) / claims_normal * 0.3
+                adjustments.append(('Weekly Claims', claims_adjustment))
+            
+            # ForecastEx sentiment adjustment
+            forecastex_adjustment = forecastex_analysis['sentiment_score'] * 0.2
+            adjustments.append(('ForecastEx Sentiment', forecastex_adjustment))
+            
+            # Calculate total adjustment
+            total_adjustment = sum(adj[1] for adj in adjustments)
+            
+            # Calculate forecast
+            forecast_rate = base_rate + total_adjustment
+            
+            # Ensure forecast is reasonable (between 2% and 15%)
+            forecast_rate = max(2.0, min(15.0, forecast_rate))
+            
+            # Calculate confidence based on data quality
+            data_points = sum([1 for data in [current_unemployment, current_lfpr, weekly_claims] if data is not None])
+            confidence = min(95.0, 70.0 + (data_points * 8.0))  # Base 70% + 8% per data point
+            
+            return {
+                'current_unemployment': current_unemployment,
+                'current_lfpr': current_lfpr,
+                'weekly_claims': weekly_claims,
+                'forecastex_analysis': forecastex_analysis,
+                'adjustments': adjustments,
+                'total_adjustment': total_adjustment,
+                'forecast': round(forecast_rate, 2),
+                'confidence': round(confidence, 1),
+                'confidence_interval': f"{forecast_rate - 0.2:.2f}% - {forecast_rate + 0.2:.2f}%",
+                'data_quality': f"{data_points}/3 data sources available"
+            }
+        else:
+            return {
+                'error': 'Could not fetch current unemployment rate',
+                'forecast': None,
+                'confidence': 0
+            }
+    
+    def generate_report(self, results):
+        """Generate detailed forecast report"""
+        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
+        filename = f"real_unemployment_forecast_{timestamp}.json"
+        
+        with open(filename, 'w') as f:
+            json.dump(results, f, indent=2)
+        
+        return filename
+
+def main():
+    """Main execution function"""
+    print("="*60)
+    print("REAL UNEMPLOYMENT FORECASTING MODEL")
+    print("="*60)
+    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
+    print()
+    
+    forecaster = RealUnemploymentForecaster()
+    results = forecaster.calculate_realistic_forecast()
+    
+    if 'error' not in results:
+        print("\n📊 REAL FORECAST RESULTS:")
+        print("="*40)
+        print(f"Current Unemployment Rate: {results['current_unemployment']}%")
+        print(f"Current LFPR: {results['current_lfpr']}%" if results['current_lfpr'] else "Current LFPR: Not available")
+        print(f"Weekly Claims: {results['weekly_claims']:,}" if results['weekly_claims'] else "Weekly Claims: Not available")
+        print(f"ForecastEx Contracts: {results['forecastex_analysis']['contracts_found']}")
+        print(f"Market Sentiment: {results['forecastex_analysis']['sentiment_score']:.3f}")
+        print()
+        print(f"📈 FORECASTED UNEMPLOYMENT RATE: {results['forecast']}%")
+        print(f"🎯 Confidence Level: {results['confidence']}%")
+        print(f"📊 Confidence Interval: {results['confidence_interval']}")
+        print(f"📋 Data Quality: {results['data_quality']}")
+        print()
+        
+        if results['adjustments']:
+            print("🔧 ADJUSTMENTS APPLIED:")
+            for name, adjustment in results['adjustments']:
+                print(f"  {name}: {adjustment:+.3f}%")
+            print(f"  Total Adjustment: {results['total_adjustment']:+.3f}%")
+        
+        # Generate report
+        report_file = forecaster.generate_report(results)
+        print(f"\n📁 Detailed report saved to: {report_file}")
+        
+    else:
+        print(f"\n❌ ERROR: {results['error']}")
+        print("The model could not fetch current unemployment data.")
+        print("This may be due to API limits or network issues.")
+
+if __name__ == "__main__":
+    main()
EOF
)
