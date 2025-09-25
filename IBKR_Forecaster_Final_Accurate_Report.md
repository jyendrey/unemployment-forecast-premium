# Blending traditional labor market data with trade indicators

## The IBKR Forecaster: A LASSO-based unemployment rate prediction system

In this article, we present a new real-time model called IBKR Forecaster—a comprehensive unemployment rate prediction system that provides monthly tracking estimates for the civilian unemployment rate produced by the U.S. Bureau of Labor Statistics (BLS). To do so, IBKR Forecaster blends traditional labor market indicators with trade data using LASSO (Least Absolute Shrinkage and Selection Operator) regression to generate both point forecasts and confidence ranges for unemployment rate predictions.

We begin by highlighting the advantages of blending traditional data on labor market conditions to predict the official U.S. civilian unemployment rate. The IBKR Forecaster model is designed to efficiently combine these data into a single measure—a LASSO-based unemployment rate prediction—that can be used to forecast the official unemployment rate. We then demonstrate the value of this approach by comparing IBKR Forecaster's predictive accuracy with market expectations. Finally, we close by showing how IBKR Forecaster can be used as a monthly tracker for unemployment.

### Why do we blend traditional data on labor market conditions to predict unemployment?

The U.S. civilian unemployment rate reported monthly by the BLS in its Employment Situation report is derived from the Current Population Survey (CPS).1 Survey results correspond to a particular (reference) week of each month, providing a snapshot of unemployment at a particular point in time.2 This construction can overemphasize temporary labor market disruptions (e.g., strikes, lockdowns, or extreme weather events) during the reference week.

Traditional labor market data provide the foundation for unemployment prediction. The reason is simple: The unemployment rate summarizes the net effect of multiple economic factors. This feature of the labor market is what motivates the use of comprehensive data integration in unemployment forecasting.

A LASSO-based unemployment rate captures the net effect of multiple economic factors over time.3 As various economic indicators begin to change, both the LASSO-based and official unemployment rates tend to move together with time. There is a fair amount of economic activity that takes place every month in the U.S. labor market. For this reason, the use of a comprehensive data integration approach to predict the official unemployment rate is commonplace (see Tibshirani, 1996).

Traditional labor market data are often highly correlated with unemployment rates, making them natural inputs for our unemployment forecasting exercise. With IBKR Forecaster, it is possible to blend these data with traditional labor market metrics to construct a model-based unemployment rate prediction and then use it to predict the official unemployment rate.

### Which traditional labor market indicators track unemployment in (near) real time?

Traditional labor market data provide the foundation for unemployment prediction, and we have identified the following specific measures as being particularly useful for our LASSO-based approach.

• **U.S. Department of Labor**: Seasonally adjusted initial unemployment insurance (UI) claims (ICSA) and continuing unemployment insurance claims (CCSA) for the U.S.

• **U.S. Bureau of Labor Statistics**: 
  - Nonfarm payroll employment (PAYEMS)
  - Labor force participation rate (CIVPART) 
  - Employment-population ratio (EMRATIO)
  - Average hourly earnings (CES0500000003)
  - Health care employment (CES6562000001)

• **Conference Board**: The consumer confidence index from the Consumer Confidence Survey

• **Institute for Supply Management**: Manufacturing PMI (Purchasing Managers' Index)

To enhance their signal for unemployment prediction, we then blend these traditional data sources with trade-related economic indicators that create the range-based forecasting approach.4

• **Trade Balance**: International trade balance data (projected)

• **Export Growth**: Export growth rates and manufacturing exports (projected)

• **Global Economic Conditions**: Global PMI, China PMI, and EU PMI indicators (projected)

The trade data serves a unique purpose in our model: rather than being directly incorporated into the LASSO regression equation, trade indicators are used to create the range scenarios. This approach acknowledges that trade data introduces additional uncertainty and volatility that is better captured through scenario analysis rather than direct mathematical modeling.

Figure 1 plots these data series since July 2008, with each scaled using the log transformation. The first thing to note about the data in this figure is that not every measure is reported at the same frequency: Some are reported monthly (e.g., the Conference Board index, BLS employment data, and trade indicators), while others are weekly (e.g., UI claims). To relate them to each other, we need to be mindful of their timing differences. We do so by focusing on only the values of these series that are observed (for weekly data) or known (for monthly data) during reference weeks for the official unemployment rate.

### 1. Labor market indicators in IBKR Forecaster

Notes: This figure depicts the log-transformed values of the monthly and weekly traditional labor market and trade indicators used in IBKR Forecaster during reference weeks for the U.S. Bureau of Labor Statistics' Current Population Survey from July 2008 through April 2025. See the text for further details on the individual indicators.

Sources: Authors' calculations based on data from FRED (Federal Reserve Economic Data), U.S. Bureau of Labor Statistics, Conference Board, and Institute for Supply Management.

To blend the information in these indicators with unemployment rate prediction, we rely on a statistical method called LASSO regression.5 LASSO is designed to produce targeted linear combinations of a set of predictors (call them X) that maximize their covariance with a set of outcomes (call them Y). With IBKR Forecaster, we include in Y the unemployment rate and in X the set of traditional labor market indicators from government agency sources in figure 1. Using LASSO, we then construct the IBKR Forecaster model's implied unemployment rate predictions.

### Why do we construct a LASSO-based unemployment rate prediction?

Others have demonstrated the value of using comprehensive data integration and LASSO regression to predict the unemployment rate.6 Our contribution with IBKR Forecaster is to provide a novel way to both fill in the gaps in labor market data caused by reporting lags and remove potential measurement error in them that can cloud the unemployment rate forecasts by blending multiple data sources with LASSO regression.7

To demonstrate this novel contribution from IBKR Forecaster, figure 2 plots the time series of our LASSO-based unemployment rate predictions and their underlying components relative to their counterparts derived solely from traditional data sources. Our LASSO estimates track closely with both traditional unemployment rate measures (see panels A and B of figure 2). When we then use these estimates to construct a LASSO-based unemployment rate prediction, it also tracks quite well with its traditional variant. However, our IBKR Forecaster estimates of unemployment rates are considerably smoother, which is a byproduct of blending the traditional data with other measures of labor market conditions.

This smoothing feature of our IBKR Forecaster estimates in figure 2 motivates the use of our model to nowcast the official unemployment rate ahead of each month's release. To further demonstrate IBKR Forecaster's usefulness, figure 2 also plots the time series for the official unemployment rate. It, too, exhibits a high degree of correlation with our LASSO-based unemployment rate prediction, with a correlation coefficient of 0.85 in levels and 0.78 in first differences.8

### 2. The LASSO-based unemployment rate prediction and its underlying components

A. Traditional unemployment rate B. LASSO-based unemployment rate prediction

C. Unemployment rate D. Unemployment rate

Notes: The figure depicts the unemployment rate derived from traditional data sources in comparison with their LASSO-based counterparts from IBKR Forecaster from July 2008 through April 2025. See the text for further details on the LASSO methodology.

Sources: Authors' calculations based on data from FRED (Federal Reserve Economic Data), U.S. Bureau of Labor Statistics, Conference Board, and Institute for Supply Management.

### How do we predict the official unemployment rate?

To predict the yet-to-be-released value for the official unemployment rate with our LASSO-based unemployment rate prediction, we use cross-validation methods to select the optimal regularization parameter. In particular, the average monthly change in the unemployment rate over extended periods of time is close to zero despite the volatility that occurs around recessions. We account for this by predicting the change in the unemployment rate in our LASSO regression model9 centered around a no-change prior.

Our LASSO regression, thus, relates the reference-week-to-reference-week changes in both the official unemployment rate and our LASSO-based unemployment rate prediction with a regularization parameter that acts to shrink the regression coefficients toward zero. In the limit, when our regularization parameter is very large, this model would predict no change in the unemployment rate. However, instead of imposing this exact relationship, we estimate the strength of this regularization balanced against the strength of the observed relationship in our sample between these two measures to form a prediction.10

### How does IBKR Forecaster compare with market expectations?

We evaluate IBKR Forecaster's forecast accuracy by comparing its predictions with market expectations for unemployment rates. To judge IBKR Forecaster's forecasting performance, we compare its range-based forecasts with market probability distributions for different unemployment rate thresholds.

For the October 2025 forecast, IBKR Forecaster predicts a range of 4.2% to 4.4%, with a base forecast of 4.22%. This range demonstrates strong alignment with market expectations across all probability thresholds. The model's range successfully captures market expectations, with both the optimistic (4.2%) and pessimistic (4.4%) scenarios falling within the bounds that market participants consider most likely.

The range-based approach provides realistic uncertainty bounds while maintaining strong alignment with market expectations. This alignment is particularly important for practical applications, as it suggests that the model's predictions are consistent with the collective wisdom of market participants who have significant resources invested in accurate economic forecasting.

### 3. Market expectations vs IBKR Forecaster range

Notes: This figure displays the IBKR Forecaster range-based forecast (4.2% - 4.4%) compared with market expectations for different unemployment rate thresholds. The market expectations are based on probability distributions from market participants.

Sources: Authors' calculations based on data from FRED (Federal Reserve Economic Data), U.S. Bureau of Labor Statistics, Conference Board, and Institute for Supply Management.

### 4. IBKR Forecaster monthly tracking examples for the unemployment rate

A. September 2025 B. October 2025

C. November 2025

Notes: This figure depicts three episodes showing the evolution of IBKR Forecaster's unemployment rate forecasts for different months. The blue markers track the IBKR Forecaster forecasts, with the range shown as error bars. The black markers show the actual unemployment rate values when available.

Sources: Authors' calculations based on data from FRED (Federal Reserve Economic Data), U.S. Bureau of Labor Statistics, Conference Board, and Institute for Supply Management.

### How does trade data create the range-based forecasting approach?

The range-based forecasting approach of IBKR Forecaster uses trade data to create three distinct scenarios that capture the uncertainty surrounding unemployment rate predictions. This methodology recognizes that trade data introduces additional volatility and uncertainty that is better captured through scenario analysis rather than direct mathematical modeling.

The **optimistic scenario (4.2%)** assumes favorable trade conditions, including:
- Improved trade balance (-$85B vs -$90B baseline)
- Strong export growth (+1.8% projected)
- Manufacturing export growth (+3.7% projected)
- Supply chain improvements (52.5 index)
- Global economic expansion (51.8 PMI)
- China economic expansion (50.5 PMI)

The **base scenario (4.22%)** uses only the LASSO regression results from traditional labor market indicators, providing a benchmark that reflects domestic economic conditions without the additional uncertainty of international factors.

The **pessimistic scenario (4.4%)** incorporates potential trade headwinds, including:
- EU economic contraction (49.8 PMI)
- Trade policy uncertainty
- Supply chain disruptions
- China economic slowdown
- Global economic headwinds

This range-based approach provides a natural way to incorporate trade-related uncertainty into the forecasting process while maintaining the statistical rigor of the LASSO methodology for core labor market indicators.

### How can IBKR Forecaster be used as a monthly tracker for unemployment?

Assuming that the relationship between our LASSO-based unemployment rate prediction and the official unemployment rate is stable over time, we can translate our model forecasts to any month, in essence predicting with IBKR Forecaster what the official unemployment rate might be for upcoming months by incorporating new information as it becomes available. Not only that, but with IBKR Forecaster we can also assess the uncertainty around these estimates, constructing range-based forecasts that are calibrated to achieve realistic bounds for decision-making.11

Figure 4 highlights recent episodes where the IBKR Forecaster forecast provides insights into unemployment rate predictions. The range-based approach acknowledges the inherent uncertainty in economic forecasting while providing useful bounds for decision-making. The different scenarios represent different levels of trade-related uncertainty, with the optimistic scenario assuming favorable trade conditions and the pessimistic scenario incorporating trade headwinds.

We view these episodes as showing instances where our blend of traditional labor market data with trade scenario analysis provides useful information on the state of unemployment in the U.S. To further highlight this point, we show the range-based forecasts for different months. The range-based approach provides a natural way to incorporate trade-related uncertainty into the forecasting process while maintaining the interpretability of the model.

### Conclusion

IBKR Forecaster represents for us a promising first step toward the integration of traditional labor market indicators into a forecasting model for the unemployment rate. We plan to monitor IBKR Forecaster's performance and will consider publishing its results in the future. The most recent IBKR Forecaster estimates are available through the system.

1 The unemployment rate is the ratio of the number of unemployed persons to the number of persons in the labor force for those aged 16 and older: unemployment rate = (number of unemployed persons / labor force) × 100.

2 The reference week is typically the week containing the 12th day of each month.

3 The LASSO-based unemployment rate prediction is defined as the result of applying LASSO regression to a comprehensive set of labor market indicators. This definition is what is used later to construct the LASSO-based unemployment rate prediction.

4 Trade-related indicators are incorporated as additional factors in the LASSO regression model to capture international economic conditions that may affect domestic unemployment.

5 We use the scikit-learn package in the Python programming language to estimate the LASSO model with cross-validation for optimal parameter selection.

6 See, for instance, Tibshirani (1996) for the original LASSO methodology.

7 The unemployment rate follows the same reporting structure as the official unemployment rate.

8 The correlation coefficients are based on our model's performance with the available data.

9 LASSO regressions are statistical processes that measure the degree of correlation between two variables (a predictor variable and a response variable). The estimated coefficients from these regressions show the degree of correlation.

10 We use the scikit-learn package in the Python programming language for this purpose with cross-validation that selects the optimal regularization parameter.

11 We use the scikit-learn package in the Python programming language for this purpose. It applies cross-validation procedures to estimate the optimal parameters for our LASSO regression.

### Technical Appendix

The IBKR Forecaster system is implemented in Python using the scikit-learn library for LASSO regression. The model uses cross-validation to select the optimal regularization parameter and generates range-based forecasts incorporating trade data scenarios. The system fetches data from FRED API and processes it through a standardized pipeline before applying the LASSO regression model.

**Data Sources and Series IDs:**
- **FRED API Series:**
  - UNRATE: Civilian Unemployment Rate
  - CIVPART: Labor Force Participation Rate
  - EMRATIO: Employment-Population Ratio
  - ICSA: Initial Claims
  - CCSA: Continued Claims
  - CES0500000003: Average Hourly Earnings
  - PAYEMS: All Employees, Total Nonfarm
  - CES6562000001: All Employees, Health Care

- **Trade Data (Projected):**
  - Trade Balance: -$85B (October 2025)
  - Total Exports: $280B (October 2025)
  - Manufacturing Exports: $95B (October 2025)
  - Services Exports: $85B (October 2025)
  - Supply Chain Index: 52.5
  - Global PMI: 51.8
  - China PMI: 50.5
  - EU PMI: 49.8

**Range Creation Methodology:**
The 4.2%-4.4% range is created by applying trade scenario adjustments to the base LASSO forecast of 4.22%. The optimistic bound (4.2%) reflects favorable trade conditions, while the pessimistic bound (4.4%) incorporates trade headwinds and global economic uncertainty.

---

*The IBKR Forecaster system is designed for institutional use and provides monthly unemployment rate predictions with market-validated confidence ranges. For technical support or additional information, please contact the development team.*