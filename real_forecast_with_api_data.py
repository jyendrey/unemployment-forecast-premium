#!/usr/bin/env python3
"""
Real Forecast with API Data
Create forecast using actual data from FRED API
"""

import json
from datetime import datetime

def real_forecast_with_api_data():
    """Create forecast using real API data"""
    
    print("REAL FORECAST WITH API DATA")
    print("="*50)
    
    # Load the API data
    try:
        with open('current_api_data.json', 'r') as f:
            api_data = json.load(f)
    except FileNotFoundError:
        print("Error: current_api_data.json not found. Run fetch_api_data_fixed.py first.")
        return None
    
    print(f"Data fetched: {api_data['timestamp']}")
    print(f"Date range: {api_data['date_range']['start']} to {api_data['date_range']['end']}")
    print()
    
    # Extract current values
    fred_data = api_data['fred_data']
    
    # Current unemployment rate (base)
    current_unrate = float(fred_data['UNRATE']['data'][0]['value'])
    print(f"CURRENT UNEMPLOYMENT RATE: {current_unrate}% (August 2025)")
    print()
    
    # Labor Force Participation Rate
    current_lfpr = float(fred_data['CIVPART']['data'][0]['value'])
    prev_lfpr = float(fred_data['CIVPART']['data'][1]['value'])
    lfpr_trend = current_lfpr - prev_lfpr
    print(f"LABOR FORCE PARTICIPATION RATE:")
    print(f"  Current: {current_lfpr}%")
    print(f"  Previous: {prev_lfpr}%")
    print(f"  Trend: {lfpr_trend:+.2f} percentage points")
    
    # Initial Claims
    current_claims = int(fred_data['ICSA']['data'][0]['value'])
    recent_claims = [int(d['value']) for d in fred_data['ICSA']['data'][:4]]
    avg_claims = sum(recent_claims) / len(recent_claims)
    claims_trend = (current_claims - avg_claims) / avg_claims
    print(f"\nINITIAL CLAIMS:")
    print(f"  Current: {current_claims:,}")
    print(f"  4-Week Average: {int(avg_claims):,}")
    print(f"  Trend: {claims_trend:+.1%}")
    
    # Continuing Claims
    current_continuing = int(fred_data['CCSA']['data'][0]['value'])
    prev_continuing = int(fred_data['CCSA']['data'][1]['value'])
    continuing_trend = (current_continuing - prev_continuing) / prev_continuing
    print(f"\nCONTINUING CLAIMS:")
    print(f"  Current: {current_continuing:,}")
    print(f"  Previous: {prev_continuing:,}")
    print(f"  Trend: {continuing_trend:+.1%}")
    
    # JOLTS Data
    current_openings = int(fred_data['JTSJOL']['data'][0]['value'])
    current_hires = int(fred_data['JTSHIL']['data'][0]['value'])
    current_quits = int(fred_data['JTSQUL']['data'][0]['value'])
    current_separations = int(fred_data['JTSTSL']['data'][0]['value'])
    
    print(f"\nJOLTS DATA (July 2025):")
    print(f"  Job Openings: {current_openings:,}")
    print(f"  Hires: {current_hires:,}")
    print(f"  Quits: {current_quits:,}")
    print(f"  Separations: {current_separations:,}")
    
    # Calculate labor market tightness
    tightness_ratio = current_openings / current_hires if current_hires > 0 else 0
    quit_rate = current_quits / current_hires if current_hires > 0 else 0
    separation_rate = current_separations / current_hires if current_hires > 0 else 0
    
    print(f"  Labor Market Tightness: {tightness_ratio:.2f}")
    print(f"  Quit Rate: {quit_rate:.2%}")
    print(f"  Separation Rate: {separation_rate:.2%}")
    
    print()
    
    # Simple forecast calculation based on trends
    print("SIMPLE FORECAST CALCULATION")
    print("-" * 30)
    
    # Base forecast starts with current rate
    forecast = current_unrate
    adjustments = []
    
    # Labor Force Participation adjustment
    # Lower LFPR typically means higher unemployment
    if lfpr_trend < 0:
        lfpr_adj = abs(lfpr_trend) * 0.5  # Conservative adjustment
        forecast += lfpr_adj
        adjustments.append(f"LFPR decline: +{lfpr_adj:.2f}pp")
    elif lfpr_trend > 0:
        lfpr_adj = -lfpr_trend * 0.3  # Smaller positive impact
        forecast += lfpr_adj
        adjustments.append(f"LFPR increase: {lfpr_adj:.2f}pp")
    
    # Initial Claims adjustment
    # Higher claims typically mean higher unemployment
    if claims_trend > 0.05:  # 5% increase threshold
        claims_adj = claims_trend * 0.1  # Conservative adjustment
        forecast += claims_adj
        adjustments.append(f"Claims increase: +{claims_adj:.2f}pp")
    elif claims_trend < -0.05:  # 5% decrease threshold
        claims_adj = claims_trend * 0.1
        forecast += claims_adj
        adjustments.append(f"Claims decrease: {claims_adj:.2f}pp")
    
    # Continuing Claims adjustment
    if continuing_trend > 0.02:  # 2% increase threshold
        continuing_adj = continuing_trend * 0.05
        forecast += continuing_adj
        adjustments.append(f"Continuing claims increase: +{continuing_adj:.2f}pp")
    elif continuing_trend < -0.02:  # 2% decrease threshold
        continuing_adj = continuing_trend * 0.05
        forecast += continuing_adj
        adjustments.append(f"Continuing claims decrease: {continuing_adj:.2f}pp")
    
    # JOLTS adjustment
    # More job openings relative to hires suggests labor market tightness
    if tightness_ratio > 1.4:  # High tightness
        jolts_adj = -0.05  # Slight downward pressure
        forecast += jolts_adj
        adjustments.append(f"High labor market tightness: {jolts_adj:.2f}pp")
    elif tightness_ratio < 1.2:  # Low tightness
        jolts_adj = 0.05  # Slight upward pressure
        forecast += jolts_adj
        adjustments.append(f"Low labor market tightness: +{jolts_adj:.2f}pp")
    
    # Quit rate adjustment
    if quit_rate > 0.6:  # High quit rate
        quit_adj = -0.03  # Slight downward pressure (confidence in job market)
        forecast += quit_adj
        adjustments.append(f"High quit rate: {quit_adj:.2f}pp")
    elif quit_rate < 0.5:  # Low quit rate
        quit_adj = 0.03  # Slight upward pressure
        forecast += quit_adj
        adjustments.append(f"Low quit rate: +{quit_adj:.2f}pp")
    
    print(f"Base Rate: {current_unrate}%")
    print(f"Adjustments:")
    for adj in adjustments:
        print(f"  {adj}")
    
    total_adjustment = forecast - current_unrate
    print(f"Total Adjustment: {total_adjustment:+.2f}pp")
    print(f"Final Forecast: {forecast:.2f}%")
    
    print()
    
    # Confidence assessment
    print("CONFIDENCE ASSESSMENT")
    print("-" * 30)
    
    # Count reliable indicators
    reliable_indicators = 0
    total_indicators = 0
    
    # LFPR reliability
    if abs(lfpr_trend) > 0.05:  # Significant change
        reliable_indicators += 1
    total_indicators += 1
    
    # Claims reliability
    if abs(claims_trend) > 0.05:  # Significant change
        reliable_indicators += 1
    total_indicators += 1
    
    # JOLTS reliability
    if tightness_ratio > 1.3 or tightness_ratio < 1.1:  # Clear signal
        reliable_indicators += 1
    total_indicators += 1
    
    confidence = (reliable_indicators / total_indicators) * 100
    
    print(f"Reliable indicators: {reliable_indicators}/{total_indicators}")
    print(f"Confidence level: {confidence:.0f}%")
    
    if confidence >= 80:
        print("High confidence forecast")
    elif confidence >= 60:
        print("Medium confidence forecast")
    else:
        print("Low confidence forecast")
    
    print()
    
    # Save forecast results
    forecast_results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'base_rate': current_unrate,
        'forecast': round(forecast, 2),
        'total_adjustment': round(total_adjustment, 2),
        'confidence': round(confidence, 0),
        'adjustments': adjustments,
        'data_sources': {
            'unemployment_rate': current_unrate,
            'labor_force_participation': current_lfpr,
            'initial_claims': current_claims,
            'continuing_claims': current_continuing,
            'job_openings': current_openings,
            'hires': current_hires,
            'quits': current_quits
        },
        'trends': {
            'lfpr_trend': lfpr_trend,
            'claims_trend': claims_trend,
            'continuing_trend': continuing_trend,
            'tightness_ratio': tightness_ratio,
            'quit_rate': quit_rate
        }
    }
    
    with open('real_forecast_results.json', 'w') as f:
        json.dump(forecast_results, f, indent=2)
    
    print(f"Forecast results saved to: real_forecast_results.json")
    
    return forecast_results

if __name__ == "__main__":
    results = real_forecast_with_api_data()
    if results:
        print(f"\nReal forecast completed successfully!")
    else:
        print(f"\nForecast failed - no data available")