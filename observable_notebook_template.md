# IBKR Forecaster - Observable Notebook Template

## Setup and Data Import

```javascript
// Import required libraries
import {Plot, dot} from "@observablehq/plot"
import {csv} from "d3-fetch"

// Data from your LASSO model
const lassoResults = {
  forecast: 3.83,
  range: {
    optimistic: 4.2,
    pessimistic: 4.4
  },
  r2: 0.7241,
  features: {
    "Initial Claims": 0.2842,
    "Employment-Population Ratio": -0.2062
  },
  contributions: {
    "Initial Claims": -0.1236,
    "Employment-Population Ratio": -0.0502
  }
}

// Market probability data
const marketProbabilities = [
  {threshold: 3.9, yes: 97, no: 3},
  {threshold: 4.0, yes: 93, no: 5},
  {threshold: 4.1, yes: 87, no: 11},
  {threshold: 4.2, yes: 63, no: 35},
  {threshold: 4.3, yes: 40, no: 58},
  {threshold: 4.4, yes: 16, no: 84}
]

// Historical unemployment data (sample - replace with your actual data)
const unemploymentData = [
  {date: "2020-02-01", rate: 3.5},
  {date: "2020-05-01", rate: 13.0},
  {date: "2020-08-01", rate: 8.4},
  {date: "2021-02-01", rate: 6.2},
  {date: "2021-08-01", rate: 5.2},
  {date: "2022-02-01", rate: 3.8},
  {date: "2022-08-01", rate: 3.7},
  {date: "2023-02-01", rate: 3.6},
  {date: "2023-08-01", rate: 3.8},
  {date: "2024-02-01", rate: 3.9},
  {date: "2024-08-01", rate: 4.3},
  {date: "2025-02-01", rate: 4.1},
  {date: "2025-08-01", rate: 4.3}
]
```

## Chart 1: Historical Unemployment Rate with LASSO Forecast

```javascript
Plot.plot({
  title: "Unemployment Rate: Historical Data and LASSO Forecast",
  subtitle: "IBKR Forecaster - LASSO Model (R² = 0.7241)",
  width: 800,
  height: 400,
  x: {type: "utc", domain: [new Date("2020-01-01"), new Date("2025-12-31")]},
  y: {domain: [0, 15], label: "Unemployment Rate (%)"},
  color: {legend: true},
  marks: [
    // Historical data line
    Plot.line(unemploymentData, {
      x: d => new Date(d.date),
      y: "rate",
      stroke: "steelblue",
      strokeWidth: 2
    }),
    
    // Historical data points
    Plot.dot(unemploymentData, {
      x: d => new Date(d.date),
      y: "rate",
      fill: "steelblue",
      r: 4
    }),
    
    // LASSO forecast point
    Plot.dot([{date: "2025-10-01", rate: lassoResults.forecast}], {
      x: d => new Date(d.date),
      y: "rate",
      fill: "red",
      r: 6,
      title: `LASSO Forecast: ${lassoResults.forecast}%`
    }),
    
    // Forecast range
    Plot.ruleY([lassoResults.range.optimistic, lassoResults.range.pessimistic], {
      x: new Date("2025-10-01"),
      stroke: "red",
      strokeWidth: 3,
      strokeOpacity: 0.7
    }),
    
    // Range labels
    Plot.text([{x: new Date("2025-10-01"), y: lassoResults.range.optimistic, text: "4.2%"}], {
      x: "x",
      y: "y",
      text: "text",
      dx: 20,
      fill: "red",
      fontSize: 12
    }),
    Plot.text([{x: new Date("2025-10-01"), y: lassoResults.range.pessimistic, text: "4.4%"}], {
      x: "x",
      y: "y",
      text: "text",
      dx: 20,
      fill: "red",
      fontSize: 12
    })
  ]
})
```

## Chart 2: LASSO Feature Importance

```javascript
const featureData = Object.entries(lassoResults.features).map(([name, value]) => ({
  feature: name,
  coefficient: value,
  abs_coefficient: Math.abs(value)
}))

Plot.plot({
  title: "LASSO Feature Importance (Coefficients)",
  subtitle: "Higher absolute values indicate greater importance",
  width: 600,
  height: 300,
  x: {label: "Coefficient Value"},
  y: {label: "Feature"},
  color: {scheme: "redblue", domain: [-0.3, 0.3]},
  marks: [
    Plot.barX(featureData, {
      x: "coefficient",
      y: "feature",
      fill: d => d.coefficient > 0 ? "red" : "blue",
      title: d => `${d.feature}: ${d.coefficient.toFixed(4)}`
    }),
    Plot.ruleX([0], {stroke: "black", strokeDasharray: "2,2"})
  ]
})
```

## Chart 3: Market Probability Ranges

```javascript
Plot.plot({
  title: "Market Probability Ranges for Unemployment Rate",
  subtitle: "Market expectations for different unemployment thresholds",
  width: 700,
  height: 400,
  x: {label: "Unemployment Rate Threshold (%)"},
  y: {domain: [0, 100], label: "Probability (%)"},
  color: {legend: true},
  marks: [
    Plot.line(marketProbabilities, {
      x: "threshold",
      y: "yes",
      stroke: "steelblue",
      strokeWidth: 3
    }),
    Plot.dot(marketProbabilities, {
      x: "threshold",
      y: "yes",
      fill: "steelblue",
      r: 5,
      title: d => `Above ${d.threshold}%: ${d.yes}% Yes, ${d.no}% No`
    }),
    
    // Add our forecast point
    Plot.dot([{threshold: lassoResults.forecast, yes: 0}], {
      x: "threshold",
      y: "yes",
      fill: "red",
      r: 8,
      title: `LASSO Forecast: ${lassoResults.forecast}%`
    }),
    
    // Add range lines
    Plot.ruleX([lassoResults.range.optimistic, lassoResults.range.pessimistic], {
      stroke: "red",
      strokeWidth: 2,
      strokeOpacity: 0.7
    })
  ]
})
```

## Chart 4: Feature Contributions to Current Forecast

```javascript
const contributionData = Object.entries(lassoResults.contributions).map(([name, value]) => ({
  feature: name,
  contribution: value,
  abs_contribution: Math.abs(value)
}))

Plot.plot({
  title: "Feature Contributions to Current LASSO Forecast",
  subtitle: "How each feature affects the 3.83% forecast",
  width: 600,
  height: 250,
  x: {label: "Contribution to Forecast"},
  y: {label: "Feature"},
  color: {scheme: "redblue", domain: [-0.2, 0.2]},
  marks: [
    Plot.barX(contributionData, {
      x: "contribution",
      y: "feature",
      fill: d => d.contribution > 0 ? "red" : "blue",
      title: d => `${d.feature}: ${d.contribution.toFixed(4)}`
    }),
    Plot.ruleX([0], {stroke: "black", strokeDasharray: "2,2"})
  ]
})
```

## Chart 5: Model Performance Metrics

```javascript
const performanceData = [
  {metric: "R² Score", value: lassoResults.r2, max: 1},
  {metric: "Data Points", value: 10, max: 100},
  {metric: "Features", value: 10, max: 20},
  {metric: "Regularization (α)", value: 0.01, max: 0.1}
]

Plot.plot({
  title: "LASSO Model Performance Metrics",
  width: 600,
  height: 200,
  x: {label: "Value"},
  y: {label: "Metric"},
  marks: [
    Plot.barX(performanceData, {
      x: "value",
      y: "metric",
      fill: "steelblue",
      title: d => `${d.metric}: ${d.value}`
    })
  ]
})
```

## Summary Dashboard

```javascript
// Create a summary table
const summaryData = [
  {metric: "LASSO Forecast", value: `${lassoResults.forecast}%`},
  {metric: "Forecast Range", value: `${lassoResults.range.optimistic}% - ${lassoResults.range.pessimistic}%`},
  {metric: "Model R²", value: lassoResults.r2.toFixed(4)},
  {metric: "Key Features", value: "Initial Claims, Employment-Population Ratio"},
  {metric: "Data Points", value: "10 aligned observations"},
  {metric: "Date Range", value: "2020-02-01 to 2025-03-01"}
]

// Display as HTML table
html`<table style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr style="background-color: #f0f0f0;">
      <th style="padding: 8px; border: 1px solid #ddd;">Metric</th>
      <th style="padding: 8px; border: 1px solid #ddd;">Value</th>
    </tr>
  </thead>
  <tbody>
    ${summaryData.map(d => html`<tr>
      <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">${d.metric}</td>
      <td style="padding: 8px; border: 1px solid #ddd;">${d.value}</td>
    </tr>`)}
  </tbody>
</table>`
```

## Instructions for Observable:

1. **Copy this code** into your Observable notebook
2. **Replace the sample data** with your actual FRED data
3. **Customize the charts** as needed
4. **Add more visualizations** for specific analysis
5. **Share the notebook** with stakeholders

## Additional Chart Ideas:

- **Time series of feature values** (Initial Claims, Employment-Population Ratio)
- **Residual analysis** (actual vs predicted)
- **Confidence intervals** around the forecast
- **Rolling window analysis** of model performance
- **Interactive sliders** to adjust forecast parameters

This gives you a comprehensive dashboard for your LASSO model results!