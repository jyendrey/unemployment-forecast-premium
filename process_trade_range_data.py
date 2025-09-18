#!/usr/bin/env python3
"""
Process Trade Range Data
Processes the new trade range data provided by user and integrates with forecasting system
Foundation ID: bc-78795d1e-6a46-4716-9ff6-78bca58ca95f
"""

import json
from datetime import datetime

class TradeRangeProcessor:
    def __init__(self):
        self.foundation_id = "bc-78795d1e-6a46-4716-9ff6-78bca58ca95f"
        self.current_date = datetime.now()
        
        # Trade range data provided by user
        self.trade_range_data = {
            "Above 3.7%": {"Yes": 97, "No": 0, "OI": 40},
            "Above 3.8%": {"Yes": 97, "No": 3, "OI": 190},
            "Above 3.9%": {"Yes": 97, "No": 3, "OI": 500},
            "Above 4.0%": {"Yes": 92, "No": 6, "OI": 480},
            "Above 4.1%": {"Yes": 73, "No": 25, "OI": 490},
            "Above 4.2%": {"Yes": 50, "No": 48, "OI": 85},
            "Above 4.3%": {"Yes": 28, "No": 70, "OI": 10},
            "Above 4.4%": {"Yes": 16, "No": 84, "OI": 0},
            "Above 4.5%": {"Yes": 8, "No": 92, "OI": 40}
        }
    
    def calculate_market_sentiment(self):
        """Calculate market sentiment from trade range data"""
        
        print("🔍 Analyzing trade range data for market sentiment...")
        
        # Calculate weighted sentiment based on open interest and price levels
        total_oi = sum(data["OI"] for data in self.trade_range_data.values())
        weighted_sentiment = 0
        total_weight = 0
        
        for threshold, data in self.trade_range_data.items():
            if data["OI"] > 0:  # Only consider contracts with open interest
                # Extract percentage from threshold (e.g., "Above 4.0%" -> 4.0)
                threshold_value = float(threshold.split("Above ")[1].replace("%", ""))
                
                # Calculate sentiment for this threshold
                yes_percentage = data["Yes"] / 100.0
                no_percentage = data["No"] / 100.0
                
                # Weight by open interest
                weight = data["OI"]
                
                # Calculate sentiment score (-1 to 1, where positive means bullish on unemployment)
                # Higher unemployment rates are generally negative for the economy
                sentiment_score = (no_percentage - yes_percentage) * (threshold_value - 3.5) / 10
                
                weighted_sentiment += sentiment_score * weight
                total_weight += weight
                
                print(f"  {threshold}: Yes={data['Yes']}%, No={data['No']}%, OI={data['OI']}, Sentiment={sentiment_score:.4f}")
        
        if total_weight > 0:
            final_sentiment = weighted_sentiment / total_weight
        else:
            final_sentiment = 0
        
        # Interpret sentiment
        if final_sentiment > 0.1:
            interpretation = "Bullish (Expecting Higher Unemployment)"
        elif final_sentiment < -0.1:
            interpretation = "Bearish (Expecting Lower Unemployment)"
        else:
            interpretation = "Neutral"
        
        print(f"📊 Final Weighted Sentiment: {final_sentiment:.4f}")
        print(f"📊 Interpretation: {interpretation}")
        
        return {
            "sentiment_score": final_sentiment,
            "sentiment_interpretation": interpretation,
            "total_open_interest": total_oi,
            "contracts_analyzed": len([d for d in self.trade_range_data.values() if d["OI"] > 0]),
            "confidence": min(total_oi / 1000, 1.0)  # Confidence based on volume
        }
    
    def calculate_forecast_adjustments(self):
        """Calculate forecast adjustments based on trade range data"""
        
        print("\n🔧 Calculating forecast adjustments from trade range data...")
        
        sentiment_data = self.calculate_market_sentiment()
        
        # Calculate adjustments based on sentiment and volume
        sentiment_adjustment = sentiment_data["sentiment_score"] * 0.15  # Scale factor
        volume_adjustment = min(sentiment_data["total_open_interest"] / 10000, 0.05)  # Volume bonus
        
        # Calculate trend adjustment based on distribution
        high_unemployment_contracts = sum(data["OI"] for threshold, data in self.trade_range_data.items() 
                                        if float(threshold.split("Above ")[1].replace("%", "")) >= 4.2)
        low_unemployment_contracts = sum(data["OI"] for threshold, data in self.trade_range_data.items() 
                                       if float(threshold.split("Above ")[1].replace("%", "")) < 4.2)
        
        if high_unemployment_contracts > low_unemployment_contracts:
            trend_adjustment = 0.001  # Slight upward pressure
            trend_interpretation = "Market expects higher unemployment"
        else:
            trend_adjustment = -0.001  # Slight downward pressure
            trend_interpretation = "Market expects lower unemployment"
        
        adjustments = {
            "sentiment_adjustment": sentiment_adjustment,
            "volume_adjustment": volume_adjustment,
            "trend_adjustment": trend_adjustment,
            "trend_interpretation": trend_interpretation,
            "total_adjustment": sentiment_adjustment + volume_adjustment + trend_adjustment
        }
        
        print(f"  Sentiment Adjustment: {sentiment_adjustment:.4f}%")
        print(f"  Volume Adjustment: {volume_adjustment:.4f}%")
        print(f"  Trend Adjustment: {trend_adjustment:.4f}% ({trend_interpretation})")
        print(f"  Total Adjustment: {adjustments['total_adjustment']:.4f}%")
        
        return adjustments
    
    def create_enhanced_forecast_input(self):
        """Create enhanced forecast input with trade range data"""
        
        print("\n📊 Creating enhanced forecast input...")
        
        sentiment_data = self.calculate_market_sentiment()
        adjustments = self.calculate_forecast_adjustments()
        
        # Create enhanced forecast input
        enhanced_input = {
            "generated_date": self.current_date.isoformat(),
            "foundation_id": self.foundation_id,
            "data_source": "Trade Range Data",
            "market_sentiment": {
                "sentiment_score": sentiment_data["sentiment_score"],
                "sentiment_interpretation": sentiment_data["sentiment_interpretation"],
                "contracts_analyzed": sentiment_data["contracts_analyzed"],
                "total_volume": sentiment_data["total_open_interest"],
                "confidence": sentiment_data["confidence"]
            },
            "forecast_adjustments": adjustments,
            "trade_range_analysis": {
                "data_points": len(self.trade_range_data),
                "total_open_interest": sum(data["OI"] for data in self.trade_range_data.values()),
                "highest_oi_threshold": max(self.trade_range_data.keys(), 
                                          key=lambda x: self.trade_range_data[x]["OI"]),
                "market_distribution": self.trade_range_data
            },
            "data_quality": {
                "total_trades_processed": sentiment_data["contracts_analyzed"],
                "unemployment_trade_ratio": 1.0,  # All contracts are unemployment-related
                "date_coverage": 1,  # Current data
                "confidence_level": sentiment_data["confidence"]
            }
        }
        
        return enhanced_input
    
    def save_enhanced_forecast_input(self, enhanced_input, filename="enhanced_forecast_input.json"):
        """Save enhanced forecast input to JSON file"""
        
        with open(filename, 'w') as f:
            json.dump(enhanced_input, f, indent=2)
        
        print(f"✅ Enhanced forecast input saved to: {filename}")
        return filename
    
    def print_analysis_summary(self, enhanced_input):
        """Print comprehensive analysis summary"""
        
        print("\n" + "="*60)
        print("TRADE RANGE DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print(f"Generated: {enhanced_input['generated_date']}")
        print("="*60)
        
        sentiment = enhanced_input['market_sentiment']
        print(f"\n📊 MARKET SENTIMENT:")
        print(f"  Sentiment Score: {sentiment['sentiment_score']:.4f}")
        print(f"  Interpretation: {sentiment['sentiment_interpretation']}")
        print(f"  Contracts Analyzed: {sentiment['contracts_analyzed']}")
        print(f"  Total Volume (OI): {sentiment['total_volume']:,}")
        print(f"  Confidence: {sentiment['confidence']:.1%}")
        
        adjustments = enhanced_input['forecast_adjustments']
        print(f"\n🔧 FORECAST ADJUSTMENTS:")
        print(f"  Sentiment Adjustment: {adjustments['sentiment_adjustment']:+.4f}%")
        print(f"  Volume Adjustment: {adjustments['volume_adjustment']:+.4f}%")
        print(f"  Trend Adjustment: {adjustments['trend_adjustment']:+.4f}%")
        print(f"  Total Adjustment: {adjustments['total_adjustment']:+.4f}%")
        print(f"  Trend Interpretation: {adjustments['trend_interpretation']}")
        
        trade_analysis = enhanced_input['trade_range_analysis']
        print(f"\n📈 TRADE RANGE ANALYSIS:")
        print(f"  Data Points: {trade_analysis['data_points']}")
        print(f"  Total Open Interest: {trade_analysis['total_open_interest']:,}")
        print(f"  Highest OI Threshold: {trade_analysis['highest_oi_threshold']}")
        
        print(f"\n📊 TRADE RANGE DISTRIBUTION:")
        for threshold, data in self.trade_range_data.items():
            print(f"  {threshold}: Yes={data['Yes']}%, No={data['No']}%, OI={data['OI']}")
        
        print("\n" + "="*60)
    
    def process_trade_range_data(self):
        """Main processing function"""
        
        print("="*60)
        print("TRADE RANGE DATA PROCESSOR")
        print("="*60)
        print(f"Foundation ID: {self.foundation_id}")
        print("="*60)
        
        # Create enhanced forecast input
        enhanced_input = self.create_enhanced_forecast_input()
        
        # Save enhanced forecast input
        input_file = self.save_enhanced_forecast_input(enhanced_input)
        
        # Print analysis summary
        self.print_analysis_summary(enhanced_input)
        
        print(f"\n🎯 Trade range data processing complete!")
        print(f"📁 Enhanced forecast input saved to: {input_file}")
        print(f"🔧 Foundation System: {self.foundation_id}")
        print("="*60)
        
        return enhanced_input

def main():
    """Main execution function"""
    processor = TradeRangeProcessor()
    processor.process_trade_range_data()

if __name__ == "__main__":
    main()