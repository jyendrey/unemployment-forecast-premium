(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/extended_fred_data_fetcher.py b/extended_fred_data_fetcher.py
--- a/extended_fred_data_fetcher.py
+++ b/extended_fred_data_fetcher.py
@@ -0,0 +1,389 @@
+#!/usr/bin/env python3
+"""
+Extended FRED Data Fetcher
+Pulls 24 months of initial and continuing claims data from FRED API
+Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
+Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
+"""
+
+import urllib.request
+import json
+from datetime import datetime, timedelta
+import statistics
+
+class ExtendedFREDDataFetcher:
+    def __init__(self):
+        self.api_key = "73c6c14c5998dda7efaf106939718f18"
+        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
+        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
+        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
+        
+    def fetch_extended_series_data(self, series_id, months=24):
+        """Fetch extended data for a specific FRED series (24 months)"""
+        
+        # Calculate the number of observations needed (approximately 24 months)
+        # Weekly data: ~104 observations, Monthly data: ~24 observations
+        if series_id in ["ICSA", "CCSA"]:  # Weekly data
+            limit = months * 4.33  # Approximately 4.33 weeks per month
+        else:  # Monthly data
+            limit = months
+        
+        limit = int(limit)
+        
+        url = f"{self.base_url}?series_id={series_id}&api_key={self.api_key}&file_type=json&sort_order=desc&limit={limit}"
+        
+        try:
+            print(f"📊 Fetching {series_id} data from FRED (last {months} months)...")
+            
+            req = urllib.request.Request(url)
+            with urllib.request.urlopen(req, timeout=60) as response:
+                data = json.loads(response.read().decode('utf-8'))
+                
+                if 'observations' in data and data['observations']:
+                    print(f"✅ Successfully fetched {len(data['observations'])} observations for {series_id}")
+                    return data['observations']
+                else:
+                    print(f"⚠️ No data found for series {series_id}")
+                    return []
+                    
+        except Exception as e:
+            print(f"❌ Error fetching {series_id}: {e}")
+            return []
+    
+    def fetch_initial_claims_24months(self):
+        """Fetch 24 months of initial jobless claims data (ICSA)"""
+        return self.fetch_extended_series_data("ICSA", 24)
+    
+    def fetch_continuing_claims_24months(self):
+        """Fetch 24 months of continuing jobless claims data (CCSA)"""
+        return self.fetch_extended_series_data("CCSA", 24)
+    
+    def fetch_unemployment_rate_24months(self):
+        """Fetch 24 months of unemployment rate data (UNRATE)"""
+        return self.fetch_extended_series_data("UNRATE", 24)
+    
+    def fetch_labor_force_participation_24months(self):
+        """Fetch 24 months of labor force participation rate (CIVPART)"""
+        return self.fetch_extended_series_data("CIVPART", 24)
+    
+    def analyze_extended_claims_data(self, initial_claims, continuing_claims):
+        """Analyze extended claims data for comprehensive insights"""
+        
+        if not initial_claims or not continuing_claims:
+            print("⚠️ Insufficient data for extended analysis")
+            return None
+        
+        print(f"\n🔍 Analyzing extended claims data ({len(initial_claims)} observations)...")
+        
+        # Get latest values
+        latest_initial = initial_claims[0]
+        latest_continuing = continuing_claims[0]
+        
+        # Calculate comprehensive statistics
+        initial_values = [float(obs['value']) for obs in initial_claims if obs['value'] != '.']
+        continuing_values = [float(obs['value']) for obs in continuing_claims if obs['value'] != '.']
+        
+        # Get date range
+        initial_dates = [obs['date'] for obs in initial_claims if obs['date']]
+        continuing_dates = [obs['date'] for obs in continuing_claims if obs['date']]
+        
+        # Calculate trends over different time periods
+        trends = self.calculate_extended_trends(initial_claims, continuing_claims)
+        
+        # Calculate volatility and stability metrics
+        volatility = self.calculate_volatility_metrics(initial_values, continuing_values)
+        
+        # Assess market health over extended period
+        market_health = self.assess_extended_market_health(initial_values, continuing_values)
+        
+        analysis = {
+            'data_coverage': {
+                'initial_claims_observations': len(initial_claims),
+                'continuing_claims_observations': len(continuing_claims),
+                'date_range': {
+                    'initial_start': min(initial_dates) if initial_dates else 'Unknown',
+                    'initial_end': max(initial_dates) if initial_dates else 'Unknown',
+                    'continuing_start': min(continuing_dates) if continuing_dates else 'Unknown',
+                    'continuing_end': max(continuing_dates) if continuing_dates else 'Unknown'
+                }
+            },
+            'latest_data': {
+                'initial_claims': {
+                    'value': int(float(latest_initial['value'])) if latest_initial['value'] != '.' else 0,
+                    'date': latest_initial['date'],
+                    'trend': trends['initial_trend'],
+                    'change': trends['initial_change']
+                },
+                'continuing_claims': {
+                    'value': int(float(latest_continuing['value'])) if latest_continuing['value'] != '.' else 0,
+                    'date': latest_continuing['date'],
+                    'trend': trends['continuing_trend'],
+                    'change': trends['continuing_change']
+                }
+            },
+            'extended_trends': trends,
+            'volatility_analysis': volatility,
+            'market_health_assessment': market_health,
+            'foundation_id': self.foundation_id,
+            'math_framework_id': self.math_framework_id,
+            'fetched_at': datetime.now().isoformat()
+        }
+        
+        return analysis
+    
+    def calculate_extended_trends(self, initial_claims, continuing_claims):
+        """Calculate trends over different time periods"""
+        
+        # Short-term trend (last 4 weeks)
+        short_term_initial = initial_claims[:4] if len(initial_claims) >= 4 else initial_claims
+        short_term_continuing = continuing_claims[:4] if len(continuing_claims) >= 4 else continuing_claims
+        
+        # Medium-term trend (last 12 weeks)
+        medium_term_initial = initial_claims[:12] if len(initial_claims) >= 12 else initial_claims
+        medium_term_continuing = continuing_claims[:12] if len(continuing_claims) >= 12 else continuing_claims
+        
+        # Long-term trend (last 24 weeks)
+        long_term_initial = initial_claims[:24] if len(initial_claims) >= 24 else initial_claims
+        long_term_continuing = continuing_claims[:24] if len(continuing_claims) >= 24 else continuing_claims
+        
+        def calculate_trend_change(observations):
+            if len(observations) < 2:
+                return 0, "Stable"
+            
+            latest = float(observations[0]['value']) if observations[0]['value'] != '.' else 0
+            previous = float(observations[-1]['value']) if observations[-1]['value'] != '.' else 0
+            
+            if latest == 0 or previous == 0:
+                return 0, "Stable"
+            
+            change = latest - previous
+            if change > 0:
+                trend = "Rising"
+            elif change < 0:
+                trend = "Declining"
+            else:
+                trend = "Stable"
+            
+            return change, trend
+        
+        # Calculate trends for each period
+        short_initial_change, short_initial_trend = calculate_trend_change(short_term_initial)
+        short_continuing_change, short_continuing_trend = calculate_trend_change(short_term_continuing)
+        
+        medium_initial_change, medium_initial_trend = calculate_trend_change(medium_term_initial)
+        medium_continuing_change, medium_continuing_trend = calculate_trend_change(medium_term_continuing)
+        
+        long_initial_change, long_initial_trend = calculate_trend_change(long_term_initial)
+        long_continuing_change, long_continuing_trend = calculate_trend_change(long_term_continuing)
+        
+        return {
+            'short_term': {
+                'initial_claims': {'change': short_initial_change, 'trend': short_initial_trend},
+                'continuing_claims': {'change': short_continuing_change, 'trend': short_continuing_trend}
+            },
+            'medium_term': {
+                'initial_claims': {'change': medium_initial_change, 'trend': medium_initial_trend},
+                'continuing_claims': {'change': medium_continuing_change, 'trend': medium_continuing_trend}
+            },
+            'long_term': {
+                'initial_claims': {'change': long_initial_change, 'trend': long_initial_trend},
+                'continuing_claims': {'change': long_continuing_change, 'trend': long_continuing_trend}
+            },
+            'initial_trend': short_initial_trend,
+            'continuing_trend': short_continuing_trend,
+            'initial_change': short_initial_change,
+            'continuing_change': short_continuing_change
+        }
+    
+    def calculate_volatility_metrics(self, initial_values, continuing_values):
+        """Calculate volatility and stability metrics"""
+        
+        if not initial_values or not continuing_values:
+            return {'error': 'Insufficient data for volatility calculation'}
+        
+        # Calculate standard deviations
+        initial_std = statistics.stdev(initial_values) if len(initial_values) > 1 else 0
+        continuing_std = statistics.stdev(continuing_values) if len(continuing_values) > 1 else 0
+        
+        # Calculate coefficients of variation (CV = std/mean)
+        initial_mean = statistics.mean(initial_values) if initial_values else 0
+        continuing_mean = statistics.mean(continuing_values) if continuing_values else 0
+        
+        initial_cv = (initial_std / initial_mean) if initial_mean > 0 else 0
+        continuing_cv = (continuing_std / continuing_mean) if continuing_mean > 0 else 0
+        
+        # Assess stability
+        def assess_stability(cv):
+            if cv < 0.1:
+                return "Very Stable"
+            elif cv < 0.2:
+                return "Stable"
+            elif cv < 0.3:
+                return "Moderately Stable"
+            else:
+                return "Volatile"
+        
+        return {
+            'initial_claims': {
+                'standard_deviation': round(initial_std, 2),
+                'coefficient_of_variation': round(initial_cv, 4),
+                'stability': assess_stability(initial_cv)
+            },
+            'continuing_claims': {
+                'standard_deviation': round(continuing_std, 2),
+                'coefficient_of_variation': round(continuing_cv, 4),
+                'stability': assess_stability(continuing_cv)
+            },
+            'overall_market_stability': assess_stability((initial_cv + continuing_cv) / 2)
+        }
+    
+    def assess_extended_market_health(self, initial_values, continuing_values):
+        """Assess market health over extended period"""
+        
+        if not initial_values or not continuing_values:
+            return {'error': 'Insufficient data for health assessment'}
+        
+        # Historical benchmarks
+        initial_normal_range = (200000, 250000)
+        continuing_normal_range = (1500000, 2000000)
+        
+        # Calculate percentage of observations in healthy ranges
+        initial_healthy_count = sum(1 for v in initial_values if initial_normal_range[0] <= v <= initial_normal_range[1])
+        continuing_healthy_count = sum(1 for v in continuing_values if continuing_normal_range[0] <= v <= continuing_normal_range[1])
+        
+        initial_health_percentage = (initial_healthy_count / len(initial_values)) * 100
+        continuing_health_percentage = (continuing_healthy_count / len(continuing_values)) * 100
+        
+        # Assess overall health
+        if initial_health_percentage >= 80 and continuing_health_percentage >= 80:
+            overall_health = "Very Strong"
+        elif initial_health_percentage >= 60 and continuing_health_percentage >= 60:
+            overall_health = "Strong"
+        elif initial_health_percentage >= 40 and continuing_health_percentage >= 40:
+            overall_health = "Moderate"
+        else:
+            overall_health = "Weak"
+        
+        return {
+            'initial_claims_health': {
+                'healthy_percentage': round(initial_health_percentage, 1),
+                'healthy_observations': initial_healthy_count,
+                'total_observations': len(initial_values),
+                'assessment': 'Excellent' if initial_health_percentage >= 80 else 'Good' if initial_health_percentage >= 60 else 'Concerning'
+            },
+            'continuing_claims_health': {
+                'healthy_percentage': round(continuing_health_percentage, 1),
+                'healthy_observations': continuing_healthy_count,
+                'total_observations': len(continuing_values),
+                'assessment': 'Excellent' if continuing_health_percentage >= 80 else 'Good' if continuing_health_percentage >= 60 else 'Concerning'
+            },
+            'overall_market_health': overall_health,
+            'initial_claims_benchmark': f"{initial_normal_range[0]:,} - {initial_normal_range[1]:,}",
+            'continuing_claims_benchmark': f"{continuing_normal_range[0]:,} - {continuing_normal_range[1]:,}"
+        }
+    
+    def print_extended_summary(self, analysis):
+        """Print comprehensive extended analysis summary"""
+        
+        if not analysis:
+            print("❌ No extended analysis data available")
+            return
+        
+        print("\n" + "="*60)
+        print("EXTENDED FRED CLAIMS DATA ANALYSIS SUMMARY")
+        print("="*60)
+        print(f"Foundation ID: {self.foundation_id}")
+        print(f"Math Framework ID: {self.math_framework_id}")
+        print(f"Data Fetched: {analysis['fetched_at']}")
+        print("="*60)
+        
+        coverage = analysis['data_coverage']
+        print(f"\n📊 DATA COVERAGE:")
+        print(f"  Initial Claims Observations: {coverage['initial_claims_observations']}")
+        print(f"  Continuing Claims Observations: {coverage['continuing_claims_observations']}")
+        print(f"  Initial Claims Date Range: {coverage['date_range']['initial_start']} to {coverage['date_range']['initial_end']}")
+        print(f"  Continuing Claims Date Range: {coverage['date_range']['continuing_start']} to {coverage['date_range']['continuing_end']}")
+        
+        latest = analysis['latest_data']
+        print(f"\n📊 LATEST DATA:")
+        print(f"  Initial Claims: {latest['initial_claims']['value']:,} ({latest['initial_claims']['date']})")
+        print(f"  Initial Claims Trend: {latest['initial_claims']['trend']} ({latest['initial_claims']['change']:+,})")
+        print(f"  Continuing Claims: {latest['continuing_claims']['value']:,} ({latest['continuing_claims']['date']})")
+        print(f"  Continuing Claims Trend: {latest['continuing_claims']['trend']} ({latest['continuing_claims']['change']:+,})")
+        
+        trends = analysis['extended_trends']
+        print(f"\n📈 EXTENDED TREND ANALYSIS:")
+        print(f"  Short-term (4 weeks): Initial {trends['short_term']['initial_claims']['trend']}, Continuing {trends['short_term']['continuing_claims']['trend']}")
+        print(f"  Medium-term (12 weeks): Initial {trends['medium_term']['initial_claims']['trend']}, Continuing {trends['medium_term']['continuing_claims']['trend']}")
+        print(f"  Long-term (24 weeks): Initial {trends['long_term']['initial_claims']['trend']}, Continuing {trends['long_term']['continuing_claims']['trend']}")
+        
+        volatility = analysis['volatility_analysis']
+        if 'error' not in volatility:
+            print(f"\n📊 VOLATILITY ANALYSIS:")
+            print(f"  Initial Claims Stability: {volatility['initial_claims']['stability']} (CV: {volatility['initial_claims']['coefficient_of_variation']})")
+            print(f"  Continuing Claims Stability: {volatility['continuing_claims']['stability']} (CV: {volatility['continuing_claims']['coefficient_of_variation']})")
+            print(f"  Overall Market Stability: {volatility['overall_market_stability']}")
+        
+        health = analysis['market_health_assessment']
+        if 'error' not in health:
+            print(f"\n🏥 EXTENDED MARKET HEALTH ASSESSMENT:")
+            print(f"  Initial Claims Health: {health['initial_claims_health']['assessment']} ({health['initial_claims_health']['healthy_percentage']}% healthy)")
+            print(f"  Continuing Claims Health: {health['continuing_claims_health']['assessment']} ({health['continuing_claims_health']['healthy_percentage']}% healthy)")
+            print(f"  Overall Market Health: {health['overall_market_health']}")
+            print(f"  Initial Claims Benchmark: {health['initial_claims_benchmark']}")
+            print(f"  Continuing Claims Benchmark: {health['continuing_claims_benchmark']}")
+        
+        print("\n" + "="*60)
+    
+    def save_extended_analysis(self, analysis, filename="extended_fred_claims_analysis.json"):
+        """Save the extended analysis results to JSON file"""
+        with open(filename, 'w') as f:
+            json.dump(analysis, f, indent=2)
+        
+        print(f"✅ Extended claims analysis saved to: {filename}")
+        return filename
+    
+    def fetch_all_extended_data(self):
+        """Fetch all relevant FRED data series for 24 months"""
+        
+        print("="*60)
+        print("EXTENDED FRED DATA FETCHER (24 MONTHS)")
+        print("="*60)
+        print(f"Foundation ID: {self.foundation_id}")
+        print(f"Math Framework ID: {self.math_framework_id}")
+        print("="*60)
+        
+        # Fetch extended data for all series
+        initial_claims = self.fetch_initial_claims_24months()
+        continuing_claims = self.fetch_continuing_claims_24months()
+        unemployment_rate = self.fetch_unemployment_rate_24months()
+        labor_force_participation = self.fetch_labor_force_participation_24months()
+        
+        # Analyze extended claims data
+        extended_analysis = self.analyze_extended_claims_data(initial_claims, continuing_claims)
+        
+        if extended_analysis:
+            # Print extended summary
+            self.print_extended_summary(extended_analysis)
+            
+            # Save extended analysis
+            analysis_file = self.save_extended_analysis(extended_analysis)
+            
+            print(f"\n🎯 Extended FRED data fetching complete!")
+            print(f"📁 Extended analysis saved to: {analysis_file}")
+            print(f"🔧 Foundation System: {self.foundation_id}")
+            print(f"🔧 Math Framework: {self.math_framework_id}")
+            print("="*60)
+            
+            return extended_analysis
+        else:
+            print("❌ Failed to analyze extended claims data")
+            return None
+
+def main():
+    """Main execution function"""
+    fetcher = ExtendedFREDDataFetcher()
+    fetcher.fetch_all_extended_data()
+
+if __name__ == "__main__":
+    main()
EOF
)
