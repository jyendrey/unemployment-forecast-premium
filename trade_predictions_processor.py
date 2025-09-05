#!/usr/bin/env python3
"""
Trade Predictions Data Processor
Processes trade prediction data for unemployment rate forecasting
"""

import json
from datetime import datetime

class TradePredictionsProcessor:
    def __init__(self):
        self.foundation_id = "bc-1aac34de-3d51-4320-a4ce-c8cab2a8cd5b"
        self.version = "v1.0-trade-predictions"
        
    def process_trade_predictions(self, predictions_data):
        """Process trade predictions data"""
        print("🔄 Processing Trade Predictions Data...")
        
        # Parse the predictions data
        contracts = []
        for contract in predictions_data:
            contract_info = {
                'threshold': contract['threshold'],
                'yes_probability': contract['yes_probability'],
                'no_probability': contract['no_probability'],
                'open_interest': contract['open_interest']
            }
            contracts.append(contract_info)
        
        # Calculate market sentiment
        sentiment_analysis = self.analyze_predictions_sentiment(contracts)
        
        # Calculate prediction confidence
        confidence_analysis = self.analyze_predictions_confidence(contracts)
        
        # Calculate threshold distribution
        threshold_analysis = self.analyze_threshold_distribution(contracts)
        
        # Generate market insights
        market_insights = self.generate_market_insights(sentiment_analysis, confidence_analysis, threshold_analysis)
        
        return {
            'contracts': contracts,
            'sentiment_analysis': sentiment_analysis,
            'confidence_analysis': confidence_analysis,
            'threshold_analysis': threshold_analysis,
            'market_insights': market_insights,
            'processing_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def analyze_predictions_sentiment(self, contracts):
        """Analyze market sentiment from predictions"""
        # Weight contracts by open interest
        total_oi = sum(contract['open_interest'] for contract in contracts)
        
        if total_oi == 0:
            return {'sentiment_score': 0, 'sentiment_level': 'neutral'}
        
        # Calculate weighted sentiment
        weighted_yes = 0
        weighted_no = 0
        
        for contract in contracts:
            weight = contract['open_interest'] / total_oi
            weighted_yes += contract['yes_probability'] * weight
            weighted_no += contract['no_probability'] * weight
        
        # Calculate sentiment score (-1 to 1, where 1 = very bullish on unemployment)
        sentiment_score = (weighted_yes - weighted_no) / 100
        
        # Determine sentiment level
        if sentiment_score > 0.5:
            sentiment_level = 'very_bullish'
        elif sentiment_score > 0.2:
            sentiment_level = 'bullish'
        elif sentiment_score > -0.2:
            sentiment_level = 'neutral'
        elif sentiment_score > -0.5:
            sentiment_level = 'bearish'
        else:
            sentiment_level = 'very_bearish'
        
        return {
            'sentiment_score': sentiment_score,
            'sentiment_level': sentiment_level,
            'weighted_yes_probability': weighted_yes,
            'weighted_no_probability': weighted_no,
            'total_contracts': len(contracts),
            'total_open_interest': total_oi
        }
    
    def analyze_predictions_confidence(self, contracts):
        """Analyze confidence in predictions"""
        # Calculate average confidence (how certain the market is)
        confidences = []
        for contract in contracts:
            yes_prob = contract['yes_probability']
            no_prob = contract['no_probability']
            # Confidence is how far from 50/50
            confidence = abs(yes_prob - no_prob) / 100
            confidences.append(confidence)
        
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate volume-weighted confidence
        total_oi = sum(contract['open_interest'] for contract in contracts)
        if total_oi > 0:
            volume_weighted_confidence = sum(
                (abs(contract['yes_probability'] - contract['no_probability']) / 100) * 
                (contract['open_interest'] / total_oi)
                for contract in contracts
            )
        else:
            volume_weighted_confidence = 0
        
        return {
            'average_confidence': avg_confidence,
            'volume_weighted_confidence': volume_weighted_confidence,
            'confidence_level': 'high' if avg_confidence > 0.7 else 'medium' if avg_confidence > 0.4 else 'low',
            'total_volume': total_oi
        }
    
    def analyze_threshold_distribution(self, contracts):
        """Analyze distribution of prediction thresholds"""
        # Group by threshold ranges
        threshold_ranges = {
            'below_4.0': [],
            '4.0_to_4.2': [],
            '4.2_to_4.3': [],
            'above_4.3': []
        }
        
        for contract in contracts:
            threshold = contract['threshold']
            if threshold < 4.0:
                threshold_ranges['below_4.0'].append(contract)
            elif threshold <= 4.2:
                threshold_ranges['4.0_to_4.2'].append(contract)
            elif threshold <= 4.3:
                threshold_ranges['4.2_to_4.3'].append(contract)
            else:
                threshold_ranges['above_4.3'].append(contract)
        
        # Calculate weighted probabilities for each range
        range_analysis = {}
        for range_name, range_contracts in threshold_ranges.items():
            if range_contracts:
                total_oi = sum(c['open_interest'] for c in range_contracts)
                if total_oi > 0:
                    weighted_yes = sum(c['yes_probability'] * c['open_interest'] for c in range_contracts) / total_oi
                    weighted_no = sum(c['no_probability'] * c['open_interest'] for c in range_contracts) / total_oi
                else:
                    weighted_yes = sum(c['yes_probability'] for c in range_contracts) / len(range_contracts)
                    weighted_no = sum(c['no_probability'] for c in range_contracts) / len(range_contracts)
                
                range_analysis[range_name] = {
                    'contracts': len(range_contracts),
                    'total_oi': total_oi,
                    'weighted_yes': weighted_yes,
                    'weighted_no': weighted_no,
                    'net_sentiment': weighted_yes - weighted_no
                }
            else:
                range_analysis[range_name] = {
                    'contracts': 0,
                    'total_oi': 0,
                    'weighted_yes': 0,
                    'weighted_no': 0,
                    'net_sentiment': 0
                }
        
        return range_analysis
    
    def generate_market_insights(self, sentiment_analysis, confidence_analysis, threshold_analysis):
        """Generate market insights from predictions"""
        insights = []
        
        # Sentiment insights
        sentiment_level = sentiment_analysis['sentiment_level']
        if sentiment_level in ['very_bullish', 'bullish']:
            insights.append(f"Market strongly predicts unemployment above 4.3% ({sentiment_level})")
        elif sentiment_level in ['very_bearish', 'bearish']:
            insights.append(f"Market predicts unemployment below 4.3% ({sentiment_level})")
        else:
            insights.append(f"Market sentiment is neutral on unemployment direction")
        
        # Confidence insights
        confidence_level = confidence_analysis['confidence_level']
        if confidence_level == 'high':
            insights.append("High market confidence in predictions")
        elif confidence_level == 'medium':
            insights.append("Moderate market confidence in predictions")
        else:
            insights.append("Low market confidence in predictions")
        
        # Threshold insights
        above_43 = threshold_analysis.get('above_4.3', {})
        if above_43['contracts'] > 0 and above_43['net_sentiment'] > 50:
            insights.append(f"Strong prediction for unemployment above 4.3% ({above_43['weighted_yes']:.0f}% yes)")
        
        below_40 = threshold_analysis.get('below_4.0', {})
        if below_40['contracts'] > 0 and below_40['net_sentiment'] < -50:
            insights.append(f"Strong prediction for unemployment below 4.0% ({below_40['weighted_no']:.0f}% no)")
        
        return insights

def main():
    """Main execution function"""
    processor = TradePredictionsProcessor()
    
    # Trade predictions data
    predictions_data = [
        {'threshold': 2.7, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 0},
        {'threshold': 2.9, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 120},
        {'threshold': 3.1, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 120},
        {'threshold': 3.3, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 150},
        {'threshold': 3.5, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 200},
        {'threshold': 3.7, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 349},
        {'threshold': 3.8, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 450},
        {'threshold': 3.9, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 470},
        {'threshold': 4.0, 'yes_probability': 97, 'no_probability': 0, 'open_interest': 450},
        {'threshold': 4.1, 'yes_probability': 94, 'no_probability': 6, 'open_interest': 430},
        {'threshold': 4.2, 'yes_probability': 64, 'no_probability': 36, 'open_interest': 180},
        {'threshold': 4.3, 'yes_probability': 26, 'no_probability': 72, 'open_interest': 70},
        {'threshold': 4.5, 'yes_probability': 0, 'no_probability': 97, 'open_interest': 12}
    ]
    
    # Process the data
    results = processor.process_trade_predictions(predictions_data)
    
    # Print results
    print("\n" + "="*80)
    print("🎯 TRADE PREDICTIONS ANALYSIS")
    print("="*80)
    
    sentiment = results['sentiment_analysis']
    print(f"📊 Market Sentiment: {sentiment['sentiment_level']} ({sentiment['sentiment_score']:.3f})")
    print(f"   • Weighted Yes Probability: {sentiment['weighted_yes_probability']:.1f}%")
    print(f"   • Weighted No Probability: {sentiment['weighted_no_probability']:.1f}%")
    print(f"   • Total Contracts: {sentiment['total_contracts']}")
    print(f"   • Total Open Interest: {sentiment['total_open_interest']:,}")
    
    confidence = results['confidence_analysis']
    print(f"\n🎯 Market Confidence: {confidence['confidence_level']}")
    print(f"   • Average Confidence: {confidence['average_confidence']:.3f}")
    print(f"   • Volume-Weighted Confidence: {confidence['volume_weighted_confidence']:.3f}")
    print(f"   • Total Volume: {confidence['total_volume']:,}")
    
    print(f"\n📈 Threshold Analysis:")
    for range_name, analysis in results['threshold_analysis'].items():
        if analysis['contracts'] > 0:
            print(f"   • {range_name}: {analysis['contracts']} contracts, {analysis['total_oi']:,} OI")
            print(f"     Yes: {analysis['weighted_yes']:.1f}%, No: {analysis['weighted_no']:.1f}%")
    
    print(f"\n💡 Market Insights:")
    for insight in results['market_insights']:
        print(f"   • {insight}")
    
    # Save results
    with open('trade_predictions_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Trade predictions analysis saved to: trade_predictions_analysis.json")
    
    return results

if __name__ == "__main__":
    main()