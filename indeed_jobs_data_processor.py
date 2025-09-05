#!/usr/bin/env python3
"""
Indeed Jobs Data Processor
Phase 1: Foundation - Data collection, cleaning, and basic aggregation
"""

import json
import csv
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
import os

class IndeedJobsDataProcessor:
    def __init__(self):
        self.version = "v4.5-indeed-jobs-integration-phase1"
        self.current_date = datetime.now()
        
        # Indeed metrics configuration
        self.metrics_config = {
            'job_postings': {
                'weight': 0.15,
                'description': 'Total job postings on Indeed',
                'correlation': 'negative',
                'lead_time_weeks': 3
            },
            'job_postings_trend': {
                'weight': 0.20,
                'description': 'Week-over-week change in job postings',
                'correlation': 'strong_negative',
                'lead_time_weeks': 2
            },
            'hiring_intensity': {
                'weight': 0.25,
                'description': 'New job postings vs. total postings ratio',
                'correlation': 'strong_negative',
                'lead_time_weeks': 1
            },
            'job_duration': {
                'weight': 0.10,
                'description': 'Average time jobs stay posted',
                'correlation': 'negative',
                'lead_time_weeks': 2
            },
            'salary_trends': {
                'weight': 0.08,
                'description': 'Average salary trends in job postings',
                'correlation': 'negative',
                'lead_time_weeks': 4
            },
            'sector_analysis': {
                'weight': 0.10,
                'description': 'Job postings by industry sector',
                'correlation': 'sector_specific',
                'lead_time_weeks': 3
            },
            'geographic_distribution': {
                'weight': 0.07,
                'description': 'Job postings by geographic region',
                'correlation': 'regional',
                'lead_time_weeks': 3
            },
            'skill_demand': {
                'weight': 0.05,
                'description': 'Most in-demand skills in job postings',
                'correlation': 'skill_mismatch',
                'lead_time_weeks': 3
            }
        }
        
        # Data storage
        self.daily_data = []
        self.weekly_aggregates = {}
        self.monthly_aggregates = {}
        
    def simulate_indeed_data(self, days=30):
        """Simulate Indeed jobs data for testing (Phase 1)"""
        print("🔄 Simulating Indeed Jobs Data for Testing...")
        print("=" * 60)
        
        # Base job postings (simulated)
        base_postings = 1500000  # 1.5M daily job postings
        base_salary = 65000  # Average salary
        
        # Simulate 30 days of data
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            
            # Add some realistic variation
            trend_factor = 1 + (math.sin(i * 0.1) * 0.05)  # Weekly cycle
            seasonal_factor = 1 + (math.sin(i * 0.02) * 0.03)  # Monthly cycle
            random_factor = 1 + (math.sin(i * 0.3) * 0.02)  # Daily variation
            
            daily_postings = int(base_postings * trend_factor * seasonal_factor * random_factor)
            daily_salary = base_salary * (1 + (math.sin(i * 0.1) * 0.02))
            
            # Simulate sector distribution
            sectors = {
                'technology': 0.25,
                'healthcare': 0.20,
                'finance': 0.15,
                'retail': 0.12,
                'manufacturing': 0.10,
                'construction': 0.08,
                'education': 0.06,
                'other': 0.04
            }
            
            sector_data = {}
            for sector, percentage in sectors.items():
                sector_data[sector] = int(daily_postings * percentage)
            
            # Simulate geographic distribution
            regions = {
                'northeast': 0.20,
                'southeast': 0.25,
                'midwest': 0.22,
                'southwest': 0.15,
                'west': 0.18
            }
            
            region_data = {}
            for region, percentage in regions.items():
                region_data[region] = int(daily_postings * percentage)
            
            # Simulate skill demand
            skills = {
                'python': 0.15,
                'javascript': 0.12,
                'data_analysis': 0.10,
                'project_management': 0.08,
                'sales': 0.07,
                'customer_service': 0.06,
                'marketing': 0.05,
                'other': 0.37
            }
            
            skill_data = {}
            for skill, percentage in skills.items():
                skill_data[skill] = int(daily_postings * percentage)
            
            daily_record = {
                'date': date.strftime('%Y-%m-%d'),
                'total_postings': daily_postings,
                'new_postings': int(daily_postings * 0.15),  # 15% new postings
                'average_salary': round(daily_salary, 2),
                'job_duration_days': 21 + (math.sin(i * 0.1) * 3),  # 18-24 days average
                'sectors': sector_data,
                'regions': region_data,
                'skills': skill_data,
                'hiring_intensity': 0.15 + (math.sin(i * 0.1) * 0.02)  # 13-17%
            }
            
            self.daily_data.append(daily_record)
        
        print(f"✅ Generated {len(self.daily_data)} days of simulated Indeed data")
        print(f"📊 Average daily postings: {sum(d['total_postings'] for d in self.daily_data) // len(self.daily_data):,}")
        print(f"📊 Date range: {self.daily_data[0]['date']} to {self.daily_data[-1]['date']}")
        
        return self.daily_data
    
    def calculate_weekly_aggregates(self):
        """Calculate weekly aggregates from daily data"""
        print("\n🔄 Calculating Weekly Aggregates...")
        print("=" * 60)
        
        # Group by week
        weekly_data = {}
        for record in self.daily_data:
            date = datetime.strptime(record['date'], '%Y-%m-%d')
            week_key = f"{date.year}-W{date.isocalendar()[1]}"
            
            if week_key not in weekly_data:
                weekly_data[week_key] = []
            weekly_data[week_key].append(record)
        
        # Calculate weekly metrics
        for week, records in weekly_data.items():
            total_postings = sum(r['total_postings'] for r in records)
            new_postings = sum(r['new_postings'] for r in records)
            avg_salary = sum(r['average_salary'] for r in records) / len(records)
            avg_duration = sum(r['job_duration_days'] for r in records) / len(records)
            avg_hiring_intensity = sum(r['hiring_intensity'] for r in records) / len(records)
            
            # Calculate week-over-week change
            if len(weekly_data) > 1:
                prev_weeks = list(weekly_data.keys())
                prev_week_idx = prev_weeks.index(week) - 1
                if prev_week_idx >= 0:
                    prev_week = prev_weeks[prev_week_idx]
                    prev_total = sum(r['total_postings'] for r in weekly_data[prev_week])
                    wow_change = (total_postings - prev_total) / prev_total if prev_total > 0 else 0
                else:
                    wow_change = 0
            else:
                wow_change = 0
            
            # Aggregate sector data
            sector_totals = {}
            for record in records:
                for sector, count in record['sectors'].items():
                    sector_totals[sector] = sector_totals.get(sector, 0) + count
            
            # Aggregate region data
            region_totals = {}
            for record in records:
                for region, count in record['regions'].items():
                    region_totals[region] = region_totals.get(region, 0) + count
            
            # Aggregate skill data
            skill_totals = {}
            for record in records:
                for skill, count in record['skills'].items():
                    skill_totals[skill] = skill_totals.get(skill, 0) + count
            
            self.weekly_aggregates[week] = {
                'week': week,
                'total_postings': total_postings,
                'new_postings': new_postings,
                'average_salary': round(avg_salary, 2),
                'average_duration_days': round(avg_duration, 1),
                'hiring_intensity': round(avg_hiring_intensity, 3),
                'wow_change': round(wow_change, 4),
                'sectors': sector_totals,
                'regions': region_totals,
                'skills': skill_totals,
                'days_in_week': len(records)
            }
        
        print(f"✅ Calculated {len(self.weekly_aggregates)} weekly aggregates")
        
        # Print sample weekly data
        if self.weekly_aggregates:
            sample_week = list(self.weekly_aggregates.keys())[-1]
            sample_data = self.weekly_aggregates[sample_week]
            print(f"\n📊 Sample Weekly Data ({sample_week}):")
            print(f"  • Total Postings: {sample_data['total_postings']:,}")
            print(f"  • New Postings: {sample_data['new_postings']:,}")
            print(f"  • WoW Change: {sample_data['wow_change']:+.1%}")
            print(f"  • Hiring Intensity: {sample_data['hiring_intensity']:.1%}")
            print(f"  • Avg Salary: ${sample_data['average_salary']:,.0f}")
        
        return self.weekly_aggregates
    
    def calculate_indeed_sentiment(self):
        """Calculate Indeed jobs sentiment indicators"""
        print("\n🔄 Calculating Indeed Jobs Sentiment...")
        print("=" * 60)
        
        if not self.weekly_aggregates:
            print("❌ No weekly aggregates available")
            return {}
        
        # Get latest week data
        latest_week = max(self.weekly_aggregates.keys())
        latest_data = self.weekly_aggregates[latest_week]
        
        # Calculate sentiment indicators
        sentiment_indicators = {}
        
        # Job postings trend sentiment
        wow_change = latest_data['wow_change']
        if wow_change > 0.05:  # 5% increase
            postings_sentiment = 0.3  # Bullish for unemployment (more jobs = lower unemployment)
        elif wow_change > 0.02:  # 2% increase
            postings_sentiment = 0.1
        elif wow_change < -0.05:  # 5% decrease
            postings_sentiment = -0.3  # Bearish for unemployment (fewer jobs = higher unemployment)
        elif wow_change < -0.02:  # 2% decrease
            postings_sentiment = -0.1
        else:
            postings_sentiment = 0.0  # Neutral
        
        sentiment_indicators['job_postings_trend'] = {
            'value': wow_change,
            'sentiment': postings_sentiment,
            'interpretation': 'Bullish' if postings_sentiment > 0 else 'Bearish' if postings_sentiment < 0 else 'Neutral'
        }
        
        # Hiring intensity sentiment
        hiring_intensity = latest_data['hiring_intensity']
        if hiring_intensity > 0.20:  # 20% hiring intensity
            intensity_sentiment = 0.2  # Bullish (high hiring activity)
        elif hiring_intensity > 0.15:  # 15% hiring intensity
            intensity_sentiment = 0.1
        elif hiring_intensity < 0.10:  # 10% hiring intensity
            intensity_sentiment = -0.2  # Bearish (low hiring activity)
        elif hiring_intensity < 0.12:  # 12% hiring intensity
            intensity_sentiment = -0.1
        else:
            intensity_sentiment = 0.0  # Neutral
        
        sentiment_indicators['hiring_intensity'] = {
            'value': hiring_intensity,
            'sentiment': intensity_sentiment,
            'interpretation': 'Bullish' if intensity_sentiment > 0 else 'Bearish' if intensity_sentiment < 0 else 'Neutral'
        }
        
        # Job duration sentiment (shorter duration = tighter labor market)
        avg_duration = latest_data['average_duration_days']
        if avg_duration < 18:  # Very short duration
            duration_sentiment = 0.2  # Bullish (tight labor market)
        elif avg_duration < 20:  # Short duration
            duration_sentiment = 0.1
        elif avg_duration > 25:  # Long duration
            duration_sentiment = -0.2  # Bearish (loose labor market)
        elif avg_duration > 23:  # Longer duration
            duration_sentiment = -0.1
        else:
            duration_sentiment = 0.0  # Neutral
        
        sentiment_indicators['job_duration'] = {
            'value': avg_duration,
            'sentiment': duration_sentiment,
            'interpretation': 'Bullish' if duration_sentiment > 0 else 'Bearish' if duration_sentiment < 0 else 'Neutral'
        }
        
        # Calculate combined sentiment
        weights = [0.4, 0.4, 0.2]  # Job postings trend, hiring intensity, job duration
        sentiments = [postings_sentiment, intensity_sentiment, duration_sentiment]
        combined_sentiment = sum(w * s for w, s in zip(weights, sentiments))
        
        sentiment_indicators['combined'] = {
            'value': combined_sentiment,
            'interpretation': 'Bullish' if combined_sentiment > 0.1 else 'Bearish' if combined_sentiment < -0.1 else 'Neutral'
        }
        
        print(f"📊 Indeed Jobs Sentiment Analysis:")
        print(f"  • Job Postings Trend: {wow_change:+.1%} ({sentiment_indicators['job_postings_trend']['interpretation']})")
        print(f"  • Hiring Intensity: {hiring_intensity:.1%} ({sentiment_indicators['hiring_intensity']['interpretation']})")
        print(f"  • Job Duration: {avg_duration:.1f} days ({sentiment_indicators['job_duration']['interpretation']})")
        print(f"  • Combined Sentiment: {combined_sentiment:+.3f} ({sentiment_indicators['combined']['interpretation']})")
        
        return sentiment_indicators
    
    def calculate_forecast_adjustments(self, sentiment_indicators):
        """Calculate forecast adjustments based on Indeed sentiment"""
        print("\n🔄 Calculating Indeed-Based Forecast Adjustments...")
        print("=" * 60)
        
        combined_sentiment = sentiment_indicators['combined']['value']
        
        # Base adjustment from Indeed sentiment
        indeed_adjustment = combined_sentiment * 0.05  # 5% of sentiment as adjustment
        
        # Individual metric adjustments
        adjustments = {
            'job_postings_trend': sentiment_indicators['job_postings_trend']['sentiment'] * 0.03,
            'hiring_intensity': sentiment_indicators['hiring_intensity']['sentiment'] * 0.04,
            'job_duration': sentiment_indicators['job_duration']['sentiment'] * 0.02,
            'combined_indeed': indeed_adjustment
        }
        
        # Confidence boost from Indeed data
        indeed_confidence_boost = 2.0  # Base boost for Indeed data
        freshness_boost = 1.0  # Fresh data boost
        total_confidence_boost = indeed_confidence_boost + freshness_boost
        
        print(f"📊 Indeed-Based Adjustments:")
        print(f"  • Job Postings Trend: {adjustments['job_postings_trend']:+.3f}%")
        print(f"  • Hiring Intensity: {adjustments['hiring_intensity']:+.3f}%")
        print(f"  • Job Duration: {adjustments['job_duration']:+.3f}%")
        print(f"  • Combined Indeed: {adjustments['combined_indeed']:+.3f}%")
        print(f"  • Confidence Boost: {total_confidence_boost:+.1f}%")
        
        return {
            'adjustments': adjustments,
            'confidence_boost': total_confidence_boost,
            'sentiment_indicators': sentiment_indicators
        }
    
    def save_indeed_analysis(self, sentiment_indicators, forecast_adjustments):
        """Save Indeed jobs analysis"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'phase': 'Phase 1 - Foundation',
            'data_summary': {
                'daily_records': len(self.daily_data),
                'weekly_aggregates': len(self.weekly_aggregates),
                'date_range': {
                    'start': self.daily_data[0]['date'] if self.daily_data else None,
                    'end': self.daily_data[-1]['date'] if self.daily_data else None
                }
            },
            'sentiment_indicators': sentiment_indicators,
            'forecast_adjustments': forecast_adjustments,
            'weekly_aggregates': self.weekly_aggregates,
            'metrics_config': self.metrics_config
        }
        
        filename = f"indeed_jobs_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            print(f"\n💾 Indeed analysis saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
        
        return filename

def main():
    """Main function to run Indeed jobs data processing"""
    processor = IndeedJobsDataProcessor()
    
    print("🚀 INDEED JOBS DATA PROCESSING - PHASE 1")
    print("=" * 70)
    print(f"📅 Processing Date: {processor.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Version: {processor.version}")
    print(f"📊 Phase: Foundation - Data Collection & Processing")
    
    # Step 1: Simulate Indeed data
    daily_data = processor.simulate_indeed_data(30)
    
    # Step 2: Calculate weekly aggregates
    weekly_aggregates = processor.calculate_weekly_aggregates()
    
    # Step 3: Calculate sentiment indicators
    sentiment_indicators = processor.calculate_indeed_sentiment()
    
    # Step 4: Calculate forecast adjustments
    forecast_adjustments = processor.calculate_forecast_adjustments(sentiment_indicators)
    
    # Step 5: Save analysis
    filename = processor.save_indeed_analysis(sentiment_indicators, forecast_adjustments)
    
    print("\n" + "=" * 70)
    print("✅ INDEED JOBS DATA PROCESSING COMPLETE")
    print("=" * 70)
    print(f"📊 Processed {len(daily_data)} daily records")
    print(f"📊 Generated {len(weekly_aggregates)} weekly aggregates")
    print(f"📊 Combined Sentiment: {sentiment_indicators['combined']['value']:+.3f}")
    print(f"📊 Forecast Adjustment: {forecast_adjustments['adjustments']['combined_indeed']:+.3f}%")
    print(f"📊 Confidence Boost: {forecast_adjustments['confidence_boost']:+.1f}%")
    print(f"💾 Analysis saved to: {filename}")

if __name__ == "__main__":
    main()