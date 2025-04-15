import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from datetime import datetime, timedelta

# Cache recommendations to avoid recomputation
@st.cache_data(ttl=3600)
def recommend_stocks(risk_profile, goal_type, amount_needed):
    """
    Recommend stocks based on risk profile and goal type.
    
    Args:
        risk_profile (str): Risk profile (Conservative, Moderate, Aggressive)
        goal_type (str): Type of financial goal
        amount_needed (float): Amount needed for the goal
        
    Returns:
        list: List of recommended stock tickers
    """
    # Map risk profiles to stock characteristics
    risk_mappings = {
        "Conservative": {
            "min_market_cap": 50000,  # 50,000 Cr
            "max_beta": 0.8,
            "min_dividend_yield": 1.0,
            "sectors": ["FMCG", "IT", "Pharma"]
        },
        "Moderate": {
            "min_market_cap": 20000,  # 20,000 Cr
            "max_beta": 1.2,
            "min_dividend_yield": 0.5,
            "sectors": ["Banking", "Auto", "Chemicals", "IT"]
        },
        "Aggressive": {
            "min_market_cap": 5000,  # 5,000 Cr
            "max_beta": 1.5,
            "min_dividend_yield": 0.0,
            "sectors": ["Auto", "Banking", "Metal", "Realty"]
        }
    }
    
    # Default to moderate if risk profile is not recognized
    if risk_profile not in risk_mappings:
        risk_profile = "Moderate"
    
    # Goal type can influence stock selection
    goal_adjustments = {
        "Retirement": {
            "Conservative": {"min_dividend_yield": 2.0},
            "Moderate": {"min_dividend_yield": 1.0},
            "Aggressive": {"min_dividend_yield": 0.5}
        },
        "Child Education": {
            "Conservative": {"max_beta": 0.7},
            "Moderate": {"max_beta": 1.0},
            "Aggressive": {"max_beta": 1.3}
        }
    }
    
    # Apply goal-specific adjustments if available
    if goal_type in goal_adjustments and risk_profile in goal_adjustments[goal_type]:
        for key, value in goal_adjustments[goal_type][risk_profile].items():
            risk_mappings[risk_profile][key] = value
    
    # Indian stock recommendations based on risk profile
    # These are dummy stocks for demonstration purposes
    stock_universe = {
        "Conservative": [
            "TCS.NS",         # Tata Consultancy Services
            "HINDUNILVR.NS",  # Hindustan Unilever
            "NESTLEIND.NS",   # Nestle India
            "SUNPHARMA.NS",   # Sun Pharmaceutical
            "BAJAJFINSV.NS",  # Bajaj Finserv
            "HDFCBANK.NS",    # HDFC Bank
            "ITC.NS",         # ITC
            "ASIANPAINT.NS",  # Asian Paints
            "POWERGRID.NS",   # Power Grid Corporation
            "NTPC.NS"         # NTPC
        ],
        "Moderate": [
            "INFY.NS",        # Infosys
            "RELIANCE.NS",    # Reliance Industries
            "HDFCBANK.NS",    # HDFC Bank
            "ICICIBANK.NS",   # ICICI Bank
            "KOTAKBANK.NS",   # Kotak Mahindra Bank
            "TCS.NS",         # Tata Consultancy Services
            "AXISBANK.NS",    # Axis Bank
            "MARUTI.NS",      # Maruti Suzuki
            "HINDUNILVR.NS",  # Hindustan Unilever
            "BAJAJFINSV.NS"   # Bajaj Finserv
        ],
        "Aggressive": [
            "RELIANCE.NS",    # Reliance Industries
            "TATAMOTORS.NS",  # Tata Motors
            "TATASTEEL.NS",   # Tata Steel
            "JINDALSTEL.NS",  # Jindal Steel
            "SBIN.NS",        # State Bank of India
            "LT.NS",          # Larsen & Toubro
            "M&M.NS",         # Mahindra & Mahindra
            "INDUSINDBK.NS",  # IndusInd Bank
            "ADANIPORTS.NS",  # Adani Ports
            "HINDALCO.NS"     # Hindalco Industries
        ]
    }
    
    # Return top 5 recommendations based on risk profile
    # In a real implementation, we would fetch real data and apply ML models
    if risk_profile in stock_universe:
        num_stocks = 5
        return stock_universe[risk_profile][:num_stocks]
    else:
        return stock_universe["Moderate"][:5]  # Default to moderate risk

# Cache recommendations to avoid recomputation
@st.cache_data(ttl=3600)
def recommend_mutual_funds(risk_profile, goal_type, amount_needed):
    """
    Recommend mutual funds based on risk profile and goal type.
    
    Args:
        risk_profile (str): Risk profile (Conservative, Moderate, Aggressive)
        goal_type (str): Type of financial goal
        amount_needed (float): Amount needed for the goal
        
    Returns:
        list: List of recommended mutual fund tickers
    """
    # Map risk profiles to fund characteristics
    risk_mappings = {
        "Conservative": {
            "fund_types": ["Debt", "Hybrid"],
            "max_volatility": 10,
            "min_return": 7
        },
        "Moderate": {
            "fund_types": ["Hybrid", "Equity"],
            "max_volatility": 15,
            "min_return": 10
        },
        "Aggressive": {
            "fund_types": ["Equity", "Sectoral"],
            "max_volatility": 20,
            "min_return": 12
        }
    }
    
    # Goal type can influence fund selection
    goal_adjustments = {
        "Retirement": {
            "timeframe": "Long Term",
            "preferred_types": ["Equity", "Index"]
        },
        "Child Education": {
            "timeframe": "Medium Term",
            "preferred_types": ["Hybrid", "Balanced"]
        },
        "Marriage": {
            "timeframe": "Medium Term",
            "preferred_types": ["Hybrid", "Debt"]
        },
        "New House": {
            "timeframe": "Medium Term",
            "preferred_types": ["Debt", "Hybrid"]
        }
    }
    
    # Indian mutual fund recommendations based on risk profile
    # These are commonly used tickers for demonstration purposes
    mf_universe = {
        "Conservative": [
            "HDFCDBT.BO",     # HDFC Corporate Bond Fund
            "ICBPRUD.BO",     # ICICI Prudential Corporate Bond Fund
            "AXBBND.BO",      # Axis Banking & PSU Debt Fund
            "SMCBALQ.BO",     # SBI Magnum Conservative Fund
            "TBABRG.BO"       # Tata Banking & PSU Debt Fund
        ],
        "Moderate": [
            "HDFCSF.BO",      # HDFC Balanced Advantage Fund
            "ICBPBAQ.BO",     # ICICI Prudential Balanced Advantage Fund
            "KOTBLD.BO",      # Kotak Balanced Advantage Fund
            "UTSMCP.BO",      # UTI Mid Cap Fund
            "AXISMQ.BO"       # Axis Midcap Fund
        ],
        "Aggressive": [
            "HDFCMQ.BO",      # HDFC Mid-Cap Opportunities Fund
            "ICICGR.BO",      # ICICI Prudential Technology Fund
            "NIPPCQ.BO",      # Nippon India Small Cap Fund
            "KOTSMQ.BO",      # Kotak Small Cap Fund
            "AXISSQ.BO"       # Axis Small Cap Fund
        ]
    }
    
    # Return top 5 recommendations based on risk profile
    # In a real implementation, we would fetch real data and apply ML models
    if risk_profile in mf_universe:
        num_funds = 5
        return mf_universe[risk_profile][:num_funds]
    else:
        return mf_universe["Moderate"][:5]  # Default to moderate risk

def get_portfolio_weights(tickers, risk_profile):
    """
    Calculate portfolio weights for given tickers based on risk profile.
    
    Args:
        tickers (list): List of stock/fund tickers
        risk_profile (str): Risk profile
        
    Returns:
        list: Portfolio weights
    """
    n = len(tickers)
    if n == 0:
        return []
    
    # Simple equal weighting for demonstration
    # In a real implementation, we would use optimization techniques
    weights = np.ones(n) / n
    
    return weights

def calculate_portfolio_metrics(tickers, weights):
    """
    Calculate portfolio metrics like expected return, volatility, etc.
    
    Args:
        tickers (list): List of stock/fund tickers
        weights (list): Portfolio weights
        
    Returns:
        dict: Portfolio metrics
    """
    if not tickers or not weights or len(tickers) != len(weights):
        return {
            "expected_return": 0,
            "volatility": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0
        }
    
    # Placeholder metrics
    # In a real implementation, we would calculate these from historical data
    metrics = {
        "expected_return": 0.12,  # 12% annual return
        "volatility": 0.15,       # 15% annual volatility
        "sharpe_ratio": 0.8,      # Sharpe ratio
        "max_drawdown": -0.2      # Maximum drawdown
    }
    
    return metrics

# Function to simulate a basic ML recommendation model
def simple_ml_recommendation(historical_data, risk_profile):
    """
    Simple ML-based recommendation model.
    
    Args:
        historical_data (dict): Dictionary of historical price data for stocks/funds
        risk_profile (str): Risk profile
        
    Returns:
        list: Sorted list of tickers based on ranking
    """
    if not historical_data:
        return []
    
    # Features to consider for ranking
    features = {
        "return": [],        # Annual return
        "volatility": [],    # Volatility (risk)
        "sharpe": [],        # Sharpe ratio (risk-adjusted return)
        "max_dd": []         # Maximum drawdown
    }
    
    tickers = list(historical_data.keys())
    
    for ticker, data in historical_data.items():
        if data.empty:
            # Skip if data is empty
            continue
        
        # Calculate returns
        returns = data['Close'].pct_change().dropna()
        
        # Annual return
        annual_return = (1 + returns.mean()) ** 252 - 1
        features["return"].append(annual_return)
        
        # Volatility
        volatility = returns.std() * np.sqrt(252)
        features["volatility"].append(volatility)
        
        # Sharpe ratio
        risk_free_rate = 0.05  # Assume 5% risk-free rate
        sharpe = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
        features["sharpe"].append(sharpe)
        
        # Max drawdown
        drawdown = (data['Close'] / data['Close'].cummax() - 1).min()
        features["max_dd"].append(drawdown)
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame({
        "ticker": tickers,
        "return": features["return"],
        "volatility": features["volatility"],
        "sharpe": features["sharpe"],
        "max_dd": features["max_dd"]
    })
    
    # Normalize features
    scaler = MinMaxScaler()
    for col in ["return", "sharpe"]:
        if not df[col].empty:
            df[col + "_norm"] = scaler.fit_transform(df[col].values.reshape(-1, 1))
        else:
            df[col + "_norm"] = 0
    
    for col in ["volatility", "max_dd"]:
        if not df[col].empty:
            # Invert these because lower is better
            df[col + "_norm"] = 1 - scaler.fit_transform(df[col].values.reshape(-1, 1))
        else:
            df[col + "_norm"] = 0
    
    # Weight factors based on risk profile
    weights = {
        "Conservative": {"return": 0.2, "volatility": 0.4, "sharpe": 0.3, "max_dd": 0.1},
        "Moderate": {"return": 0.3, "volatility": 0.3, "sharpe": 0.3, "max_dd": 0.1},
        "Aggressive": {"return": 0.4, "volatility": 0.2, "sharpe": 0.3, "max_dd": 0.1}
    }
    
    # Use moderate weights as default
    w = weights.get(risk_profile, weights["Moderate"])
    
    # Calculate score
    df["score"] = (
        w["return"] * df["return_norm"] +
        w["volatility"] * df["volatility_norm"] +
        w["sharpe"] * df["sharpe_norm"] +
        w["max_dd"] * df["max_dd_norm"]
    )
    
    # Sort by score
    df = df.sort_values("score", ascending=False)
    
    return df["ticker"].tolist()
