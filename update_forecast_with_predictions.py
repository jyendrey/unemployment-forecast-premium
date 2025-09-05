#!/usr/bin/env python3
"""
Update Forecast with Real Trade Predictions Data
Use actual market expectations to adjust the forecast
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

def analyze_trade_predictions():
    """Analyze the provided trade predictions data"""
    print("ANALYZING TRADE PREDICTIONS DATA")
    print("-" * 35)
    
    # Trade predictions data from user
    predictions_data = [
        {"contract": "Above 2.7%", "yes": 97, "no": 0, "oi": 0},
        {"contract": "Above 2.9%", "yes": 97, "no": 0, "oi": 120},
        {"contract": "Above 3.1%", "yes": 97, "no": 0, "oi": 120},
        {"contract": "Above 3.3%", "yes": 97, "no": 0, "oi": 150},
        {"contract": "Above 3.5%", "yes": 97, "no": 0, "oi": 200},
        {"contract": "Above 3.7%", "yes": 97, "no": 0, "oi": 349},
        {"contract": "Above 3.8%", "yes": 97, "no": 0, "oi": 450},
        {"contract": "Above 3.9%", "yes": 97, "no": 0, "oi": 470},
        {"contract": "Above 4.0%", "yes": 97, "no": 0, "oi": 450},
        {"contract": "Above 4.1%", "yes": 94, "no": 6, "oi": 430},
        {"contract": "Above 4.2%", "yes": 64, "no": 0, "oi": 180},
        {"contract": "Above 4.3%", "yes": 32, "no": 66, "oi": 70},
        {"contract": "Above 4.5%", "yes": 5, "no": 93, "oi": 170},
        {"contract": "Above 4.7%", "yes": 0, "no": 97, "oi": 0}
    ]
    
    # Extract rates and calculate sentiment
    rates = []
    sentiments = []
    volumes = []
    
    for pred in predictions_data:
        # Extract rate from contract name
        rate_str = pred["contract"].replace("Above ", "").replace("%", "")
        try:
            rate = float(rate_str)
            rates.append(rate)
            
            # Calculate sentiment (yes percentage - 50%)
            yes_pct = pred["yes"] / 100.0
            sentiment = yes_pct - 0.5
            sentiments.append(sentiment)
            
            # Volume (open interest)
            volume = pred["oi"]
            volumes.append(volume)
            
            print(f"  {pred['contract']}: {pred['yes']}% Yes, {pred['no']}% No, OI: {volume}")
            
        except ValueError:
            continue
    
    # Focus on rates around current levels (4.0% - 4.5%)
    relevant_indices = [i for i, rate in enumerate(rates) if 4.0 <= rate <= 4.5]
    
    if relevant_indices:
        relevant_sentiments = [sentiments[i] for i in relevant_indices]
        relevant_volumes = [volumes[i] for i in relevant_indices]
        relevant_rates = [rates[i] for i in relevant_indices]
        
        # Calculate volume-weighted sentiment
        total_volume = sum(relevant_volumes)
        if total_volume > 0:
            weighted_sentiment = sum(s * v for s, v in zip(relevant_sentiments, relevant_volumes)) / total_volume
        else:
            weighted_sentiment = sum(relevant_sentiments) / len(relevant_sentiments)
        
        print(f"\nRelevant Rates (4.0% - 4.5%): {len(relevant_indices)} contracts")
        print(f"Volume-Weighted Sentiment: {weighted_sentiment:+.3f}")
        print(f"Total Volume: {total_volume:,}")
        
        # Analyze market expectations
        print(f"\nMARKET EXPECTATIONS ANALYSIS")
        print("-" * 30)
        
        # Find the rate where sentiment crosses from positive to negative
        for i, rate in enumerate(relevant_rates):
            if i < len(relevant_sentiments) - 1:
                if relevant_sentiments[i] > 0 and relevant_sentiments[i+1] < 0:
                    print(f"Sentiment crossover around {rate}% - {relevant_rates[i+1]}%")
                    break
        
        # Calculate probability-weighted expected rate
        probabilities = []
        for i, rate in enumerate(relevant_rates):
            if i < len(relevant_sentiments):
                # Convert sentiment to probability
                prob = 0.5 + relevant_sentiments[i]
                probabilities.append(prob)
        
        if probabilities:
            # Weight by volume
            if total_volume > 0:
                weighted_expected = sum(r * p * v for r, p, v in zip(relevant_rates, probabilities, relevant_volumes)) / total_volume
            else:
                weighted_expected = sum(r * p for r, p in zip(relevant_rates, probabilities)) / len(probabilities)
            
            print(f"Volume-Weighted Expected Rate: {weighted_expected:.2f}%")
        
        return {
            'weighted_sentiment': weighted_sentiment,
            'total_volume': total_volume,
            'relevant_contracts': len(relevant_indices),
            'weighted_expected_rate': weighted_expected if 'weighted_expected' in locals() else None
        }
    
    return None

def calculate_updated_forecast_with_predictions():
    """Calculate forecast using trade predictions data"""
    print("UPDATED FORECAST WITH TRADE PREDICTIONS")
    print("=" * 50)
    print("Using real market expectations to adjust forecast")
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
    
    # Base rate
    base_forecast = 4.3  # Last published unemployment rate
    print(f"Base Rate (Last Published): {base_forecast}%")
    print()
    
    # Analyze trade predictions
    predictions_analysis = analyze_trade_predictions()
    
    if not predictions_analysis:
        print("Error: Could not analyze trade predictions")
        return None
    
    # Conservative Reform weights and scale factor
    weights = {
        'core_labor': 0.50,      # 50% - Core labor market fundamentals
        'trade_data': 0.40,      # 40% - Trade data and market sentiment
        'leading_indicators': 0.10  # 10% - Leading economic indicators
    }
    scale_factor = 0.5  # 50% of raw signal
    
    print(f"\nSYSTEM CONFIGURATION")
    print("-" * 20)
    print(f"Core Labor Market Weight: {weights['core_labor']*100:.0f}%")
    print(f"Trade Data Weight: {weights['trade_data']*100:.0f}%")
    print(f"Leading Indicators Weight: {weights['leading_indicators']*100:.0f}%")
    print(f"Scale Factor: {scale_factor}x (50% of raw signal)")
    print()
    
    # Calculate trade sentiment from predictions
    trade_sentiment = predictions_analysis['weighted_sentiment']
    trade_volume = predictions_analysis['total_volume']
    
    print("TRADE PREDICTIONS ANALYSIS")
    print("-" * 30)
    print(f"Market Sentiment: {trade_sentiment:+.3f}")
    print(f"Total Volume: {trade_volume:,}")
    print(f"Relevant Contracts: {predictions_analysis['relevant_contracts']}")
    if predictions_analysis['weighted_expected_rate']:
        print(f"Expected Rate: {predictions_analysis['weighted_expected_rate']:.2f}%")
    print()
    
    # Calculate adjustments
    print("FORECAST ADJUSTMENTS")
    print("-" * 20)
    
    # Trade data adjustment
    trade_adjustment = trade_sentiment * weights['trade_data'] * scale_factor
    print(f"Trade Predictions Adjustment: {trade_adjustment:+.3f}pp")
    print(f"  Calculation: {trade_sentiment:+.3f} × {weights['trade_data']} × {scale_factor} = {trade_adjustment:+.3f}pp")
    
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
    print(f"Trade Predictions Adjustment: {trade_adjustment:+.3f}pp")
    print(f"Core Labor Adjustment: {core_adjustment:+.3f}pp")
    print(f"Leading Indicators Adjustment: {leading_adjustment:+.3f}pp")
    print(f"Total Adjustment: {total_adjustment:+.3f}pp")
    print(f"Final Forecast: {final_forecast:.2f}%")
    
    # Calculate confidence
    base_confidence = 85  # Base confidence for published rate
    trade_confidence_boost = min(trade_volume / 1000, 15)  # Volume-based boost
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
        'system_version': 'v6.2-trade-predictions-integration',
        'forecast_method': 'Conservative Reform with Trade Predictions',
        'base_rate': {
            'rate': base_forecast,
            'source': 'Last Published Unemployment Rate',
            'confidence': base_confidence
        },
        'trade_predictions_analysis': {
            'weighted_sentiment': trade_sentiment,
            'total_volume': trade_volume,
            'relevant_contracts': predictions_analysis['relevant_contracts'],
            'expected_rate': predictions_analysis['weighted_expected_rate']
        },
        'system_configuration': {
            'weights': weights,
            'scale_factor': scale_factor,
            'approach': 'Balanced - 50% of raw signal, 40% trade data weight'
        },
        'adjustments': {
            'trade_predictions': trade_adjustment,
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
    with open('forecast_with_trade_predictions.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: forecast_with_trade_predictions.json")
    
    return results

if __name__ == "__main__":
    results = calculate_updated_forecast_with_predictions()
    if results:
        print(f"\nForecast with trade predictions completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Target Period: {results['final_forecast']['target_period']}")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
        print(f"System Version: {results['system_version']}")
    else:
        print(f"\nForecast failed - no data available")