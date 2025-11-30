# Does option flow before the earnings affect the post-earning performance?
Hi, I'm Eren Bora(34549). For my DSA 210 project my main aim is to find out if there is correlation between the option flow(call-bullish/put-bearish) and the price of the stock the day after just after they release their earnings or not. 
# Motivation
For my DSA210 project I choose a topic which I am geninely curious about: the influence of option flow just the day before earnings date and it's affect on stocks performance. Through the analyzsis I will will be focusing on  Magnificent Seven (Alphabet, Amazon, Apple, Tesla, Meta Platforms, Microsoft, and NVIDIA) companies due to their market signifence with their trading volume, ratio in S&P500(making up 37.4% of S&P500 currently) and market cap. The main goal is to analzye the impaxt of Put/Call volume that occur in the final trading session just before a company's earnings release. The analysis will determine if there is a statistically significant correlation between this pre-earnings option flow data and the direction of the stock's price response in the post-earnings session.
# Hypothesis
H₀ : Option flow before to the earnings report has no statistically significant effect on the performance of the stock's post-earnings price response.

H₁ : Option flows (Put/Call) observed in the trading session immediately before the earnings announcement is a statistically significant predictor of the performance of the stock's post-earnings price response.
# Dataset
Price Source: Yahoo Finance (Historical Price Data). Price prior to the report.

Flow Source: unusualwhales.com (Pre-Earnings Option Flow Database).

Sample Scope: To achieve adequate statistical power for the hypothesis tests, the study will include all quarters of 2025. For analytical clarity and relevance to short-term o      option liquidation, the performance will be quantified as the percent price change observed exclusively during the first hour of trading after market open. This time constraint     addresses the extreme volatility often observed and isolates the critical profit-taking period. 
The analysis will use the distribution of strike prices relative to the stock's closing price to categorize flow as At-the-Money (ATM) or Out-of-the-Money (OTM) to measure the      aggressive intent of the positioning. Key descriptive statistics (Mean, Median, Standard Deviation) will be calculated for both the P/C Ratio and the post-earnings performance to   understand the overall market bias before hypothesis testing begins.

