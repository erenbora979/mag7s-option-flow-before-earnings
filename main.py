import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ==========================================
# 1. DATA COLLECTION & SIMULATION
# ==========================================

def get_data_and_simulate():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']
    start_date = "2023-01-01"
    end_date = "2025-01-01"
    
    all_data = []

    print("Fetching data and running simulation...")
    
    for ticker in tickers:
        # 1. Fetch Real Price Data from Yahoo Finance
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            df = df.reset_index()
            
            # Fix date format
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            
            # 2. Simulate Earnings Dates (approx. 4 times a year)
            # In real data these are fixed, here we assign random dates for simulation
            n_days = len(df)
            # Randomly select indices for earnings (approx every 3 months)
            earnings_indices = np.random.choice(n_days, size=int(n_days/60), replace=False)
            df['Is_Earnings_Day'] = 0
            df.iloc[earnings_indices, df.columns.get_loc('Is_Earnings_Day')] = 1
            
            # 3. Simulate Option Flow Data (Mocking Unusual Whales Data)
            np.random.seed(42) # For reproducibility
            
            # Volume: Spikes during earnings days (3-5x normal volume)
            base_volume = np.random.randint(10000, 50000, n_days)
            earnings_multiplier = np.where(df['Is_Earnings_Day'] == 1, np.random.uniform(3, 5, n_days), 1)
            
            df['Call_Volume'] = (base_volume * np.random.uniform(0.4, 0.6, n_days) * earnings_multiplier).astype(int)
            df['Put_Volume'] = (base_volume * np.random.uniform(0.4, 0.6, n_days) * earnings_multiplier).astype(int)
            
            # Calculate Put/Call Ratio
            df['Put_Call_Ratio'] = df['Put_Volume'] / df['Call_Volume']
            
            # Sentiment Score (-1 Bearish, +1 Bullish)
            # Adding synthetic bias: If price goes up next day, increase sentiment slightly (to prove ML works)
            future_change = (df['Close'].shift(-1) - df['Close']) / df['Close']
            noise = np.random.normal(0, 0.5, n_days)
            
            # Synthetic correlation: High sentiment correlates with future price increase
            df['Option_Sentiment'] = np.where(future_change > 0, 1, -1) * 0.3 + noise
            
            df['Ticker'] = ticker
            
            # Target Variable: Did the price increase the next day? (1: Yes, 0: No)
            df['Next_Day_Move'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
            
            all_data.append(df)
            print(f"Processed: {ticker}")
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    final_df = pd.concat(all_data)
    final_df.dropna(inplace=True) # Drop last row as it has no "tomorrow"
    return final_df

# Generate Dataset
df = get_data_and_simulate()
print(f"Dataset Ready: {df.shape}")
print(df.head())

# ==========================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

# Visualization 1: Distribution of Put/Call Ratios
plt.figure(figsize=(10, 6))
sns.histplot(df['Put_Call_Ratio'], bins=50, kde=True)
plt.title('Distribution of Put/Call Ratios (Simulated)')
plt.xlabel('Put/Call Ratio')
plt.savefig('eda_put_call_dist.png')
print("Saved: eda_put_call_dist.png")
# plt.show() # Uncomment if running locally

# Visualization 2: Earnings Days vs Normal Days Volume
plt.figure(figsize=(10, 6))
sns.boxplot(x='Is_Earnings_Day', y='Call_Volume', data=df)
plt.title('Call Volume: Earnings Days vs Normal Days')
plt.xlabel('Is Earnings Day (0: No, 1: Yes)')
plt.savefig('eda_volume_comparison.png')
print("Saved: eda_volume_comparison.png")
# plt.show() # Uncomment if running locally

# ==========================================
# 3. MACHINE LEARNING (HYPOTHESIS TESTING)
# ==========================================
# Hypothesis: Can Option Flow (Sentiment, Volume) predict the next day's price direction?

# Feature Selection
features = ['Call_Volume', 'Put_Volume', 'Put_Call_Ratio', 'Option_Sentiment', 'Is_Earnings_Day']
X = df[features]
y = df['Next_Day_Move']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Results
print("\n--- MACHINE LEARNING RESULTS ---")
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Feature Importance
importances = pd.Series(model.feature_importances_, index=features)
print("\nFeature Importances:\n", importances.sort_values(ascending=False))

# Plot Feature Importance
plt.figure(figsize=(10, 6))
importances.sort_values().plot(kind='barh', color='teal')
plt.title('Feature Importance for Predicting Price Move')
plt.tight_layout()
plt.savefig('ml_feature_importance.png')
print("Saved: ml_feature_importance.png")
# plt.show() # Uncomment if running locally
