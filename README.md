# DSA 210 Term Project: Option Flow Analysis & Stock Prediction

**Student:** Eren Bora (34549)  
**Course:** DSA 210 Introduction to Data Science  
**Term:** Fall 2025-2026

---

## 1. Motivation
The primary objective of this project is to investigate the relationship between **Option Flow** (specifically Put/Call volume and sentiment) and the **post-earnings price performance** of the "Magnificent Seven" stocks (AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META).

Financial markets are often driven by institutional "smart money." The hypothesis is that significant option activity (e.g., a surge in Call volume) immediately before an earnings announcement acts as a predictor for the stock's price direction the following day.

## 2. Dataset & Data Collection
This project utilizes a **hybrid data approach** complying with the course guidelines for data enrichment.

* **Stock Price Data (Real):** Historical daily OHLCV (Open, High, Low, Close, Volume) data for the target companies was collected using the `yfinance` library (Yahoo Finance API).
* **Option Flow Data (Simulated Enrichment):**
    * *Constraint:* Due to the lack of public/free API access to proprietary option flow platforms (e.g., Unusual Whales) and strict project deadlines, real-time option flow data could not be scraped ethically.
    * *Solution:* A **stochastic simulation engine** was built to generate synthetic option flow data. This simulation uses probability distributions rooted in market microstructure theory (e.g., higher volume during earnings, correlation between sentiment and future price) to mimic "smart money" behavior for the purpose of demonstrating the ML pipeline.

## 3. Methodology & Analysis Pipeline

The project follows a standard Data Science pipeline implemented in `main.py`:

1.  **Data Ingestion:** Fetching real stock history for 7 tickers.
2.  **Feature Engineering:**
    * **`Put_Call_Ratio`**: Calculated as $Put Volume / Call Volume$.
    * **`Is_Earnings_Day`**: Dates were flagged to simulate quarterly earnings reports.
    * **`Option_Sentiment`**: A synthetic score (-1 to 1) representing the bullish/bearish skew of the premiums.
    * **Target Variable**: `Next_Day_Move` (Binary: 1 if Price Up, 0 if Price Down).
3.  **Exploratory Data Analysis (EDA):**
    * Analyzed the distribution of Put/Call ratios.
    * Compared trading volumes on Earnings Days vs. Normal Days.
4.  **Machine Learning (Hypothesis Testing):**
    * **Model:** Random Forest Classifier (`n_estimators=100`).
    * **Goal:** Predict if the stock price will close higher the next day based on the previous day's option flow.
    * **Validation:** 80/20 Train-Test split.

## 4. Findings
* **Volume Correlation:** As expected in the simulation, trading volume (both stock and options) showed significant spikes on earnings days.
* **Predictive Power:** The Random Forest model achieved an accuracy score (on synthetic data) demonstrating that if option flow is highly correlated with "insider knowledge," it can be a strong predictor.
    * *Note:* The high accuracy observed in the logs is a result of the synthetic bias introduced to validate the code pipeline. In real-world efficient markets, this predictive signal would be much weaker (closer to 50-55%).

## 5. Limitations & Future Work
* **Data limitation:** The primary limitation is the use of synthetic option data. A future iteration of this project would require a subscription to a paid API (e.g., Bloomberg or Unusual Whales) to validate the hypothesis with real-world flow.
* **Timeframe:** The analysis covers a 2-year window. Expanding this to 10 years would capture different market cycles (Bull vs. Bear markets).

## 6. How to Run the Code
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the main analysis script:
    ```bash
    python main.py
    ```
3.  The script will:
    * Fetch real price data.
    * Generate the synthetic option dataset.
    * Train the ML model.
    * Output the Accuracy Score and save EDA graphs as PNG files.

## 7. AI Tools Usage Declaration
* **Tools Used:** OpenAI ChatGPT / Google Gemini.
* **Purpose:** Assisted in debugging Python syntax errors, generating the `yfinance` boilerplate code, and structuring the Markdown report.
* **Prompts:** "How to merge two dataframes in pandas on dates", "Generate random forest classifier code for binary prediction".
