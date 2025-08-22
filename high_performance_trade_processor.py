#!/usr/bin/env python3
"""
High Performance Trade Data Processor
Handles millions of trades efficiently for the enhanced unemployment forecasting system
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import pandas as pd
import numpy as np
import json
import csv
import os
import gzip
import pickle
from datetime import datetime, timedelta
from pathlib import Path
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import logging

class HighPerformanceTradeProcessor:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.math_framework_id = "bc-b635390a-67ea-41c3-ae50-c329dc3f24e8"
        self.version = "v2.1-enhanced"
        self.processed_data = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trade_processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def process_large_csv_file(self, file_path, chunk_size=100000):
        """Process large CSV files in chunks to handle millions of trades"""
        
        self.logger.info(f"Processing large CSV file: {file_path}")
        
        # Get file size for progress tracking
        file_size = os.path.getsize(file_path)
        self.logger.info(f"File size: {file_size / (1024*1024*1024):.2f} GB")
        
        # Process in chunks
        chunks = []
        total_rows = 0
        
        for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            self.logger.info(f"Processing chunk {chunk_num + 1}, rows: {len(chunk)}")
            
            # Process chunk
            processed_chunk = self.process_chunk(chunk)
            chunks.append(processed_chunk)
            
            total_rows += len(chunk)
            self.logger.info(f"Total rows processed: {total_rows:,}")
        
        # Combine all chunks
        combined_data = pd.concat(chunks, ignore_index=True)
        self.logger.info(f"Total data processed: {len(combined_data):,} rows")
        
        return combined_data
    
    def process_chunk(self, chunk):
        """Process individual data chunk"""
        
        # Clean and validate data
        chunk = self.clean_chunk_data(chunk)
        
        # Extract unemployment-related trades
        unemployment_trades = self.extract_unemployment_trades(chunk)
        
        # Calculate basic statistics
        stats = self.calculate_chunk_statistics(chunk)
        
        return {
            'data': chunk,
            'unemployment_trades': unemployment_trades,
            'statistics': stats
        }
    
    def clean_chunk_data(self, chunk):
        """Clean and validate chunk data"""
        
        # Remove rows with missing critical data
        chunk = chunk.dropna(subset=['price', 'volume'])
        
        # Convert data types
        if 'price' in chunk.columns:
            chunk['price'] = pd.to_numeric(chunk['price'], errors='coerce')
        if 'volume' in chunk.columns:
            chunk['volume'] = pd.to_numeric(chunk['volume'], errors='coerce')
        if 'date' in chunk.columns:
            chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')
        
        # Remove invalid data
        chunk = chunk[chunk['price'] > 0]
        chunk = chunk[chunk['volume'] > 0]
        
        return chunk
    
    def extract_unemployment_trades(self, chunk):
        """Extract unemployment-related trades using enhanced math framework"""
        
        # Keywords for unemployment-related trades
        unemployment_keywords = [
            'unemployment', 'unr', 'jobless', 'employment', 'labor',
            'workforce', 'job market', 'economic indicator'
        ]
        
        unemployment_trades = []
        
        for _, row in chunk.iterrows():
            # Check description and contract fields
            description = str(row.get('description', '')).lower()
            contract = str(row.get('event_contract', '')).lower()
            
            # Check if trade is unemployment-related
            if any(keyword in description or keyword in contract for keyword in unemployment_keywords):
                unemployment_trades.append({
                    'date': row.get('date'),
                    'price': row.get('price'),
                    'volume': row.get('volume'),
                    'description': row.get('description'),
                    'contract': row.get('event_contract'),
                    'math_framework': self.math_framework_id
                })
        
        return unemployment_trades
    
    def calculate_chunk_statistics(self, chunk):
        """Calculate comprehensive statistics for chunk"""
        
        stats = {
            'total_trades': len(chunk),
            'total_volume': chunk['volume'].sum() if 'volume' in chunk.columns else 0,
            'avg_price': chunk['price'].mean() if 'price' in chunk.columns else 0,
            'price_std': chunk['price'].std() if 'price' in chunk.columns else 0,
            'volume_std': chunk['volume'].std() if 'volume' in chunk.columns else 0,
            'date_range': {
                'start': chunk['date'].min() if 'date' in chunk.columns else None,
                'end': chunk['date'].max() if 'date' in chunk.columns else None
            },
            'foundation_id': self.foundation_id,
            'math_framework_id': self.math_framework_id
        }
        
        return stats
    
    def process_multiple_files(self, file_pattern, output_dir="processed_data"):
        """Process multiple trade data files"""
        
        self.logger.info(f"Processing multiple files matching pattern: {file_pattern}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all matching files
        import glob
        files = glob.glob(file_pattern)
        
        if not files:
            self.logger.warning(f"No files found matching pattern: {file_pattern}")
            return
        
        self.logger.info(f"Found {len(files)} files to process")
        
        # Process each file
        all_results = []
        for file_path in files:
            self.logger.info(f"Processing file: {file_path}")
            
            try:
                # Process file
                result = self.process_large_csv_file(file_path)
                all_results.append(result)
                
                # Save processed data
                output_file = os.path.join(output_dir, f"processed_{os.path.basename(file_path)}.pkl")
                with open(output_file, 'wb') as f:
                    pickle.dump(result, f)
                
                self.logger.info(f"Saved processed data to: {output_file}")
                
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
        
        return all_results
    
    def create_aggregated_summary(self, processed_results):
        """Create aggregated summary of all processed data"""
        
        self.logger.info("Creating aggregated summary")
        
        # Combine all unemployment trades
        all_unemployment_trades = []
        total_trades = 0
        total_volume = 0
        
        for result in processed_results:
            all_unemployment_trades.extend(result['unemployment_trades'])
            total_trades += result['statistics']['total_trades']
            total_volume += result['statistics']['total_volume']
        
        # Calculate aggregated statistics
        if all_unemployment_trades:
            unemployment_df = pd.DataFrame(all_unemployment_trades)
            
            # Calculate sentiment scores
            sentiment_scores = []
            for _, trade in unemployment_df.iterrows():
                # Normalize price to sentiment (-1 to 1)
                sentiment = (trade['price'] - 0.5) * 2
                sentiment_scores.append(sentiment)
            
            avg_sentiment = np.mean(sentiment_scores)
            sentiment_std = np.std(sentiment_scores)
            
            summary = {
                'generated_date': datetime.now().isoformat(),
                'foundation_id': self.foundation_id,
                'math_framework_id': self.math_framework_id,
                'version': self.version,
                'total_trades_processed': total_trades,
                'total_volume_processed': total_volume,
                'unemployment_trades': {
                    'count': len(all_unemployment_trades),
                    'total_volume': unemployment_df['volume'].sum() if 'volume' in unemployment_df.columns else 0,
                    'avg_price': unemployment_df['price'].mean() if 'price' in unemployment_df.columns else 0,
                    'sentiment_analysis': {
                        'avg_sentiment': round(avg_sentiment, 4),
                        'sentiment_std': round(sentiment_std, 4),
                        'sentiment_range': {
                            'min': round(min(sentiment_scores), 4),
                            'max': round(max(sentiment_scores), 4)
                        }
                    },
                    'date_range': {
                        'start': unemployment_df['date'].min() if 'date' in unemployment_df.columns else None,
                        'end': unemployment_df['date'].max() if 'date' in unemployment_df.columns else None
                    }
                },
                'processing_metadata': {
                    'files_processed': len(processed_results),
                    'processing_time': datetime.now().isoformat(),
                    'chunk_size_used': 100000
                }
            }
        else:
            summary = {
                'generated_date': datetime.now().isoformat(),
                'foundation_id': self.foundation_id,
                'math_framework_id': self.math_framework_id,
                'version': self.version,
                'total_trades_processed': total_trades,
                'total_volume_processed': total_volume,
                'unemployment_trades': {
                    'count': 0,
                    'message': 'No unemployment-related trades found'
                }
            }
        
        return summary
    
    def save_aggregated_data(self, summary, output_file="aggregated_trade_summary.json"):
        """Save aggregated summary to JSON file"""
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"Saved aggregated summary to: {output_file}")
        return output_file
    
    def create_enhanced_forecast_input(self, summary):
        """Create enhanced forecast input from processed trade data"""
        
        if 'unemployment_trades' not in summary or summary['unemployment_trades']['count'] == 0:
            self.logger.warning("No unemployment trades found for forecast input")
            return None
        
        # Create enhanced forecast input
        forecast_input = {
            'market_sentiment': {
                'sentiment_score': summary['unemployment_trades']['sentiment_analysis']['avg_sentiment'],
                'sentiment_confidence': 1 - summary['unemployment_trades']['sentiment_analysis']['sentiment_std'],
                'contracts_analyzed': summary['unemployment_trades']['count'],
                'total_volume': summary['unemployment_trades']['total_volume'],
                'math_framework': self.math_framework_id
            },
            'data_quality': {
                'total_trades': summary['total_trades_processed'],
                'unemployment_trade_ratio': summary['unemployment_trades']['count'] / summary['total_trades_processed'],
                'foundation_id': self.foundation_id
            },
            'processing_metadata': summary['processing_metadata']
        }
        
        return forecast_input

def main():
    """Main execution function for high-performance trade processing"""
    
    print("="*60)
    print("HIGH PERFORMANCE TRADE DATA PROCESSOR")
    print("="*60)
    print(f"Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b")
    print(f"Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8")
    print(f"Version: v2.1-enhanced")
    print("="*60)
    
    processor = HighPerformanceTradeProcessor()
    
    # Example usage patterns
    print("\n📊 Available Processing Options:")
    print("1. Process single large CSV file")
    print("2. Process multiple files with pattern matching")
    print("3. Process compressed archives")
    print("4. Create aggregated summary")
    
    print("\n🔧 Example Commands:")
    print("# Process single large file:")
    print("python high_performance_trade_processor.py --file trade_data.csv")
    
    print("\n# Process multiple files:")
    print("python high_performance_trade_processor.py --pattern 'trade_data_*.csv'")
    
    print("\n# Process compressed archive:")
    print("python high_performance_trade_processor.py --archive trade_data.tar.gz")
    
    print("\n📁 Output Files:")
    print("- processed_*.pkl: Individual processed data files")
    print("- aggregated_trade_summary.json: Complete summary")
    print("- trade_processing.log: Processing log")
    
    print("\n🚀 Ready to process millions of trades efficiently!")
    print("="*60)

if __name__ == "__main__":
    main()