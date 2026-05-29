# crypto_probability_analyzer.py
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# ==============================================
# Step 1: Fetch Cryptocurrency Data
# ==============================================
def get_top_cryptos(top_n=50):
    """Fetch top cryptocurrencies by market cap (reduce to 50 for demo speed)"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": top_n,
        "page": 1
    }
    response = requests.get(url, params=params)
    cryptos = response.json()
    return [crypto['id'] for crypto in cryptos]

def fetch_historical_data(crypto_id, days=90):
    """Get 90 days of price data (compromise between speed and analysis)"""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    return prices.set_index('date').drop(columns='timestamp')

# ==============================================
# Step 2: Technical Indicators (Feature Engineering)
# ==============================================
def compute_rsi(series, window=14):
    delta = series.diff().dropna()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_macd(series, slow=26, fast=12, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd - signal_line

def add_technical_indicators(df):
    df['rsi'] = compute_rsi(df['price'])
    df['macd'] = compute_macd(df['price'])
    df['sma_20'] = df['price'].rolling(20).mean()
    df['sma_50'] = df['price'].rolling(50).mean()
    df['price_change'] = df['price'].pct_change(periods=3)  # 3-day momentum
    return df.dropna()

# ==============================================
# Step 3: Model Training & Prediction
# ==============================================
def prepare_training_data(crypto_ids):
    X, y = [], []
    for crypto_id in crypto_ids[:30]:  # Use 30 for faster training
        try:
            df = fetch_historical_data(crypto_id)
            df = add_technical_indicators(df)
            df['target'] = (df['price'].shift(-3) > df['price']).astype(int)  # 3-day lookahead
            df = df.dropna()
            X.append(df[['rsi', 'macd', 'sma_20', 'sma_50', 'price_change']])
            y.append(df['target'])
        except Exception as e:
            print(f"Skipped {crypto_id}: {str(e)}")
    return pd.concat(X), pd.concat(y)

def train_and_predict():
    # Get data
    crypto_ids = get_top_cryptos()
    
    # Prepare training data
    X, y = prepare_training_data(crypto_ids)
    if X.empty:
        raise ValueError("No training data available - check API connections")
    
    # Train model
    scaler = StandardScaler()
    model = LogisticRegression(class_weight='balanced', max_iter=1000)
    model.fit(scaler.fit_transform(X), y)
    
    # Generate predictions
    probabilities = {}
    for crypto_id in crypto_ids:
        try:
            df = fetch_historical_data(crypto_id, days=30)
            df = add_technical_indicators(df)
            if df.empty:
                continue
            features = df[['rsi', 'macd', 'sma_20', 'sma_50', 'price_change']].iloc[-1].values.reshape(1, -1)
            prob = model.predict_proba(scaler.transform(features))[0][1]
            probabilities[crypto_id] = prob
        except Exception as e:
            print(f"Failed {crypto_id}: {str(e)}")
    
    # Return sorted results
    return sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

# ==============================================
# Execute and Display Results
# ==============================================
if __name__ == "__main__":
    print("Analyzing cryptocurrencies... (this may take 2-5 minutes)")
    ranked_cryptos = train_and_predict()
    
    print("\nTop Cryptocurrencies by Upside Probability:")
    for rank, (crypto_id, prob) in enumerate(ranked_cryptos[:25], 1):
        print(f"{rank:>2}. {crypto_id:<18} {prob:.1%}")
