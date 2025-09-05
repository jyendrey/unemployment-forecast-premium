#!/usr/bin/env python3
"""
Component Cleanup Analysis
Identifies redundant, overlapping, and unnecessary components
"""

import json
from collections import defaultdict

def analyze_component_redundancy():
    """Analyze the current system for redundant components"""
    print("COMPONENT CLEANUP ANALYSIS")
    print("=" * 50)
    
    # Load current system config
    try:
        with open('enhanced_system_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: enhanced_system_config.json not found")
        return None
    
    weights = config['adjustment_weights']
    
    print("CURRENT COMPONENTS ANALYSIS")
    print("-" * 30)
    
    # Group components by category
    categories = {
        'Core Labor Market': [],
        'Trade Data': [],
        'Leading Indicators': [],
        'Redundant/Overlapping': [],
        'Low Impact': [],
        'Unclear Purpose': []
    }
    
    # Core Labor Market (essential)
    core_components = ['lfpr', 'initial_claims', 'continuing_claims']
    for comp in core_components:
        if comp in weights:
            categories['Core Labor Market'].append({
                'name': comp,
                'weight': weights[comp],
                'purpose': 'Essential labor market fundamentals'
            })
    
    # Trade Data (identify redundancies)
    trade_components = {
        'trade_sentiment': 'General unemployment trade sentiment',
        'trade_volume': 'General unemployment trade volume',
        'initial_claims_trade_sentiment': 'Initial claims trade sentiment',
        'initial_claims_volume': 'Initial claims trade volume',
        'weekly_trade_sentiment': 'Weekly unemployment trade sentiment',
        'weekly_trade_volume': 'Weekly unemployment trade volume',
        'updated_trade_data': 'Updated trade data integration'
    }
    
    for comp, purpose in trade_components.items():
        if comp in weights:
            categories['Trade Data'].append({
                'name': comp,
                'weight': weights[comp],
                'purpose': purpose
            })
    
    # Leading Indicators
    leading_components = {
        'jolts_data': 'Job openings and labor turnover',
        'business_cycle_indicators': 'GDP, PMI, LEI',
        'wage_growth_data': 'Wage growth indicators',
        'sector_employment_data': 'Sector-specific employment',
        'state_unemployment_data': 'State-level unemployment'
    }
    
    for comp, purpose in leading_components.items():
        if comp in weights:
            categories['Leading Indicators'].append({
                'name': comp,
                'weight': weights[comp],
                'purpose': purpose
            })
    
    # Identify redundancies
    print("\nREDUNDANCY ANALYSIS")
    print("-" * 20)
    
    # 1. Trade Data Redundancies
    print("1. TRADE DATA REDUNDANCIES:")
    print("   - trade_sentiment vs weekly_trade_sentiment (same data, different processing)")
    print("   - trade_volume vs weekly_trade_volume (same data, different processing)")
    print("   - initial_claims_trade_sentiment vs initial_claims_volume (overlapping)")
    print("   - updated_trade_data vs other trade components (unclear distinction)")
    
    # 2. Low Impact Components
    print("\n2. LOW IMPACT COMPONENTS:")
    low_impact = []
    for comp, weight in weights.items():
        if weight < 0.01:  # Less than 1% impact
            low_impact.append((comp, weight))
    
    for comp, weight in sorted(low_impact, key=lambda x: x[1]):
        print(f"   - {comp}: {weight:.4f} ({weight*100:.2f}% impact)")
    
    # 3. Overlapping Purposes
    print("\n3. OVERLAPPING PURPOSES:")
    print("   - Multiple trade sentiment measures for same underlying data")
    print("   - Volume and sentiment often correlated")
    print("   - Weekly vs general trade data processing")
    
    # Calculate total weights
    total_weight = sum(weights.values())
    print(f"\nTOTAL SYSTEM WEIGHT: {total_weight:.3f}")
    
    # Recommend cleanup
    print("\nCLEANUP RECOMMENDATIONS")
    print("-" * 25)
    
    print("KEEP (Essential):")
    essential = ['lfpr', 'initial_claims', 'continuing_claims']
    for comp in essential:
        if comp in weights:
            print(f"   ✓ {comp}: {weights[comp]:.4f}")
    
    print("\nCONSOLIDATE (Trade Data):")
    print("   → Combine trade_sentiment + weekly_trade_sentiment → 'unemployment_trade_sentiment'")
    print("   → Combine trade_volume + weekly_trade_volume → 'unemployment_trade_volume'")
    print("   → Combine initial_claims_trade_sentiment + initial_claims_volume → 'claims_trade_sentiment'")
    print("   → Remove 'updated_trade_data' (redundant)")
    
    print("\nKEEP (Leading Indicators - High Value):")
    high_value_leading = ['jolts_data', 'business_cycle_indicators']
    for comp in high_value_leading:
        if comp in weights:
            print(f"   ✓ {comp}: {weights[comp]:.4f}")
    
    print("\nREMOVE (Low Impact):")
    for comp, weight in low_impact:
        print(f"   ✗ {comp}: {weight:.4f} (too small impact)")
    
    print("\nSIMPLIFIED SYSTEM STRUCTURE:")
    print("   Core Labor Market (3): LFPR, Initial Claims, Continuing Claims")
    print("   Trade Data (3): Unemployment Trade Sentiment, Unemployment Trade Volume, Claims Trade Sentiment")
    print("   Leading Indicators (2): JOLTS, Business Cycle")
    print("   Total: 8 components (down from 15)")
    
    # Calculate new weights
    print("\nPROPOSED NEW WEIGHTS:")
    new_weights = {
        # Core Labor Market (70% of total)
        'lfpr': 0.35,
        'initial_claims': 0.25,
        'continuing_claims': 0.10,
        
        # Trade Data (25% of total)
        'unemployment_trade_sentiment': 0.15,
        'unemployment_trade_volume': 0.05,
        'claims_trade_sentiment': 0.05,
        
        # Leading Indicators (5% of total)
        'jolts_data': 0.03,
        'business_cycle_indicators': 0.02
    }
    
    new_total = sum(new_weights.values())
    print(f"   Total Weight: {new_total:.3f}")
    
    for category, comps in [
        ("Core Labor Market", ['lfpr', 'initial_claims', 'continuing_claims']),
        ("Trade Data", ['unemployment_trade_sentiment', 'unemployment_trade_volume', 'claims_trade_sentiment']),
        ("Leading Indicators", ['jolts_data', 'business_cycle_indicators'])
    ]:
        print(f"\n   {category}:")
        for comp in comps:
            if comp in new_weights:
                print(f"     {comp}: {new_weights[comp]:.3f} ({new_weights[comp]/new_total*100:.1f}%)")
    
    return {
        'current_components': len(weights),
        'proposed_components': len(new_weights),
        'redundancy_reduction': len(weights) - len(new_weights),
        'current_total_weight': total_weight,
        'proposed_total_weight': new_total,
        'new_weights': new_weights
    }

if __name__ == "__main__":
    results = analyze_component_redundancy()
    if results:
        print(f"\nSUMMARY:")
        print(f"  Current Components: {results['current_components']}")
        print(f"  Proposed Components: {results['proposed_components']}")
        print(f"  Redundancy Reduction: {results['redundancy_reduction']} components")
        print(f"  Weight Reduction: {results['current_total_weight']:.3f} → {results['proposed_total_weight']:.3f}")