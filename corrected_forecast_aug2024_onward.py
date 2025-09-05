#!/usr/bin/env python3
"""
Corrected Forecast: August 2024 Baseline + Trade Data from Aug 2024 Onward
Trade data should forecast FROM August 2024, not FOR August 2024
"""

import json
import csv
from datetime import datetime, timedelta
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
        # Format: UNR_0724_3.9 -> rate=3.9, month=07, year=24
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
        # Format: IJC_080324_244000 -> value=244000, month=08, day=03, year=24
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

def analyze_trade_data_from_aug2024():
    """Analyze trade data from August 2024 onward for forecasting"""
    print("ANALYZING TRADE DATA FROM AUGUST 2024 ONWARD")
    print("-" * 50)
    
    # Load unemployment rate pairs data
    unrate_pairs = []
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    rate, year, month = parse_unemployment_contract(row['event_contract'])
                    if rate and year and month:
                        # Only include data from August 2024 onward
                        if year > 2024 or (year == 2024 and month >= 8):
                            unrate_pairs.append({
                                'target_rate': rate,
                                'year': year,
                                'month': month,
                                'yes_price': float(row['yes_price']),
                                'no_price': float(row['no_price']),
                                'quantity': int(row['quantity']),
                                'expiration_date': row['expiration_date'],
                                'pair_time': row['pair_time']
                            })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Rate Pair Data.csv not found")
    
    # Load initial claims pairs data
    claims_pairs = []
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    value, year, month, day = parse_initial_claims_contract(row['event_contract'])
                    if value and year and month:
                        # Only include data from August 2024 onward
                        if year > 2024 or (year == 2024 and month >= 8):
                            claims_pairs.append({
                                'target_value': value,
                                'year': year,
                                'month': month,
                                'day': day,
                                'yes_price': float(row['yes_price']),
                                'no_price': float(row['no_price']),
                                'quantity': int(row['quantity']),
                                'expiration_date': row['expiration_date'],
                                'pair_time': row['pair_time']
                            })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Pairs not found")
    
    print(f"Unemployment Rate Pairs (Aug 2024+): {len(unrate_pairs)}")
    print(f"Initial Claims Pairs (Aug 2024+): {len(claims_pairs)}")
    
    # Group by month for temporal analysis
    monthly_unrate = defaultdict(list)
    monthly_claims = defaultdict(list)
    
    for pair in unrate_pairs:
        key = f"{pair['year']}-{pair['month']:02d}"
        monthly_unrate[key].append(pair)
    
    for pair in claims_pairs:
        key = f"{pair['year']}-{pair['month']:02d}"
        monthly_claims[key].append(pair)
    
    print(f"Months with unemployment data: {len(monthly_unrate)}")
    print(f"Months with claims data: {len(monthly_claims)}")
    
    return {
        'unrate_pairs': unrate_pairs,
        'claims_pairs': claims_pairs,
        'monthly_unrate': dict(monthly_unrate),
        'monthly_claims': dict(monthly_claims)
    }

def calculate_trade_sentiment_adjustment(trade_data):
    """Calculate trade sentiment adjustment for forecasting"""
    print("\nCALCULATING TRADE SENTIMENT ADJUSTMENT")
    print("-" * 40)
    
    # Unemployment rate sentiment (focus on rates around 4.0-4.5%)
    unrate_sentiment = 0.0
    unrate_confidence = 0.0
    
    if trade_data['unrate_pairs']:
        relevant_pairs = [p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            
            # Sentiment: higher yes_price = bullish for unemployment
            unrate_sentiment = weighted_yes - 0.5
            unrate_confidence = min(total_quantity / 1000, 1.0)
            
            print(f"Unemployment Rate Sentiment: {unrate_sentiment:+.3f}")
            print(f"Relevant pairs: {len(relevant_pairs)}")
            print(f"Total quantity: {total_quantity:,}")
    
    # Initial claims sentiment (focus on values around 220k-250k)
    claims_sentiment = 0.0
    claims_confidence = 0.0
    
    if trade_data['claims_pairs']:
        relevant_pairs = [p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            
            # Sentiment: higher yes_price = bullish for higher claims
            claims_sentiment = weighted_yes - 0.5
            claims_confidence = min(total_quantity / 1000, 1.0)
            
            print(f"Initial Claims Sentiment: {claims_sentiment:+.3f}")
            print(f"Relevant pairs: {len(relevant_pairs)}")
            print(f"Total quantity: {total_quantity:,}")
    
    # Combine sentiments
    combined_sentiment = (unrate_sentiment + claims_sentiment) / 2
    combined_confidence = (unrate_confidence + claims_confidence) / 2
    
    # Convert to forecast adjustment
    # Positive sentiment = market expects higher unemployment = upward adjustment
    # Negative sentiment = market expects lower unemployment = downward adjustment
    sentiment_adjustment = combined_sentiment * 0.1  # Scale factor
    
    print(f"\nCombined Sentiment: {combined_sentiment:+.3f}")
    print(f"Combined Confidence: {combined_confidence:.3f}")
    print(f"Sentiment Adjustment: {sentiment_adjustment:+.3f}pp")
    
    return {
        'sentiment_adjustment': sentiment_adjustment,
        'confidence_boost': combined_confidence * 10,  # Convert to percentage
        'unrate_sentiment': unrate_sentiment,
        'claims_sentiment': claims_sentiment,
        'combined_sentiment': combined_sentiment
    }

def create_corrected_forecast():
    """Create corrected forecast using August 2024 baseline + trade data from Aug 2024 onward"""
    print("CORRECTED FORECAST: AUG 2024 BASELINE + TRADE DATA FROM AUG 2024 ONWARD")
    print("=" * 80)
    
    # Load FRED baseline (August 2024)
    fred_baseline = load_fred_baseline()
    if not fred_baseline:
        return None
    
    print(f"FRED Baseline (August 2024): {fred_baseline['forecast']}%")
    print(f"FRED Confidence: {fred_baseline['confidence']}%")
    print()
    
    # Analyze trade data from August 2024 onward
    trade_data = analyze_trade_data_from_aug2024()
    
    # Calculate trade sentiment adjustment
    trade_adjustment = calculate_trade_sentiment_adjustment(trade_data)
    
    # Calculate final forecast
    base_forecast = fred_baseline['forecast']
    sentiment_adj = trade_adjustment['sentiment_adjustment']
    final_forecast = base_forecast + sentiment_adj
    
    # Calculate final confidence
    base_confidence = fred_baseline['confidence']
    trade_confidence_boost = trade_adjustment['confidence_boost']
    final_confidence = min(base_confidence + trade_confidence_boost, 100)
    
    print(f"\nFINAL FORECAST CALCULATION")
    print("-" * 30)
    print(f"FRED Base (Aug 2024): {base_forecast}%")
    print(f"Trade Data Adjustment (Aug 2024+): {sentiment_adj:+.3f}pp")
    print(f"Final Forecast (Sep 2024+): {final_forecast:.2f}%")
    print()
    print(f"FRED Base Confidence: {base_confidence}%")
    print(f"Trade Confidence Boost: +{trade_confidence_boost:.1f}%")
    print(f"Final Confidence: {final_confidence:.1f}%")
    
    # Create results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'forecast_method': 'August 2024 Baseline + Trade Data from Aug 2024 Onward',
        'fred_baseline': {
            'forecast': base_forecast,
            'confidence': base_confidence,
            'period': 'August 2024'
        },
        'trade_data_analysis': {
            'unemployment_pairs': len(trade_data['unrate_pairs']),
            'claims_pairs': len(trade_data['claims_pairs']),
            'months_covered': len(trade_data['monthly_unrate']),
            'unrate_sentiment': trade_adjustment['unrate_sentiment'],
            'claims_sentiment': trade_adjustment['claims_sentiment'],
            'combined_sentiment': trade_adjustment['combined_sentiment']
        },
        'forecast_adjustments': {
            'sentiment_adjustment': sentiment_adj,
            'confidence_boost': trade_confidence_boost
        },
        'final_forecast': {
            'rate': round(final_forecast, 2),
            'confidence': round(final_confidence, 1),
            'total_adjustment': round(sentiment_adj, 3),
            'target_period': 'September 2024 and beyond'
        }
    }
    
    # Save results
    with open('corrected_forecast_aug2024_onward.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: corrected_forecast_aug2024_onward.json")
    
    return results

if __name__ == "__main__":
    results = create_corrected_forecast()
    if results:
        print(f"\nCorrected forecast completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Target Period: {results['final_forecast']['target_period']}")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
    else:
        print(f"\nForecast failed - no data available")