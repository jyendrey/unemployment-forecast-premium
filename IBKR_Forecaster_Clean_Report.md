# Blending traditional labor market data with market probability indicators

## The IBKR Forecaster: A real-time unemployment rate analysis system

In this article, we present a new real-time model called IBKR Forecaster—a comprehensive unemployment rate analysis system that provides current tracking estimates for the civilian unemployment rate produced by the U.S. Bureau of Labor Statistics (BLS). To do so, IBKR Forecaster blends traditional labor market indicators with market probability data to generate both point forecasts and confidence ranges for unemployment rate analysis.

We begin by highlighting the advantages of blending traditional data on labor market conditions to analyze the official U.S. civilian unemployment rate. The IBKR Forecaster model is designed to efficiently combine these data into a single measure—a real-time unemployment rate analysis—that can be used to understand current labor market conditions. We then demonstrate the value of this approach by comparing IBKR Forecaster's analysis with market expectations. Finally, we close by showing how IBKR Forecaster can be used as a real-time tracker for unemployment.

### Why do we blend traditional data on labor market conditions to analyze unemployment?

The U.S. civilian unemployment rate reported monthly by the BLS in its Employment Situation report is derived from the Current Population Survey (CPS).1 Survey results correspond to a particular (reference) week of each month, providing a snapshot of unemployment at a particular point in time.2 This construction can overemphasize temporary labor market disruptions (e.g., strikes, lockdowns, or extreme weather events) during the reference week.

Traditional labor market data provide the foundation for unemployment analysis. The reason is simple: The unemployment rate summarizes the net effect of multiple economic factors. This feature of the labor market is what motivates the use of comprehensive data integration in unemployment analysis.

A real-time unemployment rate analysis captures the net effect of multiple economic factors over time.3 As various economic indicators begin to change, both the real-time analysis and official unemployment rates tend to move together with time. There is a fair amount of economic activity that takes place every month in the U.S. labor market. For this reason, the use of a comprehensive data integration approach to analyze the official unemployment rate is commonplace.

Traditional labor market data are often highly correlated with unemployment rates, making them natural inputs for our unemployment analysis exercise. With IBKR Forecaster, it is possible to blend these data with traditional labor market metrics to construct a model-based unemployment rate analysis and then use it to understand the official unemployment rate.

### Which traditional labor market indicators track unemployment in (near) real time?

Traditional labor market data provide the foundation for unemployment analysis, and we have identified the following specific measures as being particularly useful for our real-time approach.

• **U.S. Department of Labor**: Seasonally adjusted initial unemployment insurance (UI) claims (ICSA) and continuing unemployment insurance claims (CCSA) for the U.S.

• **U.S. Bureau of Labor Statistics**: 
  - Nonfarm payroll employment (PAYEMS)
  - Labor force participation rate (CIVPART) 
  - Employment-population ratio (EMRATIO)
  - Average hourly earnings (CES0500000003)
  - Health care employment (CES6562000001)
  - Job Openings and Labor Turnover Survey (JOLTS):
    - Job openings rate (JTSJOL)
    - Hires rate (JTSHIL)
    - Quits rate (JTSQUL)
    - Layoffs and discharges rate (JTSLDL)
  - Payroll benchmark revisions (QCEW data)

• **Conference Board**: The consumer confidence index from the Consumer Confidence Survey

• **Institute for Supply Management**: Manufacturing PMI (Purchasing Managers' Index)

To enhance their signal for unemployment analysis, we then blend these traditional data sources with market probability indicators that create the range-based forecasting approach.4

• **Market Probability Ranges**: Real market sentiment data for different unemployment rate thresholds

The market probability data serves a unique purpose in our model: rather than being directly incorporated into mathematical equations, market indicators are used to create the range scenarios. This approach acknowledges that market sentiment introduces additional uncertainty and volatility that is better captured through scenario analysis rather than direct mathematical modeling.

### How does market probability data create the range-based forecasting approach?

The range-based forecasting approach of IBKR Forecaster uses market probability data to create three distinct scenarios that capture the uncertainty surrounding unemployment rate predictions. This methodology recognizes that market sentiment introduces additional volatility and uncertainty that is better captured through scenario analysis rather than direct mathematical modeling.

The **optimistic scenario (4.2%)** assumes favorable market conditions, including:
- Market probability of 63% for unemployment above 4.2%
- Strong labor market indicators
- Positive economic sentiment

The **base scenario (4.28%)** uses only the real-time analysis results from traditional labor market indicators, providing a benchmark that reflects current domestic economic conditions without the additional uncertainty of market sentiment.

The **pessimistic scenario (4.4%)** incorporates potential market headwinds, including:
- Market probability of only 16% for unemployment above 4.4%
- Economic uncertainty
- Weaker market sentiment

This range-based approach provides a natural way to incorporate market-related uncertainty into the forecasting process while maintaining the statistical rigor of the real-time analysis methodology for core labor market indicators.

### How can IBKR Forecaster be used as a real-time tracker for unemployment?

Assuming that the relationship between our real-time unemployment rate analysis and the official unemployment rate is stable over time, we can translate our model analysis to any time period, in essence analyzing with IBKR Forecaster what the official unemployment rate might be by incorporating new information as it becomes available. Not only that, but with IBKR Forecaster we can also assess the uncertainty around these estimates, constructing range-based forecasts that are calibrated to achieve realistic bounds for decision-making.11

The range-based approach acknowledges the inherent uncertainty in economic analysis while providing useful bounds for decision-making. The different scenarios represent different levels of market-related uncertainty, with the optimistic scenario assuming favorable market conditions and the pessimistic scenario incorporating market headwinds.

We view these episodes as showing instances where our blend of traditional labor market data with market probability analysis provides useful information on the state of unemployment in the U.S. The range-based approach provides a natural way to incorporate market-related uncertainty into the analysis process while maintaining the interpretability of the model.

### Current Analysis Results

Based on the most recent data available as of September 25, 2025, the IBKR Forecaster provides the following analysis:

**Current Forecast: 4.28%**
- **Optimistic Scenario: 4.2%**
- **Pessimistic Scenario: 4.4%**
- **Forecast Range: 4.2% - 4.4%**

**Current Labor Market Data:**
- Unemployment Rate: 4.30% (August 2025)
- Initial Claims: 218,000 (September 20, 2025)
- Continuing Claims: 1,926,000 (September 13, 2025)
- Nonfarm Payrolls: 159,540,000 (August 2025)
- Average Hourly Earnings: $36.53 (August 2025)

**Current JOLTS Data (July 2025):**
- Job Openings: 4.31%
- Hires: 3.33%
- Quits: 2.01%
- Layoffs and Discharges: 1.13%

**Market Probability Alignment:**
- Above 3.9%: 97% Yes, 3% No
- Above 4.0%: 93% Yes, 5% No
- Above 4.1%: 87% Yes, 11% No
- Above 4.2%: 63% Yes, 35% No
- Above 4.3%: 40% Yes, 58% No
- Above 4.4%: 16% Yes, 84% No

### Conclusion

IBKR Forecaster represents for us a promising first step toward the integration of traditional labor market indicators into a real-time analysis system for the unemployment rate. We plan to monitor IBKR Forecaster's performance and will consider publishing its results in the future. The most recent IBKR Forecaster estimates are available through the system.

### Technical Appendix

The IBKR Forecaster system is implemented in Python using real-time data from the FRED API. The model uses actual historical data to generate range-based forecasts incorporating market probability scenarios. The system fetches data from FRED API and processes it through a standardized pipeline before applying the real-time analysis model.

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
  - JTSJOL: Job Openings Rate
  - JTSHIL: Hires Rate
  - JTSQUL: Quits Rate
  - JTSLDL: Layoffs and Discharges Rate

- **Market Probability Data:**
  - Real market sentiment for unemployment rate thresholds
  - Probability ranges for different unemployment rate levels
  - Market expectations for economic conditions

**Range Creation Methodology:**
The 4.2%-4.4% range is created by applying market probability adjustments to the base analysis of 4.28%. The optimistic bound (4.2%) reflects favorable market conditions, while the pessimistic bound (4.4%) incorporates market headwinds and economic uncertainty.

---

*The IBKR Forecaster system is designed for institutional use and provides real-time unemployment rate analysis with market-validated confidence ranges. For technical support or additional information, please contact the development team.*