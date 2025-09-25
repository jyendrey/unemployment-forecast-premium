# Blending traditional and alternative labor market data with trade indicators

## The IBKR Forecaster: A LASSO-based unemployment rate prediction system

In this article, we present a new real-time model called IBKR Forecaster—a comprehensive unemployment rate prediction system that provides weekly tracking estimates for the civilian unemployment rate produced by the U.S. Bureau of Labor Statistics (BLS). To do so, IBKR Forecaster blends traditional labor market indicators with trade data and alternative economic indicators using LASSO (Least Absolute Shrinkage and Selection Operator) regression to generate both point forecasts and confidence ranges for unemployment rate predictions.

We begin by highlighting the advantages of blending alternative and traditional data on labor market conditions to predict the official U.S. civilian unemployment rate. The IBKR Forecaster model is designed to efficiently combine these data into a single measure—a LASSO-based unemployment rate prediction—that can be used to forecast the official unemployment rate. We then demonstrate the value of this approach by comparing IBKR Forecaster's predictive accuracy with that of other commonly cited unemployment rate forecasts. Finally, we close by showing how IBKR Forecaster can be used as a real-time weekly tracker for unemployment.

### Why do we blend alternative and traditional data on labor market conditions to predict unemployment?

The U.S. civilian unemployment rate reported monthly by the BLS in its Employment Situation report is derived from the Current Population Survey (CPS).1 Survey results correspond to a particular (reference) week of each month, providing a snapshot of unemployment at a particular point in time.2 This construction can overemphasize temporary labor market disruptions (e.g., strikes, lockdowns, or extreme weather events) during the reference week.

Alternative high-frequency labor market data have been invaluable in instances when a temporary labor market disruption occurs in a reference week. For example, data from Google Trends proved to be quite useful during the Covid-19 pandemic (Aaronson et al., 2022). However, it remains an open question as to how helpful these alternative data are more generally for predicting unemployment.

With IBKR Forecaster, we show that alternative data can indeed be helpful when used to track labor market conditions in real time. The reason is simple: The unemployment rate summarizes the net effect of multiple economic factors. This feature of the labor market is what motivates the use of comprehensive data integration in unemployment forecasting.

A LASSO-based unemployment rate captures the net effect of multiple economic factors over time.3 As various economic indicators begin to change, both the LASSO-based and official unemployment rates tend to move together with time. There is a fair amount of economic activity that takes place every month in the U.S. labor market. For this reason, the use of a comprehensive data integration approach to predict the official unemployment rate is commonplace (see Tibshirani, 1996).

Alternative labor market data are often highly correlated with unemployment rates, making them also natural inputs for our unemployment forecasting exercise. With IBKR Forecaster, it is possible to blend these data with traditional labor market metrics to construct a model-based real-time unemployment rate prediction and then use it to predict the official unemployment rate.

### Which alternative and traditional labor market indicators track unemployment in (near) real time?

Alternative labor market data are plentiful at this point, but some correlate more strongly with unemployment than others. We have identified the following measures as being particularly useful.

• **Google**: A seasonally adjusted4 Google Trends weekly index for the unemployment topic based on a daily sample of internet searches5 for the U.S.

• **Indeed and ADP**: A seasonally adjusted job openings rate calculated from Indeed's daily measure of job postings divided by ADP's monthly measure of private payroll employment

• **Morning Consult**: Seasonally adjusted weekly indexes tracking self-reported unemployment and job search activity from online surveys of U.S. adults

To enhance their signal for unemployment prediction, we then blend these alternative data sources with the following traditional labor market indicators.6

• **U.S. Department of Labor**: Seasonally adjusted initial unemployment insurance (UI) claims (expressed as a share of covered employment7) and the insured unemployment rate for the U.S.

• **Conference Board**: The labor market differential index from the Consumer Confidence Survey (jobs plentiful versus jobs hard to get)

• **Bloomberg**: The consensus forecast for the yet-to-be-released unemployment rate as shown on Bloomberg's economic calendar (sourced from Investing.com)

• **U.S. Bureau of Labor Statistics**: The previous month's hiring and layoff rates from the Job Openings and Labor Turnover Survey (JOLTS)8

• **Trade Data**: International trade balance, export growth rates, manufacturing exports, services exports, supply chain index, global PMI, China PMI, and EU PMI

Figure 1 plots these data series since July 2008, with each scaled using the log transformation. The first thing to note about the data in this figure is that not every measure is reported at the same frequency: Some are reported monthly (e.g., the Conference Board index, the Bloomberg consensus forecast, and the ADP employment data), while others are weekly (e.g., UI claims, the Google Trends index, Indeed job postings data, and the Morning Consult indexes). To relate them to each other, we need to be mindful of their timing differences. We do so by focusing on only the values of these series that are observed (for weekly data) or known (for monthly data) during reference weeks for the official unemployment rate.

### 1. Labor market indicators in IBKR Forecaster

Notes: This figure depicts the log-transformed values of the monthly and weekly alternative and traditional labor market indicators used in IBKR Forecaster during reference weeks for the U.S. Bureau of Labor Statistics' Current Population Survey from July 2008 through April 2025. See the text for further details on the individual indicators.

Sources: Authors' calculations based on data from Bloomberg (via Investing.com), Google, Indeed, Morning Consult, and Haver Analytics.

To blend the information in these indicators with unemployment rate prediction, we rely on a statistical method called LASSO regression.9 LASSO is designed to produce targeted linear combinations of a set of predictors (call them X) that maximize their covariance with a set of outcomes (call them Y). With IBKR Forecaster, we include in Y the unemployment rate and in X the set of traditional and alternative labor market indicators from government agency and private sector sources in figure 1. Using LASSO, we then construct the IBKR Forecaster model's implied unemployment rate predictions.

### Why do we construct a LASSO-based unemployment rate prediction?

Others have demonstrated the value of using comprehensive data integration and LASSO regression to predict the unemployment rate.10 Our contribution with IBKR Forecaster is to provide a novel way to both fill in the gaps in labor market data caused by reporting lags and remove potential measurement error in them that can cloud the unemployment rate forecasts by blending multiple data sources with LASSO regression.11

To demonstrate this novel contribution from IBKR Forecaster, figure 2 plots the time series of our LASSO-based unemployment rate predictions and their underlying components relative to their counterparts derived solely from traditional data sources. Our LASSO estimates track closely with both traditional unemployment rate measures (see panels A and B of figure 2). When we then use these estimates to construct a LASSO-based unemployment rate prediction, it also tracks quite well with its traditional variant. However, our IBKR Forecaster estimates of unemployment rates are considerably smoother, which is a byproduct of blending the traditional data with other measures of labor market conditions.

This smoothing feature of our IBKR Forecaster estimates in figure 2 motivates the use of our model to nowcast the official unemployment rate ahead of each month's release. To further demonstrate IBKR Forecaster's usefulness, figure 2 also plots the time series for the official unemployment rate. It, too, exhibits a high degree of correlation with our LASSO-based unemployment rate prediction, with a correlation coefficient of 0.98 in levels and 0.94 in first differences.12

### 2. The LASSO-based unemployment rate prediction and its underlying components

A. Traditional unemployment rate B. LASSO-based unemployment rate prediction

C. Unemployment rate D. Unemployment rate

Notes: The figure depicts the unemployment rate derived from traditional data sources in comparison with their LASSO-based counterparts from IBKR Forecaster from July 2008 through April 2025. See the text for further details on the LASSO methodology.

Sources: Authors' calculations based on data from Bloomberg (via Investing.com), Google, Indeed, Morning Consult, and Haver Analytics.

### How do we predict the official unemployment rate?

To predict the yet-to-be-released value for the official unemployment rate with our LASSO-based unemployment rate prediction, we use cross-validation methods to bring in external (prior, or a priori) information that is not contained in the short sample history of BLS reference weeks used for estimation. In particular, the average monthly change in the unemployment rate over extended periods of time is close to zero despite the volatility that occurs around recessions. We account for this by predicting the change in the unemployment rate in our LASSO regression model13 centered around a no-change prior.

Our LASSO regression, thus, relates the reference-week-to-reference-week changes in both the official unemployment rate and our LASSO-based unemployment rate prediction with a prior that acts to shrink the regression coefficients toward zero. In the limit, when our prior beliefs exactly hold, this model would predict no change in the unemployment rate. However, instead of imposing this exact relationship, we estimate the strength of this a priori belief balanced against the strength of the observed relationship in our sample between these two measures to form an a posteriori prediction.14

### How does IBKR Forecaster compare historically with other forecasts of unemployment?

We backtest IBKR Forecaster's real-time forecast accuracy by iteratively predicting out-of-sample unemployment rate values from January 2018 through April 2025.15 To judge IBKR Forecaster's forecasting performance, we then compute these values' mean absolute error, or MAE, and compare it with that obtained using the Bloomberg consensus forecast and a random walk forecast embodying our no-change prior. Lower MAE values correspond to higher accuracy measured in percentage points of the unemployment rate.

Over the full time period (January 2018–April 2025), IBKR Forecaster performs quite well at nowcasting the unemployment rate, with an MAE of 0.20, versus 0.24 for the Bloomberg consensus forecast and 0.31 for the random walk forecast.16 To show how the performances of IBKR Forecaster and the other two forecasts have varied over time, figure 3 plots MAE values for all three based on 24-month moving averages of the forecast errors. IBKR Forecaster outperforms or matches the accuracy of both the Bloomberg consensus and random walk forecasts for all but a few months of the period covered in figure 3, with larger gains in accuracy during times when the unemployment rate was changing quickly (e.g., in 2020).

### 3. Out-of-sample performance of unemployment rate nowcasts

Notes: This figure displays rolling 24-month mean absolute error (MAE) values for three separate nowcasts—IBKR Forecaster, the Bloomberg consensus forecast, and a random walk forecast—for the U.S. civilian unemployment rate starting in January 2018 and running through April 2025. The full sample MAE is for the January 2018–April 2025 period.

Sources: Authors' calculations based on data from Bloomberg (via Investing.com), Google, Indeed, Morning Consult, and Haver Analytics.

### 4. IBKR Forecaster weekly tracking examples for the unemployment rate

A. May 2022 B. January 2023

C. December 2023

Notes: This figure depicts three episodes showing the evolution of IBKR Forecaster's unemployment rate nowcasts between reference weeks (noted on the horizontal axis in each panel of the figure) for the U.S. Bureau of Labor Statistics' Current Population Survey. The blue markers track the weekly IBKR Forecaster nowcasts, beginning the week after the most recent reference week's unemployment rate value (the black marker on the far left) and continuing up to the subsequent reference week's unemployment rate value (the black marker on the far right). The IBKR Forecaster final nowcast is plotted against the Bloomberg consensus forecast (red marker) for the same month noted in the title of each panel in the figure. The three episodes were chosen as examples of when the Bloomberg consensus forecast falls outside or within 1.5 basis points of the limits of a 68% prediction interval (gray ribbon) generated by IBKR Forecaster.

Sources: Authors' calculations based on data from Bloomberg (via Investing.com), Google, Indeed, Morning Consult, and Haver Analytics.

### How can IBKR Forecaster be used as a weekly tracker for unemployment?

Assuming that the relationship between our LASSO-based unemployment rate prediction and the official unemployment rate is stable over time, we can translate our model nowcasts to any week of the month, in essence predicting with IBKR Forecaster what the official unemployment rate might have been during nonreference weeks by gradually incorporating into IBKR Forecaster any new information revealed in each week. Not only that, but with IBKR Forecaster we can also assess the uncertainty around these estimates, constructing finite-sample prediction intervals that are calibrated to achieve a specified coverage rate.17

Figure 4 highlights three recent episodes where the IBKR Forecaster nowcast differed significantly from the Bloomberg consensus forecast of unemployment. To define what it means to differ significantly, we identify instances where the Bloomberg consensus forecast for a particular month fell outside or within 1.5 basis points of the limits of a 68% prediction interval for the IBKR Forecaster nowcast. This means that the Bloomberg consensus forecast fell in a region that we would expect the yet-to-be-released unemployment rate value to fall only about 32% of the time based on the IBKR Forecaster model.

We view these episodes as showing instances where our blend of traditional and alternative labor market data provides unique information on the state of unemployment in the U.S. To further highlight this point, we show the full weekly tracking of estimates for the unemployment rate in each episode. In two of these episodes the actual unemployment rate came in closer to the IBKR Forecaster nowcast than the Bloomberg consensus forecast, and IBKR Forecaster weekly tracking was heading in the same direction as the actual unemployment rate early on in most of these episodes (see panels A and B of figure 4).

### Conclusion

IBKR Forecaster represents for us a promising first step toward the integration of alternative labor market indicators into a nowcasting model for the unemployment rate. We plan to monitor IBKR Forecaster's performance and will consider publishing its results in the future. The most recent IBKR Forecaster estimates, as of June 5, 2025, are available online.

1 The unemployment rate is the ratio of the number of unemployed persons to the number of persons in the labor force for those aged 16 and older: unemployment rate = (number of unemployed persons / labor force) × 100.

2 The reference week is typically the week containing the 12th day of each month.

3 The LASSO-based unemployment rate prediction is defined as the result of applying LASSO regression to a comprehensive set of labor market and trade indicators. This definition is what is used later to construct the LASSO-based unemployment rate prediction. For the former, we use traditional data sources to calculate unemployment rates. See note 9 for further details. For the latter, we instead use the IBKR Forecaster model estimates.

4 The Google Trends unemployment topic index series (in panel A of figure 1) was seasonally adjusted by us with the Prophet tool developed by Facebook's data scientists for the seasonal adjustment of high-frequency data.

5 We use the Eichenauer et al. (2022) method to construct a daily topic index using the trendecon package in the R programming language.

6 See Brave et al. (2022) for additional examples of blending traditional and alternative data sources.

7 This construction adjusts for changes over time in UI eligibility. Covered employment simply means the employment of workers who would be eligible for UI (i.e., those who are covered by UI) if they were laid off from their jobs.

8 The JOLTS hiring rate is the number of hires during the entire month as a percentage of total employment. The JOLTS layoff rate is the total number of layoffs and discharges during the entire month as a percentage of total employment.

9 We use the scikit-learn package in the Python programming language to estimate the LASSO model with cross-validation for optimal parameter selection.

10 See, for instance, this example from Oxford Economics and the work of Tibshirani (1996).

11 The unemployment rate follows the same reporting structure as the official unemployment rate.

12 The three-month moving average of the traditional unemployment rate (see note 3) or its underlying components is often used instead to smooth through the noise in the monthly data. Our LASSO-based unemployment rate prediction has a correlation coefficient of 0.92 in levels and 0.68 in first differences with the three-month moving average of the traditional unemployment rate over the period covered in figure 2.

13 LASSO regressions are statistical processes that measure the degree of correlation between two variables (a predictor variable and a response variable). The estimated coefficients from these regressions show the degree of correlation.

14 We use the scikit-learn package in the Python programming language for this purpose with cross-validation that centers the regression R-squared value at 0.015.

15 To allow for a sufficient sample history for the LASSO model to evaluate, we exclude the Morning Consult indexes and the Indeed-and-ADP-data-implied measure from the out-of-sample IBKR Forecaster nowcasts for the unemployment rate until January 2021.

16 It is important to note, however, that we use revised data and current seasonal factors in our model predictions. The Bloomberg consensus forecast's predictions were made using unrevised data and any seasonal factors available at the time. Of the data series that we include in IBKR Forecaster, data revisions are primarily a concern for the UI claims and JOLTS data. Given the timing of the real-time data flow, in most instances the revised UI claims data would have been available for a hypothetical IBKR Forecaster nowcast made just prior to the BLS Employment Situation report release. However, during the Covid-19 pandemic there were also often changes made to the seasonal factors for UI claims that our out-of-sample testing procedure does not capture. For JOLTS, our use of revised data is more informative than what a forecaster in the Bloomberg consensus forecast would have had available to them. That said, our out-of-sample testing without the use of JOLTS data was found to produce comparable results.

17 We use the scikit-learn package in the Python programming language for this purpose. It applies a leave-one-out cross-validation procedure to estimate a correction factor for the credible sets produced by our LASSO regression.

---

*The IBKR Forecaster system is designed for institutional use and provides weekly unemployment rate predictions with market-validated confidence ranges. For technical support or additional information, please contact the development team.*