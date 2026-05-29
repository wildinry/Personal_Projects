import os
import time
import requests
import pandas as pd
import ta
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# === 1. CONFIGURATION ===
# Load environment variables from a .env file for security
load_dotenv()
api_key = os.getenv('[redacted]')
api_secret = os.getenv('[redacted]')

# General Settings
SYMBOL = 'SOLUSDT' # Binance uses USDT for trading pairs
INTERVAL = Client.KLINE_INTERVAL_3MINUTE # Set to 3-minute timeframe
CAPITAL = 23 # Your initial capital
QTY_PERCENT_OF_EQUITY = 80.0 # From your Pine Script (80%)
DRY_RUN = False # Set to False to place real orders

# Discord Notifications
DISCORD_WEBHOOK_URL = os.getenv('https://discord.com/api/webhooks/[redacted]/[redacted]')

# Strategy Parameters
SHORT_MA_LENGTH = 17
LONG_MA_LENGTH = 49
VOLUME_MA_LENGTH = 20
STOP_LOSS_PERC = 1.4 # 1.4%
RISK_TO_REWARD = 2.4

# === 2. HELPER FUNCTIONS ===
def send_discord_notification(message):
    """Sends a message to the configured Discord channel via webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Skipping notification.")
        return
    try:
        payload = {
            'content': message,
            'username': 'Trading Bot'
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord notification: {e}")

def get_binance_client():
    """Initializes and returns the Binance client."""
    try:
        # Use testnet for a dry run
        client = Client(api_key, api_secret, tld='us', testnet=DRY_RUN)
        print("Connected to Binance API successfully.")
        return client
    except Exception as e:
        print(f"Error connecting to Binance: {e}")
        send_discord_notification(f"Error connecting to Binance: {e}")
        return None

def get_historical_data(client, symbol, interval, limit=1000):
    """Fetches historical candlestick data and calculates indicators."""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        data = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
        
        # Convert relevant columns to numeric types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            data[col] = pd.to_numeric(data[col])
            
        # Calculate technical indicators using `ta` library
        data['short_ma'] = ta.trend.sma_indicator(data['close'], window=SHORT_MA_LENGTH)
        data['long_ma'] = ta.trend.sma_indicator(data['close'], window=LONG_MA_LENGTH)
        data['volume_ma'] = ta.trend.sma_indicator(data['volume'], window=VOLUME_MA_LENGTH)
        
        return data

    except BinanceAPIException as e:
        print(f"Binance API Error: {e}")
        send_discord_notification(f"Binance API Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        send_discord_notification(f"An error occurred while fetching data: {e}")
        return None

def get_current_position(client, symbol):
    """Checks for an open position and returns its side and quantity."""
    try:
        positions = client.futures_position_information(symbol=symbol)
        for position in positions:
            if float(position['positionAmt']) != 0:
                side = 'long' if float(position['positionAmt']) > 0 else 'short'
                return side, abs(float(position['positionAmt']))
        return None, 0
    except Exception as e:
        print(f"Error getting position info: {e}")
        return None, 0

def calculate_order_details(client, symbol, position_side):
    """Calculates quantity and SL/TP levels."""
    try:
        if DRY_RUN:
            available_balance = CAPITAL
        else:
            quote_asset = 'USDT'
            balance_info = client.get_asset_balance(asset=quote_asset)
            available_balance = float(balance_info['free'])

        if available_balance < CAPITAL:
            msg = f"Insufficient balance in USDT. Available: {available_balance}, Needed at least: {CAPITAL}"
            print(msg)
            send_discord_notification(msg)
            return None, None, None

        current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        
        qty_to_trade_usdt = available_balance * (QTY_PERCENT_OF_EQUITY / 100)
        quantity = qty_to_trade_usdt / current_price
        
        info = client.get_symbol_info(symbol=symbol)
        
        # Corrected logic: find the LOT_SIZE filter by type
        lot_size_filter = next((f for f in info['filters'] if f['filterType'] == 'LOT_SIZE'), None)
        
        if lot_size_filter:
            step_size = lot_size_filter['stepSize']
            qty_precision = step_size.find('1') - 1
            if qty_precision == -1: # For step size '1.0' or '10' etc.
                qty_precision = 0
            quantity = round(quantity, qty_precision)
        else:
            print("Could not find LOT_SIZE filter for the symbol.")
            return None, None, None


        if position_side == 'long':
            stop_loss_level = current_price * (1 - STOP_LOSS_PERC / 100)
            take_profit_level = current_price + (current_price - stop_loss_level) * RISK_TO_REWARD
        else: # short
            stop_loss_level = current_price * (1 + STOP_LOSS_PERC / 100)
            take_profit_level = current_price - (stop_loss_level - current_price) * RISK_TO_REWARD
            
        return quantity, stop_loss_level, take_profit_level

    except Exception as e:
        print(f"Error calculating order details: {e}")
        send_discord_notification(f"Error calculating order details: {e}")
        return None, None, None

def place_order(client, symbol, order_side):
    """Places a hypothetical or real order (long or short)."""
    quantity, stop_loss_level, take_profit_level = calculate_order_details(client, symbol, order_side)

    if quantity and stop_loss_level and take_profit_level:
        if DRY_RUN:
            msg = f"[DRY RUN] Would have placed a {order_side} order for {quantity} {symbol} with SL at {stop_loss_level:.2f} and TP at {take_profit_level:.2f}"
            print(msg)
            send_discord_notification(msg)
        else:
            try:
                # Place a real market order
                order = client.create_order(
                    symbol=symbol,
                    side=Client.SIDE_BUY if order_side == 'long' else Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                msg = f"Market {order_side} entry order placed: {order['orderId']} for {quantity} {symbol}"
                print(msg)
                send_discord_notification(msg)

                # Place OCO order for SL/TP (if supported)
                # Note: OCO orders are complex and may not be available on all markets.
                # A manual stop-limit/take-profit-limit management loop is often required.
                try:
                    # For a long position, a sell OCO is used.
                    # For a short position, a buy OCO is used.
                    oco_order = client.create_oco_order(
                        symbol=symbol,
                        side=Client.SIDE_SELL if order_side == 'long' else Client.SIDE_BUY,
                        quantity=quantity,
                        price=take_profit_level,
                        stopPrice=stop_loss_level,
                        stopLimitPrice=stop_loss_level
                    )
                    msg = f"OCO order (SL/TP) placed with order list ID: {oco_order['orderListId']}"
                    print(msg)
                    send_discord_notification(msg)
                except Exception as e:
                    msg = f"Could not place OCO order. Consider using separate orders: {e}"
                    print(msg)
                    send_discord_notification(msg)

            except Exception as e:
                msg = f"Error placing real {order_side} order: {e}"
                print(msg)
                send_discord_notification(msg)

def close_position(client, symbol, side, quantity):
    """Closes an existing position by placing an opposite market order."""
    if DRY_RUN:
        msg = f"[DRY RUN] Would have closed the existing {side} position for {quantity} {symbol}."
        print(msg)
        send_discord_notification(msg)
    else:
        try:
            client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL if side == 'long' else Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity,
                reduceOnly=True # This parameter ensures the order only closes a position
            )
            msg = f"Closed existing {side} position for {quantity} {symbol}."
            print(msg)
            send_discord_notification(msg)
        except Exception as e:
            msg = f"Error closing existing {side} position: {e}"
            print(msg)
            send_discord_notification(msg)


# === 3. MAIN BOT LOGIC LOOP ===
def run_bot():
    """Main function to run the trading bot."""
    client = get_binance_client()
    if not client:
        return

    msg = f"Starting {'DRY RUN ' if DRY_RUN else 'LIVE '} bot for {SYMBOL} on {INTERVAL} interval with new strategy..."
    print(msg)
    send_discord_notification(msg)
    
    while True:
        try:
            data = get_historical_data(client, SYMBOL, INTERVAL, limit=100)
            if data is None:
                time.sleep(60)
                continue
            
            last_bar = data.iloc[-1]
            prev_bar = data.iloc[-2]

            # Strategy logic from the TradingView script
            long_condition = (prev_bar['short_ma'] <= prev_bar['long_ma']) and (last_bar['short_ma'] > last_bar['long_ma'])
            short_condition = (prev_bar['short_ma'] >= prev_bar['long_ma']) and (last_bar['short_ma'] < last_bar['long_ma'])
            
            liquidity_confirmation = last_bar['volume'] >= last_bar['volume_ma']
            
            long_entry_signal = long_condition and liquidity_confirmation
            short_entry_signal = short_condition and liquidity_confirmation
            
            current_position_side, current_position_qty = get_current_position(client, SYMBOL)
            
            print(f"Checking for signals at {pd.to_datetime(last_bar['open_time'], unit='ms')}... Long Signal: {long_entry_signal}, Short Signal: {short_entry_signal}")

            # Execution logic
            if long_entry_signal:
                if current_position_side == 'short':
                    print("Long signal detected. Closing existing short position before entry.")
                    close_position(client, SYMBOL, 'short', current_position_qty)
                
                print("Long entry signal detected!")
                send_discord_notification("Long entry signal detected! Executing trade.")
                place_order(client, SYMBOL, 'long')

            if short_entry_signal:
                if current_position_side == 'long':
                    print("Short signal detected. Closing existing long position before entry.")
                    close_position(client, SYMBOL, 'long', current_position_qty)
                
                print("Short entry signal detected!")
                send_discord_notification("Short entry signal detected! Executing trade.")
                place_order(client, SYMBOL, 'short')
            
            print("Waiting for next check...")
            time.sleep(30 * 1)

        except KeyboardInterrupt:
            msg = "Bot stopped by user."
            print(msg)
            send_discord_notification(msg)
            break
        except Exception as e:
            msg = f"An unexpected error occurred in the main loop: {e}"
            print(msg)
            send_discord_notification(msg)
            print("Restarting in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
