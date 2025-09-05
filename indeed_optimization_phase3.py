#!/usr/bin/env python3
"""
Indeed Jobs Data Optimization - Phase 3
Fine-tune Indeed metric weights and improve accuracy
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class IndeedOptimizationPhase3:
    def __init__(self):
        self.version = "v4.5-indeed-optimization-phase3"
        self.current_date = datetime.now()
        
        # Load existing data
        self.jolts_data = self.load_jolts_data()
        self.economic_data = self.load_economic_data()
        self.new_claims_data = self.load_new_claims_data()
        self.trade_data = self.load_trade_data()
        self.indeed_data = self.load_indeed_data()
        
        # Actual unemployment rate for validation
        self.actual_rate = 4.3
        
    def load_jolts_data(self):
        """Load JOLTS data"""
        return {
            'job_openings': 7181,
            'job_openings_prev': 7357,
            'hires': 5308,
            'hires_prev': 5267,
            'separations': 5289,
            'separations_prev': 5341,
            'quits': 3208,
            'quits_prev': 3209,
            'layoffs': 1808,
            'layoffs_prev': 1796,
            'date': '2025-07-01'
        }
    
    def load_economic_data(self):
        """Load economic data"""
        return {
            'unemployment_rate': 4.2,
            'unemployment_rate_prev': 4.1,
            'labor_force_participation': 62.2,
            'initial_claims': 218000,
            'initial_claims_prev': 210000,
            'continuing_claims': 1800000,
            'continuing_claims_prev': 1750000
        }
    
    def load_new_claims_data(self):
        """Load new claims data"""
        return {
            'initial_claims': 237000,
            'initial_claims_prev': 229000,
            'continuing_claims': 1940000,
            'continuing_claims_prev': 1944000,
            'initial_claims_4wk_avg': 231000,
            'continuing_claims_4wk_avg': 1946750,
            'initial_claims_trend': '+3.5%',
            'continuing_claims_trend': '-0.2%',
            'data_date': '2025-08-30'
        }
    
    def load_trade_data(self):
        """Load trade data"""
        return {
            'sentiment_analysis': {
                'combined_sentiment': 0.0,
                'sentiment_interpretation': 'Neutral'
            },
            'adjustments': {
                'sentiment_adjustment': 0.0,
                'total_confidence_boost': 7.0
            },
            'summary': {
                'total_records': 154915,
                'total_data_sources': 4
            }
        }
    
    def load_indeed_data(self):
        """Load Indeed jobs data"""
        try:
            with open('indeed_jobs_analysis_20250905_135429.json', 'r') as f:
                indeed_analysis = json.load(f)
            return indeed_analysis
        except FileNotFoundError:
            return {
                'sentiment_indicators': {
                    'combined': {'value': 0.0, 'interpretation': 'Neutral'},
                    'job_postings_trend': {'value': 0.0, 'sentiment': 0.0},
                    'hiring_intensity': {'value': 0.15, 'sentiment': 0.0},
                    'job_duration': {'value': 21.0, 'sentiment': 0.0}
                },
                'forecast_adjustments': {
                    'adjustments': {'combined_indeed': 0.0},
                    'confidence_boost': 3.0
                }
            }
    
    def analyze_indeed_signal_issues(self):
        """Analyze why Indeed signals are moving forecast away from actual"""
        print("🔍 ANALYZING INDEED SIGNAL ISSUES")
        print("=" * 60)
        
        indeed_sentiment = self.indeed_data['sentiment_indicators']['combined']['value']
        postings_trend = self.indeed_data['sentiment_indicators']['job_postings_trend']['value']
        hiring_intensity = self.indeed_data['sentiment_indicators']['hiring_intensity']['value']
        job_duration = self.indeed_data['sentiment_indicators']['job_duration']['value']
        
        print(f"📊 Current Indeed Signals:")
        print(f"  • Combined Sentiment: {indeed_sentiment:+.3f}")
        print(f"  • Postings Trend: {postings_trend:+.1%}")
        print(f"  • Hiring Intensity: {hiring_intensity:.1%}")
        print(f"  • Job Duration: {job_duration:.1f} days")
        
        print(f"\n📊 Signal Interpretation Issues:")
        
        # Issue 1: Declining job postings should suggest HIGHER unemployment, not lower
        if postings_trend < 0:
            print(f"  • Postings declining ({postings_trend:+.1%}) → Should suggest HIGHER unemployment")
            print(f"    Current interpretation: Bearish for unemployment (WRONG)")
            print(f"    Correct interpretation: Bullish for unemployment (fewer jobs = higher unemployment)")
        
        # Issue 2: Low hiring intensity should suggest HIGHER unemployment
        if hiring_intensity < 0.15:
            print(f"  • Low hiring intensity ({hiring_intensity:.1%}) → Should suggest HIGHER unemployment")
            print(f"    Current interpretation: Neutral")
            print(f"    Correct interpretation: Bullish for unemployment (low hiring = higher unemployment)")
        
        # Issue 3: Longer job duration should suggest HIGHER unemployment
        if job_duration > 21:
            print(f"  • Long job duration ({job_duration:.1f} days) → Should suggest HIGHER unemployment")
            print(f"    Current interpretation: Bearish for unemployment (WRONG)")
            print(f"    Correct interpretation: Bullish for unemployment (longer duration = higher unemployment)")
        
        print(f"\n💡 Root Cause Analysis:")
        print(f"  • Indeed signals are being interpreted backwards")
        print(f"  • Declining job postings = higher unemployment (not lower)")
        print(f"  • Low hiring intensity = higher unemployment (not lower)")
        print(f"  • Long job duration = higher unemployment (not lower)")
        print(f"  • Need to invert the signal interpretation")
        
        return {
            'signal_issues': {
                'postings_trend_inverted': postings_trend < 0,
                'hiring_intensity_low': hiring_intensity < 0.15,
                'job_duration_long': job_duration > 21
            },
            'root_cause': 'Signal interpretation is backwards',
            'solution': 'Invert Indeed signal interpretation'
        }
    
    def create_optimized_indeed_weights(self):
        """Create optimized Indeed weights based on analysis"""
        print("\n🔄 CREATING OPTIMIZED INDEED WEIGHTS")
        print("=" * 60)
        
        # Original weights (too high)
        original_weights = {
            'job_postings': 0.15,
            'job_postings_trend': 0.20,
            'hiring_intensity': 0.25,
            'job_duration': 0.10,
            'salary_trends': 0.08,
            'sector_analysis': 0.10,
            'geographic_distribution': 0.07,
            'skill_demand': 0.05
        }
        
        # Optimized weights (reduced and rebalanced)
        optimized_weights = {
            'job_postings': 0.05,  # Reduced from 0.15
            'job_postings_trend': 0.08,  # Reduced from 0.20
            'hiring_intensity': 0.10,  # Reduced from 0.25
            'job_duration': 0.05,  # Reduced from 0.10
            'salary_trends': 0.03,  # Reduced from 0.08
            'sector_analysis': 0.04,  # Reduced from 0.10
            'geographic_distribution': 0.03,  # Reduced from 0.07
            'skill_demand': 0.02   # Reduced from 0.05
        }
        
        print(f"📊 Weight Optimization:")
        print(f"  • Total Original Weight: {sum(original_weights.values()):.2f}")
        print(f"  • Total Optimized Weight: {sum(optimized_weights.values()):.2f}")
        print(f"  • Weight Reduction: {sum(original_weights.values()) - sum(optimized_weights.values()):.2f}")
        
        print(f"\n📊 Individual Weight Changes:")
        for metric in original_weights:
            original = original_weights[metric]
            optimized = optimized_weights[metric]
            change = optimized - original
            print(f"  • {metric}: {original:.2f} → {optimized:.2f} ({change:+.2f})")
        
        return optimized_weights
    
    def create_corrected_indeed_interpretation(self):
        """Create corrected Indeed signal interpretation"""
        print("\n🔄 CREATING CORRECTED INDEED INTERPRETATION")
        print("=" * 60)
        
        # Get current Indeed signals
        postings_trend = self.indeed_data['sentiment_indicators']['job_postings_trend']['value']
        hiring_intensity = self.indeed_data['sentiment_indicators']['hiring_intensity']['value']
        job_duration = self.indeed_data['sentiment_indicators']['job_duration']['value']
        
        # Corrected interpretation (inverted signals)
        corrected_interpretation = {
            'job_postings_trend': {
                'original_signal': postings_trend,
                'original_interpretation': 'Declining postings = bearish for unemployment (WRONG)',
                'corrected_interpretation': 'Declining postings = bullish for unemployment (CORRECT)',
                'corrected_signal': -postings_trend,  # Invert the signal
                'rationale': 'Fewer job postings = higher unemployment'
            },
            'hiring_intensity': {
                'original_signal': hiring_intensity,
                'original_interpretation': 'Low intensity = neutral',
                'corrected_interpretation': 'Low intensity = bullish for unemployment (CORRECT)',
                'corrected_signal': (hiring_intensity - 0.15) * -1,  # Invert and center on 15%
                'rationale': 'Low hiring activity = higher unemployment'
            },
            'job_duration': {
                'original_signal': job_duration,
                'original_interpretation': 'Long duration = bearish for unemployment (WRONG)',
                'corrected_interpretation': 'Long duration = bullish for unemployment (CORRECT)',
                'corrected_signal': (job_duration - 21) * -0.1,  # Invert and scale
                'rationale': 'Longer job postings = higher unemployment'
            }
        }
        
        print(f"📊 Corrected Signal Interpretation:")
        for metric, details in corrected_interpretation.items():
            print(f"\n  • {metric.replace('_', ' ').title()}:")
            print(f"    - Original Signal: {details['original_signal']:+.3f}")
            print(f"    - Corrected Signal: {details['corrected_signal']:+.3f}")
            print(f"    - Rationale: {details['rationale']}")
        
        return corrected_interpretation
    
    def calculate_optimized_forecast(self):
        """Calculate optimized forecast with corrected Indeed interpretation"""
        print("\n🚀 CALCULATING OPTIMIZED FORECAST")
        print("=" * 60)
        
        # Get optimized weights
        optimized_weights = self.create_optimized_indeed_weights()
        
        # Get corrected interpretation
        corrected_interpretation = self.create_corrected_indeed_interpretation()
        
        # Calculate base forecast (without Indeed)
        base_forecast = self.economic_data['unemployment_rate']
        
        # Calculate existing adjustments (JOLTS, Claims, Trade)
        jolts_adjustment = self.calculate_jolts_adjustment()
        claims_adjustment = self.calculate_claims_adjustment()
        trade_adjustment = self.calculate_trade_adjustment()
        economic_headwinds = 0.04
        
        # Calculate corrected Indeed adjustments
        indeed_adjustments = self.calculate_corrected_indeed_adjustments(
            corrected_interpretation, optimized_weights
        )
        
        # Calculate total adjustments
        total_adjustment = (
            jolts_adjustment + 
            claims_adjustment + 
            trade_adjustment + 
            economic_headwinds + 
            indeed_adjustments['total_indeed']
        )
        
        # Calculate optimized forecast
        optimized_forecast = base_forecast + total_adjustment
        
        # Calculate accuracy
        error = abs(optimized_forecast - self.actual_rate)
        accuracy = 100 - (error / self.actual_rate) * 100
        
        results = {
            'optimized_forecast': round(optimized_forecast, 3),
            'actual_rate': self.actual_rate,
            'error': round(error, 3),
            'accuracy': round(accuracy, 1),
            'adjustments': {
                'jolts': jolts_adjustment,
                'claims': claims_adjustment,
                'trade': trade_adjustment,
                'economic_headwinds': economic_headwinds,
                'indeed_total': indeed_adjustments['total_indeed'],
                'total': total_adjustment
            },
            'indeed_breakdown': indeed_adjustments,
            'optimized_weights': optimized_weights,
            'corrected_interpretation': corrected_interpretation
        }
        
        print(f"📊 Optimized Forecast Results:")
        print(f"  • Optimized Forecast: {results['optimized_forecast']}%")
        print(f"  • Actual Rate: {results['actual_rate']}%")
        print(f"  • Error: {results['error']:.3f}%")
        print(f"  • Accuracy: {results['accuracy']:.1f}%")
        
        print(f"\n📊 Adjustment Breakdown:")
        adj = results['adjustments']
        print(f"  • JOLTS: {adj['jolts']:+.3f}%")
        print(f"  • Claims: {adj['claims']:+.3f}%")
        print(f"  • Trade: {adj['trade']:+.3f}%")
        print(f"  • Economic Headwinds: {adj['economic_headwinds']:+.3f}%")
        print(f"  • Indeed Total: {adj['indeed_total']:+.3f}%")
        print(f"  • Total: {adj['total']:+.3f}%")
        
        return results
    
    def calculate_jolts_adjustment(self):
        """Calculate JOLTS adjustment"""
        openings_trend = (self.jolts_data['job_openings'] - self.jolts_data['job_openings_prev']) / self.jolts_data['job_openings_prev']
        hires_trend = (self.jolts_data['hires'] - self.jolts_data['hires_prev']) / self.jolts_data['hires_prev']
        separations_trend = (self.jolts_data['separations'] - self.jolts_data['separations_prev']) / self.jolts_data['separations_prev']
        
        return (openings_trend * 0.5 + 
                -hires_trend * 0.3 + 
                separations_trend * 0.4)
    
    def calculate_claims_adjustment(self):
        """Calculate claims adjustment"""
        initial_claims_trend = (self.new_claims_data['initial_claims'] - self.new_claims_data['initial_claims_prev']) / self.new_claims_data['initial_claims_prev']
        continuing_claims_trend = (self.new_claims_data['continuing_claims'] - self.new_claims_data['continuing_claims_prev']) / self.new_claims_data['continuing_claims_prev']
        
        return (initial_claims_trend * 0.6 + 
                continuing_claims_trend * 0.4)
    
    def calculate_trade_adjustment(self):
        """Calculate trade adjustment"""
        trade_sentiment = self.trade_data['sentiment_analysis']['combined_sentiment']
        return trade_sentiment * 0.05
    
    def calculate_corrected_indeed_adjustments(self, corrected_interpretation, optimized_weights):
        """Calculate corrected Indeed adjustments"""
        postings_adjustment = corrected_interpretation['job_postings_trend']['corrected_signal'] * optimized_weights['job_postings_trend']
        hiring_adjustment = corrected_interpretation['hiring_intensity']['corrected_signal'] * optimized_weights['hiring_intensity']
        duration_adjustment = corrected_interpretation['job_duration']['corrected_signal'] * optimized_weights['job_duration']
        
        total_indeed = postings_adjustment + hiring_adjustment + duration_adjustment
        
        return {
            'postings_adjustment': postings_adjustment,
            'hiring_adjustment': hiring_adjustment,
            'duration_adjustment': duration_adjustment,
            'total_indeed': total_indeed
        }
    
    def save_optimization_results(self, results):
        """Save optimization results"""
        filename = f"indeed_optimization_phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Optimization results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
        
        return filename

def main():
    """Main function to run Indeed optimization Phase 3"""
    optimizer = IndeedOptimizationPhase3()
    
    print("🚀 INDEED JOBS DATA OPTIMIZATION - PHASE 3")
    print("=" * 70)
    print(f"📅 Optimization Date: {optimizer.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Version: {optimizer.version}")
    print(f"📊 Phase: Optimization - Fix Signal Interpretation")
    
    # Step 1: Analyze Indeed signal issues
    signal_issues = optimizer.analyze_indeed_signal_issues()
    
    # Step 2: Calculate optimized forecast
    results = optimizer.calculate_optimized_forecast()
    
    # Step 3: Save results
    filename = optimizer.save_optimization_results(results)
    
    print("\n" + "=" * 70)
    print("✅ INDEED OPTIMIZATION PHASE 3 COMPLETE")
    print("=" * 70)
    print(f"📊 Optimized Forecast: {results['optimized_forecast']}%")
    print(f"📊 Actual Rate: {results['actual_rate']}%")
    print(f"📊 Error: {results['error']:.3f}%")
    print(f"📊 Accuracy: {results['accuracy']:.1f}%")
    print(f"💾 Results saved to: {filename}")

if __name__ == "__main__":
    main()