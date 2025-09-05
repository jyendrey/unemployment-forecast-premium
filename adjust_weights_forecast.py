#!/usr/bin/env python3
"""
Adjust Weights and Test Forecast Impact
Test different weight distributions to see how they affect the forecast
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
    """Parse unemployment rate contract to extract target rate"""
    try:
        parts = contract_str.split('_')
        if len(parts) >= 3:
            return float(parts[2])
    except:
        pass
    return None

def parse_initial_claims_contract(contract_str):
    """Parse initial claims contract to extract target value"""
    try:
        parts = contract_str.split('_')
        if len(parts) >= 3:
            return int(parts[2])
    except:
        pass
    return None

def calculate_forecast_with_weights(weights, historical_data, trade_data):
    """Calculate forecast with given weights"""
    
    # Core Labor Market Adjustments
    core_adjustments = {}
    
    # LFPR
    lfpr_data = historical_data['historical_data'].get('CIVPART', {}).get('data', [])
    if lfpr_data:
        latest_lfpr = float(lfpr_data[-1]['value'])
        if len(lfpr_data) >= 12:
            recent_avg = sum(float(d['value']) for d in lfpr_data[-12:]) / 12
            older_avg = sum(float(d['value']) for d in lfpr_data[-24:-12]) / 12
            lfpr_trend = recent_avg - older_avg
        else:
            lfpr_trend = 0
        lfpr_adjustment = -lfpr_trend * weights['lfpr'] * 0.1
        core_adjustments['lfpr'] = lfpr_adjustment
    
    # Initial Claims
    icsa_data = historical_data['historical_data'].get('ICSA', {}).get('data', [])
    if icsa_data:
        latest_claims = int(icsa_data[-1]['value'])
        if len(icsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in icsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in icsa_data[-8:-4]) / 4
            claims_trend = (recent_avg - older_avg) / older_avg
        else:
            claims_trend = 0
        claims_adjustment = claims_trend * weights['initial_claims'] * 0.1
        core_adjustments['initial_claims'] = claims_adjustment
    
    # Continuing Claims
    ccsa_data = historical_data['historical_data'].get('CCSA', {}).get('data', [])
    if ccsa_data:
        latest_continuing = int(ccsa_data[-1]['value'])
        if len(ccsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in ccsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in ccsa_data[-8:-4]) / 4
            continuing_trend = (recent_avg - older_avg) / older_avg
        else:
            continuing_trend = 0
        continuing_adjustment = continuing_trend * weights['continuing_claims'] * 0.1
        core_adjustments['continuing_claims'] = continuing_adjustment
    
    # Trade Data Adjustments
    trade_adjustments = {}
    
    # Unemployment Trade Sentiment
    if trade_data['unrate_pairs']:
        relevant_pairs = [p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            sentiment = weighted_yes - 0.5
            adjustment = sentiment * weights['unemployment_trade_sentiment'] * 0.1
            trade_adjustments['unemployment_trade_sentiment'] = adjustment
    
    # Unemployment Trade Volume
    if trade_data['unrate_pairs']:
        total_volume = sum(p['quantity'] for p in trade_data['unrate_pairs'])
        volume_adjustment = min(total_volume / 10000, 1.0) * weights['unemployment_trade_volume'] * 0.05
        trade_adjustments['unemployment_trade_volume'] = volume_adjustment
    
    # Claims Trade Sentiment
    if trade_data['claims_pairs']:
        relevant_pairs = [p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            sentiment = weighted_yes - 0.5
            adjustment = sentiment * weights['claims_trade_sentiment'] * 0.1
            trade_adjustments['claims_trade_sentiment'] = adjustment
    
    # Leading Indicators Adjustments
    leading_adjustments = {}
    
    # JOLTS
    jolts_data = historical_data['historical_data'].get('JTSJOL', {}).get('data', [])
    if jolts_data:
        latest_jolts = int(jolts_data[-1]['value'])
        if len(jolts_data) >= 6:
            recent_avg = sum(int(d['value']) for d in jolts_data[-6:]) / 6
            older_avg = sum(int(d['value']) for d in jolts_data[-12:-6]) / 6
            jolts_trend = (recent_avg - older_avg) / older_avg
        else:
            jolts_trend = 0
        jolts_adjustment = -jolts_trend * weights['jolts_data'] * 0.1
        leading_adjustments['jolts_data'] = jolts_adjustment
    
    # Business Cycle (GDP)
    gdp_data = historical_data['historical_data'].get('GDP', {}).get('data', [])
    if gdp_data:
        latest_gdp = float(gdp_data[-1]['value'])
        if len(gdp_data) >= 2:
            gdp_growth = (latest_gdp - float(gdp_data[-2]['value'])) / float(gdp_data[-2]['value'])
        else:
            gdp_growth = 0
        gdp_adjustment = -gdp_growth * weights['business_cycle_indicators'] * 0.1
        leading_adjustments['business_cycle_indicators'] = gdp_adjustment
    
    # Calculate total adjustment
    all_adjustments = {**core_adjustments, **trade_adjustments, **leading_adjustments}
    total_adjustment = sum(all_adjustments.values())
    
    return {
        'core_adjustments': core_adjustments,
        'trade_adjustments': trade_adjustments,
        'leading_adjustments': leading_adjustments,
        'total_adjustment': total_adjustment,
        'all_adjustments': all_adjustments
    }

def load_trade_data():
    """Load trade data"""
    trade_data = {'unrate_pairs': [], 'claims_pairs': []}
    
    # Load unemployment rate pairs
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate:
                        trade_data['unrate_pairs'].append({
                            'target_rate': target_rate,
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
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value:
                        trade_data['claims_pairs'].append({
                            'target_value': target_value,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity'])
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        pass
    
    return trade_data

def test_weight_scenarios():
    """Test different weight scenarios"""
    print("WEIGHT ADJUSTMENT ANALYSIS")
    print("=" * 40)
    
    # Load data
    fred_baseline = load_fred_baseline()
    historical_data = load_historical_data()
    trade_data = load_trade_data()
    
    if not all([fred_baseline, historical_data]):
        print("Error: Missing required data")
        return None
    
    base_forecast = fred_baseline['forecast']
    print(f"FRED Baseline: {base_forecast}%")
    print()
    
    # Define weight scenarios
    scenarios = {
        "Current (Cleaned)": {
            'lfpr': 0.35,
            'initial_claims': 0.25,
            'continuing_claims': 0.10,
            'unemployment_trade_sentiment': 0.15,
            'unemployment_trade_volume': 0.05,
            'claims_trade_sentiment': 0.05,
            'jolts_data': 0.03,
            'business_cycle_indicators': 0.02
        },
        "Labor Market Heavy": {
            'lfpr': 0.50,
            'initial_claims': 0.30,
            'continuing_claims': 0.15,
            'unemployment_trade_sentiment': 0.03,
            'unemployment_trade_volume': 0.01,
            'claims_trade_sentiment': 0.01,
            'jolts_data': 0.00,
            'business_cycle_indicators': 0.00
        },
        "Trade Data Heavy": {
            'lfpr': 0.20,
            'initial_claims': 0.15,
            'continuing_claims': 0.05,
            'unemployment_trade_sentiment': 0.30,
            'unemployment_trade_volume': 0.15,
            'claims_trade_sentiment': 0.10,
            'jolts_data': 0.03,
            'business_cycle_indicators': 0.02
        },
        "Balanced": {
            'lfpr': 0.25,
            'initial_claims': 0.20,
            'continuing_claims': 0.10,
            'unemployment_trade_sentiment': 0.20,
            'unemployment_trade_volume': 0.10,
            'claims_trade_sentiment': 0.10,
            'jolts_data': 0.03,
            'business_cycle_indicators': 0.02
        },
        "Leading Indicators Heavy": {
            'lfpr': 0.20,
            'initial_claims': 0.15,
            'continuing_claims': 0.05,
            'unemployment_trade_sentiment': 0.15,
            'unemployment_trade_volume': 0.05,
            'claims_trade_sentiment': 0.05,
            'jolts_data': 0.20,
            'business_cycle_indicators': 0.15
        }
    }
    
    results = {}
    
    for scenario_name, weights in scenarios.items():
        print(f"{scenario_name.upper()}")
        print("-" * len(scenario_name))
        
        # Calculate forecast
        forecast_data = calculate_forecast_with_weights(weights, historical_data, trade_data)
        final_forecast = base_forecast + forecast_data['total_adjustment']
        
        print(f"  Core Labor Market: {sum(forecast_data['core_adjustments'].values()):+.3f}pp")
        print(f"  Trade Data: {sum(forecast_data['trade_adjustments'].values()):+.3f}pp")
        print(f"  Leading Indicators: {sum(forecast_data['leading_adjustments'].values()):+.3f}pp")
        print(f"  Total Adjustment: {forecast_data['total_adjustment']:+.3f}pp")
        print(f"  Final Forecast: {final_forecast:.2f}%")
        print(f"  Weight Total: {sum(weights.values()):.3f}")
        print()
        
        results[scenario_name] = {
            'weights': weights,
            'forecast': final_forecast,
            'adjustment': forecast_data['total_adjustment'],
            'core_adj': sum(forecast_data['core_adjustments'].values()),
            'trade_adj': sum(forecast_data['trade_adjustments'].values()),
            'leading_adj': sum(forecast_data['leading_adjustments'].values())
        }
    
    # Analysis
    print("WEIGHT IMPACT ANALYSIS")
    print("-" * 25)
    
    forecasts = [r['forecast'] for r in results.values()]
    min_forecast = min(forecasts)
    max_forecast = max(forecasts)
    forecast_range = max_forecast - min_forecast
    
    print(f"Forecast Range: {min_forecast:.2f}% to {max_forecast:.2f}%")
    print(f"Range: {forecast_range:.2f}pp")
    print()
    
    # Find most/least sensitive scenarios
    adjustments = [abs(r['adjustment']) for r in results.values()]
    most_sensitive = max(enumerate(adjustments), key=lambda x: x[1])[0]
    least_sensitive = min(enumerate(adjustments), key=lambda x: x[1])[0]
    
    scenario_names = list(results.keys())
    print(f"Most Sensitive: {scenario_names[most_sensitive]} ({adjustments[most_sensitive]:.3f}pp)")
    print(f"Least Sensitive: {scenario_names[least_sensitive]} ({adjustments[least_sensitive]:.3f}pp)")
    
    # Save results
    with open('weight_adjustment_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'base_forecast': base_forecast,
            'scenarios': results,
            'analysis': {
                'forecast_range': forecast_range,
                'min_forecast': min_forecast,
                'max_forecast': max_forecast,
                'most_sensitive': scenario_names[most_sensitive],
                'least_sensitive': scenario_names[least_sensitive]
            }
        }, f, indent=2)
    
    print(f"\nResults saved to: weight_adjustment_results.json")
    
    return results

if __name__ == "__main__":
    results = test_weight_scenarios()
    if results:
        print(f"\nWeight adjustment analysis completed successfully!")
    else:
        print(f"\nAnalysis failed - no data available")