#!/usr/bin/env python3
"""
FRED-Based Forecast for August 2024
Using historical data to forecast unemployment rate
"""

import json
from datetime import datetime

def fred_based_forecast_aug2024():
    """Create FRED-based forecast for August 2024"""
    
    print("FRED-BASED FORECAST FOR AUGUST 2024")
    print("="*50)
    
    # Load historical data
    try:
        with open('historical_data.json', 'r') as f:
            hist_data = json.load(f)
    except FileNotFoundError:
        print("Error: historical_data.json not found. Run fetch_historical_data.py first.")
        return None
    
    print(f"Historical data loaded: {hist_data['timestamp']}")
    print(f"Data range: {hist_data['date_range']['start']} to {hist_data['date_range']['end']}")
    print()
    
    # Extract data for analysis
    unrate_data = hist_data['historical_data']['UNRATE']['data']
    lfpr_data = hist_data['historical_data']['CIVPART']['data']
    claims_data = hist_data['historical_data']['ICSA']['data']
    continuing_data = hist_data['historical_data']['CCSA']['data']
    jolts_data = hist_data['historical_data']['JTSJOL']['data']
    
    # Find August 2024 data point
    aug2024_unrate = None
    aug2024_lfpr = None
    aug2024_claims = None
    aug2024_continuing = None
    aug2024_jolts = None
    
    # Get August 2024 unemployment rate
    for obs in unrate_data:
        if obs['date'].startswith('2024-08'):
            aug2024_unrate = float(obs['value'])
            break
    
    # Get August 2024 labor force participation
    for obs in lfpr_data:
        if obs['date'].startswith('2024-08'):
            aug2024_lfpr = float(obs['value'])
            break
    
    # Get August 2024 claims data (weekly, so get closest)
    aug2024_claims_list = [obs for obs in claims_data if obs['date'].startswith('2024-08')]
    if aug2024_claims_list:
        aug2024_claims = int(aug2024_claims_list[0]['value'])
    
    # Get August 2024 continuing claims
    aug2024_continuing_list = [obs for obs in continuing_data if obs['date'].startswith('2024-08')]
    if aug2024_continuing_list:
        aug2024_continuing = int(aug2024_continuing_list[0]['value'])
    
    # Get July 2024 JOLTS data (latest available)
    july2024_jolts_list = [obs for obs in jolts_data if obs['date'].startswith('2024-07')]
    if july2024_jolts_list:
        aug2024_jolts = int(july2024_jolts_list[0]['value'])
    
    print("AUGUST 2024 DATA")
    print("-" * 30)
    if aug2024_unrate:
        print(f"Unemployment Rate: {aug2024_unrate}%")
    if aug2024_lfpr:
        print(f"Labor Force Participation: {aug2024_lfpr}%")
    if aug2024_claims:
        print(f"Initial Claims: {aug2024_claims:,}")
    if aug2024_continuing:
        print(f"Continuing Claims: {aug2024_continuing:,}")
    if aug2024_jolts:
        print(f"Job Openings (July): {aug2024_jolts:,}")
    
    print()
    
    # Calculate trends for forecasting
    print("TREND ANALYSIS")
    print("-" * 30)
    
    # Get previous month data for comparison
    july2024_unrate = None
    july2024_lfpr = None
    
    for obs in unrate_data:
        if obs['date'].startswith('2024-07'):
            july2024_unrate = float(obs['value'])
            break
    
    for obs in lfpr_data:
        if obs['date'].startswith('2024-07'):
            july2024_lfpr = float(obs['value'])
            break
    
    if aug2024_unrate and july2024_unrate:
        unrate_trend = aug2024_unrate - july2024_unrate
        print(f"Unemployment Rate Trend: {unrate_trend:+.2f}pp (July to August)")
    
    if aug2024_lfpr and july2024_lfpr:
        lfpr_trend = aug2024_lfpr - july2024_lfpr
        print(f"Labor Force Participation Trend: {lfpr_trend:+.2f}pp (July to August)")
    
    # Calculate 4-week average claims
    if aug2024_claims:
        # Get 4 weeks of August claims data
        aug_claims_data = [obs for obs in claims_data if obs['date'].startswith('2024-08')]
        if len(aug_claims_data) >= 4:
            recent_claims = [int(obs['value']) for obs in aug_claims_data[:4]]
            avg_claims = sum(recent_claims) / len(recent_claims)
            print(f"4-Week Average Initial Claims: {int(avg_claims):,}")
    
    print()
    
    # Historical analysis for forecasting
    print("HISTORICAL ANALYSIS")
    print("-" * 30)
    
    # Get 2024 data for trend analysis
    unrate_2024 = [float(obs['value']) for obs in unrate_data if obs['date'].startswith('2024')]
    lfpr_2024 = [float(obs['value']) for obs in lfpr_data if obs['date'].startswith('2024')]
    
    if unrate_2024:
        min_2024 = min(unrate_2024)
        max_2024 = max(unrate_2024)
        avg_2024 = sum(unrate_2024) / len(unrate_2024)
        print(f"2024 Unemployment Rate:")
        print(f"  Range: {min_2024:.1f}% to {max_2024:.1f}%")
        print(f"  Average: {avg_2024:.1f}%")
        print(f"  Months: {len(unrate_2024)}")
    
    if lfpr_2024:
        min_lfpr_2024 = min(lfpr_2024)
        max_lfpr_2024 = max(lfpr_2024)
        avg_lfpr_2024 = sum(lfpr_2024) / len(lfpr_2024)
        print(f"\n2024 Labor Force Participation:")
        print(f"  Range: {min_lfpr_2024:.1f}% to {max_lfpr_2024:.1f}%")
        print(f"  Average: {avg_lfpr_2024:.1f}%")
        print(f"  Months: {len(lfpr_2024)}")
    
    print()
    
    # Simple forecast for September 2024
    print("SEPTEMBER 2024 FORECAST")
    print("-" * 30)
    
    if aug2024_unrate:
        # Base forecast starts with August 2024 rate
        forecast = aug2024_unrate
        adjustments = []
        
        # Trend-based adjustment
        if 'unrate_trend' in locals():
            if unrate_trend > 0.1:  # Rising trend
                trend_adj = 0.05  # Continue rising
                forecast += trend_adj
                adjustments.append(f"Rising trend: +{trend_adj:.2f}pp")
            elif unrate_trend < -0.1:  # Falling trend
                trend_adj = -0.05  # Continue falling
                forecast += trend_adj
                adjustments.append(f"Falling trend: {trend_adj:.2f}pp")
        
        # Labor force participation adjustment
        if 'lfpr_trend' in locals():
            if lfpr_trend > 0.1:  # Rising LFPR
                lfpr_adj = -0.03  # Slight downward pressure
                forecast += lfpr_adj
                adjustments.append(f"Rising LFPR: {lfpr_adj:.2f}pp")
            elif lfpr_trend < -0.1:  # Falling LFPR
                lfpr_adj = 0.03  # Slight upward pressure
                forecast += lfpr_adj
                adjustments.append(f"Falling LFPR: +{lfpr_adj:.2f}pp")
        
        # Claims adjustment
        if 'avg_claims' in locals() and aug2024_claims:
            claims_ratio = aug2024_claims / avg_claims
            if claims_ratio > 1.05:  # 5% above average
                claims_adj = 0.02  # Slight upward pressure
                forecast += claims_adj
                adjustments.append(f"High claims: +{claims_adj:.2f}pp")
            elif claims_ratio < 0.95:  # 5% below average
                claims_adj = -0.02  # Slight downward pressure
                forecast += claims_adj
                adjustments.append(f"Low claims: {claims_adj:.2f}pp")
        
        print(f"Base Rate (August 2024): {aug2024_unrate}%")
        if adjustments:
            print(f"Adjustments:")
            for adj in adjustments:
                print(f"  {adj}")
        else:
            print(f"Adjustments: None (stable conditions)")
        
        total_adjustment = forecast - aug2024_unrate
        print(f"Total Adjustment: {total_adjustment:+.2f}pp")
        print(f"September 2024 Forecast: {forecast:.2f}%")
        
        # Confidence assessment
        print(f"\nConfidence Assessment:")
        if abs(total_adjustment) < 0.05:
            print(f"High confidence (stable conditions)")
            confidence = 85
        elif abs(total_adjustment) < 0.15:
            print(f"Medium confidence (moderate changes)")
            confidence = 70
        else:
            print(f"Low confidence (significant changes)")
            confidence = 55
        
        print(f"Confidence Level: {confidence}%")
        
        # Save forecast results
        forecast_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'forecast_date': 'September 2024',
            'base_rate': aug2024_unrate,
            'forecast': round(forecast, 2),
            'total_adjustment': round(total_adjustment, 2),
            'confidence': confidence,
            'adjustments': adjustments,
            'data_sources': {
                'unemployment_rate': aug2024_unrate,
                'labor_force_participation': aug2024_lfpr,
                'initial_claims': aug2024_claims,
                'continuing_claims': aug2024_continuing,
                'job_openings': aug2024_jolts
            }
        }
        
        with open('aug2024_forecast.json', 'w') as f:
            json.dump(forecast_results, f, indent=2)
        
        print(f"\nForecast results saved to: aug2024_forecast.json")
        
        return forecast_results
    
    else:
        print("Error: Could not find August 2024 unemployment rate data")
        return None

if __name__ == "__main__":
    results = fred_based_forecast_aug2024()
    if results:
        print(f"\nFRED-based forecast completed successfully!")
    else:
        print(f"\nForecast failed - no data available")