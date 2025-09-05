#!/usr/bin/env python3
"""
Adjust Base to Last Published Unemployment Rate (4.3%)
Update the Conservative Reform system with correct base rate
"""

import json
import csv
from datetime import datetime
from collections import defaultdict

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

def calculate_updated_forecast_with_4_3_base():
    """Calculate forecast using 4.3% as the base rate"""
    print("UPDATED FORECAST: 4.3% BASE RATE")
    print("=" * 40)
    print("Using last published unemployment rate as base")
    print()
    
    # Load data
    historical_data = load_historical_data()
    unrate_pairs, claims_pairs = load_trade_data_from_aug2024()
    
    if not historical_data:
        print("Error: Missing required data")
        return None
    
    trade_data = {
        'unrate_pairs': unrate_pairs,
        'claims_pairs': claims_pairs
    }
    
    # Updated base rate
    base_forecast = 4.3  # Last published unemployment rate
    print(f"Base Rate (Last Published): {base_forecast}%")
    print(f"Trade Data Volume: {len(unrate_pairs) + len(claims_pairs):,} trades")
    print()
    
    # Conservative Reform weights and scale factor
    weights = {
        'core_labor': 0.50,      # 50% - Core labor market fundamentals
        'trade_data': 0.40,      # 40% - Trade data and market sentiment
        'leading_indicators': 0.10  # 10% - Leading economic indicators
    }
    scale_factor = 0.5  # 50% of raw signal
    
    print("SYSTEM CONFIGURATION")
    print("-" * 20)
    print(f"Core Labor Market Weight: {weights['core_labor']*100:.0f}%")
    print(f"Trade Data Weight: {weights['trade_data']*100:.0f}%")
    print(f"Leading Indicators Weight: {weights['leading_indicators']*100:.0f}%")
    print(f"Scale Factor: {scale_factor}x (50% of raw signal)")
    print()
    
    # Calculate trade sentiment
    print("TRADE DATA ANALYSIS")
    print("-" * 20)
    
    # Unemployment rate sentiment
    unrate_sentiment = 0.0
    unrate_volume = 0
    if trade_data['unrate_pairs']:
        relevant_pairs = [p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
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
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            claims_sentiment = weighted_yes - 0.5
            claims_volume = total_quantity
    
    combined_sentiment = (unrate_sentiment + claims_sentiment) / 2
    total_volume = unrate_volume + claims_volume
    
    print(f"Unemployment Rate Sentiment: {unrate_sentiment:+.3f}")
    print(f"  Relevant pairs: {len([p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5])}")
    print(f"  Volume: {unrate_volume:,}")
    print(f"Initial Claims Sentiment: {claims_sentiment:+.3f}")
    print(f"  Relevant pairs: {len([p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000])}")
    print(f"  Volume: {claims_volume:,}")
    print(f"Combined Sentiment: {combined_sentiment:+.3f}")
    print(f"Total Volume: {total_volume:,}")
    print()
    
    # Calculate adjustments
    print("FORECAST ADJUSTMENTS")
    print("-" * 20)
    
    # Trade data adjustment
    trade_adjustment = combined_sentiment * weights['trade_data'] * scale_factor
    print(f"Trade Data Adjustment: {trade_adjustment:+.3f}pp")
    print(f"  Calculation: {combined_sentiment:+.3f} × {weights['trade_data']} × {scale_factor} = {trade_adjustment:+.3f}pp")
    
    # Core labor market adjustment
    core_adjustment = 0.0
    if historical_data:
        # LFPR adjustment
        lfpr_data = historical_data['historical_data'].get('CIVPART', {}).get('data', [])
        if lfpr_data and len(lfpr_data) >= 12:
            recent_avg = sum(float(d['value']) for d in lfpr_data[-12:]) / 12
            older_avg = sum(float(d['value']) for d in lfpr_data[-24:-12]) / 12
            lfpr_trend = recent_avg - older_avg
            lfpr_adj = -lfpr_trend * weights['core_labor'] * scale_factor
            core_adjustment += lfpr_adj
            print(f"LFPR Adjustment: {lfpr_adj:+.3f}pp")
            print(f"  LFPR Trend: {lfpr_trend:+.2f}pp")
        
        # Initial claims adjustment
        icsa_data = historical_data['historical_data'].get('ICSA', {}).get('data', [])
        if icsa_data and len(icsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in icsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in icsa_data[-8:-4]) / 4
            claims_trend = (recent_avg - older_avg) / older_avg
            claims_adj = claims_trend * weights['core_labor'] * scale_factor
            core_adjustment += claims_adj
            print(f"Initial Claims Adjustment: {claims_adj:+.3f}pp")
            print(f"  Claims Trend: {claims_trend:+.1%}")
    
    print(f"Total Core Labor Adjustment: {core_adjustment:+.3f}pp")
    
    # Leading indicators adjustment
    leading_adjustment = 0.0
    if historical_data:
        jolts_data = historical_data['historical_data'].get('JTSJOL', {}).get('data', [])
        if jolts_data and len(jolts_data) >= 6:
            recent_avg = sum(int(d['value']) for d in jolts_data[-6:]) / 6
            older_avg = sum(int(d['value']) for d in jolts_data[-12:-6]) / 6
            jolts_trend = (recent_avg - older_avg) / older_avg
            jolts_adj = -jolts_trend * weights['leading_indicators'] * scale_factor
            leading_adjustment += jolts_adj
            print(f"JOLTS Adjustment: {jolts_adj:+.3f}pp")
            print(f"  JOLTS Trend: {jolts_trend:+.1%}")
    
    print(f"Total Leading Indicators Adjustment: {leading_adjustment:+.3f}pp")
    
    # Calculate final forecast
    total_adjustment = trade_adjustment + core_adjustment + leading_adjustment
    final_forecast = base_forecast + total_adjustment
    
    print()
    print("FINAL FORECAST CALCULATION")
    print("-" * 30)
    print(f"Base Rate (Last Published): {base_forecast}%")
    print(f"Trade Data Adjustment: {trade_adjustment:+.3f}pp")
    print(f"Core Labor Adjustment: {core_adjustment:+.3f}pp")
    print(f"Leading Indicators Adjustment: {leading_adjustment:+.3f}pp")
    print(f"Total Adjustment: {total_adjustment:+.3f}pp")
    print(f"Final Forecast: {final_forecast:.2f}%")
    
    # Calculate confidence
    base_confidence = 85  # Base confidence for published rate
    trade_confidence_boost = min(total_volume / 10000, 10)  # Volume-based boost
    final_confidence = min(base_confidence + trade_confidence_boost, 95)
    
    print()
    print("CONFIDENCE ANALYSIS")
    print("-" * 20)
    print(f"Base Confidence: {base_confidence}%")
    print(f"Trade Volume Boost: +{trade_confidence_boost:.1f}%")
    print(f"Final Confidence: {final_confidence:.1f}%")
    
    # Create results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_version': 'v6.1-updated-base-4.3',
        'forecast_method': 'Conservative Reform with 4.3% Base Rate',
        'base_rate': {
            'rate': base_forecast,
            'source': 'Last Published Unemployment Rate',
            'confidence': base_confidence
        },
        'system_configuration': {
            'weights': weights,
            'scale_factor': scale_factor,
            'approach': 'Balanced - 50% of raw signal, 40% trade data weight'
        },
        'trade_data_analysis': {
            'unrate_sentiment': unrate_sentiment,
            'claims_sentiment': claims_sentiment,
            'combined_sentiment': combined_sentiment,
            'total_volume': total_volume,
            'relevant_pairs': len([p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]) + 
                             len([p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000])
        },
        'adjustments': {
            'trade_data': trade_adjustment,
            'core_labor': core_adjustment,
            'leading_indicators': leading_adjustment,
            'total': total_adjustment
        },
        'final_forecast': {
            'rate': round(final_forecast, 2),
            'confidence': round(final_confidence, 1),
            'total_adjustment': round(total_adjustment, 3),
            'target_period': 'Next unemployment release'
        }
    }
    
    # Save results
    with open('updated_forecast_4_3_base.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: updated_forecast_4_3_base.json")
    
    return results

if __name__ == "__main__":
    results = calculate_updated_forecast_with_4_3_base()
    if results:
        print(f"\nUpdated forecast with 4.3% base completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Target Period: {results['final_forecast']['target_period']}")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
        print(f"System Version: {results['system_version']}")
    else:
        print(f"\nForecast failed - no data available")