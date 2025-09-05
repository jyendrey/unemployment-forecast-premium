#!/usr/bin/env python3
"""
Comprehensive Enhanced Forecast: ALL Components Integration
Uses the complete enhanced system with all 17+ factors
"""

import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

def load_system_config():
    """Load the enhanced system configuration"""
    try:
        with open('enhanced_system_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: enhanced_system_config.json not found")
        return None

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

def analyze_comprehensive_trade_data():
    """Analyze all trade data components"""
    print("Analyzing Comprehensive Trade Data...")
    
    # 1. Unemployment Rate Pairs Data
    unrate_pairs = []
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate:
                        unrate_pairs.append({
                            'target_rate': target_rate,
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
    
    # 2. Unemployment Rate Prices Data
    unrate_prices = []
    try:
        with open('Unemployment Trade Prices Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate and row['subtype'] in ['YES', 'NO']:
                        unrate_prices.append({
                            'target_rate': target_rate,
                            'subtype': row['subtype'],
                            'end_price': float(row['end_price']) if row['end_price'] else 0,
                            'settlement_price': float(row['settlement_price']) if row['settlement_price'] else 0,
                            'open_interest': int(row['open_interest']) if row['open_interest'] else 0,
                            'vwap': float(row['vwap']) if row['vwap'] else 0,
                            'expiration_date': row['expiration_date'],
                            'date': row['date']
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Trade Prices Data.csv not found")
    
    # 3. Initial Claims Pairs Data
    claims_pairs = []
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value:
                        claims_pairs.append({
                            'target_value': target_value,
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
    
    # 4. Initial Claims Prices Data
    claims_prices = []
    try:
        with open('Initial Claims Trade Data - Prices', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value and row['subtype'] in ['YES', 'NO']:
                        claims_prices.append({
                            'target_value': target_value,
                            'subtype': row['subtype'],
                            'end_price': float(row['end_price']) if row['end_price'] else 0,
                            'settlement_price': float(row['settlement_price']) if row['settlement_price'] else 0,
                            'open_interest': int(row['open_interest']) if row['open_interest'] else 0,
                            'vwap': float(row['vwap']) if row['vwap'] else 0,
                            'expiration_date': row['expiration_date'],
                            'date': row['date']
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Prices not found")
    
    print(f"  Unemployment Rate Pairs: {len(unrate_pairs)}")
    print(f"  Unemployment Rate Prices: {len(unrate_prices)}")
    print(f"  Initial Claims Pairs: {len(claims_pairs)}")
    print(f"  Initial Claims Prices: {len(claims_prices)}")
    
    return {
        'unrate_pairs': unrate_pairs,
        'unrate_prices': unrate_prices,
        'claims_pairs': claims_pairs,
        'claims_prices': claims_prices
    }

def calculate_core_labor_market_adjustments(historical_data, config):
    """Calculate core labor market adjustments"""
    print("Calculating Core Labor Market Adjustments...")
    
    if not historical_data:
        return {}
    
    adjustments = {}
    
    # Labor Force Participation Rate (LFPR)
    lfpr_data = historical_data['historical_data'].get('CIVPART', {}).get('data', [])
    if lfpr_data:
        latest_lfpr = float(lfpr_data[-1]['value'])
        # Calculate trend
        if len(lfpr_data) >= 12:
            recent_avg = sum(float(d['value']) for d in lfpr_data[-12:]) / 12
            older_avg = sum(float(d['value']) for d in lfpr_data[-24:-12]) / 12
            lfpr_trend = recent_avg - older_avg
        else:
            lfpr_trend = 0
        
        # LFPR adjustment: rising LFPR = downward pressure on unemployment
        lfpr_weight = config['adjustment_weights']['lfpr']
        lfpr_adjustment = -lfpr_trend * lfpr_weight * 0.1
        adjustments['lfpr'] = {
            'value': latest_lfpr,
            'trend': lfpr_trend,
            'adjustment': lfpr_adjustment,
            'weight': lfpr_weight
        }
        print(f"  LFPR: {latest_lfpr:.1f}% (trend: {lfpr_trend:+.2f}pp, adj: {lfpr_adjustment:+.3f}pp)")
    
    # Initial Claims
    icsa_data = historical_data['historical_data'].get('ICSA', {}).get('data', [])
    if icsa_data:
        latest_claims = int(icsa_data[-1]['value'])
        # Calculate 4-week average
        if len(icsa_data) >= 4:
            recent_avg = sum(int(d['value']) for d in icsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in icsa_data[-8:-4]) / 4
            claims_trend = (recent_avg - older_avg) / older_avg
        else:
            claims_trend = 0
        
        # Claims adjustment: rising claims = upward pressure on unemployment
        claims_weight = config['adjustment_weights']['initial_claims']
        claims_adjustment = claims_trend * claims_weight * 0.1
        adjustments['initial_claims'] = {
            'value': latest_claims,
            'trend': claims_trend,
            'adjustment': claims_adjustment,
            'weight': claims_weight
        }
        print(f"  Initial Claims: {latest_claims:,} (trend: {claims_trend:+.1%}, adj: {claims_adjustment:+.3f}pp)")
    
    # Continuing Claims
    ccsa_data = historical_data['historical_data'].get('CCSA', {}).get('data', [])
    if ccsa_data:
        latest_continuing = int(ccsa_data[-1]['value'])
        # Calculate trend
        if len(ccsa_data) >= 4:
            recent_avg = sum(int(d['value']) for d in ccsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in ccsa_data[-8:-4]) / 4
            continuing_trend = (recent_avg - older_avg) / older_avg
        else:
            continuing_trend = 0
        
        # Continuing claims adjustment
        continuing_weight = config['adjustment_weights']['continuing_claims']
        continuing_adjustment = continuing_trend * continuing_weight * 0.1
        adjustments['continuing_claims'] = {
            'value': latest_continuing,
            'trend': continuing_trend,
            'adjustment': continuing_adjustment,
            'weight': continuing_weight
        }
        print(f"  Continuing Claims: {latest_continuing:,} (trend: {continuing_trend:+.1%}, adj: {continuing_adjustment:+.3f}pp)")
    
    return adjustments

def calculate_trade_data_adjustments(trade_data, config):
    """Calculate trade data adjustments"""
    print("Calculating Trade Data Adjustments...")
    
    adjustments = {}
    
    # Unemployment Rate Trade Sentiment
    if trade_data['unrate_pairs']:
        # Focus on rates around 4.0-4.5%
        relevant_pairs = [p for p in trade_data['unrate_pairs'] if 4.0 <= p['target_rate'] <= 4.5]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            
            # Sentiment: higher yes_price = bullish for unemployment
            sentiment = weighted_yes - 0.5
            weight = config['adjustment_weights']['trade_sentiment']
            adjustment = sentiment * weight * 0.1
            
            adjustments['trade_sentiment'] = {
                'sentiment': sentiment,
                'weighted_yes': weighted_yes,
                'weighted_no': weighted_no,
                'adjustment': adjustment,
                'weight': weight,
                'volume': total_quantity
            }
            print(f"  Trade Sentiment: {sentiment:+.3f} (adj: {adjustment:+.3f}pp)")
    
    # Trade Volume
    if trade_data['unrate_pairs']:
        total_volume = sum(p['quantity'] for p in trade_data['unrate_pairs'])
        volume_weight = config['adjustment_weights']['trade_volume']
        # Volume-based adjustment (higher volume = more confidence)
        volume_adjustment = min(total_volume / 10000, 1.0) * volume_weight * 0.05
        
        adjustments['trade_volume'] = {
            'volume': total_volume,
            'adjustment': volume_adjustment,
            'weight': volume_weight
        }
        print(f"  Trade Volume: {total_volume:,} (adj: {volume_adjustment:+.3f}pp)")
    
    # Initial Claims Trade Sentiment
    if trade_data['claims_pairs']:
        # Focus on values around 220k-250k
        relevant_pairs = [p for p in trade_data['claims_pairs'] if 220000 <= p['target_value'] <= 250000]
        if relevant_pairs:
            total_quantity = sum(p['quantity'] for p in relevant_pairs)
            weighted_yes = sum(p['yes_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            weighted_no = sum(p['no_price'] * p['quantity'] for p in relevant_pairs) / total_quantity
            
            # Sentiment: higher yes_price = bullish for higher claims
            sentiment = weighted_yes - 0.5
            weight = config['adjustment_weights']['initial_claims_trade_sentiment']
            adjustment = sentiment * weight * 0.1
            
            adjustments['initial_claims_trade_sentiment'] = {
                'sentiment': sentiment,
                'weighted_yes': weighted_yes,
                'weighted_no': weighted_no,
                'adjustment': adjustment,
                'weight': weight,
                'volume': total_quantity
            }
            print(f"  Claims Trade Sentiment: {sentiment:+.3f} (adj: {adjustment:+.3f}pp)")
    
    return adjustments

def calculate_leading_indicators_adjustments(historical_data, config):
    """Calculate leading indicators adjustments"""
    print("Calculating Leading Indicators Adjustments...")
    
    if not historical_data:
        return {}
    
    adjustments = {}
    
    # JOLTS Data
    jolts_data = historical_data['historical_data'].get('JTSJOL', {}).get('data', [])
    if jolts_data:
        latest_jolts = int(jolts_data[-1]['value'])
        # Calculate trend
        if len(jolts_data) >= 6:
            recent_avg = sum(int(d['value']) for d in jolts_data[-6:]) / 6
            older_avg = sum(int(d['value']) for d in jolts_data[-12:-6]) / 6
            jolts_trend = (recent_avg - older_avg) / older_avg
        else:
            jolts_trend = 0
        
        # JOLTS adjustment: more openings = downward pressure on unemployment
        jolts_weight = config['adjustment_weights']['jolts_data']
        jolts_adjustment = -jolts_trend * jolts_weight * 0.1
        adjustments['jolts_data'] = {
            'value': latest_jolts,
            'trend': jolts_trend,
            'adjustment': jolts_adjustment,
            'weight': jolts_weight
        }
        print(f"  JOLTS: {latest_jolts:,} (trend: {jolts_trend:+.1%}, adj: {jolts_adjustment:+.3f}pp)")
    
    # Business Cycle Indicators (using GDP as proxy)
    gdp_data = historical_data['historical_data'].get('GDP', {}).get('data', [])
    if gdp_data:
        latest_gdp = float(gdp_data[-1]['value'])
        # Calculate growth rate
        if len(gdp_data) >= 2:
            gdp_growth = (latest_gdp - float(gdp_data[-2]['value'])) / float(gdp_data[-2]['value'])
        else:
            gdp_growth = 0
        
        # GDP adjustment: higher growth = downward pressure on unemployment
        gdp_weight = config['adjustment_weights']['business_cycle_indicators']
        gdp_adjustment = -gdp_growth * gdp_weight * 0.1
        adjustments['business_cycle_indicators'] = {
            'value': latest_gdp,
            'growth': gdp_growth,
            'adjustment': gdp_adjustment,
            'weight': gdp_weight
        }
        print(f"  GDP Growth: {gdp_growth:+.1%} (adj: {gdp_adjustment:+.3f}pp)")
    
    return adjustments

def calculate_comprehensive_forecast():
    """Calculate comprehensive forecast using all components"""
    print("COMPREHENSIVE ENHANCED FORECAST")
    print("=" * 50)
    
    # Load system configuration
    config = load_system_config()
    if not config:
        return None
    
    # Load FRED baseline
    fred_baseline = load_fred_baseline()
    if not fred_baseline:
        return None
    
    # Load historical data
    historical_data = load_historical_data()
    if not historical_data:
        return None
    
    # Load trade data
    trade_data = analyze_comprehensive_trade_data()
    
    print(f"System Version: {config['system_version']}")
    print(f"FRED Baseline: {fred_baseline['forecast']}%")
    print()
    
    # Calculate all adjustments
    core_adjustments = calculate_core_labor_market_adjustments(historical_data, config)
    trade_adjustments = calculate_trade_data_adjustments(trade_data, config)
    leading_adjustments = calculate_leading_indicators_adjustments(historical_data, config)
    
    # Combine all adjustments
    all_adjustments = {**core_adjustments, **trade_adjustments, **leading_adjustments}
    
    # Calculate total adjustment
    total_adjustment = sum(adj['adjustment'] for adj in all_adjustments.values())
    final_forecast = fred_baseline['forecast'] + total_adjustment
    
    # Calculate confidence
    base_confidence = fred_baseline['confidence']
    
    # Add confidence boosts
    confidence_boosts = []
    
    # Trade data confidence boost
    if 'trade_volume' in trade_adjustments:
        volume_boost = min(trade_adjustments['trade_volume']['volume'] / 10000, 10)
        confidence_boosts.append(volume_boost)
    
    # Leading indicators confidence boost
    leading_boost = config['confidence_calculation']['leading_indicators_boost']['total_estimated_boost']
    if '+' in leading_boost and '-' in leading_boost:
        # Handle range like "7-11%"
        boost_range = leading_boost.replace('+', '').replace('%', '')
        boost_min, boost_max = map(float, boost_range.split('-'))
        boost_value = (boost_min + boost_max) / 2  # Use average
        confidence_boosts.append(boost_value)
    elif '+' in leading_boost:
        boost_value = float(leading_boost.replace('+', '').replace('%', ''))
        confidence_boosts.append(boost_value)
    
    # Updated trade data boost
    if 'updated_trade_data_boost' in config['confidence_calculation']:
        confidence_boosts.append(config['confidence_calculation']['updated_trade_data_boost'])
    
    total_confidence_boost = sum(confidence_boosts)
    final_confidence = min(base_confidence + total_confidence_boost, config['confidence_calculation']['max_confidence'])
    
    print(f"\nFINAL FORECAST CALCULATION")
    print("-" * 30)
    print(f"FRED Base: {fred_baseline['forecast']}%")
    print(f"Total Adjustment: {total_adjustment:+.3f}pp")
    print(f"Final Forecast: {final_forecast:.2f}%")
    print()
    print(f"Base Confidence: {base_confidence}%")
    print(f"Confidence Boosts: +{total_confidence_boost:.1f}%")
    print(f"Final Confidence: {final_confidence:.1f}%")
    
    # Create comprehensive results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_version': config['system_version'],
        'forecast_method': 'Comprehensive Enhanced System',
        'fred_baseline': {
            'forecast': fred_baseline['forecast'],
            'confidence': fred_baseline['confidence']
        },
        'adjustments': {
            'core_labor_market': core_adjustments,
            'trade_data': trade_adjustments,
            'leading_indicators': leading_adjustments,
            'total_adjustment': total_adjustment
        },
        'final_forecast': {
            'rate': round(final_forecast, 2),
            'confidence': round(final_confidence, 1),
            'total_adjustment': round(total_adjustment, 3)
        },
        'confidence_analysis': {
            'base_confidence': base_confidence,
            'confidence_boosts': confidence_boosts,
            'total_boost': total_confidence_boost,
            'final_confidence': final_confidence
        }
    }
    
    # Save results
    with open('comprehensive_enhanced_forecast_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: comprehensive_enhanced_forecast_results.json")
    
    return results

if __name__ == "__main__":
    results = calculate_comprehensive_forecast()
    if results:
        print(f"\nComprehensive enhanced forecast completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
    else:
        print(f"\nForecast failed - no data available")