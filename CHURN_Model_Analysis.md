# CHURN: Chicago Fed Unemployment Rate Nowcast
## Blending Traditional and Alternative Labor Market Data

**Document ID:** bc-bde4048d-a0ab-4529-88ec-d335bbfe685c  
**Source:** [Chicago Fed Letter #506](https://www.chicagofed.org/publications/chicago-fed-letter/2025/506)  
**Authors:** Scott A. Brave, Benjamin Henken, Ezra Karger  
**Date:** 2025

---

## Executive Summary

The Chicago Fed Unemployment Rate Nowcast (CHURN) represents a novel approach to predicting the U.S. civilian unemployment rate by blending traditional labor market indicators with alternative high-frequency data sources. This model provides weekly tracking estimates that outperform existing forecasting methods, particularly during periods of rapid economic change.

## Introduction

CHURN addresses a critical limitation in traditional unemployment rate measurement: the monthly Current Population Survey (CPS) provides only a snapshot during a specific reference week, which can overemphasize temporary disruptions. By incorporating alternative data sources that track job flows in real-time, CHURN offers a more dynamic and accurate forecasting tool.

### Key Innovation

The model's core innovation lies in its ability to:
- Blend monthly BLS job flow statistics with high-frequency alternative indicators
- Create a model-implied flow-consistent unemployment rate (FCR)
- Provide weekly tracking capabilities for unemployment rate prediction
- Outperform traditional forecasting methods with a mean absolute error of 0.20

## Methodology

### Data Sources

CHURN integrates ten key indicators across two categories:

#### Alternative Data Sources
- **Google Trends**: Seasonally adjusted weekly index for unemployment-related searches
- **Indeed and ADP**: Job openings rate calculated from daily job postings divided by monthly payroll employment
- **Morning Consult**: Weekly indexes tracking self-reported unemployment and job search activity

#### Traditional Labor Market Indicators
- **U.S. Department of Labor**: Initial unemployment insurance claims and insured unemployment rate
- **Conference Board**: Labor market differential index from Consumer Confidence Survey
- **Bloomberg**: Consensus forecast for upcoming unemployment rate releases
- **Bureau of Labor Statistics**: Previous month's hiring and layoff rates from JOLTS

### Statistical Approach

The model employs **Partial Least Squares (PLS)** regression to:
- Maximize covariance between predictors (X) and outcomes (Y)
- Include job-separation and job-finding rates from CPS as outcomes
- Incorporate all traditional and alternative indicators as predictors
- Generate model-implied job flow rates and FCR

### Bayesian Framework

CHURN uses Bayesian estimation methods with:
- **No-change prior**: Acknowledging that average monthly unemployment rate changes are near zero
- **Bayesian linear regression**: Relating reference-week changes in official unemployment rate and model-implied FCR
- **Shrinkage toward zero**: Balancing prior beliefs with observed relationships
- **Uncertainty quantification**: Providing prediction intervals calibrated to specified coverage rates

## Key Findings

### Performance Metrics

**Out-of-sample testing (January 2018–April 2025):**
- **CHURN MAE**: 0.20 percentage points
- **Bloomberg Consensus MAE**: 0.24 percentage points  
- **Random Walk MAE**: 0.31 percentage points

### Correlation Analysis

The model-implied FCR demonstrates strong correlation with official unemployment rates:
- **Levels**: 0.98 correlation coefficient
- **First differences**: 0.94 correlation coefficient

### Smoothing Benefits

CHURN estimates provide smoother tracking compared to CPS-derived rates, reducing noise while maintaining accuracy. This smoothing is particularly valuable for:
- Real-time monitoring
- Identifying underlying trends
- Reducing temporary disruption effects

## Practical Applications

### Weekly Tracking Capabilities

CHURN enables prediction of unemployment rates for any week of the month by:
- Gradually incorporating new information as it becomes available
- Translating model nowcasts to non-reference weeks
- Providing uncertainty estimates through prediction intervals

### Real-World Performance

Analysis of three recent episodes (May 2022, January 2023, December 2023) shows:
- CHURN nowcasts often closer to actual unemployment rates than Bloomberg consensus
- Early directional accuracy in weekly tracking
- Significant differences from consensus forecasts in 32% of cases (outside 68% prediction intervals)

## Technical Implementation

### Data Processing
- **Seasonal Adjustment**: Prophet tool for high-frequency data
- **Topic Index Construction**: Eichenauer et al. (2022) method using R's trendecon package
- **Job Flow Calculations**: Shimer (2005) method for CPS-derived rates

### Software Tools
- **R Programming**: Primary implementation language
- **ropls package**: PLS model estimation
- **rstanarm package**: Bayesian regression
- **conformalbayes package**: Prediction interval calibration

### Model Specifications
- **PLS Components**: Two common components assumption
- **Bayesian Prior**: LKJ prior with R-squared centered at 0.015
- **Cross-validation**: Leave-one-out procedure for credible sets

## Limitations and Considerations

### Data Revisions
- Model uses revised data and current seasonal factors
- Real-time performance may differ due to data revision timing
- UI claims seasonal factors changed frequently during COVID-19 pandemic

### Sample Limitations
- Morning Consult indexes and Indeed-ADP measure excluded until January 2021
- Sufficient sample history required for PLS model evaluation
- JOLTS data revisions provide more information than real-time consensus forecasts

## Future Directions

The Chicago Fed plans to:
- Monitor CHURN's ongoing performance
- Consider publishing regular results
- Continue refining the model based on new data sources
- Explore additional alternative indicators

## Conclusion

CHURN represents a significant advancement in unemployment rate forecasting by successfully integrating alternative data sources with traditional labor market indicators. The model's superior performance, particularly during periods of rapid change, demonstrates the value of blending diverse data sources for economic nowcasting.

The weekly tracking capabilities and uncertainty quantification make CHURN a valuable tool for policymakers, researchers, and market participants seeking real-time insights into labor market conditions.

---

## References

- Aaronson, D., et al. (2022). "Google Trends and Unemployment During COVID-19"
- Barnichon, R., & Nekarda, C. (2012). "The Ins and Outs of Forecasting Unemployment"
- Brave, S. A., et al. (2022). "Blending Traditional and Alternative Data Sources"
- Eichenauer, V. Z., et al. (2022). "Topic Index Construction Methods"
- Şahin, A., & Patterson, C. (2012). "The Bathtub Model of Unemployment"
- Şahin, A., et al. (2021). "Flow-Consistent Unemployment Rate Applications"
- Shimer, R. (2005). "Job Finding and Job Separation Rates"

---

*This document is based on Chicago Fed Letter #506, published by the Federal Reserve Bank of Chicago. The most recent CHURN estimates are available online as of June 5, 2025.*