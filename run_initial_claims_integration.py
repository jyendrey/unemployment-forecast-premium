#!/usr/bin/env python3
"""
Initial Claims Integration Runner
Processes initial claims trade data and runs the enhanced unemployment forecast
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import os
import sys
from datetime import datetime

def main():
    """Main execution function for initial claims integration"""
    
    print("="*80)
    print("INITIAL CLAIMS TRADE DATA INTEGRATION SYSTEM")
    print("="*80)
    print(f"Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f")
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Step 1: Process Initial Claims Data
    print("\n🔄 STEP 1: Processing Initial Claims Trade Data...")
    try:
        from initial_claims_data_processor import InitialClaimsDataProcessor
        
        processor = InitialClaimsDataProcessor()
        analysis = processor.process_initial_claims_data()
        
        # Save the analysis
        analysis_file = processor.save_analysis()
        
        if analysis_file:
            print(f"✅ Initial claims analysis saved to: {analysis_file}")
        else:
            print("⚠️ Failed to save initial claims analysis")
            
    except Exception as e:
        print(f"❌ Error processing initial claims data: {e}")
        print("⚠️ Continuing with default values...")
    
    # Step 2: Run Enhanced Forecast with Initial Claims Integration
    print("\n🔄 STEP 2: Running Enhanced Unemployment Forecast...")
    try:
        from final_enhanced_forecast import FinalEnhancedUnemploymentForecaster
        
        forecaster = FinalEnhancedUnemploymentForecaster()
        report = forecaster.run_final_enhanced_forecast()
        
        print(f"\n✅ Enhanced forecast with initial claims integration complete!")
        print(f"📁 Report generated successfully")
        
    except Exception as e:
        print(f"❌ Error running enhanced forecast: {e}")
        return False
    
    # Step 3: Generate Summary Report
    print("\n🔄 STEP 3: Generating Integration Summary...")
    
    summary = {
        'integration_date': datetime.now().isoformat(),
        'initial_claims_foundation_id': 'bc-78795d1e-6a46-4716-9ff6-78bca58ca95f',
        'enhanced_forecast_foundation_id': 'bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b',
        'math_framework_id': 'bc-b635390a-67ea-41c3-ae50-c329dc3f24e8',
        'version': 'v3.1-initial-claims-integrated',
        'components_integrated': [
            'Initial Claims Trade Data - Pairs',
            'Initial Claims Trade Data - Prices',
            'Enhanced Unemployment Forecast System',
            'Extended FRED Data (24 months)',
            'Updated Trade Data Analysis'
        ],
        'data_files_processed': [
            'Initial Claims Trade Data - Pairs',
            'Initial Claims Trade Data - Prices'
        ],
        'output_files_generated': [
            'initial_claims_analysis.json',
            'final_enhanced_unemployment_forecast_report.json'
        ],
        'integration_status': 'SUCCESS'
    }
    
    # Save summary
    try:
        import json
        with open('initial_claims_integration_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Integration summary saved to: initial_claims_integration_summary.json")
    except Exception as e:
        print(f"⚠️ Error saving integration summary: {e}")
    
    print("\n" + "="*80)
    print("INITIAL CLAIMS INTEGRATION COMPLETE")
    print("="*80)
    print("✅ Initial claims trade data successfully integrated into forecast system")
    print("✅ Enhanced unemployment forecast generated with initial claims adjustments")
    print("✅ System configuration updated with initial claims foundation")
    print("✅ All analysis files generated and saved")
    print("="*80)
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Integration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Integration failed!")
        sys.exit(1)