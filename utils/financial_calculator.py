import numpy as np

def calculate_future_value(present_value, inflation_rate, years):
    """
    Calculate the future value of a goal considering inflation.
    
    Args:
        present_value (float): The present value or cost of the goal
        inflation_rate (float): Annual inflation rate as a decimal (e.g., 0.05 for 5%)
        years (int): Number of years until the goal
        
    Returns:
        float: The future value of the goal
    """
    return present_value * (1 + inflation_rate) ** years

def calculate_one_time_investment(future_value, expected_return, years):
    """
    Calculate the one-time investment needed to reach the future value.
    
    Args:
        future_value (float): The target future value
        expected_return (float): Expected annual return as a decimal (e.g., 0.12 for 12%)
        years (int): Number of years for investment
        
    Returns:
        float: The one-time investment amount required
    """
    if years <= 0 or expected_return <= 0:
        return future_value
    
    return future_value / ((1 + expected_return) ** years)

def calculate_monthly_investment(future_value, expected_return, years):
    """
    Calculate the monthly investment needed to reach the future value.
    
    Args:
        future_value (float): The target future value
        expected_return (float): Expected annual return as a decimal (e.g., 0.12 for 12%)
        years (int): Number of years for investment
        
    Returns:
        float: The monthly investment amount required
    """
    if years <= 0 or expected_return <= 0:
        return future_value / (years * 12) if years > 0 else future_value
    
    # Convert annual rate to monthly rate
    monthly_rate = (1 + expected_return) ** (1/12) - 1
    months = years * 12
    
    # PMT formula: FV = PMT * ((1 + r)^n - 1) / r
    # Solving for PMT: PMT = FV * r / ((1 + r)^n - 1)
    denominator = ((1 + monthly_rate) ** months - 1)
    
    if denominator == 0:
        return future_value / months
    
    return future_value * monthly_rate / denominator

def calculate_investment_growth(initial_investment, monthly_investment, expected_return, years):
    """
    Calculate the year-by-year growth of an investment.
    
    Args:
        initial_investment (float): Initial one-time investment amount
        monthly_investment (float): Monthly recurring investment amount
        expected_return (float): Expected annual return as a decimal (e.g., 0.12 for 12%)
        years (int): Number of years for investment
        
    Returns:
        list: Year-by-year investment values
    """
    monthly_rate = (1 + expected_return) ** (1/12) - 1
    values = [initial_investment]
    
    for year in range(1, years + 1):
        prev_value = values[-1]
        year_end_value = prev_value
        
        # Calculate month by month for the year
        for month in range(12):
            year_end_value = year_end_value * (1 + monthly_rate) + monthly_investment
            
        values.append(year_end_value)
    
    return values

def calculate_roi(total_invested, final_value):
    """
    Calculate the Return on Investment (ROI).
    
    Args:
        total_invested (float): Total amount invested
        final_value (float): Final value of the investment
        
    Returns:
        float: ROI as a percentage
    """
    if total_invested == 0:
        return 0
    
    return ((final_value - total_invested) / total_invested) * 100

def calculate_asset_allocation(risk_profile, amount):
    """
    Calculate asset allocation based on risk profile.
    
    Args:
        risk_profile (str): Risk profile (Conservative, Moderate, Aggressive)
        amount (float): Total amount to allocate
        
    Returns:
        dict: Asset allocation percentages
    """
    if risk_profile == "Conservative":
        return {
            "Equity": 0.3,
            "Debt": 0.6,
            "Gold": 0.1
        }
    elif risk_profile == "Moderate":
        return {
            "Equity": 0.5,
            "Debt": 0.4,
            "Gold": 0.1
        }
    elif risk_profile == "Aggressive":
        return {
            "Equity": 0.7,
            "Debt": 0.25,
            "Gold": 0.05
        }
    else:
        # Default to moderate
        return {
            "Equity": 0.5,
            "Debt": 0.4,
            "Gold": 0.1
        }
