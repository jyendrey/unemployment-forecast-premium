#!/usr/bin/env python3
"""
Trade Data Processing Command Line Interface
Easy-to-use script for processing large trade datasets
Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b
Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8
"""

import argparse
import os
import sys
from high_performance_trade_processor import HighPerformanceTradeProcessor

def main():
    """Main command line interface"""
    
    parser = argparse.ArgumentParser(
        description="Process large trade datasets for enhanced unemployment forecasting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single large CSV file
  python process_trade_data.py --file trade_data_2024.csv
  
  # Process multiple files with pattern matching
  python process_trade_data.py --pattern "trade_data_*.csv"
  
  # Process compressed archive
  python process_trade_data.py --archive trade_data.tar.gz
  
  # Process with custom chunk size
  python process_trade_data.py --file large_file.csv --chunk-size 50000
  
  # Process with custom output directory
  python process_trade_data.py --file data.csv --output-dir custom_output
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file', 
        help='Single CSV file to process'
    )
    input_group.add_argument(
        '--pattern', 
        help='File pattern to match multiple files (e.g., "trade_data_*.csv")'
    )
    input_group.add_argument(
        '--archive', 
        help='Compressed archive file (.tar.gz, .zip) to extract and process'
    )
    
    # Processing options
    parser.add_argument(
        '--chunk-size', 
        type=int, 
        default=100000,
        help='Number of rows to process in each chunk (default: 100000)'
    )
    parser.add_argument(
        '--output-dir', 
        default='processed_data',
        help='Output directory for processed data (default: processed_data)'
    )
    parser.add_argument(
        '--create-forecast-input',
        action='store_true',
        help='Create enhanced forecast input file'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize processor
    print("="*60)
    print("ENHANCED TRADE DATA PROCESSOR")
    print("="*60)
    print(f"Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b")
    print(f"Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8")
    print(f"Version: v2.1-enhanced")
    print("="*60)
    
    processor = HighPerformanceTradeProcessor()
    
    try:
        if args.file:
            # Process single file
            print(f"\n📊 Processing single file: {args.file}")
            
            if not os.path.exists(args.file):
                print(f"❌ Error: File {args.file} not found")
                sys.exit(1)
            
            # Process the file
            result = processor.process_large_csv_file(args.file, args.chunk_size)
            
            # Save processed data
            output_file = os.path.join(args.output_dir, f"processed_{os.path.basename(args.file)}.pkl")
            os.makedirs(args.output_dir, exist_ok=True)
            
            import pickle
            with open(output_file, 'wb') as f:
                pickle.dump(result, f)
            
            print(f"✅ Processed data saved to: {output_file}")
            
            # Create summary
            summary = processor.create_aggregated_summary([result])
            summary_file = processor.save_aggregated_data(summary, "single_file_summary.json")
            print(f"✅ Summary saved to: {summary_file}")
            
        elif args.pattern:
            # Process multiple files
            print(f"\n📊 Processing files matching pattern: {args.pattern}")
            
            import glob
            files = glob.glob(args.pattern)
            
            if not files:
                print(f"❌ Error: No files found matching pattern: {args.pattern}")
                sys.exit(1)
            
            print(f"Found {len(files)} files to process")
            
            # Process all files
            results = processor.process_multiple_files(args.pattern, args.output_dir)
            
            # Create aggregated summary
            summary = processor.create_aggregated_summary(results)
            summary_file = processor.save_aggregated_data(summary, "multi_file_summary.json")
            print(f"✅ Aggregated summary saved to: {summary_file}")
            
        elif args.archive:
            # Process compressed archive
            print(f"\n📊 Processing compressed archive: {args.archive}")
            
            if not os.path.exists(args.archive):
                print(f"❌ Error: Archive {args.archive} not found")
                sys.exit(1)
            
            # Extract archive
            extract_dir = f"extracted_{os.path.splitext(os.path.basename(args.archive))[0]}"
            os.makedirs(extract_dir, exist_ok=True)
            
            if args.archive.endswith('.tar.gz'):
                import tarfile
                with tarfile.open(args.archive, 'r:gz') as tar:
                    tar.extractall(extract_dir)
                print(f"✅ Extracted archive to: {extract_dir}")
                
            elif args.archive.endswith('.zip'):
                import zipfile
                with zipfile.ZipFile(args.archive, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"✅ Extracted archive to: {extract_dir}")
                
            else:
                print(f"❌ Error: Unsupported archive format. Use .tar.gz or .zip")
                sys.exit(1)
            
            # Find CSV files in extracted directory
            csv_files = []
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith('.csv'):
                        csv_files.append(os.path.join(root, file))
            
            if not csv_files:
                print(f"❌ Error: No CSV files found in extracted archive")
                sys.exit(1)
            
            print(f"Found {len(csv_files)} CSV files in archive")
            
            # Process all CSV files
            results = []
            for csv_file in csv_files:
                print(f"Processing: {csv_file}")
                result = processor.process_large_csv_file(csv_file, args.chunk_size)
                results.append(result)
                
                # Save individual processed file
                output_file = os.path.join(args.output_dir, f"processed_{os.path.basename(csv_file)}.pkl")
                os.makedirs(args.output_dir, exist_ok=True)
                
                import pickle
                with open(output_file, 'wb') as f:
                    pickle.dump(result, f)
            
            # Create aggregated summary
            summary = processor.create_aggregated_summary(results)
            summary_file = processor.save_aggregated_data(summary, "archive_summary.json")
            print(f"✅ Archive summary saved to: {summary_file}")
        
        # Create enhanced forecast input if requested
        if args.create_forecast_input and 'summary' in locals():
            forecast_input = processor.create_enhanced_forecast_input(summary)
            if forecast_input:
                forecast_file = "enhanced_forecast_input.json"
                import json
                with open(forecast_file, 'w') as f:
                    json.dump(forecast_input, f, indent=2)
                print(f"✅ Enhanced forecast input saved to: {forecast_file}")
            else:
                print("⚠️ Could not create forecast input (no unemployment trades found)")
        
        print("\n" + "="*60)
        print("PROCESSING COMPLETE!")
        print("="*60)
        print(f"📁 Output directory: {args.output_dir}")
        print(f"📊 Summary files: *_summary.json")
        print(f"🔧 Foundation ID: bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b")
        print(f"🔧 Math Framework ID: bc-b635390a-67ea-41c3-ae50-c329dc3f24e8")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()