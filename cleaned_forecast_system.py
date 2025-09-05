#!/usr/bin/env python3
"""
Cleaned Forecast System
Streamlined to 8 essential components, removing redundancies
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

def calculate_core_labor_market_adjustments(historical_data):
    """Calculate core labor market adjustments (3 components)"""
    print("CORE LABOR MARKET ADJUSTMENTS")
    print("-" * 30)
    
    if not historical_data:
        return {}
    
    adjustments = {}
    
    # 1. Labor Force Participation Rate (35% weight)
    lfpr_data = historical_data['historical_data'].get('CIVPART', {}).get('data', [])
    if lfpr_data:
        latest_lfpr = float(lfpr_data[-1]['value'])
        # Calculate 12-month trend
        if len(lfpr_data) >= 12:
            recent_avg = sum(float(d['value']) for d in lfpr_data[-12:]) / 12
            older_avg = sum(float(d['value']) for d in lfpr_data[-24:-12]) / 12
            lfpr_trend = recent_avg - older_avg
        else:
            lfpr_trend = 0
        
        # LFPR adjustment: rising LFPR = downward pressure on unemployment
        lfpr_adjustment = -lfpr_trend * 0.35 * 0.1
        adjustments['lfpr'] = {
            'value': latest_lfpr,
            'trend': lfpr_trend,
            'adjustment': lfpr_adjustment,
            'weight': 0.35
        }
        print(f"  LFPR: {latest_lfpr:.1f}% (trend: {lfpr_trend:+.2f}pp, adj: {lfpr_adjustment:+.3f}pp)")
    
    # 2. Initial Claims (25% weight)
    icsa_data = historical_data['historical_data'].get('ICSA', {}).get('data', [])
    if icsa_data:
        latest_claims = int(icsa_data[-1]['value'])
        # Calculate 4-week average trend
        if len(icsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in icsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in icsa_data[-8:-4]) / 4
            claims_trend = (recent_avg - older_avg) / older_avg
        else:
            claims_trend = 0
        
        # Claims adjustment: rising claims = upward pressure on unemployment
        claims_adjustment = claims_trend * 0.25 * 0.1
        adjustments['initial_claims'] = {
            'value': latest_claims,
            'trend': claims_trend,
            'adjustment': claims_adjustment,
            'weight': 0.25
        }
        print(f"  Initial Claims: {latest_claims:,} (trend: {claims_trend:+.1%}, adj: {claims_adjustment:+.3f}pp)")
    
    # 3. Continuing Claims (10% weight)
    ccsa_data = historical_data['historical_data'].get('CCSA', {}).get('data', [])
    if ccsa_data:
        latest_continuing = int(ccsa_data[-1]['value'])
        # Calculate 4-week average trend
        if len(ccsa_data) >= 8:
            recent_avg = sum(int(d['value']) for d in ccsa_data[-4:]) / 4
            older_avg = sum(int(d['value']) for d in ccsa_data[-8:-4]) / 4
            continuing_trend = (recent_avg - older_avg) / older_avg
        else:
            continuing_trend = 0
        
        # Continuing claims adjustment
        continuing_adjustment = continuing_trend * 0.10 * 0.1
        adjustments['continuing_claims'] = {
            'value': latest_continuing,
            'trend': continuing_trend,
            'adjustment': continuing_adjustment,
            'weight': 0.10
        }
        print(f"  Continuing Claims: {latest_continuing:,} (trend: {continuing_trend:+.1%}, adj: {continuing_adjustment:+.3f}pp)")
    
    return adjustments

def calculate_trade_data_adjustments():
    """Calculate trade data adjustments (3 components)"""
    print("\nTRADE DATA ADJUSTMENTS")
    print("-" * 25)
    
    adjustments = {}
    
    # 1. Unemployment Trade Sentiment (15% weight)
    unrate_pairs = []
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_rate = parse_unemployment_contract(row['event_contract'])
                    if target_rate and 4.0 <= target_rate <= 4.5:  # Focus on relevant rates
                        unrate_pairs.append({
                            'target_rate': target_rate,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity'])
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Rate Pair Data.csv not found")
    
    if unrate_pairs:
        total_quantity = sum(p['quantity'] for p in unrate_pairs)
        weighted_yes = sum(p['yes_price'] * p['quantity'] for p in unrate_pairs) / total_quantity
        weighted_no = sum(p['no_price'] * p['quantity'] for p in unrate_pairs) / total_quantity
        
        # Sentiment: higher yes_price = bullish for unemployment
        sentiment = weighted_yes - 0.5
        adjustment = sentiment * 0.15 * 0.1
        
        adjustments['unemployment_trade_sentiment'] = {
            'sentiment': sentiment,
            'weighted_yes': weighted_yes,
            'weighted_no': weighted_no,
            'adjustment': adjustment,
            'weight': 0.15,
            'volume': total_quantity
        }
        print(f"  Unemployment Trade Sentiment: {sentiment:+.3f} (adj: {adjustment:+.3f}pp)")
    
    # 2. Unemployment Trade Volume (5% weight)
    if unrate_pairs:
        total_volume = sum(p['quantity'] for p in unrate_pairs)
        # Volume-based adjustment (higher volume = more confidence)
        volume_adjustment = min(total_volume / 10000, 1.0) * 0.05 * 0.05
        
        adjustments['unemployment_trade_volume'] = {
            'volume': total_volume,
            'adjustment': volume_adjustment,
            'weight': 0.05
        }
        print(f"  Unemployment Trade Volume: {total_volume:,} (adj: {volume_adjustment:+.3f}pp)")
    
    # 3. Claims Trade Sentiment (5% weight)
    claims_pairs = []
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    target_value = parse_initial_claims_contract(row['event_contract'])
                    if target_value and 220000 <= target_value <= 250000:  # Focus on relevant values
                        claims_pairs.append({
                            'target_value': target_value,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity'])
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Pairs not found")
    
    if claims_pairs:
        total_quantity = sum(p['quantity'] for p in claims_pairs)
        weighted_yes = sum(p['yes_price'] * p['quantity'] for p in claims_pairs) / total_quantity
        weighted_no = sum(p['no_price'] * p['quantity'] for p in claims_pairs) / total_quantity
        
        # Sentiment: higher yes_price = bullish for higher claims
        sentiment = weighted_yes - 0.5
        adjustment = sentiment * 0.05 * 0.1
        
        adjustments['claims_trade_sentiment'] = {
            'sentiment': sentiment,
            'weighted_yes': weighted_yes,
            'weighted_no': weighted_no,
            'adjustment': adjustment,
            'weight': 0.05,
            'volume': total_quantity
        }
        print(f"  Claims Trade Sentiment: {sentiment:+.3f} (adj: {adjustment:+.3f}pp)")
    
    return adjustments

def calculate_leading_indicators_adjustments(historical_data):
    """Calculate leading indicators adjustments (2 components)"""
    print("\nLEADING INDICATORS ADJUSTMENTS")
    print("-" * 30)
    
    if not historical_data:
        return {}
    
    adjustments = {}
    
    # 1. JOLTS Data (3% weight)
    jolts_data = historical_data['historical_data'].get('JTSJOL', {}).get('data', [])
    if jolts_data:
        latest_jolts = int(jolts_data[-1]['value'])
        # Calculate 6-month trend
        if len(jolts_data) >= 6:
            recent_avg = sum(int(d['value']) for d in jolts_data[-6:]) / 6
            older_avg = sum(int(d['value']) for d in jolts_data[-12:-6]) / 6
            jolts_trend = (recent_avg - older_avg) / older_avg
        else:
            jolts_trend = 0
        
        # JOLTS adjustment: more openings = downward pressure on unemployment
        jolts_adjustment = -jolts_trend * 0.03 * 0.1
        adjustments['jolts_data'] = {
            'value': latest_jolts,
            'trend': jolts_trend,
            'adjustment': jolts_adjustment,
            'weight': 0.03
        }
        print(f"  JOLTS: {latest_jolts:,} (trend: {jolts_trend:+.1%}, adj: {jolts_adjustment:+.3f}pp)")
    
    # 2. Business Cycle Indicators - GDP (2% weight)
    gdp_data = historical_data['historical_data'].get('GDP', {}).get('data', [])
    if gdp_data:
        latest_gdp = float(gdp_data[-1]['value'])
        # Calculate growth rate
        if len(gdp_data) >= 2:
            gdp_growth = (latest_gdp - float(gdp_data[-2]['value'])) / float(gdp_data[-2]['value'])
        else:
            gdp_growth = 0
        
        # GDP adjustment: higher growth = downward pressure on unemployment
        gdp_adjustment = -gdp_growth * 0.02 * 0.1
        adjustments['business_cycle_indicators'] = {
            'value': latest_gdp,
            'growth': gdp_growth,
            'adjustment': gdp_adjustment,
            'weight': 0.02
        }
        print(f"  GDP Growth: {gdp_growth:+.1%} (adj: {gdp_adjustment:+.3f}pp)")
    
    return adjustments

def calculate_cleaned_forecast():
    """Calculate cleaned forecast using 8 essential components"""
    print("CLEANED FORECAST SYSTEM")
    print("=" * 40)
    print("8 Essential Components (down from 15)")
    print()
    
    # Load baseline
    fred_baseline = load_fred_baseline()
    if not fred_baseline:
        return None
    
    historical_data = load_historical_data()
    if not historical_data:
        return None
    
    print(f"FRED Baseline: {fred_baseline['forecast']}%")
    print()
    
    # Calculate all adjustments
    core_adjustments = calculate_core_labor_market_adjustments(historical_data)
    trade_adjustments = calculate_trade_data_adjustments()
    leading_adjustments = calculate_leading_indicators_adjustments(historical_data)
    
    # Combine all adjustments
    all_adjustments = {**core_adjustments, **trade_adjustments, **leading_adjustments}
    
    # Calculate total adjustment
    total_adjustment = sum(adj['adjustment'] for adj in all_adjustments.values())
    final_forecast = fred_baseline['forecast'] + total_adjustment
    
    # Calculate confidence
    base_confidence = fred_baseline['confidence']
    
    # Add confidence boosts
    confidence_boosts = []
    
    # Trade volume confidence boost
    if 'unemployment_trade_volume' in trade_adjustments:
        volume_boost = min(trade_adjustments['unemployment_trade_volume']['volume'] / 10000, 5)
        confidence_boosts.append(volume_boost)
    
    # Leading indicators confidence boost
    confidence_boosts.append(3.0)  # JOLTS + Business Cycle
    
    total_confidence_boost = sum(confidence_boosts)
    final_confidence = min(base_confidence + total_confidence_boost, 95)  # Cap at 95%
    
    print(f"\nFINAL FORECAST CALCULATION")
    print("-" * 30)
    print(f"FRED Base: {fred_baseline['forecast']}%")
    print(f"Total Adjustment: {total_adjustment:+.3f}pp")
    print(f"Final Forecast: {final_forecast:.2f}%")
    print()
    print(f"Base Confidence: {base_confidence}%")
    print(f"Confidence Boosts: +{total_confidence_boost:.1f}%")
    print(f"Final Confidence: {final_confidence:.1f}%")
    
    # Component summary
    print(f"\nCOMPONENT SUMMARY")
    print("-" * 20)
    print("Core Labor Market (70%):")
    for comp in ['lfpr', 'initial_claims', 'continuing_claims']:
        if comp in core_adjustments:
            adj = core_adjustments[comp]
            print(f"  {comp}: {adj['weight']*100:.0f}% weight, {adj['adjustment']:+.3f}pp")
    
    print("Trade Data (25%):")
    for comp in ['unemployment_trade_sentiment', 'unemployment_trade_volume', 'claims_trade_sentiment']:
        if comp in trade_adjustments:
            adj = trade_adjustments[comp]
            print(f"  {comp}: {adj['weight']*100:.0f}% weight, {adj['adjustment']:+.3f}pp")
    
    print("Leading Indicators (5%):")
    for comp in ['jolts_data', 'business_cycle_indicators']:
        if comp in leading_adjustments:
            adj = leading_adjustments[comp]
            print(f"  {comp}: {adj['weight']*100:.0f}% weight, {adj['adjustment']:+.3f}pp")
    
    # Create results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_version': 'v5.0-cleaned-8-components',
        'forecast_method': 'Cleaned 8-Component System',
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
        'component_summary': {
            'total_components': 8,
            'core_labor_market': 3,
            'trade_data': 3,
            'leading_indicators': 2,
            'redundancy_removed': 7
        }
    }
    
    # Save results
    with open('cleaned_forecast_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: cleaned_forecast_results.json")
    
    return results

if __name__ == "__main__":
    results = calculate_cleaned_forecast()
    if results:
        print(f"\nCleaned forecast completed successfully!")
        print(f"Final Forecast: {results['final_forecast']['rate']}%")
        print(f"Final Confidence: {results['final_forecast']['confidence']}%")
        print(f"Components: {results['component_summary']['total_components']} (down from 15)")
    else:
        print(f"\nForecast failed - no data available")