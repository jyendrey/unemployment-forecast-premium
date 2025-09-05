#!/usr/bin/env python3
"""
Comprehensive Forecast: FRED August 2024 Base + Trade Data Aug 2024-Aug 2025
Combines historical FRED data with trade market sentiment
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
        print("Error: aug2024_forecast.json not found. Run fred_based_forecast_aug2024.py first.")
        return None

def parse_unemployment_contract(contract_str):
    """Parse unemployment rate contract to extract target rate"""
    try:
        # Format: UNR_0724_3.9 -> 3.9
        parts = contract_str.split('_')
        if len(parts) >= 3:
            return float(parts[2])
    except:
        pass
    return None

def parse_initial_claims_contract(contract_str):
    """Parse initial claims contract to extract target value"""
    try:
        # Format: IJC_080324_244000 -> 244000
        parts = contract_str.split('_')
        if len(parts) >= 3:
            return int(parts[2])
    except:
        pass
    return None

def analyze_unemployment_pairs_data():
    """Analyze unemployment rate pairs data"""
    print("Analyzing Unemployment Rate Pairs Data...")
    
    pairs_data = []
    target_rates = set()
    
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate:
                        target_rates.add(target_rate)
                        pairs_data.append({
                            'target_rate': target_rate,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity']),
                            'expiration_date': row['expiration_date'],
                            'pair_time': row['pair_time']
                        })
                except (ValueError, KeyError) as e:
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Rate Pair Data.csv not found")
        return None
    
    print(f"  Found {len(pairs_data)} pairs across {len(target_rates)} target rates")
    print(f"  Target rates: {sorted(target_rates)}")
    
    # Calculate sentiment for each target rate
    rate_sentiment = {}
    for rate in target_rates:
        rate_pairs = [p for p in pairs_data if p['target_rate'] == rate]
        if rate_pairs:
            total_quantity = sum(p['quantity'] for p in rate_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in rate_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in rate_pairs) / total_quantity
            
            rate_sentiment[rate] = {
                'weighted_yes': weighted_yes,
                'weighted_no': weighted_no,
                'total_quantity': total_quantity,
                'pair_count': len(rate_pairs)
            }
    
    return {
        'pairs_data': pairs_data,
        'target_rates': sorted(target_rates),
        'rate_sentiment': rate_sentiment
    }

def analyze_unemployment_prices_data():
    """Analyze unemployment rate prices data"""
    print("Analyzing Unemployment Rate Prices Data...")
    
    prices_data = []
    target_rates = set()
    
    try:
        with open('Unemployment Trade Prices Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate and row['subtype'] in ['YES', 'NO']:
                        target_rates.add(target_rate)
                        prices_data.append({
                            'target_rate': target_rate,
                            'subtype': row['subtype'],
                            'end_price': float(row['end_price']) if row['end_price'] else 0,
                            'settlement_price': float(row['settlement_price']) if row['settlement_price'] else 0,
                            'open_interest': int(row['open_interest']) if row['open_interest'] else 0,
                            'vwap': float(row['vwap']) if row['vwap'] else 0,
                            'expiration_date': row['expiration_date'],
                            'date': row['date']
                        })
                except (ValueError, KeyError) as e:
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Trade Prices Data.csv not found")
        return None
    
    print(f"  Found {len(prices_data)} price records across {len(target_rates)} target rates")
    
    # Calculate sentiment for each target rate
    rate_sentiment = {}
    for rate in target_rates:
        rate_prices = [p for p in prices_data if p['target_rate'] == rate]
        if rate_prices:
            yes_prices = [p for p in rate_prices if p['subtype'] == 'YES']
            no_prices = [p for p in rate_prices if p['subtype'] == 'NO']
            
            if yes_prices and no_prices:
                yes_avg = sum(p['end_price'] for p in yes_prices) / len(yes_prices)
                no_avg = sum(p['end_price'] for p in no_prices) / len(no_prices)
                total_oi = sum(p['open_interest'] for p in rate_prices)
                
                rate_sentiment[rate] = {
                    'yes_avg': yes_avg,
                    'no_avg': no_avg,
                    'total_open_interest': total_oi,
                    'record_count': len(rate_prices)
                }
    
    return {
        'prices_data': prices_data,
        'target_rates': sorted(target_rates),
        'rate_sentiment': rate_sentiment
    }

def analyze_initial_claims_pairs_data():
    """Analyze initial claims pairs data"""
    print("Analyzing Initial Claims Pairs Data...")
    
    pairs_data = []
    target_values = set()
    
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value:
                        target_values.add(target_value)
                        pairs_data.append({
                            'target_value': target_value,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity']),
                            'expiration_date': row['expiration_date'],
                            'pair_time': row['pair_time']
                        })
                except (ValueError, KeyError) as e:
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Pairs not found")
        return None
    
    print(f"  Found {len(pairs_data)} pairs across {len(target_values)} target values")
    print(f"  Target values: {sorted(target_values)}")
    
    # Calculate sentiment for each target value
    value_sentiment = {}
    for value in target_values:
        value_pairs = [p for p in pairs_data if p['target_value'] == value]
        if value_pairs:
            total_quantity = sum(p['quantity'] for p in value_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in value_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in value_pairs) / total_quantity
            
            value_sentiment[value] = {
                'weighted_yes': weighted_yes,
                'weighted_no': weighted_no,
                'total_quantity': total_quantity,
                'pair_count': len(value_pairs)
            }
    
    return {
        'pairs_data': pairs_data,
        'target_values': sorted(target_values),
        'value_sentiment': value_sentiment
    }

def analyze_initial_claims_prices_data():
    """Analyze initial claims prices data"""
    print("Analyzing Initial Claims Prices Data...")
    
    prices_data = []
    target_values = set()
    
    try:
        with open('Initial Claims Trade Data - Prices', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value and row['subtype'] in ['YES', 'NO']:
                        target_values.add(target_value)
                        prices_data.append({
                            'target_value': target_value,
                            'subtype': row['subtype'],
                            'end_price': float(row['end_price']) if row['end_price'] else 0,
                            'settlement_price': float(row['settlement_price']) if row['settlement_price'] else 0,
                            'open_interest': int(row['open_interest']) if row['open_interest'] else 0,
                            'vwap': float(row['vwap']) if row['vwap'] else 0,
                            'expiration_date': row['expiration_date'],
                            'date': row['date']
                        })
                except (ValueError, KeyError) as e:
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Prices not found")
        return None
    
    print(f"  Found {len(prices_data)} price records across {len(target_values)} target values")
    
    # Calculate sentiment for each target value
    value_sentiment = {}
    for value in target_values:
        value_prices = [p for p in prices_data if p['target_value'] == value]
        if value_prices:
            yes_prices = [p for p in value_prices if p['subtype'] == 'YES']
            no_prices = [p for p in value_prices if p['subtype'] == 'NO']
            
            if yes_prices and no_prices:
                yes_avg = sum(p['end_price'] for p in yes_prices) / len(yes_prices)
                no_avg = sum(p['end_price'] for p in no_prices) / len(no_prices)
                total_oi = sum(p['open_interest'] for p in value_prices)
                
                value_sentiment[value] = {
                    'yes_avg': yes_avg,
                    'no_avg': no_avg,
                    'total_open_interest': total_oi,
                    'record_count': len(value_prices)
                }
    
    return {
        'prices_data': prices_data,
        'target_values': sorted(target_values),
        'value_sentiment': value_sentiment
    }

def calculate_trade_sentiment_adjustment(unemployment_analysis, claims_analysis):
    """Calculate forecast adjustment based on trade sentiment"""
    print("\nCalculating Trade Sentiment Adjustment...")
    
    # Unemployment rate sentiment
    unrate_sentiment = 0.0
    unrate_confidence = 0.0
    
    if unemployment_analysis and unemployment_analysis['rate_sentiment']:
        # Focus on rates around current levels (3.8% - 4.5%)
        relevant_rates = [r for r in unemployment_analysis['target_rates'] if 3.8 <= r <= 4.5]
        
        if relevant_rates:
            total_weight = 0
            weighted_sentiment = 0
            
            for rate in relevant_rates:
                sentiment = unemployment_analysis['rate_sentiment'][rate]
                weight = sentiment['total_quantity']
                
                # Calculate sentiment score (higher yes_price = bullish for unemployment)
                sentiment_score = sentiment['weighted_yes'] - 0.5
                weighted_sentiment += sentiment_score * weight
                total_weight += weight
            
            if total_weight > 0:
                unrate_sentiment = weighted_sentiment / total_weight
                unrate_confidence = min(total_weight / 1000, 1.0)  # Scale confidence by volume
        
        print(f"  Unemployment Rate Sentiment: {unrate_sentiment:.3f}")
        print(f"  Unemployment Rate Confidence: {unrate_confidence:.3f}")
    
    # Initial claims sentiment
    claims_sentiment = 0.0
    claims_confidence = 0.0
    
    if claims_analysis and claims_analysis['value_sentiment']:
        # Focus on values around current levels (220k - 250k)
        relevant_values = [v for v in claims_analysis['target_values'] if 220000 <= v <= 250000]
        
        if relevant_values:
            total_weight = 0
            weighted_sentiment = 0
            
            for value in relevant_values:
                sentiment = claims_analysis['value_sentiment'][value]
                weight = sentiment['total_quantity']
                
                # Calculate sentiment score (higher yes_price = bullish for higher claims)
                sentiment_score = sentiment['weighted_yes'] - 0.5
                weighted_sentiment += sentiment_score * weight
                total_weight += weight
            
            if total_weight > 0:
                claims_sentiment = weighted_sentiment / total_weight
                claims_confidence = min(total_weight / 1000, 1.0)  # Scale confidence by volume
        
        print(f"  Initial Claims Sentiment: {claims_sentiment:.3f}")
        print(f"  Initial Claims Confidence: {claims_confidence:.3f}")
    
    # Combine sentiments
    total_confidence = (unrate_confidence + claims_confidence) / 2
    combined_sentiment = (unrate_sentiment + claims_sentiment) / 2
    
    # Convert sentiment to forecast adjustment
    # Positive sentiment = market expects higher unemployment = upward adjustment
    # Negative sentiment = market expects lower unemployment = downward adjustment
    sentiment_adjustment = combined_sentiment * 0.1  # Scale factor
    
    print(f"  Combined Sentiment: {combined_sentiment:.3f}")
    print(f"  Total Confidence: {total_confidence:.3f}")
    print(f"  Sentiment Adjustment: {sentiment_adjustment:+.3f}pp")
    
    return {
        'sentiment_adjustment': sentiment_adjustment,
        'confidence_boost': total_confidence * 10,  # Convert to percentage
        'unrate_sentiment': unrate_sentiment,
        'claims_sentiment': claims_sentiment,
        'combined_sentiment': combined_sentiment
    }

def create_comprehensive_forecast():
    """Create comprehensive forecast combining FRED baseline with trade data"""
    print("COMPREHENSIVE FORECAST: FRED + TRADE DATA")
    print("=" * 60)
    
    # Load FRED baseline
    fred_baseline = load_fred_baseline()
    if not fred_baseline:
        return None
    
    print(f"FRED Baseline (August 2024): {fred_baseline['forecast']}%")
    print(f"FRED Confidence: {fred_baseline['confidence']}%")
    print()
    
    # Analyze trade data
    print("TRADE DATA ANALYSIS")
    print("-" * 30)
    
    unemployment_pairs = analyze_unemployment_pairs_data()
    unemployment_prices = analyze_unemployment_prices_data()
    claims_pairs = analyze_initial_claims_pairs_data()
    claims_prices = analyze_initial_claims_prices_data()
    
    # Calculate trade sentiment adjustment
    trade_adjustment = calculate_trade_sentiment_adjustment(
        unemployment_pairs or unemployment_prices,
        claims_pairs or claims_prices
    )
    
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
    print(f"FRED Base Forecast: {base_forecast}%")
    print(f"Trade Sentiment Adjustment: {sentiment_adj:+.3f}pp")
    print(f"Final Forecast: {final_forecast:.2f}%")
    print()
    print(f"FRED Base Confidence: {base_confidence}%")
    print(f"Trade Confidence Boost: +{trade_confidence_boost:.1f}%")
    print(f"Final Confidence: {final_confidence:.1f}%")
    
    # Create comprehensive results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'forecast_method': 'FRED Baseline + Trade Data Integration',
        'fred_baseline': {
            'forecast': base_forecast,
            'confidence': base_confidence,
            'data_sources': fred_baseline['data_sources']
        },
        'trade_data_analysis': {
            'unemployment_pairs': len(unemployment_pairs['pairs_data']) if unemployment_pairs else 0,
            'unemployment_prices': len(unemployment_prices['prices_data']) if unemployment_prices else 0,
            'claims_pairs': len(claims_pairs['pairs_data']) if claims_pairs else 0,
            'claims_prices': len(claims_prices['prices_data']) if claims_prices else 0,
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
            'total_adjustment': round(sentiment_adj, 3)
        }
    }
    
    # Save results
    with open('comprehensive_forecast_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: comprehensive_forecast_results.json")
    
    return results

if __name__ == "__main__":
    results = create_comprehensive_forecast()
    if results:
        print(f"\nComprehensive forecast completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
    else:
        print(f"\nForecast failed - no data available")