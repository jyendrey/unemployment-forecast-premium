#!/usr/bin/env python3
"""
Test Different Trade Data Weights
Compare forecast impact with varying trade data weights
"""

import json
import csv
from datetime import datetime
from collections import defaultdict

def load_fred_baseline():
    """Load the FRED-based August 2024 baseline forecast"""
    try:
        with open('aug2024_forecast.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: aug2024_forecast.json not found")
        return None

def load_historical_data():
    """Load historical FRED data"""
    try:
        with open('historical_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: historical_data.json not found")
        return None

def parse_unemployment_contract(contract_str):
    """Parse unemployment rate contract to extract target rate and date"""
    try:
        parts = contract_str.split('_')
        if len(parts) >= 3:
            rate = float(parts[2])
            date_str = parts[1]  # 0724
            month = int(date_str[:2])
            year = 2000 + int(date_str[2:])
            return rate, year, month
    except:
        pass
    return None, None, None

def parse_initial_claims_contract(contract_str):
    """Parse initial claims contract to extract target value and date"""
    try:
        parts = contract_str.split('_')
        if len(parts) >= 3:
            value = int(parts[2])
            date_str = parts[1]  # 080324
            month = int(date_str[:2])
            day = int(date_str[2:4])
            year = 2000 + int(date_str[4:])
            return value, year, month, day
    except:
        pass
    return None, None, None, None

def load_trade_data_from_aug2024():
    """Load trade data from August 2024 onward"""
    unrate_pairs = []
    claims_pairs = []
    
    # Load unemployment rate pairs
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    rate, year, month = parse_unemployment_contract(row['event_contract'])
                    if rate and year and month:
                        if year > 2024 or (year == 2024 and month >= 8):
                            unrate_pairs.append({
                                'target_rate': rate,
                                'yes_price': float(row['yes_price']),
                                'no_price': float(row['no_price']),
                                'quantity': int(row['quantity'])
                            })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        pass
    
    # Load initial claims pairs
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    value, year, month, day = parse_initial_claims_contract(row['event_contract'])
                    if value and year and month:
                        if year > 2024 or (year == 2024 and month >= 8):
                            claims_pairs.append({
                                'target_value': value,
                                'yes_price': float(row['yes_price']),
                                'no_price': float(row['no_price']),
                                'quantity': int(row['quantity'])
                            })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        pass
    
    return unrate_pairs, claims_pairs

def calculate_trade_sentiment(trade_data, scale_factor=0.1):
    """Calculate trade sentiment with given scale factor"""
    
    # Unemployment rate sentiment
    unrate_sentiment = 0.0
    unrate_volume = 0
    
    if trade_data['unrate_pairs']:
        relevant_pairs = [p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            unrate_sentiment = weighted_yes - 0.5
            unrate_volume = total_quantity
    
    # Initial claims sentiment
    claims_sentiment = 0.0
    claims_volume = 0
    
    if trade_data['claims_pairs']:
        relevant_pairs = [p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            claims_sentiment = weighted_yes - 0.5
            claims_volume = total_quantity
    
    # Combine sentiments
    combined_sentiment = (unrate_sentiment + claims_sentiment) / 2
    total_volume = unrate_volume + claims_volume
    
    return {
        'unrate_sentiment': unrate_sentiment,
        'claims_sentiment': claims_sentiment,
        'combined_sentiment': combined_sentiment,
        'unrate_volume': unrate_volume,
        'claims_volume': claims_volume,
        'total_volume': total_volume
    }

def calculate_forecast_with_weights(weights, scale_factor, trade_data, historical_data):
    """Calculate forecast with given weights and scale factor"""
    
    # Get trade sentiment
    trade_sentiment = calculate_trade_sentiment(trade_data, scale_factor)
    
    # Calculate trade data adjustment
    trade_adjustment = trade_sentiment['combined_sentiment'] * weights['trade_data'] * scale_factor
    
    # Calculate core labor market adjustment (simplified)
    core_adjustment = 0.0
    if historical_data:
        # LFPR adjustment
        lfpr_data = historical_data['historical_data'].get('CIVPART', {}).get('data', [])
        if lfpr_data and len(lfpr_data) >= 12:
            recent_avg = sum(float(d['value']) for d in lfpr_data[-12:]) / 12
            older_avg = sum(float(d['value']) for d in lfpr_data[-24:-12]) / 12
            lfpr_trend = recent_avg - older_avg
            core_adjustment += -lfpr_trend * weights['core_labor'] * scale_factor
        
        # Initial claims adjustment
        icsa_data = historical_data['historical_data'].get('ICSA', {}).get('data', [])
        if icsa_data and len(icsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in icsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in icsa_data[-8:-4]) / 4
            claims_trend = (recent_avg - older_avg) / older_avg
            core_adjustment += claims_trend * weights['core_labor'] * scale_factor
    
    # Leading indicators adjustment (simplified)
    leading_adjustment = 0.0
    if historical_data:
        jolts_data = historical_data['historical_data'].get('JTSJOL', {}).get('data', [])
        if jolts_data and len(jolts_data) >= 6:
            recent_avg = sum(int(d['value']) for d in jolts_data[-6:]) / 6
            older_avg = sum(int(d['value']) for d in jolts_data[-12:-6]) / 6
            jolts_trend = (recent_avg - older_avg) / older_avg
            leading_adjustment += -jolts_trend * weights['leading_indicators'] * scale_factor
    
    total_adjustment = trade_adjustment + core_adjustment + leading_adjustment
    
    return {
        'trade_adjustment': trade_adjustment,
        'core_adjustment': core_adjustment,
        'leading_adjustment': leading_adjustment,
        'total_adjustment': total_adjustment,
        'trade_sentiment': trade_sentiment
    }

def test_trade_data_weights():
    """Test different trade data weight scenarios"""
    print("TRADE DATA WEIGHT TESTING")
    print("=" * 40)
    
    # Load data
    fred_baseline = load_fred_baseline()
    historical_data = load_historical_data()
    unrate_pairs, claims_pairs = load_trade_data_from_aug2024()
    
    if not all([fred_baseline, historical_data]):
        print("Error: Missing required data")
        return None
    
    trade_data = {
        'unrate_pairs': unrate_pairs,
        'claims_pairs': claims_pairs
    }
    
    base_forecast = fred_baseline['forecast']
    print(f"FRED Baseline: {base_forecast}%")
    print(f"Trade Data Volume: {len(unrate_pairs) + len(claims_pairs):,} trades")
    print()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Current (25% Trade)',
            'weights': {'core_labor': 0.70, 'trade_data': 0.25, 'leading_indicators': 0.05},
            'scale_factor': 0.1
        },
        {
            'name': 'Balanced (40% Trade)',
            'weights': {'core_labor': 0.50, 'trade_data': 0.40, 'leading_indicators': 0.10},
            'scale_factor': 0.1
        },
        {
            'name': 'Market-Heavy (50% Trade)',
            'weights': {'core_labor': 0.40, 'trade_data': 0.50, 'leading_indicators': 0.10},
            'scale_factor': 0.1
        },
        {
            'name': 'High Impact (40% Trade, 0.5x Scale)',
            'weights': {'core_labor': 0.50, 'trade_data': 0.40, 'leading_indicators': 0.10},
            'scale_factor': 0.5
        },
        {
            'name': 'Very High Impact (50% Trade, 1.0x Scale)',
            'weights': {'core_labor': 0.40, 'trade_data': 0.50, 'leading_indicators': 0.10},
            'scale_factor': 1.0
        }
    ]
    
    results = {}
    
    for scenario in scenarios:
        print(f"{scenario['name'].upper()}")
        print("-" * len(scenario['name']))
        
        forecast_data = calculate_forecast_with_weights(
            scenario['weights'], 
            scenario['scale_factor'], 
            trade_data, 
            historical_data
        )
        
        final_forecast = base_forecast + forecast_data['total_adjustment']
        
        print(f"  Trade Data Weight: {scenario['weights']['trade_data']*100:.0f}%")
        print(f"  Scale Factor: {scenario['scale_factor']}")
        print(f"  Trade Sentiment: {forecast_data['trade_sentiment']['combined_sentiment']:+.3f}")
        print(f"  Trade Adjustment: {forecast_data['trade_adjustment']:+.3f}pp")
        print(f"  Core Adjustment: {forecast_data['core_adjustment']:+.3f}pp")
        print(f"  Leading Adjustment: {forecast_data['leading_adjustment']:+.3f}pp")
        print(f"  Total Adjustment: {forecast_data['total_adjustment']:+.3f}pp")
        print(f"  Final Forecast: {final_forecast:.2f}%")
        print()
        
        results[scenario['name']] = {
            'weights': scenario['weights'],
            'scale_factor': scenario['scale_factor'],
            'forecast': final_forecast,
            'trade_adjustment': forecast_data['trade_adjustment'],
            'total_adjustment': forecast_data['total_adjustment'],
            'trade_sentiment': forecast_data['trade_sentiment']['combined_sentiment']
        }
    
    # Analysis
    print("IMPACT ANALYSIS")
    print("-" * 15)
    
    forecasts = [r['forecast'] for r in results.values()]
    trade_adjustments = [r['trade_adjustment'] for r in results.values()]
    
    min_forecast = min(forecasts)
    max_forecast = max(forecasts)
    forecast_range = max_forecast - min_forecast
    
    min_trade_adj = min(trade_adjustments)
    max_trade_adj = max(trade_adjustments)
    trade_range = max_trade_adj - min_trade_adj
    
    print(f"Forecast Range: {min_forecast:.2f}% to {max_forecast:.2f}% ({forecast_range:.2f}pp)")
    print(f"Trade Adjustment Range: {min_trade_adj:+.3f}pp to {max_trade_adj:+.3f}pp ({trade_range:.3f}pp)")
    print()
    
    # Find most impactful scenario
    most_impactful = max(enumerate([abs(r['trade_adjustment']) for r in results.values()]), key=lambda x: x[1])[0]
    scenario_names = list(results.keys())
    
    print(f"Most Trade Data Impact: {scenario_names[most_impactful]}")
    print(f"Trade Adjustment: {trade_adjustments[most_impactful]:+.3f}pp")
    
    # Save results
    with open('trade_weight_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'base_forecast': base_forecast,
            'scenarios': results,
            'analysis': {
                'forecast_range': forecast_range,
                'trade_adjustment_range': trade_range,
                'most_impactful': scenario_names[most_impactful]
            }
        }, f, indent=2)
    
    print(f"\nResults saved to: trade_weight_test_results.json")
    
    return results

if __name__ == "__main__":
    results = test_trade_data_weights()
    if results:
        print(f"\nTrade weight testing completed successfully!")
    else:
        print(f"\nTesting failed - no data available")