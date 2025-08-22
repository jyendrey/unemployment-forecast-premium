#!/usr/bin/env python3
"""
Simple Trade Data Processor
Processes unemployment trade data using Python standard library
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import csv
import json
from datetime import datetime
from collections import defaultdict, Counter
import statistics

class SimpleTradeProcessor:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        self.version = "v2.1-enhanced"
        self.trades = []
        self.unemployment_trades = []
        
    def process_csv_file(self, filename):
        """Process the CSV file and extract trade data"""
        print(f"📊 Processing trade data file: {filename}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                # Check if it's tab-separated or comma-separated
                if '\t' in sample:
                    delimiter = '\t'
                    print("🔍 Detected tab-separated file")
                else:
                    delimiter = ','
                    print("🔍 Detected comma-separated file")
                
                reader = csv.DictReader(file, delimiter=delimiter)
                
                # Process each row
                for row_num, row in enumerate(reader, 1):
                    if row_num % 10000 == 0:
                        print(f"📈 Processed {row_num:,} rows...")
                    
                    # Clean and validate row
                    cleaned_row = self.clean_row(row)
                    if cleaned_row:
                        self.trades.append(cleaned_row)
                        
                        # Check if it's unemployment-related
                        if self.is_unemployment_trade(cleaned_row):
                            self.unemployment_trades.append(cleaned_row)
                
                print(f"✅ Total trades processed: {len(self.trades):,}")
                print(f"✅ Unemployment trades found: {len(self.unemployment_trades):,}")
                
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            return False
        
        return True
    
    def clean_row(self, row):
        """Clean and validate a single row of data"""
        try:
            # Extract key fields
            event_contract = row.get('event_contract', '').strip()
            date = row.get('date', '').strip()
            start_price = row.get('start_price', '').strip()
            end_price = row.get('end_price', '').strip()
            pair_quantity = row.get('pair_quantity', '').strip()
            
            # Skip rows with missing critical data
            if not event_contract or not date:
                return None
            
            # Convert numeric fields
            try:
                start_price = float(start_price) if start_price else 0.0
                end_price = float(end_price) if end_price else 0.0
                pair_quantity = int(pair_quantity) if pair_quantity else 0
            except ValueError:
                return None
            
            # Skip invalid data
            if start_price < 0 or end_price < 0 or pair_quantity < 0:
                return None
            
            return {
                'event_contract': event_contract,
                'subtype': row.get('subtype', '').strip(),
                'expiration_date': row.get('expiration_date', '').strip(),
                'date': date,
                'start_price': start_price,
                'end_price': end_price,
                'pair_quantity': pair_quantity,
                'open_interest': row.get('open_interest', '').strip(),
                'vwap': row.get('vwap', '').strip()
            }
            
        except Exception:
            return None
    
    def is_unemployment_trade(self, trade):
        """Check if a trade is unemployment-related"""
        contract = trade['event_contract'].lower()
        return 'unr' in contract or 'unemployment' in contract
    
    def analyze_unemployment_trades(self):
        """Analyze unemployment-related trades"""
        if not self.unemployment_trades:
            print("⚠️ No unemployment trades found for analysis")
            return None
        
        print(f"\n🔍 Analyzing {len(self.unemployment_trades):,} unemployment trades...")
        
        # Extract key metrics
        prices = [trade['end_price'] for trade in self.unemployment_trades if trade['end_price'] > 0]
        quantities = [trade['pair_quantity'] for trade in self.unemployment_trades if trade['pair_quantity'] > 0]
        
        # Calculate statistics
        analysis = {
            'total_trades': len(self.unemployment_trades),
            'total_volume': sum(quantities),
            'avg_price': statistics.mean(prices) if prices else 0,
            'price_std': statistics.stdev(prices) if len(prices) > 1 else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'avg_quantity': statistics.mean(quantities) if quantities else 0,
            'date_range': self.get_date_range(),
            'contract_breakdown': self.get_contract_breakdown(),
            'sentiment_analysis': self.calculate_sentiment(),
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id
        }
        
        return analysis
    
    def get_date_range(self):
        """Get the date range of unemployment trades"""
        dates = []
        for trade in self.unemployment_trades:
            try:
                # Try to parse the date
                date_str = trade['date']
                if len(date_str) >= 10:  # At least YYYY-MM-DD
                    parsed_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
                    dates.append(parsed_date)
            except:
                continue
        
        if dates:
            return {
                'start': min(dates).strftime('%Y-%m-%d'),
                'end': max(dates).strftime('%Y-%m-%d'),
                'total_days': (max(dates) - min(dates)).days
            }
        return {'start': 'Unknown', 'end': 'Unknown', 'total_days': 0}
    
    def get_contract_breakdown(self):
        """Break down trades by contract type"""
        contract_counts = Counter()
        for trade in self.unemployment_trades:
            contract = trade['event_contract']
            contract_counts[contract] += 1
        
        return dict(contract_counts.most_common(10))  # Top 10 contracts
    
    def calculate_sentiment(self):
        """Calculate market sentiment from unemployment trades"""
        if not self.unemployment_trades:
            return {'sentiment_score': 0, 'confidence': 0}
        
        # Calculate sentiment based on price movements
        sentiment_scores = []
        for trade in self.unemployment_trades:
            if trade['start_price'] > 0 and trade['end_price'] > 0:
                # Price change from start to end
                price_change = (trade['end_price'] - trade['start_price']) / trade['start_price']
                sentiment_scores.append(price_change)
        
        if sentiment_scores:
            avg_sentiment = statistics.mean(sentiment_scores)
            sentiment_std = statistics.stdev(sentiment_scores) if len(sentiment_scores) > 1 else 0
            
            return {
                'sentiment_score': round(avg_sentiment, 4),
                'sentiment_std': round(sentiment_std, 4),
                'trades_analyzed': len(sentiment_scores),
                'interpretation': self.interpret_sentiment(avg_sentiment)
            }
        
        return {'sentiment_score': 0, 'confidence': 0}
    
    def interpret_sentiment(self, sentiment_score):
        """Interpret the sentiment score"""
        if sentiment_score > 0.1:
            return "Strongly Bullish (expecting higher unemployment)"
        elif sentiment_score > 0.05:
            return "Bullish (expecting higher unemployment)"
        elif sentiment_score > -0.05:
            return "Neutral"
        elif sentiment_score > -0.1:
            return "Bearish (expecting lower unemployment)"
        else:
            return "Strongly Bearish (expecting lower unemployment)"
    
    def create_enhanced_forecast_input(self, analysis):
        """Create enhanced forecast input for the unemployment forecasting system"""
        if not analysis:
            return None
        
        forecast_input = {
            'generated_date': datetime.now().isoformat(),
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id,
            'version': self.version,
            'market_sentiment': {
                'sentiment_score': analysis['sentiment_analysis']['sentiment_score'],
                'sentiment_interpretation': analysis['sentiment_analysis']['interpretation'],
                'contracts_analyzed': analysis['total_trades'],
                'total_volume': analysis['total_volume'],
                'confidence': 1 - min(analysis['sentiment_analysis']['sentiment_std'], 1)
            },
            'data_quality': {
                'total_trades_processed': len(self.trades),
                'unemployment_trade_ratio': len(self.unemployment_trades) / len(self.trades),
                'date_coverage': analysis['date_range']['total_days'],
                'foundation_id': self.foundation_id
            },
            'contract_analysis': {
                'unique_contracts': len(analysis['contract_breakdown']),
                'top_contracts': analysis['contract_breakdown'],
                'math_framework': self.math_framework_id
            }
        }
        
        return forecast_input
    
    def save_analysis(self, analysis, filename="unemployment_trade_analysis.json"):
        """Save the analysis results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Analysis saved to: {filename}")
        return filename
    
    def print_summary(self, analysis):
        """Print a comprehensive summary of the analysis"""
        print("\n" + "="*60)
        print("UNEMPLOYMENT TRADE DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Math Framework ID: {self.math_framework_id}")
        print(f"Version: {self.version}")
        print("="*60)
        
        print(f"\n📊 DATA OVERVIEW:")
        print(f"  Total trades processed: {len(self.trades):,}")
        print(f"  Unemployment trades found: {len(self.unemployment_trades):,}")
        print(f"  Unemployment trade ratio: {len(self.unemployment_trades)/len(self.trades)*100:.2f}%")
        
        if analysis:
            print(f"\n🔍 UNEMPLOYMENT TRADE ANALYSIS:")
            print(f"  Total volume: {analysis['total_volume']:,}")
            print(f"  Average price: ${analysis['avg_price']:.4f}")
            print(f"  Price range: ${analysis['min_price']:.4f} - ${analysis['max_price']:.4f}")
            print(f"  Date range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
            print(f"  Total days: {analysis['date_range']['total_days']}")
            
            print(f"\n📈 SENTIMENT ANALYSIS:")
            sentiment = analysis['sentiment_analysis']
            print(f"  Sentiment score: {sentiment['sentiment_score']:.4f}")
            print(f"  Interpretation: {sentiment['interpretation']}")
            print(f"  Trades analyzed: {sentiment['trades_analyzed']:,}")
            
            print(f"\n📋 TOP CONTRACTS:")
            for contract, count in list(analysis['contract_breakdown'].items())[:5]:
                print(f"  {contract}: {count} trades")
        
        print("\n" + "="*60)

def main():
    """Main execution function"""
    print("="*60)
    print("SIMPLE TRADE DATA PROCESSOR")
    print("="*60)
    print(f"Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b")
    print(f"Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8")
    print(f"Version: v2.1-enhanced")
    print("="*60)
    
    processor = SimpleTradeProcessor()
    
    # Process the unemployment trade data
    filename = "Unemployment Trade Prices Data.csv"
    
    if processor.process_csv_file(filename):
        # Analyze unemployment trades
        analysis = processor.analyze_unemployment_trades()
        
        if analysis:
            # Print summary
            processor.print_summary(analysis)
            
            # Save analysis
            analysis_file = processor.save_analysis(analysis)
            
            # Create enhanced forecast input
            forecast_input = processor.create_enhanced_forecast_input(analysis)
            if forecast_input:
                forecast_file = "enhanced_forecast_input.json"
                with open(forecast_file, 'w') as f:
                    json.dump(forecast_input, f, indent=2)
                print(f"✅ Enhanced forecast input saved to: {forecast_file}")
            
            print(f"\n🎯 Ready for enhanced unemployment forecasting!")
            print(f"🔧 Foundation System: {processor.foundation_id}")
            print(f"🔧 Math Framework: {processor.math_framework_id}")
        else:
            print("❌ No unemployment trades found for analysis")
    else:
        print("❌ Failed to process trade data file")

if __name__ == "__main__":
    main()