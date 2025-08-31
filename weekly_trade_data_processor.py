#!/usr/bin/env python3
"""
Weekly Unemployment Trade Data Processor
Processes updated weekly unemployment trade data (prices and pairs) for enhanced forecasting
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
"""

import csv
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os

class WeeklyTradeDataProcessor:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.version = "v3.2-weekly-trade-updated"
        self.current_date = datetime.now()
        
        # File paths for weekly trade data
        self.prices_file = "Unemployment Trade Prices Data.csv"
        self.pairs_file = "Unemployment Rate Pair Data.csv"
        
        # Processed data storage
        self.prices_data = []
        self.pairs_data = []
        self.processed_analysis = None
        
    def load_prices_data(self) -> List[Dict]:
        """Load unemployment trade prices data"""
        try:
            data = []
            with open(self.prices_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Clean and validate the data
                    cleaned_row = self.clean_prices_row(row)
                    if cleaned_row:
                        data.append(cleaned_row)
            
            print(f"✅ Loaded {len(data)} prices records from weekly unemployment trade data")
            return data
        except Exception as e:
            print(f"⚠️ Error loading prices data: {e}")
            return []
    
    def load_pairs_data(self) -> List[Dict]:
        """Load unemployment rate pairs data"""
        try:
            data = []
            with open(self.pairs_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Clean and validate the data
                    cleaned_row = self.clean_pairs_row(row)
                    if cleaned_row:
                        data.append(cleaned_row)
            
            print(f"✅ Loaded {len(data)} pairs records from weekly unemployment rate data")
            return data
        except Exception as e:
            print(f"⚠️ Error loading pairs data: {e}")
            return []
    
    def clean_prices_row(self, row: Dict) -> Optional[Dict]:
        """Clean and validate a prices data row"""
        try:
            # Extract key fields
            event_contract = row.get('event_contract', '').strip()
            if not event_contract:
                return None
            
            # Parse contract information
            contract_info = self.parse_unemployment_contract(event_contract)
            if not contract_info:
                return None
            
            # Clean numeric fields
            cleaned_row = {
                'event_contract': event_contract,
                'subtype': row.get('subtype', '').strip(),
                'expiration_date': row.get('expiration_date', '').strip(),
                'date': row.get('date', '').strip(),
                'start_price': self.parse_float(row.get('start_price', 0)),
                'high_price': self.parse_float(row.get('high_price', 0)),
                'low_price': self.parse_float(row.get('low_price', 0)),
                'end_price': self.parse_float(row.get('end_price', 0)),
                'settlement_price': self.parse_float(row.get('settlement_price', 0)),
                'pair_quantity': self.parse_int(row.get('pair_quantity', 0)),
                'open_interest': self.parse_int(row.get('open_interest', 0)),
                'vwap': self.parse_float(row.get('vwap', 0)),
                'contract_info': contract_info
            }
            
            return cleaned_row
        except Exception as e:
            print(f"⚠️ Error cleaning prices row: {e}")
            return None
    
    def clean_pairs_row(self, row: Dict) -> Optional[Dict]:
        """Clean and validate a pairs data row"""
        try:
            # Extract key fields
            event_contract = row.get('event_contract', '').strip()
            if not event_contract:
                return None
            
            # Parse contract information
            contract_info = self.parse_unemployment_contract(event_contract)
            if not contract_info:
                return None
            
            # Clean numeric fields
            cleaned_row = {
                'pair_id': row.get('pair_id', '').strip(),
                'event_contract': event_contract,
                'expiration_date': row.get('expiration_date', '').strip(),
                'quantity': self.parse_int(row.get('quantity', 0)),
                'yes_price': self.parse_float(row.get('yes_price', 0)),
                'no_price': self.parse_float(row.get('no_price', 0)),
                'pair_time': row.get('pair_time', '').strip(),
                'contract_info': contract_info
            }
            
            return cleaned_row
        except Exception as e:
            print(f"⚠️ Error cleaning pairs row: {e}")
            return None
    
    def parse_unemployment_contract(self, contract_str: str) -> Optional[Dict]:
        """Parse unemployment contract string to extract key information"""
        try:
            # Format: UNR_MMYY_RATE (e.g., UNR_0724_3.9)
            parts = contract_str.split('_')
            if len(parts) == 3:
                month_part = parts[1]  # MMYY
                rate_part = parts[2]   # RATE
                
                # Parse month and year
                month = int(month_part[:2])
                year = 2000 + int(month_part[2:4])
                
                # Parse unemployment rate
                rate = float(rate_part)
                
                # Create date for the month
                contract_date = datetime(year, month, 1)
                
                return {
                    'month': month,
                    'year': year,
                    'unemployment_rate': rate,
                    'contract_date': contract_date,
                    'contract_type': 'Unemployment Rate'
                }
            return None
        except Exception as e:
            print(f"⚠️ Error parsing contract {contract_str}: {e}")
            return None
    
    def parse_float(self, value) -> float:
        """Parse float value with error handling"""
        try:
            if value is None or value == '':
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def parse_int(self, value) -> int:
        """Parse integer value with error handling"""
        try:
            if value is None or value == '':
                return 0
            return int(float(value))  # Handle cases where value might be float
        except (ValueError, TypeError):
            return 0
    
    def analyze_prices_sentiment(self, data: List[Dict]) -> Dict:
        """Analyze sentiment from prices data"""
        if not data:
            return {}
        
        # Filter active contracts (with trading activity)
        active_contracts = [row for row in data if row['pair_quantity'] > 0 and row['settlement_price'] > 0]
        
        if not active_contracts:
            return {}
        
        # Calculate sentiment metrics
        total_volume = sum(row['pair_quantity'] for row in active_contracts)
        total_contracts = len(active_contracts)
        
        # Analyze price movements
        price_changes = []
        for row in active_contracts:
            if row['start_price'] > 0 and row['end_price'] > 0:
                change = (row['end_price'] - row['start_price']) / row['start_price']
                price_changes.append(change)
        
        # Calculate sentiment score based on price changes
        if price_changes:
            avg_change = sum(price_changes) / len(price_changes)
            # Normalize to -1 to 1 range
            sentiment_score = max(-1.0, min(1.0, avg_change * 10))  # Scale for better sensitivity
        else:
            sentiment_score = 0.0
        
        # Interpret sentiment
        if sentiment_score > 0.3:
            sentiment_interpretation = "Bullish (Lower Unemployment Expected)"
        elif sentiment_score < -0.3:
            sentiment_interpretation = "Bearish (Higher Unemployment Expected)"
        else:
            sentiment_interpretation = "Neutral"
        
        return {
            'sentiment_score': round(sentiment_score, 4),
            'sentiment_interpretation': sentiment_interpretation,
            'total_volume': int(total_volume),
            'total_contracts': int(total_contracts),
            'active_contracts': len(active_contracts),
            'avg_price_change': round(avg_change if price_changes else 0, 4),
            'confidence': min(0.95, 0.7 + (total_contracts / 100) * 0.25)
        }
    
    def analyze_pairs_sentiment(self, data: List[Dict]) -> Dict:
        """Analyze sentiment from pairs data"""
        if not data:
            return {}
        
        # Filter valid pairs
        valid_pairs = [row for row in data if row['yes_price'] > 0 and row['no_price'] > 0]
        
        if not valid_pairs:
            return {}
        
        # Calculate sentiment metrics
        total_volume = sum(row['quantity'] for row in valid_pairs)
        total_trades = len(valid_pairs)
        
        # Analyze price spreads (yes_price vs no_price)
        price_spreads = []
        price_ratios = []
        
        for row in valid_pairs:
            spread = row['yes_price'] - row['no_price']
            ratio = row['yes_price'] / row['no_price']
            price_spreads.append(spread)
            price_ratios.append(ratio)
        
        # Calculate sentiment score based on price spreads
        avg_spread = sum(price_spreads) / len(price_spreads)
        avg_ratio = sum(price_ratios) / len(price_ratios)
        
        # Normalize sentiment score (-1 to 1)
        # Higher yes_price relative to no_price indicates lower unemployment expectations
        sentiment_score = (avg_ratio - 1.0) * 2  # Convert 0.5-2.0 range to -1 to 1
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Interpret sentiment
        if sentiment_score > 0.3:
            sentiment_interpretation = "Bullish (Lower Unemployment Expected)"
        elif sentiment_score < -0.3:
            sentiment_interpretation = "Bearish (Higher Unemployment Expected)"
        else:
            sentiment_interpretation = "Neutral"
        
        return {
            'sentiment_score': round(sentiment_score, 4),
            'sentiment_interpretation': sentiment_interpretation,
            'total_volume': int(total_volume),
            'total_trades': int(total_trades),
            'avg_price_spread': round(avg_spread, 4),
            'avg_price_ratio': round(avg_ratio, 4),
            'confidence': min(0.95, 0.7 + (total_trades / 1000) * 0.25)
        }
    
    def analyze_contract_distribution(self, data: List[Dict]) -> Dict:
        """Analyze distribution of unemployment rate contracts"""
        if not data:
            return {}
        
        # Extract contract information
        contracts = []
        for row in data:
            if 'contract_info' in row and row['contract_info']:
                contracts.append(row['contract_info'])
        
        if not contracts:
            return {}
        
        # Analyze unemployment rate thresholds
        rates = [contract['unemployment_rate'] for contract in contracts]
        
        # Calculate statistics
        rate_stats = {
            'min_rate': min(rates),
            'max_rate': max(rates),
            'mean_rate': sum(rates) / len(rates),
            'total_contracts': len(contracts),
            'rate_range': max(rates) - min(rates)
        }
        
        # Analyze by month
        monthly_distribution = {}
        for contract in contracts:
            month_key = f"{contract['year']}-{contract['month']:02d}"
            if month_key not in monthly_distribution:
                monthly_distribution[month_key] = []
            monthly_distribution[month_key].append(contract['unemployment_rate'])
        
        rate_stats['monthly_distribution'] = monthly_distribution
        
        return rate_stats
    
    def analyze_temporal_patterns(self, data: List[Dict]) -> Dict:
        """Analyze temporal patterns in the data"""
        if not data:
            return {}
        
        # Extract dates and analyze patterns
        dates = []
        for row in data:
            if 'date' in row and row['date']:
                try:
                    # Parse date (format: M/D/YYYY)
                    date_obj = datetime.strptime(row['date'], '%m/%d/%Y')
                    dates.append(date_obj)
                except:
                    continue
        
        if not dates:
            return {}
        
        # Analyze temporal patterns
        temporal_analysis = {}
        
        # Date range
        min_date = min(dates)
        max_date = max(dates)
        temporal_analysis['date_range'] = {
            'start': min_date.strftime('%Y-%m-%d'),
            'end': max_date.strftime('%Y-%m-%d'),
            'total_days': (max_date - min_date).days + 1
        }
        
        # Daily activity
        daily_counts = {}
        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        temporal_analysis['daily_activity'] = daily_counts
        temporal_analysis['peak_trading_day'] = max(daily_counts, key=daily_counts.get) if daily_counts else None
        
        return temporal_analysis
    
    def integrate_sentiment(self, prices_sentiment: Dict, pairs_sentiment: Dict) -> Dict:
        """Integrate sentiment from both data sources"""
        integrated = {
            'overall_sentiment_score': 0.0,
            'overall_sentiment_interpretation': 'Neutral',
            'data_source_weights': {},
            'confidence': 0.0
        }
        
        # Weight the sentiment based on data availability and quality
        total_weight = 0
        weighted_sentiment = 0
        total_confidence = 0
        
        if prices_sentiment:
            weight = prices_sentiment.get('total_contracts', 0) / 100  # Normalize weight
            weighted_sentiment += prices_sentiment['sentiment_score'] * weight
            total_weight += weight
            total_confidence += prices_sentiment.get('confidence', 0) * weight
            integrated['data_source_weights']['prices'] = round(weight, 4)
        
        if pairs_sentiment:
            weight = pairs_sentiment.get('total_trades', 0) / 1000  # Normalize weight
            weighted_sentiment += pairs_sentiment['sentiment_score'] * weight
            total_weight += weight
            total_confidence += pairs_sentiment.get('confidence', 0) * weight
            integrated['data_source_weights']['pairs'] = round(weight, 4)
        
        if total_weight > 0:
            integrated['overall_sentiment_score'] = round(weighted_sentiment / total_weight, 4)
            integrated['confidence'] = round(total_confidence / total_weight, 4)
            
            # Interpret overall sentiment
            score = integrated['overall_sentiment_score']
            if score > 0.3:
                integrated['overall_sentiment_interpretation'] = 'Bullish (Lower Unemployment Expected)'
            elif score < -0.3:
                integrated['overall_sentiment_interpretation'] = 'Bearish (Higher Unemployment Expected)'
            else:
                integrated['overall_sentiment_interpretation'] = 'Neutral'
        
        return integrated
    
    def generate_market_insights(self, prices_sentiment: Dict, pairs_sentiment: Dict, contract_distribution: Dict) -> Dict:
        """Generate market insights from the analysis"""
        insights = {
            'key_findings': [],
            'risk_factors': [],
            'opportunities': [],
            'market_dynamics': {}
        }
        
        # Analyze sentiment trends
        if prices_sentiment and 'sentiment_score' in prices_sentiment:
            score = prices_sentiment['sentiment_score']
            if score > 0.5:
                insights['key_findings'].append("Strong bullish sentiment indicates market expects lower unemployment")
                insights['opportunities'].append("Positive economic outlook reflected in unemployment expectations")
            elif score < -0.5:
                insights['key_findings'].append("Strong bearish sentiment indicates market expects higher unemployment")
                insights['risk_factors'].append("Potential economic slowdown reflected in unemployment expectations")
        
        if pairs_sentiment and 'sentiment_score' in pairs_sentiment:
            score = pairs_sentiment['sentiment_score']
            if score > 0.5:
                insights['key_findings'].append("Strong bullish sentiment in pairs trading indicates lower unemployment expectations")
            elif score < -0.5:
                insights['key_findings'].append("Strong bearish sentiment in pairs trading indicates higher unemployment expectations")
        
        # Analyze contract distribution
        if contract_distribution:
            mean_rate = contract_distribution.get('mean_rate')
            if mean_rate:
                insights['market_dynamics']['average_unemployment_expectation'] = round(mean_rate, 2)
                insights['key_findings'].append(f"Market average unemployment expectation: {mean_rate:.1f}%")
        
        return insights
    
    def process_weekly_trade_data(self) -> Dict:
        """Process all weekly unemployment trade data and generate comprehensive analysis"""
        print("🔄 Processing Weekly Unemployment Trade Data...")
        print(f"Foundation ID: {self.foundation_id}")
        print("="*60)
        
        # Load data
        self.prices_data = self.load_prices_data()
        self.pairs_data = self.load_pairs_data()
        
        if not self.prices_data and not self.pairs_data:
            print("⚠️ No weekly trade data available")
            return self.get_default_analysis()
        
        # Analyze prices data
        prices_analysis = {}
        if self.prices_data:
            print("📊 Analyzing prices data...")
            prices_analysis = {
                'sentiment': self.analyze_prices_sentiment(self.prices_data),
                'contract_distribution': self.analyze_contract_distribution(self.prices_data),
                'temporal_patterns': self.analyze_temporal_patterns(self.prices_data)
            }
        
        # Analyze pairs data
        pairs_analysis = {}
        if self.pairs_data:
            print("📈 Analyzing pairs data...")
            pairs_analysis = {
                'sentiment': self.analyze_pairs_sentiment(self.pairs_data),
                'contract_distribution': self.analyze_contract_distribution(self.pairs_data)
            }
        
        # Combine analysis
        combined_analysis = {
            'foundation_id': self.foundation_id,
            'version': self.version,
            'processed_date': self.current_date.isoformat(),
            'data_summary': {
                'prices_records': len(self.prices_data),
                'pairs_records': len(self.pairs_data),
                'total_records': len(self.prices_data) + len(self.pairs_data)
            },
            'prices_analysis': prices_analysis,
            'pairs_analysis': pairs_analysis,
            'integrated_sentiment': self.integrate_sentiment(prices_analysis, pairs_analysis),
            'market_insights': self.generate_market_insights(prices_analysis, pairs_analysis, 
                                                          prices_analysis.get('contract_distribution', {}))
        }
        
        self.processed_analysis = combined_analysis
        print("✅ Weekly trade data processing complete!")
        
        return combined_analysis
    
    def get_default_analysis(self) -> Dict:
        """Get default analysis if no data is available"""
        return {
            'foundation_id': self.foundation_id,
            'version': self.version,
            'processed_date': self.current_date.isoformat(),
            'data_summary': {
                'prices_records': 0,
                'pairs_records': 0,
                'total_records': 0
            },
            'prices_analysis': {},
            'pairs_analysis': {},
            'integrated_sentiment': {
                'overall_sentiment_score': 0.0,
                'overall_sentiment_interpretation': 'Neutral',
                'data_source_weights': {},
                'confidence': 0.0
            },
            'market_insights': {
                'key_findings': ['No weekly trade data available'],
                'risk_factors': [],
                'opportunities': [],
                'market_dynamics': {}
            }
        }
    
    def save_analysis(self, filename: str = "weekly_trade_analysis.json") -> str:
        """Save the processed analysis to a JSON file"""
        if not self.processed_analysis:
            print("⚠️ No analysis to save. Run process_weekly_trade_data() first.")
            return ""
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.processed_analysis, f, indent=2)
            
            print(f"✅ Weekly trade analysis saved to: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ Error saving analysis: {e}")
            return ""
    
    def print_summary(self):
        """Print a summary of the processed data"""
        if not self.processed_analysis:
            print("⚠️ No analysis available. Run process_weekly_trade_data() first.")
            return
        
        print("\n" + "="*60)
        print("WEEKLY UNEMPLOYMENT TRADE DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print(f"Processed Date: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Data summary
        data_summary = self.processed_analysis['data_summary']
        print(f"\n📊 DATA SUMMARY:")
        print(f"  Prices Records: {data_summary['prices_records']:,}")
        print(f"  Pairs Records: {data_summary['pairs_records']:,}")
        print(f"  Total Records: {data_summary['total_records']:,}")
        
        # Integrated sentiment
        sentiment = self.processed_analysis['integrated_sentiment']
        print(f"\n📈 INTEGRATED SENTIMENT:")
        print(f"  Overall Score: {sentiment['overall_sentiment_score']:.4f}")
        print(f"  Interpretation: {sentiment['overall_sentiment_interpretation']}")
        print(f"  Confidence: {sentiment['confidence']:.2f}")
        
        # Data source weights
        if sentiment['data_source_weights']:
            print(f"  Data Source Weights:")
            for source, weight in sentiment['data_source_weights'].items():
                print(f"    {source.capitalize()}: {weight:.4f}")
        
        # Market insights
        insights = self.processed_analysis['market_insights']
        if insights['key_findings']:
            print(f"\n🔍 KEY FINDINGS:")
            for finding in insights['key_findings']:
                print(f"  • {finding}")
        
        if insights['risk_factors']:
            print(f"\n⚠️ RISK FACTORS:")
            for risk in insights['risk_factors']:
                print(f"  • {risk}")
        
        if insights['opportunities']:
            print(f"\n💡 OPPORTUNITIES:")
            for opportunity in insights['opportunities']:
                print(f"  • {opportunity}")
        
        print("\n" + "="*60)

def main():
    """Main execution function"""
    processor = WeeklyTradeDataProcessor()
    
    # Process the data
    analysis = processor.process_weekly_trade_data()
    
    # Save analysis
    processor.save_analysis()
    
    # Print summary
    processor.print_summary()
    
    return analysis

if __name__ == "__main__":
    main()