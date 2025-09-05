#!/usr/bin/env python3
"""
Updated Trade Data Processor (Simple Version)
Processes all updated trade data files without external dependencies
"""

import json
import csv
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
import os

class UpdatedTradeDataProcessor:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.initial_claims_foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.version = "v4.4-updated-trade-data"
        self.current_date = datetime.now()
        
        # File paths
        self.files = {
            'unemployment_prices': 'Unemployment Trade Prices Data.csv',
            'unemployment_pairs': 'Unemployment Rate Pair Data.csv',
            'initial_claims_prices': 'Initial Claims Trade Data - Prices',
            'initial_claims_pairs': 'Initial Claims Trade Data - Pairs'
        }
        
    def load_trade_data(self):
        """Load all updated trade data files"""
        print("🔄 Loading Updated Trade Data Files...")
        print("=" * 60)
        
        trade_data = {}
        
        # Load Unemployment Trade Prices Data
        try:
            print("📊 Loading Unemployment Trade Prices Data...")
            prices_data = self.load_csv_file(self.files['unemployment_prices'])
            trade_data['unemployment_prices'] = self.process_unemployment_prices(prices_data)
            print(f"✅ Loaded {len(prices_data)} unemployment price records")
        except Exception as e:
            print(f"❌ Error loading unemployment prices: {e}")
            trade_data['unemployment_prices'] = self.get_default_unemployment_prices()
        
        # Load Unemployment Rate Pair Data
        try:
            print("📊 Loading Unemployment Rate Pair Data...")
            pairs_data = self.load_csv_file(self.files['unemployment_pairs'])
            trade_data['unemployment_pairs'] = self.process_unemployment_pairs(pairs_data)
            print(f"✅ Loaded {len(pairs_data)} unemployment pair records")
        except Exception as e:
            print(f"❌ Error loading unemployment pairs: {e}")
            trade_data['unemployment_pairs'] = self.get_default_unemployment_pairs()
        
        # Load Initial Claims Trade Data - Prices
        try:
            print("📊 Loading Initial Claims Trade Prices Data...")
            claims_prices_data = self.load_csv_file(self.files['initial_claims_prices'])
            trade_data['initial_claims_prices'] = self.process_initial_claims_prices(claims_prices_data)
            print(f"✅ Loaded {len(claims_prices_data)} initial claims price records")
        except Exception as e:
            print(f"❌ Error loading initial claims prices: {e}")
            trade_data['initial_claims_prices'] = self.get_default_initial_claims_prices()
        
        # Load Initial Claims Trade Data - Pairs
        try:
            print("📊 Loading Initial Claims Trade Pairs Data...")
            claims_pairs_data = self.load_csv_file(self.files['initial_claims_pairs'])
            trade_data['initial_claims_pairs'] = self.process_initial_claims_pairs(claims_pairs_data)
            print(f"✅ Loaded {len(claims_pairs_data)} initial claims pair records")
        except Exception as e:
            print(f"❌ Error loading initial claims pairs: {e}")
            trade_data['initial_claims_pairs'] = self.get_default_initial_claims_pairs()
        
        return trade_data
    
    def load_csv_file(self, filename):
        """Load CSV file and return as list of dictionaries"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")
        
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filename, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        
        return data
    
    def process_unemployment_prices(self, data):
        """Process unemployment trade prices data"""
        if not data:
            return self.get_default_unemployment_prices()
        
        # Extract relevant columns
        price_columns = []
        for col in data[0].keys():
            if any(keyword in col.lower() for keyword in ['price', 'bid', 'ask', 'last']):
                price_columns.append(col)
        
        if not price_columns:
            return self.get_default_unemployment_prices()
        
        # Calculate price statistics
        price_stats = {}
        for col in price_columns:
            values = []
            for row in data:
                if col in row and row[col]:
                    # Clean and convert to float
                    clean_val = re.sub(r'[^\d.-]', '', str(row[col]))
                    try:
                        val = float(clean_val)
                        if not np.isnan(val):
                            values.append(val)
                    except (ValueError, TypeError):
                        continue
            
            if values:
                price_stats[col] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'count': len(values)
                }
        
        # Calculate overall sentiment
        if price_stats:
            avg_price = np.mean([stats['mean'] for stats in price_stats.values()])
            sentiment_score = self.calculate_price_sentiment(avg_price)
        else:
            sentiment_score = 0.0
        
        return {
            'data': price_stats,
            'sentiment_score': sentiment_score,
            'total_records': len(data),
            'processed_columns': len(price_columns),
            'data_freshness': 1.0
        }
    
    def process_unemployment_pairs(self, data):
        """Process unemployment rate pair data"""
        if not data:
            return self.get_default_unemployment_pairs()
        
        # Look for probability or percentage columns
        prob_columns = []
        for col in data[0].keys():
            if any(keyword in col.lower() for keyword in ['prob', 'percent', '%', 'yes', 'no']):
                prob_columns.append(col)
        
        if not prob_columns:
            return self.get_default_unemployment_pairs()
        
        # Process probability data
        prob_data = {}
        for col in prob_columns:
            values = []
            for row in data:
                if col in row and row[col]:
                    # Clean and convert to float
                    clean_val = re.sub(r'[^\d.-]', '', str(row[col]))
                    try:
                        val = float(clean_val)
                        if not np.isnan(val):
                            values.append(val)
                    except (ValueError, TypeError):
                        continue
            
            if values:
                prob_data[col] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'std': float(np.std(values)),
                    'count': len(values)
                }
        
        # Calculate pair sentiment
        if prob_data:
            # Look for 'yes' probabilities
            yes_cols = [col for col in prob_data.keys() if 'yes' in col.lower()]
            if yes_cols:
                avg_yes_prob = np.mean([prob_data[col]['mean'] for col in yes_cols])
                sentiment_score = (avg_yes_prob - 50) / 50  # Convert to -1 to 1 scale
            else:
                sentiment_score = 0.0
        else:
            sentiment_score = 0.0
        
        return {
            'data': prob_data,
            'sentiment_score': sentiment_score,
            'total_records': len(data),
            'processed_columns': len(prob_columns),
            'data_freshness': 1.0
        }
    
    def process_initial_claims_prices(self, data):
        """Process initial claims trade prices data"""
        if not data:
            return self.get_default_initial_claims_prices()
        
        # Extract price columns
        price_columns = []
        for col in data[0].keys():
            if any(keyword in col.lower() for keyword in ['price', 'bid', 'ask', 'last']):
                price_columns.append(col)
        
        if not price_columns:
            return self.get_default_initial_claims_prices()
        
        # Process price data
        price_stats = {}
        for col in price_columns:
            values = []
            for row in data:
                if col in row and row[col]:
                    # Clean and convert to float
                    clean_val = re.sub(r'[^\d.-]', '', str(row[col]))
                    try:
                        val = float(clean_val)
                        if not np.isnan(val):
                            values.append(val)
                    except (ValueError, TypeError):
                        continue
            
            if values:
                price_stats[col] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'count': len(values)
                }
        
        # Calculate sentiment based on claims levels
        if price_stats:
            avg_price = np.mean([stats['mean'] for stats in price_stats.values()])
            sentiment_score = self.calculate_claims_sentiment(avg_price)
        else:
            sentiment_score = 0.0
        
        return {
            'data': price_stats,
            'sentiment_score': sentiment_score,
            'total_records': len(data),
            'processed_columns': len(price_columns),
            'data_freshness': 1.0
        }
    
    def process_initial_claims_pairs(self, data):
        """Process initial claims trade pairs data"""
        if not data:
            return self.get_default_initial_claims_pairs()
        
        # Look for probability columns
        prob_columns = []
        for col in data[0].keys():
            if any(keyword in col.lower() for keyword in ['prob', 'percent', '%', 'yes', 'no']):
                prob_columns.append(col)
        
        if not prob_columns:
            return self.get_default_initial_claims_pairs()
        
        # Process probability data
        prob_data = {}
        for col in prob_columns:
            values = []
            for row in data:
                if col in row and row[col]:
                    # Clean and convert to float
                    clean_val = re.sub(r'[^\d.-]', '', str(row[col]))
                    try:
                        val = float(clean_val)
                        if not np.isnan(val):
                            values.append(val)
                    except (ValueError, TypeError):
                        continue
            
            if values:
                prob_data[col] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'std': float(np.std(values)),
                    'count': len(values)
                }
        
        # Calculate claims pair sentiment
        if prob_data:
            # Look for 'yes' probabilities (higher claims)
            yes_cols = [col for col in prob_data.keys() if 'yes' in col.lower()]
            if yes_cols:
                avg_yes_prob = np.mean([prob_data[col]['mean'] for col in yes_cols])
                sentiment_score = (avg_yes_prob - 50) / 50
            else:
                sentiment_score = 0.0
        else:
            sentiment_score = 0.0
        
        return {
            'data': prob_data,
            'sentiment_score': sentiment_score,
            'total_records': len(data),
            'processed_columns': len(prob_columns),
            'data_freshness': 1.0
        }
    
    def calculate_price_sentiment(self, avg_price):
        """Calculate sentiment from unemployment price data"""
        # Normalize price to sentiment (-1 to 1)
        if avg_price > 50:
            return (avg_price - 50) / 50
        else:
            return (avg_price - 50) / 50
    
    def calculate_claims_sentiment(self, avg_price):
        """Calculate sentiment from claims price data"""
        # Higher claims prices suggest more unemployment pressure
        if avg_price > 50:
            return (avg_price - 50) / 50
        else:
            return (avg_price - 50) / 50
    
    def get_default_unemployment_prices(self):
        """Default unemployment prices data"""
        return {
            'data': {},
            'sentiment_score': 0.0,
            'total_records': 0,
            'processed_columns': 0,
            'data_freshness': 0.0
        }
    
    def get_default_unemployment_pairs(self):
        """Default unemployment pairs data"""
        return {
            'data': {},
            'sentiment_score': 0.0,
            'total_records': 0,
            'processed_columns': 0,
            'data_freshness': 0.0
        }
    
    def get_default_initial_claims_prices(self):
        """Default initial claims prices data"""
        return {
            'data': {},
            'sentiment_score': 0.0,
            'total_records': 0,
            'processed_columns': 0,
            'data_freshness': 0.0
        }
    
    def get_default_initial_claims_pairs(self):
        """Default initial claims pairs data"""
        return {
            'data': {},
            'sentiment_score': 0.0,
            'total_records': 0,
            'processed_columns': 0,
            'data_freshness': 0.0
        }
    
    def analyze_combined_sentiment(self, trade_data):
        """Analyze combined sentiment from all trade data sources"""
        print("\n🔍 Analyzing Combined Trade Data Sentiment...")
        print("=" * 60)
        
        sentiments = []
        weights = []
        
        # Unemployment data
        if trade_data['unemployment_prices']['total_records'] > 0:
            sentiments.append(trade_data['unemployment_prices']['sentiment_score'])
            weights.append(0.3)
            print(f"📊 Unemployment Prices Sentiment: {trade_data['unemployment_prices']['sentiment_score']:+.3f}")
        
        if trade_data['unemployment_pairs']['total_records'] > 0:
            sentiments.append(trade_data['unemployment_pairs']['sentiment_score'])
            weights.append(0.3)
            print(f"📊 Unemployment Pairs Sentiment: {trade_data['unemployment_pairs']['sentiment_score']:+.3f}")
        
        # Initial Claims data
        if trade_data['initial_claims_prices']['total_records'] > 0:
            sentiments.append(trade_data['initial_claims_prices']['sentiment_score'])
            weights.append(0.2)
            print(f"📊 Initial Claims Prices Sentiment: {trade_data['initial_claims_prices']['sentiment_score']:+.3f}")
        
        if trade_data['initial_claims_pairs']['total_records'] > 0:
            sentiments.append(trade_data['initial_claims_pairs']['sentiment_score'])
            weights.append(0.2)
            print(f"📊 Initial Claims Pairs Sentiment: {trade_data['initial_claims_pairs']['sentiment_score']:+.3f}")
        
        if sentiments:
            # Weighted average sentiment
            combined_sentiment = np.average(sentiments, weights=weights)
            print(f"\n📊 Combined Trade Sentiment: {combined_sentiment:+.3f}")
            
            # Sentiment interpretation
            if combined_sentiment > 0.1:
                sentiment_interpretation = "Bullish (expecting higher unemployment)"
            elif combined_sentiment < -0.1:
                sentiment_interpretation = "Bearish (expecting lower unemployment)"
            else:
                sentiment_interpretation = "Neutral"
            
            print(f"📊 Sentiment Interpretation: {sentiment_interpretation}")
        else:
            combined_sentiment = 0.0
            sentiment_interpretation = "No data available"
            print(f"📊 Combined Trade Sentiment: {combined_sentiment:+.3f} (No data)")
        
        return {
            'combined_sentiment': combined_sentiment,
            'sentiment_interpretation': sentiment_interpretation,
            'individual_sentiments': sentiments,
            'weights': weights
        }
    
    def calculate_forecast_adjustments(self, sentiment_analysis, trade_data):
        """Calculate forecast adjustments based on trade data sentiment"""
        print("\n🔄 Calculating Forecast Adjustments...")
        print("=" * 60)
        
        combined_sentiment = sentiment_analysis['combined_sentiment']
        
        # Base adjustments
        sentiment_adjustment = combined_sentiment * 0.05  # 5% of sentiment as adjustment
        
        # Volume-based confidence boost
        total_records = sum([
            trade_data.get('unemployment_prices', {}).get('total_records', 0),
            trade_data.get('unemployment_pairs', {}).get('total_records', 0),
            trade_data.get('initial_claims_prices', {}).get('total_records', 0),
            trade_data.get('initial_claims_pairs', {}).get('total_records', 0)
        ])
        
        volume_confidence_boost = min(5.0, total_records / 1000)  # Max 5% boost
        
        # Data freshness boost
        avg_freshness = np.mean([
            trade_data.get('unemployment_prices', {}).get('data_freshness', 0),
            trade_data.get('unemployment_pairs', {}).get('data_freshness', 0),
            trade_data.get('initial_claims_prices', {}).get('data_freshness', 0),
            trade_data.get('initial_claims_pairs', {}).get('data_freshness', 0)
        ])
        
        freshness_confidence_boost = avg_freshness * 2.0  # Max 2% boost
        
        adjustments = {
            'sentiment_adjustment': sentiment_adjustment,
            'volume_confidence_boost': volume_confidence_boost,
            'freshness_confidence_boost': freshness_confidence_boost,
            'total_confidence_boost': volume_confidence_boost + freshness_confidence_boost
        }
        
        print(f"📊 Sentiment Adjustment: {sentiment_adjustment:+.3f}%")
        print(f"📊 Volume Confidence Boost: {volume_confidence_boost:+.1f}%")
        print(f"📊 Freshness Confidence Boost: {freshness_confidence_boost:+.1f}%")
        print(f"📊 Total Confidence Boost: {adjustments['total_confidence_boost']:+.1f}%")
        
        return adjustments
    
    def save_updated_trade_analysis(self, trade_data, sentiment_analysis, adjustments):
        """Save updated trade data analysis"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'foundation_ids': {
                'main': self.foundation_id,
                'initial_claims': self.initial_claims_foundation_id
            },
            'trade_data': trade_data,
            'sentiment_analysis': sentiment_analysis,
            'adjustments': adjustments,
            'summary': {
                'total_data_sources': len([k for k, v in trade_data.items() if v.get('total_records', 0) > 0]),
                'total_records': sum([v.get('total_records', 0) for v in trade_data.values()]),
                'combined_sentiment': sentiment_analysis['combined_sentiment'],
                'sentiment_interpretation': sentiment_analysis['sentiment_interpretation']
            }
        }
        
        filename = f"updated_trade_data_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2, default=str)
            print(f"\n💾 Updated trade analysis saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving trade analysis: {e}")
        
        return filename

def main():
    """Main function to process updated trade data"""
    processor = UpdatedTradeDataProcessor()
    
    print("🚀 UPDATED TRADE DATA PROCESSING")
    print("=" * 70)
    print(f"📅 Processing Date: {processor.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Version: {processor.version}")
    print(f"📊 Foundation IDs: {processor.foundation_id}, {processor.initial_claims_foundation_id}")
    
    # Load trade data
    trade_data = processor.load_trade_data()
    
    # Analyze sentiment
    sentiment_analysis = processor.analyze_combined_sentiment(trade_data)
    
    # Calculate adjustments
    adjustments = processor.calculate_forecast_adjustments(sentiment_analysis, trade_data)
    
    # Save analysis
    filename = processor.save_updated_trade_analysis(trade_data, sentiment_analysis, adjustments)
    
    print("\n" + "=" * 70)
    print("✅ UPDATED TRADE DATA PROCESSING COMPLETE")
    print("=" * 70)
    print(f"📊 Processed {len(sentiment_analysis['individual_sentiments'])} sentiment sources")
    print(f"📊 Combined Sentiment: {sentiment_analysis['combined_sentiment']:+.3f}")
    print(f"📊 Sentiment: {sentiment_analysis['sentiment_interpretation']}")
    print(f"📊 Forecast Adjustment: {adjustments['sentiment_adjustment']:+.3f}%")
    print(f"📊 Confidence Boost: {adjustments['total_confidence_boost']:+.1f}%")
    print(f"💾 Analysis saved to: {filename}")

if __name__ == "__main__":
    main()