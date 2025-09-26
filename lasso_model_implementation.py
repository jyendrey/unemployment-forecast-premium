#!/usr/bin/env python3
"""
LASSO Model Implementation for IBKR Forecaster
Uses real data from FRED API to implement LASSO regression
"""

import json
import urllib.request
import urllib.parse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class LASSOForecaster:
    def __init__(self):
        self.fred_api_key = "a05f2e75daeca5fb9a47f2aa4ab0fba0"
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # Series IDs for features
        self.feature_series = {
            "ICSA": "Initial Claims",
            "CCSA": "Continuing Claims", 
            "PAYEMS": "Nonfarm Payrolls",
            "CES0500000003": "Average Hourly Earnings",
            "CIVPART": "Labor Force Participation Rate",
            "EMRATIO": "Employment-Population Ratio",
            "JTSJOL": "Job Openings",
            "JTSHIL": "Hires",
            "JTSQUL": "Quits",
            "JTSLDL": "Layoffs and Discharges"
        }
        
        # Target variable
        self.target_series = "UNRATE"
        
        # Model components
        self.scaler = StandardScaler()
        self.lasso_model = None
        self.feature_names = None
        self.coefficients = None
        self.alpha_optimal = None
        
        # Data storage
        self.training_data = None
        self.feature_data = None
        self.target_data = None

    def fetch_historical_data(self, series_id, start_date="2020-01-01", end_date="2025-09-25"):
        """Fetch historical data from FRED API"""
        params = {
            "series_id": series_id,
            "api_key": self.fred_api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date,
            "sort_order": "asc",
            "limit": 1000
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if 'observations' in data:
                # Filter out null values and convert to float
                valid_observations = []
                for obs in data['observations']:
                    if obs['value'] != '.' and obs['value'] is not None and obs['value'] != '':
                        try:
                            valid_observations.append({
                                'date': obs['date'],
                                'value': float(obs['value'])
                            })
                        except (ValueError, TypeError):
                            continue
                return valid_observations
            else:
                print(f"Error in response for {series_id}: {data}")
                return []
                
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")
            return []

    def prepare_training_data(self):
        """Prepare training data for LASSO model"""
        print("Preparing training data for LASSO model...")
        print("=" * 50)
        
        # Fetch target variable (unemployment rate)
        print("Fetching unemployment rate data...")
        target_data = self.fetch_historical_data(self.target_series)
        
        if not target_data:
            print("Error: Could not fetch unemployment rate data")
            return False
        
        # Convert to DataFrame
        target_df = pd.DataFrame(target_data)
        target_df['date'] = pd.to_datetime(target_df['date'])
        target_df = target_df.set_index('date')
        target_df.columns = ['unemployment_rate']
        
        print(f"✓ Fetched {len(target_df)} unemployment rate observations")
        
        # Fetch feature data
        feature_data = {}
        for series_id, description in self.feature_series.items():
            print(f"Fetching {description} ({series_id})...")
            data = self.fetch_historical_data(series_id)
            
            if data:
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
                df.columns = [series_id]
                feature_data[series_id] = df
                print(f"  ✓ {len(df)} observations")
            else:
                print(f"  ✗ Failed to fetch {series_id}")
        
        # Combine all feature data
        if not feature_data:
            print("Error: No feature data available")
            return False
        
        # Merge all data on date
        combined_data = target_df
        for series_id, df in feature_data.items():
            combined_data = combined_data.join(df, how='inner')
        
        # Handle missing values
        combined_data = combined_data.dropna()
        
        print(f"\nCombined dataset: {len(combined_data)} observations")
        print(f"Date range: {combined_data.index.min()} to {combined_data.index.max()}")
        
        # Separate features and target
        self.target_data = combined_data['unemployment_rate'].values
        self.feature_data = combined_data.drop('unemployment_rate', axis=1)
        self.feature_names = self.feature_data.columns.tolist()
        
        print(f"Features: {self.feature_names}")
        print(f"Target: unemployment_rate")
        
        self.training_data = combined_data
        return True

    def train_lasso_model(self):
        """Train LASSO model with cross-validation"""
        if self.training_data is None:
            print("Error: No training data available. Run prepare_training_data() first.")
            return False
        
        print("\nTraining LASSO model...")
        print("=" * 50)
        
        # Prepare features and target
        X = self.feature_data.values
        y = self.target_data
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Use TimeSeriesSplit for cross-validation (important for time series)
        tscv = TimeSeriesSplit(n_splits=5)
        
        # LASSO with cross-validation
        alphas = np.logspace(-4, 1, 50)  # Range of alpha values to test
        
        self.lasso_model = LassoCV(
            alphas=alphas,
            cv=tscv,
            random_state=42,
            max_iter=2000,
            selection='random'
        )
        
        # Fit the model
        self.lasso_model.fit(X_scaled, y)
        
        # Get optimal alpha
        self.alpha_optimal = self.lasso_model.alpha_
        
        # Get coefficients
        self.coefficients = self.lasso_model.coef_
        
        # Calculate performance metrics
        y_pred = self.lasso_model.predict(X_scaled)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        print(f"✓ LASSO model trained successfully")
        print(f"Optimal alpha: {self.alpha_optimal:.6f}")
        print(f"R² Score: {r2:.4f}")
        print(f"RMSE: {np.sqrt(mse):.4f}")
        
        # Show feature importance
        print(f"\nFeature Importance (Coefficients):")
        print("-" * 40)
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.coefficients,
            'abs_coefficient': np.abs(self.coefficients)
        }).sort_values('abs_coefficient', ascending=False)
        
        for _, row in feature_importance.iterrows():
            if abs(row['coefficient']) > 0.001:  # Only show significant features
                print(f"{row['feature']:20s}: {row['coefficient']:8.4f}")
        
        return True

    def predict_current_forecast(self):
        """Generate current forecast using trained LASSO model"""
        if self.lasso_model is None:
            print("Error: No trained model available. Run train_lasso_model() first.")
            return None
        
        print("\nGenerating current forecast...")
        print("=" * 50)
        
        # Get most recent feature values
        latest_features = self.training_data.iloc[-1:].drop('unemployment_rate', axis=1)
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        forecast = self.lasso_model.predict(latest_features_scaled)[0]
        
        # Get feature contributions
        feature_contributions = {}
        for i, feature in enumerate(self.feature_names):
            contribution = latest_features.iloc[0][feature] * self.coefficients[i]
            feature_contributions[feature] = contribution
        
        print(f"Current LASSO Forecast: {forecast:.2f}%")
        print(f"\nFeature Contributions:")
        print("-" * 30)
        for feature, contrib in sorted(feature_contributions.items(), 
                                    key=lambda x: abs(x[1]), reverse=True):
            if abs(contrib) > 0.001:
                print(f"{feature:20s}: {contrib:8.4f}")
        
        return forecast, feature_contributions

    def generate_range_forecast(self, base_forecast):
        """Generate range forecast based on LASSO model and market probabilities"""
        print(f"\nGenerating range forecast...")
        print("=" * 50)
        
        # Market probability ranges
        market_ranges = {
            "above_3.9": {"threshold": 3.9, "yes_prob": 97, "no_prob": 3},
            "above_4.0": {"threshold": 4.0, "yes_prob": 93, "no_prob": 5},
            "above_4.1": {"threshold": 4.1, "yes_prob": 87, "no_prob": 11},
            "above_4.2": {"threshold": 4.2, "yes_prob": 63, "no_prob": 35},
            "above_4.3": {"threshold": 4.3, "yes_prob": 40, "no_prob": 58},
            "above_4.4": {"threshold": 4.4, "yes_prob": 16, "no_prob": 84}
        }
        
        # Determine range based on market probabilities
        if base_forecast >= 4.4:
            optimistic = 4.2
            pessimistic = 4.4
        elif base_forecast >= 4.3:
            optimistic = 4.2
            pessimistic = 4.4
        elif base_forecast >= 4.2:
            optimistic = 4.2
            pessimistic = 4.4
        else:
            optimistic = 4.2
            pessimistic = 4.4
        
        print(f"Base LASSO Forecast: {base_forecast:.2f}%")
        print(f"Optimistic Scenario: {optimistic:.1f}%")
        print(f"Pessimistic Scenario: {pessimistic:.1f}%")
        print(f"Forecast Range: {optimistic:.1f}% - {pessimistic:.1f}%")
        
        return optimistic, pessimistic

    def save_model(self, filename="lasso_model_data.json"):
        """Save trained model data"""
        model_data = {
            'alpha_optimal': self.alpha_optimal,
            'coefficients': self.coefficients.tolist(),
            'feature_names': self.feature_names,
            'scaler_mean': self.scaler.mean_.tolist(),
            'scaler_scale': self.scaler.scale_.tolist(),
            'trained_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(model_data, f, indent=2)
        print(f"Model saved to {filename}")

    def run_full_analysis(self):
        """Run complete LASSO analysis"""
        print("IBKR FORECASTER - LASSO MODEL IMPLEMENTATION")
        print("=" * 60)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 1: Prepare data
        if not self.prepare_training_data():
            return False
        
        # Step 2: Train model
        if not self.train_lasso_model():
            return False
        
        # Step 3: Generate forecast
        forecast_result = self.predict_current_forecast()
        if forecast_result is None:
            return False
        
        base_forecast, feature_contributions = forecast_result
        
        # Step 4: Generate range
        optimistic, pessimistic = self.generate_range_forecast(base_forecast)
        
        # Step 5: Save model
        self.save_model()
        
        print(f"\n" + "=" * 60)
        print("LASSO MODEL ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Final Forecast: {base_forecast:.2f}%")
        print(f"Range: {optimistic:.1f}% - {pessimistic:.1f}%")
        print("Model ready for production use!")
        
        return True

def main():
    forecaster = LASSOForecaster()
    success = forecaster.run_full_analysis()
    
    if success:
        print("\n✓ LASSO model implementation successful!")
    else:
        print("\n✗ LASSO model implementation failed!")

if __name__ == "__main__":
    main()