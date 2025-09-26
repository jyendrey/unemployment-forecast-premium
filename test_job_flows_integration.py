#!/usr/bin/env python3
"""
Test Job Flows Integration
Tests the BLS CPS job flows integration with the enhanced forecasting system
"""

import json
from datetime import datetime
from bls_cps_job_flows_fetcher import BLSCPSJobFlowsFetcher
from enhanced_forecast_with_job_flows import EnhancedUnemploymentForecasterWithJobFlows

def test_job_flows_fetcher():
    """Test the BLS CPS job flows fetcher"""
    print("🧪 Testing BLS CPS Job Flows Fetcher...")
    print("="*50)
    
    fetcher = BLSCPSJobFlowsFetcher()
    
    # Test fallback data generation
    print("📊 Testing fallback data generation...")
    fallback_data = fetcher.get_fallback_job_flows_data()
    
    if fallback_data:
        print("✅ Fallback data generated successfully")
        print(f"   Flows available: {list(fallback_data.keys())}")
        
        # Test job finding rate calculation
        job_finding_rate = fetcher.calculate_job_finding_rate(fallback_data)
        print(f"   Job Finding Rate: {job_finding_rate:.4f}")
        
        # Test job separation rate calculation
        job_separation_rate = fetcher.calculate_job_separation_rate(fallback_data)
        print(f"   Job Separation Rate: {job_separation_rate:.4f}")
        
        # Test net flows calculation
        net_flows = fetcher.calculate_net_job_flows(fallback_data)
        print(f"   Net Employment Growth: {net_flows['net_employment_growth']:,.0f}")
        
    else:
        print("❌ Fallback data generation failed")
        return False
    
    return True

def test_enhanced_forecaster():
    """Test the enhanced forecaster with job flows"""
    print("\n🧪 Testing Enhanced Forecaster with Job Flows...")
    print("="*50)
    
    forecaster = EnhancedUnemploymentForecasterWithJobFlows()
    
    # Test job flows data loading
    print("📊 Testing job flows data loading...")
    job_flows_data = forecaster.job_flows_data
    
    if job_flows_data:
        print("✅ Job flows data loaded successfully")
        print(f"   Data quality: {job_flows_data.get('data_quality', 'Unknown')}")
        
        if 'key_metrics' in job_flows_data:
            metrics = job_flows_data['key_metrics']
            print(f"   Job Finding Rate: {metrics.get('job_finding_rate', 'N/A')}")
            print(f"   Job Separation Rate: {metrics.get('job_separation_rate', 'N/A')}")
    else:
        print("⚠️ Job flows data not available, using defaults")
    
    # Test forecast calculation
    print("\n📊 Testing forecast calculation...")
    try:
        forecast, adjustments = forecaster.calculate_enhanced_forecast_with_job_flows()
        print(f"✅ Forecast calculated successfully: {forecast:.2f}%")
        print(f"   Number of adjustments: {len(adjustments)}")
        
        # Check for job flows adjustments
        job_flows_adjustments = [adj for adj in adjustments if 'Job' in adj[0] or 'Net' in adj[0]]
        print(f"   Job flows adjustments: {len(job_flows_adjustments)}")
        for adj in job_flows_adjustments:
            print(f"     - {adj[0]}: {adj[1]:.4f}%")
            
    except Exception as e:
        print(f"❌ Forecast calculation failed: {e}")
        return False
    
    # Test confidence calculation
    print("\n📊 Testing confidence calculation...")
    try:
        confidence = forecaster.calculate_enhanced_confidence_with_job_flows()
        print(f"✅ Confidence calculated successfully: {confidence:.1f}%")
    except Exception as e:
        print(f"❌ Confidence calculation failed: {e}")
        return False
    
    return True

def test_report_generation():
    """Test report generation with job flows"""
    print("\n🧪 Testing Report Generation...")
    print("="*50)
    
    forecaster = EnhancedUnemploymentForecasterWithJobFlows()
    
    try:
        # Calculate forecast and confidence
        forecast, adjustments = forecaster.calculate_enhanced_forecast_with_job_flows()
        confidence = forecaster.calculate_enhanced_confidence_with_job_flows()
        
        # Generate report
        report = forecaster.create_enhanced_report_with_job_flows(forecast, adjustments, confidence)
        
        print("✅ Report generated successfully")
        print(f"   Report version: {report['version']}")
        print(f"   Job flows analysis included: {'job_flows_analysis' in report}")
        
        if 'job_flows_analysis' in report:
            job_flows = report['job_flows_analysis']
            print(f"   Job Finding Rate: {job_flows.get('job_finding_rate', 'N/A')}")
            print(f"   Job Separation Rate: {job_flows.get('job_separation_rate', 'N/A')}")
            print(f"   Data Quality: {job_flows.get('data_quality', 'N/A')}")
        
        # Check for job flows adjustments in report
        job_flows_adjustments = [adj for adj in report['enhanced_adjustments'] if 'Job' in adj['adjustment_name'] or 'Net' in adj['adjustment_name']]
        print(f"   Job flows adjustments in report: {len(job_flows_adjustments)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Job Flows Integration Tests")
    print("="*60)
    
    tests = [
        ("BLS CPS Job Flows Fetcher", test_job_flows_fetcher),
        ("Enhanced Forecaster with Job Flows", test_enhanced_forecaster),
        ("Report Generation", test_report_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Job flows integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()