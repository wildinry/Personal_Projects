# crypto_probability_analyzer.py (FINAL VERSION WITH RATE LIMITING)
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ==============================================
# Configure API Rate Limiting
# ==============================================
API_DELAY = 6.1  # CoinGecko allows 10-30 reqs/minute (6.1s delay = ~10 reqs/min)
MAX_RETRIES = 3
RETRY_DELAY = 15  # Seconds to wait after hitting rate limit

# Set up requests session with retry logic
session = requests.Session()
retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

# ==============================================
# Modified Data Fetching Functions
# ==============================================
def get_top_cryptos(top_n=30):  # Reduced default to stay within limits
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": top_n,
        "page": 1
    }
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        cryptos = response.json()
        return [crypto['id'] for crypto in cryptos]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return []

def fetch_historical_data(crypto_id, days=90):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    try:
        response = session.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        # Check rate limit headers
        if 'x-ratelimit-remaining' in response.headers:
            remaining = int(response.headers['x-ratelimit-remaining'])
            if remaining < 2:  # Slow down if approaching limit
                time.sleep(RETRY_DELAY)
        
        data = response.json()
        if 'prices' not in data:
            return pd.DataFrame()
            
        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
        return prices.set_index('date').drop(columns='timestamp')
        
    except Exception as e:
        print(f"Failed {crypto_id}: {str(e)}")
        if response.status_code == 429:
            time.sleep(RETRY_DELAY)
        return pd.DataFrame()

# ==============================================
# Modified Training/Prediction Flow
# ==============================================
def prepare_training_data(crypto_ids):
    X, y = [], []
    for crypto_id in crypto_ids:
        try:
            time.sleep(API_DELAY)  # Rate limiting before each request
            df = fetch_historical_data(crypto_id)
            if df.empty:
                continue
            df = add_technical_indicators(df)
            df['target'] = (df['price'].shift(-3) > df['price']).astype(int)
            df = df.dropna()
            X.append(df[['rsi', 'macd', 'sma_20', 'sma_50', 'price_change']])
            y.append(df['target'])
        except Exception as e:
            print(f"Skipped {crypto_id}: {str(e)}")
    return pd.concat(X) if X else pd.DataFrame(), pd.concat(y) if y else pd.Series()

def train_and_predict():
    crypto_ids = get_top_cryptos(top_n=20)  # Reduced to 20 for initial testing
    if not crypto_ids:
        return []
    
    X, y = prepare_training_data(crypto_ids)
    if X.empty:
        return []
    
    try:
        scaler = StandardScaler()
        model = LogisticRegression(class_weight='balanced', max_iter=1000)
        model.fit(scaler.fit_transform(X), y)
    except Exception as e:
        print(f"Model training failed: {str(e)}")
        return []
    
    probabilities = {}
    for crypto_id in crypto_ids:
        try:
            time.sleep(API_DELAY)  # Rate limiting for prediction phase
            df = fetch_historical_data(crypto_id, days=30)
            if df.empty:
                continue
            df = add_technical_indicators(df)
            features = df[['rsi', 'macd', 'sma_20', 'sma_50', 'price_change']].iloc[-1].values.reshape(1, -1)
            prob = model.predict_proba(scaler.transform(features))[0][1]
            probabilities[crypto_id] = prob
        except Exception as e:
            print(f"Failed {crypto_id}: {str(e)}")
    
    return sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

# ==============================================
# Execution (Unchanged)
# ==============================================
if __name__ == "__main__":
    print("Analyzing cryptocurrencies...")
    start_time = time.time()
    
    ranked_cryptos = train_and_predict()
    
    print(f"\nAnalysis completed in {time.time()-start_time:.1f} seconds")
    
    if ranked_cryptos:
        print("\nTop Cryptocurrencies by Upside Probability:")
        for rank, (crypto_id, prob) in enumerate(ranked_cryptos[:15], 1):
            print(f"{rank:>2}. {crypto_id:<18} {prob:.1%}")
    else:
        print("No valid predictions generated")