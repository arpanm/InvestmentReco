import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st

# Cache data to avoid unnecessary API calls
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Period of historical data (e.g., 1y, 2y, 5y)
        interval (str): Data interval (e.g., 1d, 1wk, 1mo)
        
    Returns:
        pandas.DataFrame: Historical stock data
    """
    try:
        # Add .NS suffix for Indian stocks if not already present
        if not ticker.endswith(('.NS', '.BO')):
            ticker = f"{ticker}.NS"
        
        data = yf.download(ticker, period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        # Return empty dataframe with proper columns
        return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

# Cache data to avoid unnecessary API calls
@st.cache_data(ttl=3600)
def fetch_mutual_fund_data(ticker, period="1y", interval="1d"):
    """
    Fetch mutual fund data from Yahoo Finance.
    
    Args:
        ticker (str): Mutual fund ticker symbol
        period (str): Period of historical data (e.g., 1y, 2y, 5y)
        interval (str): Data interval (e.g., 1d, 1wk, 1mo)
        
    Returns:
        pandas.DataFrame: Historical mutual fund data
    """
    try:
        data = yf.download(ticker, period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        # Return empty dataframe with proper columns
        return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

@st.cache_data(ttl=3600)
def get_stock_info(ticker):
    """
    Get stock information from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        dict: Stock information
    """
    try:
        # Add .NS suffix for Indian stocks if not already present
        if not ticker.endswith(('.NS', '.BO')):
            ticker = f"{ticker}.NS"
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract relevant information
        return {
            "Name": info.get("longName", ticker),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap (Cr)": round(info.get("marketCap", 0) / 10000000, 2),
            "P/E Ratio": round(info.get("trailingPE", 0), 2),
            "Dividend Yield (%)": round(info.get("dividendYield", 0) * 100, 2),
            "52 Week High": round(info.get("fiftyTwoWeekHigh", 0), 2),
            "52 Week Low": round(info.get("fiftyTwoWeekLow", 0), 2),
            "Current Price": round(info.get("currentPrice", 0), 2)
        }
    except Exception as e:
        st.error(f"Error fetching info for {ticker}: {str(e)}")
        # Return placeholder data
        return {
            "Name": ticker,
            "Sector": "N/A",
            "Industry": "N/A",
            "Market Cap (Cr)": 0,
            "P/E Ratio": 0,
            "Dividend Yield (%)": 0,
            "52 Week High": 0,
            "52 Week Low": 0,
            "Current Price": 0
        }

@st.cache_data(ttl=3600)
def get_mutual_fund_info(ticker):
    """
    Get mutual fund information from Yahoo Finance.
    
    Args:
        ticker (str): Mutual fund ticker symbol
        
    Returns:
        dict: Mutual fund information
    """
    try:
        mf = yf.Ticker(ticker)
        info = mf.info
        
        # Extract relevant information
        return {
            "Name": info.get("longName", ticker),
            "Category": info.get("category", "N/A"),
            "AUM (Cr)": round(info.get("totalAssets", 0) / 10000000, 2),
            "Expense Ratio (%)": round(info.get("annualReportExpenseRatio", 0) * 100, 2),
            "Morningstar Rating": info.get("morningStarRating", "N/A"),
            "YTD Return (%)": round(info.get("ytdReturn", 0) * 100, 2),
            "3Y Return (%)": round(info.get("threeYearAverageReturn", 0) * 100, 2),
            "5Y Return (%)": round(info.get("fiveYearAverageReturn", 0) * 100, 2),
            "NAV": round(info.get("navPrice", 0), 2)
        }
    except Exception as e:
        st.error(f"Error fetching info for {ticker}: {str(e)}")
        # Return placeholder data
        return {
            "Name": ticker,
            "Category": "N/A",
            "AUM (Cr)": 0,
            "Expense Ratio (%)": 0,
            "Morningstar Rating": "N/A",
            "YTD Return (%)": 0,
            "3Y Return (%)": 0,
            "5Y Return (%)": 0,
            "NAV": 0
        }

def get_index_data(index_ticker="^NSEI", period="1y"):
    """
    Get index data (default: Nifty 50).
    
    Args:
        index_ticker (str): Index ticker symbol
        period (str): Period of historical data
        
    Returns:
        pandas.DataFrame: Historical index data
    """
    try:
        data = yf.download(index_ticker, period=period)
        return data
    except Exception as e:
        st.error(f"Error fetching index data: {str(e)}")
        return pd.DataFrame()

def fetch_sector_performance():
    """
    Fetch sector performance data.
    
    Returns:
        pandas.DataFrame: Sector performance data
    """
    # Sample Indian sectors and their tickers
    sectors = {
        "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
        "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
        "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "BIOCON.NS"],
        "Auto": ["MARUTI.NS", "M&M.NS", "TATAMOTORS.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS"],
        "Energy": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "BPCL.NS"]
    }
    
    sector_returns = {}
    
    for sector, tickers in sectors.items():
        returns = []
        for ticker in tickers:
            try:
                data = fetch_stock_data(ticker, period="1y")
                if not data.empty:
                    returns.append((data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100)
            except Exception:
                continue
        
        if returns:
            sector_returns[sector] = np.mean(returns)
        else:
            sector_returns[sector] = 0
    
    # Create dataframe
    df = pd.DataFrame(list(sector_returns.items()), columns=['Sector', 'Return (%)'])
    df = df.sort_values('Return (%)', ascending=False)
    
    return df
