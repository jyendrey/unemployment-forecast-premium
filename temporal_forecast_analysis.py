#!/usr/bin/env python3
"""
Temporal Forecast Analysis: August 2024 to August 2025
Shows how the forecast evolves over time using trade data
"""

import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

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

def analyze_temporal_unemployment_data():
    """Analyze unemployment rate data by time period"""
    print("Analyzing Temporal Unemployment Rate Data...")
    
    monthly_data = defaultdict(list)
    
    try:
        with open('Unemployment Rate Pair Data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    rate, year, month = parse_unemployment_contract(row['event_contract'])
                    if rate and year and month:
                        key = f"{year}-{month:02d}"
                        monthly_data[key].append({
                            'rate': rate,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity']),
                            'pair_time': row['pair_time']
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Unemployment Rate Pair Data.csv not found")
        return None
    
    # Calculate monthly sentiment
    monthly_sentiment = {}
    for month_key, data in monthly_data.items():
        if data:
            total_quantity = sum(d['quantity'] for d in data)
            weighted_yes = sum(d['yes_price'] * d['quantity'] for d in data) / total_quantity
            weighted_no = sum(d['no_price'] * d['quantity'] for d in data) / total_quantity
            
            # Focus on rates around 4.0-4.5%
            relevant_data = [d for d in data if 4.0 <= d['rate'] <= 4.5]
            if relevant_data:
                rel_total_quantity = sum(d['quantity'] for d in relevant_data)
                rel_weighted_yes = sum(d['yes_price'] * d['quantity'] for d in relevant_data) / rel_total_quantity
                sentiment = rel_weighted_yes - 0.5  # Positive = bullish for unemployment
            else:
                sentiment = weighted_yes - 0.5
            
            monthly_sentiment[month_key] = {
                'sentiment': sentiment,
                'confidence': min(total_quantity / 1000, 1.0),
                'total_quantity': total_quantity,
                'data_points': len(data)
            }
    
    return monthly_sentiment

def analyze_temporal_claims_data():
    """Analyze initial claims data by time period"""
    print("Analyzing Temporal Initial Claims Data...")
    
    monthly_data = defaultdict(list)
    
    try:
        with open('Initial Claims Trade Data - Pairs', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    value, year, month, day = parse_initial_claims_contract(row['event_contract'])
                    if value and year and month:
                        key = f"{year}-{month:02d}"
                        monthly_data[key].append({
                            'value': value,
                            'yes_price': float(row['yes_price']),
                            'no_price': float(row['no_price']),
                            'quantity': int(row['quantity']),
                            'pair_time': row['pair_time']
                        })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print("Warning: Initial Claims Trade Data - Pairs not found")
        return None
    
    # Calculate monthly sentiment
    monthly_sentiment = {}
    for month_key, data in monthly_data.items():
        if data:
            total_quantity = sum(d['quantity'] for d in data)
            weighted_yes = sum(d['yes_price'] * d['quantity'] for d in data) / total_quantity
            weighted_no = sum(d['no_price'] * d['quantity'] for d in data) / total_quantity
            
            # Focus on values around 220k-250k
            relevant_data = [d for d in data if 220000 <= d['value'] <= 250000]
            if relevant_data:
                rel_total_quantity = sum(d['quantity'] for d in relevant_data)
                rel_weighted_yes = sum(d['yes_price'] * d['quantity'] for d in relevant_data) / rel_total_quantity
                sentiment = rel_weighted_yes - 0.5  # Positive = bullish for higher claims
            else:
                sentiment = weighted_yes - 0.5
            
            monthly_sentiment[month_key] = {
                'sentiment': sentiment,
                'confidence': min(total_quantity / 1000, 1.0),
                'total_quantity': total_quantity,
                'data_points': len(data)
            }
    
    return monthly_sentiment

def create_temporal_forecast():
    """Create temporal forecast showing evolution from Aug 2024 to Aug 2025"""
    print("TEMPORAL FORECAST ANALYSIS: AUG 2024 - AUG 2025")
    print("=" * 60)
    
    # Load FRED baseline
    try:
        with open('aug2024_forecast.json', 'r') as f:
            fred_baseline = json.load(f)
    except FileNotFoundError:
        print("Error: aug2024_forecast.json not found")
        return None
    
    base_forecast = fred_baseline['forecast']
    base_confidence = fred_baseline['confidence']
    
    print(f"FRED Baseline (August 2024): {base_forecast}%")
    print()
    
    # Analyze temporal data
    unrate_sentiment = analyze_temporal_unemployment_data()
    claims_sentiment = analyze_temporal_claims_data()
    
    # Create monthly forecasts
    monthly_forecasts = {}
    
    # Get all months from the data
    all_months = set()
    if unrate_sentiment:
        all_months.update(unrate_sentiment.keys())
    if claims_sentiment:
        all_months.update(claims_sentiment.keys())
    
    sorted_months = sorted(all_months)
    
    print("MONTHLY FORECAST EVOLUTION")
    print("-" * 40)
    
    for month in sorted_months:
        # Get sentiment data for this month
        unrate_data = unrate_sentiment.get(month, {})
        claims_data = claims_sentiment.get(month, {})
        
        # Calculate combined sentiment
        unrate_sent = unrate_data.get('sentiment', 0)
        claims_sent = claims_data.get('sentiment', 0)
        combined_sentiment = (unrate_sent + claims_sent) / 2
        
        # Calculate confidence
        unrate_conf = unrate_data.get('confidence', 0)
        claims_conf = claims_data.get('confidence', 0)
        combined_confidence = (unrate_conf + claims_conf) / 2
        
        # Calculate forecast adjustment
        sentiment_adjustment = combined_sentiment * 0.1  # Scale factor
        forecast = base_forecast + sentiment_adjustment
        
        # Calculate final confidence
        confidence_boost = combined_confidence * 10
        final_confidence = min(base_confidence + confidence_boost, 100)
        
        monthly_forecasts[month] = {
            'forecast': round(forecast, 2),
            'confidence': round(final_confidence, 1),
            'sentiment_adjustment': round(sentiment_adjustment, 3),
            'unrate_sentiment': round(unrate_sent, 3),
            'claims_sentiment': round(claims_sent, 3),
            'combined_sentiment': round(combined_sentiment, 3),
            'confidence_boost': round(confidence_boost, 1)
        }
        
        print(f"{month}: {forecast:.2f}% (Conf: {final_confidence:.1f}%, Adj: {sentiment_adjustment:+.3f}pp)")
    
    print()
    
    # Calculate summary statistics
    forecasts = [data['forecast'] for data in monthly_forecasts.values()]
    confidences = [data['confidence'] for data in monthly_forecasts.values()]
    
    if forecasts:
        min_forecast = min(forecasts)
        max_forecast = max(forecasts)
        avg_forecast = sum(forecasts) / len(forecasts)
        forecast_range = max_forecast - min_forecast
        
        min_confidence = min(confidences)
        max_confidence = max(confidences)
        avg_confidence = sum(confidences) / len(confidences)
        
        print("SUMMARY STATISTICS")
        print("-" * 20)
        print(f"Forecast Range: {min_forecast:.2f}% to {max_forecast:.2f}%")
        print(f"Average Forecast: {avg_forecast:.2f}%")
        print(f"Forecast Volatility: {forecast_range:.2f}pp")
        print()
        print(f"Confidence Range: {min_confidence:.1f}% to {max_confidence:.1f}%")
        print(f"Average Confidence: {avg_confidence:.1f}%")
        print()
        
        # Identify trends
        if len(forecasts) >= 3:
            early_avg = sum(forecasts[:3]) / 3
            late_avg = sum(forecasts[-3:]) / 3
            trend = late_avg - early_avg
            
            print("TREND ANALYSIS")
            print("-" * 15)
            print(f"Early Period Average: {early_avg:.2f}%")
            print(f"Late Period Average: {late_avg:.2f}%")
            print(f"Trend: {trend:+.2f}pp")
            
            if trend > 0.1:
                print("Trend: Rising unemployment expected")
            elif trend < -0.1:
                print("Trend: Falling unemployment expected")
            else:
                print("Trend: Stable unemployment expected")
    
    # Save results
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analysis_period': 'August 2024 - August 2025',
        'fred_baseline': {
            'forecast': base_forecast,
            'confidence': base_confidence
        },
        'monthly_forecasts': monthly_forecasts,
        'summary_statistics': {
            'forecast_range': [min_forecast, max_forecast] if forecasts else None,
            'average_forecast': avg_forecast if forecasts else None,
            'forecast_volatility': forecast_range if forecasts else None,
            'confidence_range': [min_confidence, max_confidence] if confidences else None,
            'average_confidence': avg_confidence if confidences else None,
            'trend': trend if 'trend' in locals() else None
        }
    }
    
    with open('temporal_forecast_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTemporal analysis saved to: temporal_forecast_analysis.json")
    
    return results

if __name__ == "__main__":
    results = create_temporal_forecast()
    if results:
        print(f"\nTemporal forecast analysis completed successfully!")
    else:
        print(f"\nAnalysis failed - no data available")