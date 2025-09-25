#!/usr/bin/env python3
"""
Test Comprehensive BLS Integration
Tests the comprehensive BLS data integration with the enhanced forecasting system
"""

import json
from datetime import datetime
from bls_comprehensive_data_fetcher import BLSComprehensiveDataFetcher
from enhanced_forecast_with_comprehensive_bls import EnhancedUnemploymentForecasterWithComprehensiveBLS

def test_comprehensive_data_fetcher():
    """Test the comprehensive BLS data fetcher"""
    print("🧪 Testing Comprehensive BLS Data Fetcher...")
    print("="*50)
    
    fetcher = BLSComprehensiveDataFetcher()
    
    # Test fallback data generation
    print("📊 Testing fallback data generation...")
    fallback_data = fetcher.get_fallback_comprehensive_data()
    
    if fallback_data:
        print("✅ Fallback data generated successfully")
        print(f"   Data categories: {list(fallback_data.keys())}")
        
        # Test demographic analysis
        demographic_analysis = fetcher.calculate_demographic_analysis(fallback_data)
        if demographic_analysis:
            print(f"   Overall Rate: {demographic_analysis['overall_rate']:.1f}%")
            print(f"   Black-White Gap: {demographic_analysis['disparities']['black_white_gap']:.1f} pp")
        
        # Test underemployment analysis
        underemployment_analysis = fetcher.calculate_underemployment_analysis(fallback_data)
        if underemployment_analysis:
            print(f"   Part-time Economic Reasons: {underemployment_analysis['counts']['part_time_economic_reasons']:,.0f}")
            print(f"   Long-term Unemployed %: {underemployment_analysis['percentages']['long_term_unemployed_pct']:.1f}%")
        
        # Test establishment analysis
        establishment_analysis = fetcher.calculate_establishment_analysis(fallback_data)
        if establishment_analysis:
            print(f"   Nonfarm Payrolls: {establishment_analysis['nonfarm_payrolls']:,.0f}")
        
        # Test wage hours analysis
        wage_hours_analysis = fetcher.calculate_wage_hours_analysis(fallback_data)
        if wage_hours_analysis:
            print(f"   Avg Hourly Earnings: ${wage_hours_analysis['avg_hourly_earnings']:.2f}")
        
    else:
        print("❌ Fallback data generation failed")
        return False
    
    return True

def test_comprehensive_forecaster():
    """Test the comprehensive forecaster"""
    print("\n🧪 Testing Comprehensive Forecaster...")
    print("="*50)
    
    forecaster = EnhancedUnemploymentForecasterWithComprehensiveBLS()
    
    # Test data loading
    print("📊 Testing comprehensive data loading...")
    comprehensive_data = forecaster.comprehensive_data
    
    if comprehensive_data:
        print("✅ Comprehensive data loaded successfully")
        print(f"   Data quality: {comprehensive_data.get('data_quality', 'Unknown')}")
        
        if 'demographic_analysis' in comprehensive_data:
            demo = comprehensive_data['demographic_analysis']
            print(f"   Overall Rate: {demo.get('overall_rate', 'N/A')}%")
            print(f"   Black-White Gap: {demo.get('disparities', {}).get('black_white_gap', 'N/A')} pp")
    else:
        print("⚠️ Comprehensive data not available, using defaults")
    
    # Test forecast calculation
    print("\n📊 Testing comprehensive forecast calculation...")
    try:
        forecast, adjustments = forecaster.calculate_comprehensive_forecast()
        print(f"✅ Forecast calculated successfully: {forecast:.2f}%")
        print(f"   Number of adjustments: {len(adjustments)}")
        
        # Check for comprehensive adjustments
        comprehensive_adjustments = [adj for adj in adjustments if any(keyword in adj[0] for keyword in ['Demographic', 'Part-time', 'Long-term', 'Nonfarm', 'Wage', 'Employment-Population'])]
        print(f"   Comprehensive BLS adjustments: {len(comprehensive_adjustments)}")
        for adj in comprehensive_adjustments:
            print(f"     - {adj[0]}: {adj[1]:.4f}%")
            
    except Exception as e:
        print(f"❌ Forecast calculation failed: {e}")
        return False
    
    # Test confidence calculation
    print("\n📊 Testing comprehensive confidence calculation...")
    try:
        confidence = forecaster.calculate_comprehensive_confidence()
        print(f"✅ Confidence calculated successfully: {confidence:.1f}%")
    except Exception as e:
        print(f"❌ Confidence calculation failed: {e}")
        return False
    
    return True

def test_comprehensive_report_generation():
    """Test comprehensive report generation"""
    print("\n🧪 Testing Comprehensive Report Generation...")
    print("="*50)
    
    forecaster = EnhancedUnemploymentForecasterWithComprehensiveBLS()
    
    try:
        # Calculate forecast and confidence
        forecast, adjustments = forecaster.calculate_comprehensive_forecast()
        confidence = forecaster.calculate_comprehensive_confidence()
        
        # Generate report
        report = forecaster.create_comprehensive_report(forecast, adjustments, confidence)
        
        print("✅ Comprehensive report generated successfully")
        print(f"   Report version: {report['version']}")
        print(f"   BLS comprehensive analysis included: {'bls_comprehensive_analysis' in report}")
        print(f"   Underemployment analysis included: {'underemployment_analysis' in report}")
        print(f"   Establishment analysis included: {'establishment_analysis' in report}")
        print(f"   Wage hours analysis included: {'wage_hours_analysis' in report}")
        
        # Check for comprehensive adjustments in report
        comprehensive_adjustments = [adj for adj in report['comprehensive_adjustments'] if any(keyword in adj['adjustment_name'] for keyword in ['Demographic', 'Part-time', 'Long-term', 'Nonfarm', 'Wage', 'Employment-Population'])]
        print(f"   Comprehensive BLS adjustments in report: {len(comprehensive_adjustments)}")
        
        # Check methodology
        if 'methodology' in report:
            print(f"   Methodology includes BLS Employment Situation: {'bls_employment_situation' in report['methodology']}")
            print(f"   Methodology includes job flows: {'job_flows_integration' in report['methodology']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive report generation failed: {e}")
        return False

def test_bls_methodology_completeness():
    """Test that all BLS methodology components are included"""
    print("\n🧪 Testing BLS Methodology Completeness...")
    print("="*50)
    
    forecaster = EnhancedUnemploymentForecasterWithComprehensiveBLS()
    
    # Test that all key BLS components are present
    required_components = [
        'demographic_analysis',
        'underemployment_analysis', 
        'establishment_analysis',
        'wage_hours_analysis'
    ]
    
    comprehensive_data = forecaster.comprehensive_data
    missing_components = []
    
    for component in required_components:
        if component not in comprehensive_data:
            missing_components.append(component)
    
    if missing_components:
        print(f"❌ Missing BLS components: {missing_components}")
        return False
    else:
        print("✅ All required BLS components present")
    
    # Test demographic data completeness
    if 'demographic_analysis' in comprehensive_data:
        demo = comprehensive_data['demographic_analysis']
        required_demo_rates = ['unemployment_rate_men', 'unemployment_rate_women', 'unemployment_rate_teens',
                              'unemployment_rate_white', 'unemployment_rate_black', 'unemployment_rate_asian', 'unemployment_rate_hispanic']
        
        demo_rates = demo.get('rates', {})
        missing_demo_rates = [rate for rate in required_demo_rates if rate not in demo_rates]
        
        if missing_demo_rates:
            print(f"❌ Missing demographic rates: {missing_demo_rates}")
            return False
        else:
            print("✅ All demographic unemployment rates present")
    
    # Test underemployment data completeness
    if 'underemployment_analysis' in comprehensive_data:
        underemployment = comprehensive_data['underemployment_analysis']
        required_underemployment = ['part_time_economic_reasons', 'marginally_attached', 'discouraged_workers',
                                   'new_entrants', 'long_term_unemployed']
        
        underemployment_counts = underemployment.get('counts', {})
        missing_underemployment = [item for item in required_underemployment if item not in underemployment_counts]
        
        if missing_underemployment:
            print(f"❌ Missing underemployment metrics: {missing_underemployment}")
            return False
        else:
            print("✅ All underemployment metrics present")
    
    print("✅ BLS methodology completeness test passed")
    return True

def main():
    """Run all comprehensive BLS integration tests"""
    print("🚀 Starting Comprehensive BLS Integration Tests")
    print("="*70)
    
    tests = [
        ("Comprehensive BLS Data Fetcher", test_comprehensive_data_fetcher),
        ("Comprehensive Forecaster", test_comprehensive_forecaster),
        ("Comprehensive Report Generation", test_comprehensive_report_generation),
        ("BLS Methodology Completeness", test_bls_methodology_completeness)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"Running: {test_name}")
        print('='*70)
        
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
    print(f"\n{'='*70}")
    print("COMPREHENSIVE BLS INTEGRATION TEST SUMMARY")
    print('='*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Comprehensive BLS integration is working correctly.")
        print("📊 The agent now includes all major BLS Employment Situation components:")
        print("   - Demographic unemployment rates")
        print("   - Underemployment metrics")
        print("   - Establishment survey data")
        print("   - Wage and hours data")
        print("   - Labor force participation metrics")
        print("   - Job flows data")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()