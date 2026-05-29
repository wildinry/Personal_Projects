# options_signal_engine.py
# This script has been configured to display a GUI with the signal data.
# If it is still outputting to the console, it means your Python environment
# is not correctly linked to the Tkinter graphical library.
#
# Requirements: pip install yfinance pandas numpy scikit-learn plotly statsmodels arch hurst ta
# (tkinter is part of the Python stdlib; on some Linux you may need apt install python3-tk)

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from itertools import combinations
from math import ceil
import sys

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import OPTICS
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from arch.unitroot.cointegration import engle_granger
from hurst import compute_Hc

from ta.volatility import AverageTrueRange
from ta.trend import SMAIndicator

# This script will now only display a GUI.
# If Tkinter is not available, the program will exit with an error message.
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    print("Error: Tkinter could not be imported. This program requires a fully functional Tkinter library to run the GUI.")
    print("On macOS, please ensure your Python installation includes Tcl/Tk. The official installer from python.org is recommended.")
    sys.exit(1)


def main():
    # ----------- PRINT CHEAT SHEET HEADER -----------
    print("""
================= OPTIONS GREEKS QUICK GUIDE =================
Delta: Sensitivity to stock price. High delta (~0.6-1.0) = moves like stock.
Gamma: Rate of change of delta. High near strike = large payoff swings.
Theta: Time decay. High negative theta loses value quickly each day.
Vega: Sensitivity to IV. High vega profits if implied volatility rises.
IV: Implied volatility. Higher IV = more expensive, bigger expected moves.
===============================================================
    """)

    # ---------- USER PARAMETERS ----------
    TICKERS = ["INTC","PFE","F","SOFI","CCL","SIRI","NU","GE","AAL","RIVN","BTU","LEVI","ET","OPHC","ADTN","T","SAN","ALLY","ARLO","BNGO","CENX","CHWY","CLF","CRSR","DKNG","FCEL","FUBO","GOEV","HIMS","HUYA","IONQ","KOS","KOSS","LAZR","LYFT","MARA","NIO","NOK","OCGN","OPK","PLUG","PTON","RBLX","RKT","SPCE","SIRI","SNDL","STNE","UAL","VZ","WBD","WKHS","XELA","ZIM","ENVX","WOOF","NRG","CNX","SOFI","ADTN","ET","T","SAN","LEVI"]    
    YEARS = 0.5
    END = datetime.today()
    START = END - timedelta(days=YEARS * 365)

    P_VALUE_THRESH = 0.01
    HURST_MR_MAX = 0.50
    HURST_TREND_MIN = 0.60
    Z_SCORE_ENTRY = 1.5
    RECENT_MOMENTUM_DAYS = 10
    MIN_EXPIRY_DAYS = 21
    MAX_EXPIRY_DAYS_MR = 30
    MAX_EXPIRY_DAYS_TREND = 90
    TARGET_ATR_MULTIPLIER = 1.0


    # ---------- 1) Download price data ----------
    try:
        data = yf.download(TICKERS, start=START, end=END)
        prices = data["Close"].dropna(axis=1)
        highs = data["High"]
        lows = data["Low"]
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    if prices.shape[1] < 5:
        raise SystemExit("Too few tickers downloaded. Adjust tickers or check connectivity.")
    daily_returns = prices.pct_change().dropna()

    # ---------- 2) PCA -> 3 components ----------
    std_ret = StandardScaler().fit_transform(daily_returns)
    pca = PCA(n_components=3, random_state=0).fit(std_ret)
    factor_exposures = pd.DataFrame(data=pca.components_.T,
                                    index=daily_returns.columns,
                                    columns=["component_0","component_1","component_2"])

    # ---------- 3) OPTICS clustering ----------
    clustering = OPTICS(min_samples=5).fit(factor_exposures)
    factor_exposures["cluster"] = clustering.labels_

    # ---------- 4) compute per-asset Hurst + ATR ----------
    asset_hurst, asset_atr = {}, {}
    SMA_PERIOD = 50

    for sym in factor_exposures.index:
        try:
            asset_hurst[sym] = float(compute_Hc(prices[sym].dropna().values, kind="price", simplified=False)[0])
        except Exception:
            asset_hurst[sym] = np.nan
        try:
            atr_series = AverageTrueRange(highs[sym], lows[sym], prices[sym], window=14, fillna=True).average_true_range()
            asset_atr[sym] = float(atr_series.dropna().iloc[-1])
        except Exception:
            asset_atr[sym] = np.nan

    # ---------- 5) find detected pairs ----------
    pairs_detected = []
    for cluster_id in sorted(set(clustering.labels_)):
        if cluster_id == -1:
            continue
        members = list(factor_exposures.index[factor_exposures["cluster"] == cluster_id])
        if len(members) < 2:
            continue
        for a, b in combinations(members, 2):
            try:
                r1 = engle_granger(prices[a], prices[b])
                r2 = engle_granger(prices[b], prices[a])
                candidate = min([r1, r2], key=lambda x: getattr(x, "stat", np.inf))
            except Exception:
                continue
            if getattr(candidate, "pvalue", 1.0) > P_VALUE_THRESH:
                continue
            try:
                cv = candidate.cointegrating_vector
                idx = list(cv.index)
                coeffs = cv.values
                spread = (coeffs[0]*prices[idx[0]] + coeffs[1]*prices[idx[1]]).dropna()
            except Exception:
                continue
            try:
                Hs = compute_Hc(spread.values, kind="price", simplified=False)[0]
            except Exception:
                continue
            try:
                s_lag = spread.shift(1).fillna(method='bfill')
                ds = spread - s_lag
                beta = OLS(ds.values, add_constant(s_lag.values)).fit().params[1]
                half_life = -np.log(2) / beta if beta != 0 else np.inf
            except Exception:
                half_life = np.inf
            pairs_detected.append({"a": a, "b": b, "spread": spread, "H_spread": float(Hs), "half_life": float(half_life), "cluster": cluster_id})

    # ---------- 6) Signal logic with Greeks ----------
    signal_rows = []
    for cluster_id in sorted(set(clustering.labels_)):
        if cluster_id == -1: continue
        cluster_syms = list(factor_exposures.index[factor_exposures["cluster"] == cluster_id])
        if not cluster_syms: continue

        norm_prices = prices[cluster_syms].apply(lambda col: col / col.mean(), axis=0)
        cluster_mean = norm_prices.mean(axis=1)

        for sym in cluster_syms:
            try:
                resid = norm_prices[sym] - cluster_mean
                z = (resid - resid.rolling(60, min_periods=10).mean()) / resid.rolling(60, min_periods=10).std()
                recent_z = float(z.dropna().iloc[-1]) if z.dropna().size > 0 else np.nan
                recent_mom = float(prices[sym].pct_change(RECENT_MOMENTUM_DAYS).iloc[-1])
                H = asset_hurst.get(sym, np.nan)
                ATR = asset_atr.get(sym, np.nan)

                suggested_side, reason, target_half_life = None, None, None
                if not np.isnan(H) and H < HURST_MR_MAX:
                    if recent_z <= -1.2: suggested_side, reason = "CALL","MR_rebound_low_z"
                    elif recent_z >= 1.2: suggested_side, reason = "PUT","MR_rebound_high_z"
                    rel = [p for p in pairs_detected if (p["a"]==sym or p["b"]==sym)]
                    target_half_life = np.nanmean([p["half_life"] for p in rel]) if rel else 14.0
                elif not np.isnan(H) and H > HURST_TREND_MIN:
                    if recent_mom > 0: suggested_side, reason = "CALL","TREND_pos_mom"
                    elif recent_mom < 0: suggested_side, reason = "PUT","TREND_neg_mom"
                    target_half_life = 30.0

                if not suggested_side: continue

                desired_days = int(min(max(ceil((target_half_life or 14)* (2 if H<HURST_MR_MAX else 3)),30),
                                    (MAX_EXPIRY_DAYS_MR if H<HURST_MR_MAX else MAX_EXPIRY_DAYS_TREND)))
                tkdata = yf.Ticker(sym)
                exps = tkdata.options
                if not exps: continue
                chosen_exp = next((e for e in exps if (datetime.strptime(e,"%Y-%m-%d")-END).days >= desired_days), exps[-1])
                chain = tkdata.option_chain(chosen_exp)
                opt_df = chain.calls if suggested_side=="CALL" else chain.puts
                if opt_df.empty: continue

                spot = float(prices[sym].iloc[-1])
                strikes = opt_df["strike"].values
                strike_idx = np.argmin(np.abs(strikes-spot))
                chosen = opt_df.iloc[strike_idx]
                opt_price = float(chosen.get("lastPrice", np.nan))

                if not np.isnan(ATR) and not np.isnan(opt_price) and spot != 0:
                    expected_spot = spot + TARGET_ATR_MULTIPLIER*ATR if suggested_side=="CALL" else spot - TARGET_ATR_MULTIPLIER*ATR
                    goal_price = opt_price * (expected_spot/spot)
                else:
                    goal_price = np.nan

                signal_rows.append({
                    "ticker": sym,
                    "side": suggested_side,
                    "reason": reason,
                    "expiry": chosen_exp,
                    "strike": float(chosen["strike"]),
                    "option_last": opt_price,
                    "bid": float(chosen.get("bid", np.nan)),
                    "ask": float(chosen.get("ask", np.nan)),
                    "impvol": float(chosen.get("impliedVolatility", np.nan)),
                    "delta": float(chosen.get("delta", np.nan)),
                    "gamma": float(chosen.get("gamma", np.nan)),
                    "theta": float(chosen.get("theta", np.nan)),
                    "vega": float(chosen.get("vega", np.nan)),
                    "recent_z": recent_z,
                    "H": H,
                    "recent_momentum": recent_mom,
                    "goal_price": float(goal_price)
                })
            except Exception:
                continue

    # ---------- 7) Output (GUI) ----------
    df = pd.DataFrame(signal_rows)
    if df.empty:
        print("No signals.")
        return

    df["score"] = df.apply(lambda r: (abs(r["recent_momentum"])*100 if r["reason"].startswith("TREND")
                                     else abs(r["recent_z"])*2)
                                     - (r["impvol"]*0.5 if not np.isnan(r["impvol"]) else 0), axis=1)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)

    out_cols = ["ticker","side","reason","expiry","strike","option_last","bid","ask","impvol","delta","gamma","theta","vega","recent_z","H","recent_momentum","goal_price","score"]
    display_df = df[out_cols].copy()

    def fmt(x):
        if pd.isna(x): return ""
        if isinstance(x, (int, np.integer)): return str(int(x))
        if isinstance(x, (float, np.floating)):
            if abs(x) >= 100: return f"{x:,.2f}"
            if abs(x) >= 10: return f"{x:,.3f}"
            return f"{x:,.4f}"
        return str(x)

    root = tk.Tk()
    root.title("Options Signal Engine - Screener")
    root.geometry("1400x700")

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    cols = list(display_df.columns)
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=25)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(side="left", fill="both", expand=True)

    col_widths = {
        "ticker":80,"side":70,"reason":140,"expiry":100,"strike":80,"option_last":100,"bid":80,"ask":80,
        "impvol":90,"delta":80,"gamma":80,"theta":80,"vega":80,"recent_z":100,"H":80,"recent_momentum":110,"goal_price":110,"score":90
    }
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=col_widths.get(c, 100), anchor="center")

    for _, row in display_df.iterrows():
        vals = [fmt(row[c]) for c in cols]
        tree.insert("", "end", values=vals)

    info = ttk.Label(root, text=f"Date: {END.strftime('%Y-%m-%d')}   Tickers: {len(TICKERS)}   Signals: {len(display_df)}", anchor="w")
    info.pack(side="bottom", fill="x")

    root.mainloop()

if __name__ == "__main__":
    main()