#!/usr/bin/env python3
"""
Simple JOLTS Data Fetcher (No external dependencies)
Fetches latest JOLTS data from FRED using only built-in Python libraries
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time

class SimpleJOLTSFetcher:
    def __init__(self):
        self.fred_api_key = "73c6c14c5998dda7efaf106939718f18"
        self.fred_endpoint = "https://api.stlouisfed.org/fred/series/observations"
        
        # JOLTS Series IDs from config
        self.jolts_series = {
            "JTSJOL": "Job Openings: Total Nonfarm",
            "JTSHIL": "Hires: Total Nonfarm", 
            "JTSTSL": "Total Separations: Total Nonfarm",
            "JTSQUL": "Quits: Total Nonfarm",
            "JTSLDL": "Layoffs and Discharges: Total Nonfarm",
            "JTSOSL": "Other Separations: Total Nonfarm"
        }
        
    def fetch_series_data(self, series_id, description):
        """Fetch data for a single JOLTS series"""
        try:
            print(f"\n📊 Fetching {description} ({series_id})...")
            
            # Build URL with parameters
            params = {
                'series_id': series_id,
                'api_key': self.fred_api_key,
                'file_type': 'json',
                'limit': 24,  # Last 24 months
                'sort_order': 'desc',
                'observation_start': (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d'),
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
                    
                    return result
                else:
                    print(f"⚠️ No valid data found for {series_id}")
                    return None
            else:
                print(f"⚠️ No observations found for {series_id}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching {series_id}: {e}")
            return None
    
    def fetch_all_jolts_data(self):
        """Fetch all JOLTS data"""
        print("🔄 Fetching latest JOLTS data from FRED...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        jolts_data = {}
        
        for series_id, description in self.jolts_series.items():
            data = self.fetch_series_data(series_id, description)
            if data:
                jolts_data[series_id] = data
            
            # Rate limiting for FRED API
            time.sleep(0.5)
        
        return jolts_data
    
    def analyze_jolts_indicators(self, jolts_data):
        """Analyze JOLTS data for labor market insights"""
        print("\n" + "=" * 60)
        print("🔍 JOLTS LABOR MARKET ANALYSIS")
        print("=" * 60)
        
        analysis = {}
        
        # Job Openings Analysis
        if 'JTSJOL' in jolts_data:
            job_openings = jolts_data['JTSJOL']
            current_openings = job_openings['latest_value']
            analysis['job_openings'] = {
                'current': current_openings,
                'date': job_openings['latest_date'],
                'trend': self._calculate_trend(job_openings['data'][:3])
            }
            print(f"\n📋 Job Openings: {current_openings:,.0f} ({job_openings['latest_date']})")
            print(f"   Trend: {analysis['job_openings']['trend']}")
        
        # Hires Analysis
        if 'JTSHIL' in jolts_data:
            hires = jolts_data['JTSHIL']
            current_hires = hires['latest_value']
            analysis['hires'] = {
                'current': current_hires,
                'date': hires['latest_date'],
                'trend': self._calculate_trend(hires['data'][:3])
            }
            print(f"\n👥 Hires: {current_hires:,.0f} ({hires['latest_date']})")
            print(f"   Trend: {analysis['hires']['trend']}")
        
        # Quits Analysis
        if 'JTSQUL' in jolts_data:
            quits = jolts_data['JTSQUL']
            current_quits = quits['latest_value']
            analysis['quits'] = {
                'current': current_quits,
                'date': quits['latest_date'],
                'trend': self._calculate_trend(quits['data'][:3])
            }
            print(f"\n🚪 Quits: {current_quits:,.0f} ({quits['latest_date']})")
            print(f"   Trend: {analysis['quits']['trend']}")
        
        # Layoffs Analysis
        if 'JTSLDL' in jolts_data:
            layoffs = jolts_data['JTSLDL']
            current_layoffs = layoffs['latest_value']
            analysis['layoffs'] = {
                'current': current_layoffs,
                'date': layoffs['latest_date'],
                'trend': self._calculate_trend(layoffs['data'][:3])
            }
            print(f"\n📉 Layoffs: {current_layoffs:,.0f} ({layoffs['latest_date']})")
            print(f"   Trend: {analysis['layoffs']['trend']}")
        
        # Labor Market Tightness (Job Openings to Hires Ratio)
        if 'JTSJOL' in jolts_data and 'JTSHIL' in jolts_data:
            openings = jolts_data['JTSJOL']['latest_value']
            hires = jolts_data['JTSHIL']['latest_value']
            ratio = openings / hires if hires > 0 else 0
            
            analysis['labor_market_tightness'] = {
                'ratio': ratio,
                'openings': openings,
                'hires': hires,
                'interpretation': self._interpret_tightness(ratio)
            }
            
            print(f"\n⚖️ Labor Market Tightness:")
            print(f"   Job Openings/Hires Ratio: {ratio:.2f}")
            print(f"   Interpretation: {analysis['labor_market_tightness']['interpretation']}")
        
        # Quits Rate Analysis
        if 'JTSQUL' in jolts_data:
            quits = jolts_data['JTSQUL']['latest_value']
            # Using rough estimate based on typical employment levels
            estimated_employment = 160_000_000
            quits_rate = (quits / estimated_employment) * 100
            
            analysis['quits_rate'] = {
                'rate': quits_rate,
                'quits': quits,
                'interpretation': self._interpret_quits_rate(quits_rate)
            }
            
            print(f"\n🔄 Quits Rate: {quits_rate:.2f}%")
            print(f"   Interpretation: {analysis['quits_rate']['interpretation']}")
        
        return analysis
    
    def _calculate_trend(self, data_points):
        """Calculate trend from recent data points"""
        if len(data_points) < 2:
            return "Insufficient data"
        
        current = data_points[0]['value']
        previous = data_points[1]['value']
        change = current - previous
        change_pct = (change / previous) * 100 if previous != 0 else 0
        
        if change_pct > 2:
            return f"Strongly Rising (+{change_pct:.1f}%)"
        elif change_pct > 0.5:
            return f"Rising (+{change_pct:.1f}%)"
        elif change_pct < -2:
            return f"Strongly Falling ({change_pct:.1f}%)"
        elif change_pct < -0.5:
            return f"Falling ({change_pct:.1f}%)"
        else:
            return f"Stable ({change_pct:+.1f}%)"
    
    def _interpret_tightness(self, ratio):
        """Interpret labor market tightness ratio"""
        if ratio > 1.2:
            return "Very Tight - More openings than hires"
        elif ratio > 1.0:
            return "Tight - Slight excess of openings"
        elif ratio > 0.8:
            return "Balanced - Healthy labor market"
        else:
            return "Loose - More hires than openings"
    
    def _interpret_quits_rate(self, rate):
        """Interpret quits rate"""
        if rate > 3.0:
            return "High - Strong worker confidence"
        elif rate > 2.5:
            return "Moderate - Normal worker mobility"
        else:
            return "Low - Cautious worker behavior"
    
    def save_analysis(self, jolts_data, analysis):
        """Save JOLTS analysis to file"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'data_source': 'FRED API',
            'jolts_data': jolts_data,
            'analysis': analysis,
            'summary': {
                'total_series': len(jolts_data),
                'latest_update': max([data['latest_date'] for data in jolts_data.values()]) if jolts_data else None
            }
        }
        
        filename = f"jolts_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"\n💾 Analysis saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")

def main():
    """Main function to fetch and analyze JOLTS data"""
    fetcher = SimpleJOLTSFetcher()
    
    # Fetch JOLTS data
    jolts_data = fetcher.fetch_all_jolts_data()
    
    if jolts_data:
        # Analyze the data
        analysis = fetcher.analyze_jolts_indicators(jolts_data)
        
        # Save analysis
        fetcher.save_analysis(jolts_data, analysis)
        
        print("\n" + "=" * 60)
        print("✅ JOLTS DATA FETCH COMPLETE")
        print("=" * 60)
        print(f"📊 Fetched {len(jolts_data)} JOLTS series")
        print(f"📅 Latest data from: {max([data['latest_date'] for data in jolts_data.values()]) if jolts_data else 'N/A'}")
        
        # Print summary for forecast integration
        print("\n" + "=" * 60)
        print("📈 FORECAST INTEGRATION SUMMARY")
        print("=" * 60)
        
        if 'labor_market_tightness' in analysis:
            tightness = analysis['labor_market_tightness']
            print(f"🔧 Labor Market Tightness: {tightness['ratio']:.2f} ({tightness['interpretation']})")
            
            # Determine confidence boost
            if tightness['ratio'] > 1.2:
                confidence_boost = "High (+3-4%)"
            elif tightness['ratio'] > 1.0:
                confidence_boost = "Moderate (+2-3%)"
            else:
                confidence_boost = "Low (+1-2%)"
            
            print(f"🚀 Expected Confidence Boost: {confidence_boost}")
        
        if 'quits_rate' in analysis:
            quits_rate = analysis['quits_rate']
            print(f"🔄 Quits Rate: {quits_rate['rate']:.2f}% ({quits_rate['interpretation']})")
        
    else:
        print("\n❌ No JOLTS data was successfully fetched")

if __name__ == "__main__":
    main()