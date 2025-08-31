#!/usr/bin/env python3
"""
Initial Claims Trade Data Processor
Integrates initial claims trade data (pairs and prices) into the unemployment forecast framework
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class InitialClaimsDataProcessor:
    def __init__(self):
        self.foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.version = "v1.0-initial-claims-integration"
        self.current_date = datetime.now()
        
        # File paths for initial claims data
        self.pairs_file = "Initial Claims Trade Data - Pairs"
        self.prices_file = "Initial Claims Trade Data - Prices"
        
        # Load and process data
        self.pairs_data = None
        self.prices_data = None
        self.processed_analysis = None
        
    def load_pairs_data(self) -> pd.DataFrame:
        """Load initial claims pairs data"""
        try:
            # Read the pairs data (tab-separated)
            df = pd.read_csv(self.pairs_file, sep='\t')
            print(f"✅ Loaded {len(df)} pairs records from initial claims data")
            return df
        except Exception as e:
            print(f"⚠️ Error loading pairs data: {e}")
            return pd.DataFrame()
    
    def load_prices_data(self) -> pd.DataFrame:
        """Load initial claims prices data"""
        try:
            # Read the prices data (tab-separated)
            df = pd.read_csv(self.prices_file, sep='\t')
            print(f"✅ Loaded {len(df)} prices records from initial claims data")
            return df
        except Exception as e:
            print(f"⚠️ Error loading prices data: {e}")
            return pd.DataFrame()
    
    def parse_event_contract(self, contract_str: str) -> Dict:
        """Parse event contract string to extract key information"""
        try:
            # Format: IJC_MMDDYY_XXXXXX (e.g., IJC_080324_244000)
            parts = contract_str.split('_')
            if len(parts) == 3:
                date_part = parts[1]  # MMDDYY
                threshold = parts[2]   # XXXXXX
                
                # Parse date
                month = int(date_part[:2])
                day = int(date_part[2:4])
                year = 2000 + int(date_part[4:6])
                
                # Parse threshold (remove leading zeros)
                threshold_value = int(threshold)
                
                return {
                    'month': month,
                    'day': day,
                    'year': year,
                    'threshold': threshold_value,
                    'date': datetime(year, month, day),
                    'contract_type': 'Initial Claims'
                }
            return {}
        except Exception as e:
            print(f"⚠️ Error parsing contract {contract_str}: {e}")
            return {}
    
    def analyze_pairs_sentiment(self, df: pd.DataFrame) -> Dict:
        """Analyze sentiment from pairs data"""
        if df.empty:
            return {}
        
        # Parse contracts and extract thresholds
        df['contract_info'] = df['event_contract'].apply(self.parse_event_contract)
        
        # Filter valid contracts
        valid_contracts = df[df['contract_info'].apply(lambda x: bool(x))]
        
        if valid_contracts.empty:
            return {}
        
        # Calculate sentiment metrics
        total_volume = valid_contracts['quantity'].sum()
        total_trades = len(valid_contracts)
        
        # Analyze price movements (yes_price vs no_price)
        valid_contracts['price_spread'] = valid_contracts['yes_price'] - valid_contracts['no_price']
        valid_contracts['price_ratio'] = valid_contracts['yes_price'] / valid_contracts['no_price']
        
        # Calculate sentiment score based on price spreads
        # Positive spread indicates bullish sentiment on initial claims
        avg_spread = valid_contracts['price_spread'].mean()
        avg_ratio = valid_contracts['price_ratio'].mean()
        
        # Normalize sentiment score (-1 to 1)
        # Higher yes_price relative to no_price indicates higher initial claims expectations
        sentiment_score = (avg_ratio - 1.0) * 2  # Convert 0.5-2.0 range to -1 to 1
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Interpret sentiment
        if sentiment_score > 0.3:
            sentiment_interpretation = "Bearish (Higher Claims Expected)"
        elif sentiment_score < -0.3:
            sentiment_interpretation = "Bullish (Lower Claims Expected)"
        else:
            sentiment_interpretation = "Neutral"
        
        return {
            'sentiment_score': round(sentiment_score, 4),
            'sentiment_interpretation': sentiment_interpretation,
            'total_volume': int(total_volume),
            'total_trades': int(total_trades),
            'avg_price_spread': round(avg_spread, 4),
            'avg_price_ratio': round(avg_ratio, 4),
            'contracts_analyzed': len(valid_contracts),
            'confidence': min(0.95, 0.7 + (total_trades / 1000) * 0.25)  # Scale confidence with data volume
        }
    
    def analyze_threshold_distribution(self, df: pd.DataFrame) -> Dict:
        """Analyze distribution of initial claims thresholds"""
        if df.empty:
            return {}
        
        # Parse contracts
        df['contract_info'] = df['event_contract'].apply(self.parse_event_contract)
        valid_contracts = df[df['contract_info'].apply(lambda x: bool(x))]
        
        if valid_contracts.empty:
            return {}
        
        # Extract thresholds
        thresholds = [contract['threshold'] for contract in valid_contracts['contract_info']]
        
        if not thresholds:
            return {}
        
        # Calculate threshold statistics
        threshold_stats = {
            'min_threshold': min(thresholds),
            'max_threshold': max(thresholds),
            'mean_threshold': np.mean(thresholds),
            'median_threshold': np.median(thresholds),
            'std_threshold': np.std(thresholds),
            'threshold_range': max(thresholds) - min(thresholds)
        }
        
        # Analyze threshold trends over time
        df_with_dates = valid_contracts.copy()
        df_with_dates['date'] = df_with_dates['contract_info'].apply(lambda x: x.get('date'))
        df_with_dates = df_with_dates.dropna(subset=['date'])
        
        if not df_with_dates.empty:
            # Sort by date and analyze trends
            df_with_dates = df_with_dates.sort_values('date')
            
            # Calculate trend (positive = increasing thresholds, negative = decreasing)
            if len(df_with_dates) > 1:
                x = np.arange(len(df_with_dates))
                y = df_with_dates['contract_info'].apply(lambda x: x.get('threshold', 0))
                
                if len(y) > 1:
                    slope = np.polyfit(x, y, 1)[0]
                    threshold_stats['trend_slope'] = round(slope, 2)
                    threshold_stats['trend_direction'] = 'Increasing' if slope > 0 else 'Decreasing'
                else:
                    threshold_stats['trend_slope'] = 0
                    threshold_stats['trend_direction'] = 'Stable'
            else:
                threshold_stats['trend_slope'] = 0
                threshold_stats['trend_direction'] = 'Single Data Point'
        
        return threshold_stats
    
    def analyze_temporal_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze temporal patterns in the data"""
        if df.empty:
            return {}
        
        # Parse contracts and dates
        df['contract_info'] = df['event_contract'].apply(self.parse_event_contract)
        valid_contracts = df[df['contract_info'].apply(lambda x: bool(x))]
        
        if valid_contracts.empty:
            return {}
        
        # Extract dates and pair times
        df_with_dates = valid_contracts.copy()
        df_with_dates['contract_date'] = df_with_dates['contract_info'].apply(lambda x: x.get('date'))
        df_with_dates['pair_datetime'] = pd.to_datetime(df_with_dates['pair_time'])
        
        # Filter valid dates
        df_with_dates = df_with_dates.dropna(subset=['contract_date', 'pair_datetime'])
        
        if df_with_dates.empty:
            return {}
        
        # Analyze temporal patterns
        temporal_analysis = {}
        
        # Contract expiration patterns
        contract_dates = df_with_dates['contract_date'].dt.date.value_counts().sort_index()
        temporal_analysis['contract_expirations'] = {
            'total_expirations': len(contract_dates),
            'date_range': {
                'start': contract_dates.index.min().isoformat() if len(contract_dates) > 0 else None,
                'end': contract_dates.index.max().isoformat() if len(contract_dates) > 0 else None
            }
        }
        
        # Trading activity patterns
        df_with_dates['hour'] = df_with_dates['pair_datetime'].dt.hour
        df_with_dates['day_of_week'] = df_with_dates['pair_datetime'].dt.day_name()
        
        # Peak trading hours
        hourly_activity = df_with_dates['hour'].value_counts().sort_index()
        if not hourly_activity.empty:
            peak_hour = hourly_activity.idxmax()
            temporal_analysis['trading_patterns'] = {
                'peak_trading_hour': int(peak_hour),
                'total_trading_hours': len(hourly_activity),
                'hourly_distribution': hourly_activity.to_dict()
            }
        
        # Day of week patterns
        daily_activity = df_with_dates['day_of_week'].value_counts()
        if not daily_activity.empty:
            peak_day = daily_activity.idxmax()
            temporal_analysis['daily_patterns'] = {
                'peak_trading_day': peak_day,
                'daily_distribution': daily_activity.to_dict()
            }
        
        return temporal_analysis
    
    def process_initial_claims_data(self) -> Dict:
        """Process all initial claims trade data and generate comprehensive analysis"""
        print("🔄 Processing Initial Claims Trade Data...")
        print(f"Foundation ID: {self.foundation_id}")
        print("="*60)
        
        # Load data
        self.pairs_data = self.load_pairs_data()
        self.prices_data = self.load_prices_data()
        
        if self.pairs_data.empty and self.prices_data.empty:
            print("⚠️ No initial claims data available")
            return self.get_default_analysis()
        
        # Analyze pairs data
        pairs_analysis = {}
        if not self.pairs_data.empty:
            print("📊 Analyzing pairs data...")
            pairs_analysis = {
                'sentiment': self.analyze_pairs_sentiment(self.pairs_data),
                'thresholds': self.analyze_threshold_distribution(self.pairs_data),
                'temporal_patterns': self.analyze_temporal_patterns(self.pairs_data)
            }
        
        # Analyze prices data (if available)
        prices_analysis = {}
        if not self.prices_data.empty:
            print("📈 Analyzing prices data...")
            # For now, use similar analysis as pairs
            prices_analysis = {
                'sentiment': self.analyze_pairs_sentiment(self.prices_data),
                'thresholds': self.analyze_threshold_distribution(self.prices_data),
                'temporal_patterns': self.analyze_temporal_patterns(self.prices_data)
            }
        
        # Combine analysis
        combined_analysis = {
            'foundation_id': self.foundation_id,
            'version': self.version,
            'processed_date': self.current_date.isoformat(),
            'data_summary': {
                'pairs_records': len(self.pairs_data) if not self.pairs_data.empty else 0,
                'prices_records': len(self.prices_data) if not self.prices_data.empty else 0,
                'total_records': len(self.pairs_data) + len(self.prices_data)
            },
            'pairs_analysis': pairs_analysis,
            'prices_analysis': prices_analysis,
            'integrated_sentiment': self.integrate_sentiment(pairs_analysis, prices_analysis),
            'market_insights': self.generate_market_insights(pairs_analysis, prices_analysis)
        }
        
        self.processed_analysis = combined_analysis
        print("✅ Initial claims data processing complete!")
        
        return combined_analysis
    
    def integrate_sentiment(self, pairs_analysis: Dict, prices_analysis: Dict) -> Dict:
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
        
        if pairs_analysis and 'sentiment' in pairs_analysis:
            pairs_sentiment = pairs_analysis['sentiment']
            if 'sentiment_score' in pairs_sentiment:
                weight = pairs_sentiment.get('total_trades', 0) / 1000  # Normalize weight
                weighted_sentiment += pairs_sentiment['sentiment_score'] * weight
                total_weight += weight
                total_confidence += pairs_sentiment.get('confidence', 0) * weight
                integrated['data_source_weights']['pairs'] = round(weight, 4)
        
        if prices_analysis and 'sentiment' in prices_analysis:
            prices_sentiment = prices_analysis['sentiment']
            if 'sentiment_score' in prices_sentiment:
                weight = prices_sentiment.get('total_trades', 0) / 1000  # Normalize weight
                weighted_sentiment += prices_sentiment['sentiment_score'] * weight
                total_weight += weight
                total_confidence += prices_sentiment.get('confidence', 0) * weight
                integrated['data_source_weights']['prices'] = round(weight, 4)
        
        if total_weight > 0:
            integrated['overall_sentiment_score'] = round(weighted_sentiment / total_weight, 4)
            integrated['confidence'] = round(total_confidence / total_weight, 4)
            
            # Interpret overall sentiment
            score = integrated['overall_sentiment_score']
            if score > 0.3:
                integrated['overall_sentiment_interpretation'] = 'Bearish (Higher Claims Expected)'
            elif score < -0.3:
                integrated['overall_sentiment_interpretation'] = 'Bullish (Lower Claims Expected)'
            else:
                integrated['overall_sentiment_interpretation'] = 'Neutral'
        
        return integrated
    
    def generate_market_insights(self, pairs_analysis: Dict, prices_analysis: Dict) -> Dict:
        """Generate market insights from the analysis"""
        insights = {
            'key_findings': [],
            'risk_factors': [],
            'opportunities': [],
            'market_dynamics': {}
        }
        
        # Analyze sentiment trends
        if pairs_analysis and 'sentiment' in pairs_analysis:
            sentiment = pairs_analysis['sentiment']
            if 'sentiment_score' in sentiment:
                score = sentiment['sentiment_score']
                if score > 0.5:
                    insights['key_findings'].append("Strong bearish sentiment indicates market expects higher initial claims")
                    insights['risk_factors'].append("Potential economic slowdown reflected in claims expectations")
                elif score < -0.5:
                    insights['key_findings'].append("Strong bullish sentiment indicates market expects lower initial claims")
                    insights['opportunities'].append("Positive economic outlook reflected in claims expectations")
        
        # Analyze threshold trends
        if pairs_analysis and 'thresholds' in pairs_analysis:
            thresholds = pairs_analysis['thresholds']
            if 'trend_direction' in thresholds:
                direction = thresholds['trend_direction']
                if direction == 'Increasing':
                    insights['key_findings'].append("Rising threshold levels suggest market adjusting to higher claims environment")
                    insights['market_dynamics']['threshold_trend'] = 'Increasing'
                elif direction == 'Decreasing':
                    insights['key_findings'].append("Falling threshold levels suggest market adjusting to lower claims environment")
                    insights['market_dynamics']['threshold_trend'] = 'Decreasing'
        
        # Trading activity insights
        if pairs_analysis and 'temporal_patterns' in pairs_analysis:
            temporal = pairs_analysis['temporal_patterns']
            if 'trading_patterns' in temporal:
                peak_hour = temporal['trading_patterns'].get('peak_trading_hour')
                if peak_hour:
                    insights['market_dynamics']['peak_trading_hour'] = peak_hour
                    insights['key_findings'].append(f"Peak trading activity occurs at {peak_hour}:00")
        
        return insights
    
    def get_default_analysis(self) -> Dict:
        """Get default analysis if no data is available"""
        return {
            'foundation_id': self.foundation_id,
            'version': self.version,
            'processed_date': self.current_date.isoformat(),
            'data_summary': {
                'pairs_records': 0,
                'prices_records': 0,
                'total_records': 0
            },
            'pairs_analysis': {},
            'prices_analysis': {},
            'integrated_sentiment': {
                'overall_sentiment_score': 0.0,
                'overall_sentiment_interpretation': 'Neutral',
                'data_source_weights': {},
                'confidence': 0.0
            },
            'market_insights': {
                'key_findings': ['No initial claims data available'],
                'risk_factors': [],
                'opportunities': [],
                'market_dynamics': {}
            }
        }
    
    def save_analysis(self, filename: str = "initial_claims_analysis.json") -> str:
        """Save the processed analysis to a JSON file"""
        if not self.processed_analysis:
            print("⚠️ No analysis to save. Run process_initial_claims_data() first.")
            return ""
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.processed_analysis, f, indent=2)
            
            print(f"✅ Initial claims analysis saved to: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ Error saving analysis: {e}")
            return ""
    
    def print_summary(self):
        """Print a summary of the processed data"""
        if not self.processed_analysis:
            print("⚠️ No analysis available. Run process_initial_claims_data() first.")
            return
        
        print("\n" + "="*60)
        print("INITIAL CLAIMS TRADE DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Version: {self.version}")
        print(f"Processed Date: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Data summary
        data_summary = self.processed_analysis['data_summary']
        print(f"\n📊 DATA SUMMARY:")
        print(f"  Pairs Records: {data_summary['pairs_records']:,}")
        print(f"  Prices Records: {data_summary['prices_records']:,}")
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
    processor = InitialClaimsDataProcessor()
    
    # Process the data
    analysis = processor.process_initial_claims_data()
    
    # Save analysis
    processor.save_analysis()
    
    # Print summary
    processor.print_summary()
    
    return analysis

if __name__ == "__main__":
    main()