import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from utils.financial_calculator import (
    calculate_future_value,
    calculate_one_time_investment,
    calculate_monthly_investment
)
from utils.data_fetcher import (
    fetch_stock_data,
    fetch_mutual_fund_data,
    get_stock_info,
    get_mutual_fund_info
)
from utils.recommendation_engine import (
    recommend_stocks,
    recommend_mutual_funds
)

# Page configuration
st.set_page_config(
    page_title="Financial Goal Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing goals
if 'goals' not in st.session_state:
    st.session_state.goals = []

if 'current_goal' not in st.session_state:
    st.session_state.current_goal = {}

if 'view_recommendations' not in st.session_state:
    st.session_state.view_recommendations = False

# Title and description
st.title("Financial Goal Planner")
st.markdown("""
    Plan your financial future with personalized investment recommendations.
    Set your goals, analyze potential investments, and track your progress.
""")

# Sidebar for goal management
with st.sidebar:
    st.header("Financial Goals")
    
    # Add new goal section
    st.subheader("Create a New Goal")
    goal_types = ["Marriage", "New House", "Child Education", "Retirement", "Other"]
    goal_type = st.selectbox("Goal Type", goal_types)
    goal_name = st.text_input("Goal Name", f"My {goal_type}")
    
    if st.button("Create Goal"):
        new_goal = {
            "id": len(st.session_state.goals) + 1,
            "name": goal_name,
            "type": goal_type,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "details": {}
        }
        st.session_state.goals.append(new_goal)
        st.session_state.current_goal = new_goal
        st.session_state.view_recommendations = False
        st.rerun()
    
    # Display existing goals
    if st.session_state.goals:
        st.divider()
        st.subheader("Your Goals")
        
        for i, goal in enumerate(st.session_state.goals):
            if st.button(f"{goal['name']} ({goal['type']})", key=f"goal_{i}"):
                st.session_state.current_goal = goal
                st.session_state.view_recommendations = False
                st.rerun()
    
    # Settings for calculations
    st.divider()
    st.subheader("Settings")
    default_inflation = 5.0
    default_return = 12.0
    
    st.session_state.inflation_rate = st.slider(
        "Average Inflation Rate (%)", 
        min_value=1.0, 
        max_value=10.0, 
        value=default_inflation, 
        step=0.1
    )
    
    st.session_state.expected_return = st.slider(
        "Expected Annual Return (%)", 
        min_value=4.0, 
        max_value=20.0, 
        value=default_return, 
        step=0.1
    )

# Main content area
if not st.session_state.goals:
    st.info("👈 Start by creating a financial goal in the sidebar")
elif not st.session_state.current_goal:
    st.info("👈 Select a goal from the sidebar to continue")
else:
    current_goal = st.session_state.current_goal
    
    # Display goal details and form
    if not st.session_state.view_recommendations:
        st.header(f"{current_goal['name']} ({current_goal['type']})")
        
        with st.form(key=f"goal_form_{current_goal['id']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                current_amount = st.number_input(
                    "Current Savings (₹)",
                    min_value=0,
                    value=current_goal.get("details", {}).get("current_amount", 0),
                    step=1000
                )
                
                target_year = st.number_input(
                    "Target Year",
                    min_value=datetime.now().year + 1,
                    max_value=datetime.now().year + 50,
                    value=current_goal.get("details", {}).get("target_year", datetime.now().year + 5)
                )
            
            with col2:
                if current_goal["type"] == "Marriage":
                    target_amount = st.number_input(
                        "Estimated Marriage Expenses (₹)",
                        min_value=100000,
                        value=current_goal.get("details", {}).get("target_amount", 1000000),
                        step=100000
                    )
                
                elif current_goal["type"] == "New House":
                    target_amount = st.number_input(
                        "Estimated House Cost (₹)",
                        min_value=1000000,
                        value=current_goal.get("details", {}).get("target_amount", 5000000),
                        step=500000
                    )
                
                elif current_goal["type"] == "Child Education":
                    target_amount = st.number_input(
                        "Estimated Education Cost (₹)",
                        min_value=500000,
                        value=current_goal.get("details", {}).get("target_amount", 2000000),
                        step=100000
                    )
                
                elif current_goal["type"] == "Retirement":
                    monthly_expenses = st.number_input(
                        "Expected Monthly Expenses After Retirement (₹)",
                        min_value=10000,
                        value=current_goal.get("details", {}).get("monthly_expenses", 50000),
                        step=5000
                    )
                    
                    retirement_years = st.number_input(
                        "Expected Years After Retirement",
                        min_value=1,
                        max_value=50,
                        value=current_goal.get("details", {}).get("retirement_years", 25)
                    )
                    
                    target_amount = monthly_expenses * 12 * retirement_years
                    st.write(f"Total retirement corpus needed: ₹{target_amount:,.2f}")
                
                else:  # Other
                    target_amount = st.number_input(
                        "Target Amount (₹)",
                        min_value=10000,
                        value=current_goal.get("details", {}).get("target_amount", 1000000),
                        step=10000
                    )
                
                risk_profile = st.select_slider(
                    "Risk Profile",
                    options=["Conservative", "Moderate", "Aggressive"],
                    value=current_goal.get("details", {}).get("risk_profile", "Moderate")
                )
            
            submitted = st.form_submit_button("Calculate & Get Recommendations")
            
            if submitted:
                # Save form data
                details = {
                    "current_amount": current_amount,
                    "target_year": target_year,
                    "target_amount": target_amount,
                    "risk_profile": risk_profile
                }
                
                if current_goal["type"] == "Retirement":
                    details["monthly_expenses"] = monthly_expenses
                    details["retirement_years"] = retirement_years
                
                # Update goal
                for i, goal in enumerate(st.session_state.goals):
                    if goal["id"] == current_goal["id"]:
                        st.session_state.goals[i]["details"] = details
                        st.session_state.current_goal = st.session_state.goals[i]
                        break
                
                st.session_state.view_recommendations = True
                st.rerun()
    
    # Display recommendations and visualizations
    else:
        goal = st.session_state.current_goal
        details = goal["details"]
        
        # Basic information
        st.header(f"{goal['name']} ({goal['type']})")
        
        years_to_goal = details["target_year"] - datetime.now().year
        inflation_rate = st.session_state.inflation_rate / 100
        expected_return = st.session_state.expected_return / 100
        risk_profile = details["risk_profile"]
        
        # Calculate future value considering inflation
        future_value = calculate_future_value(
            details["target_amount"], 
            inflation_rate, 
            years_to_goal
        )
        
        # Calculate required investments
        amount_needed = max(0, future_value - details["current_amount"])
        one_time_investment = calculate_one_time_investment(
            amount_needed, 
            expected_return, 
            years_to_goal
        )
        monthly_investment = calculate_monthly_investment(
            amount_needed, 
            expected_return, 
            years_to_goal
        )
        
        # Display financial summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Amount", 
                f"₹{details['current_amount']:,.2f}"
            )
            st.metric(
                "Target Year", 
                f"{details['target_year']} ({years_to_goal} years)"
            )
        
        with col2:
            st.metric(
                "Today's Value", 
                f"₹{details['target_amount']:,.2f}"
            )
            st.metric(
                "Future Value (with inflation)", 
                f"₹{future_value:,.2f}"
            )
        
        with col3:
            st.metric(
                "One-time Investment Needed", 
                f"₹{one_time_investment:,.2f}"
            )
            st.metric(
                "Monthly Investment Needed", 
                f"₹{monthly_investment:,.2f}"
            )
        
        # Get investment recommendations
        with st.spinner("Generating personalized investment recommendations..."):
            # Fetch recommended stocks and mutual funds based on risk profile and goal
            recommended_stocks = recommend_stocks(risk_profile, goal["type"], amount_needed)
            recommended_mutual_funds = recommend_mutual_funds(risk_profile, goal["type"], amount_needed)
            
            # Calculate allocation percentages based on risk profile
            stock_allocation = {
                "Conservative": 0.3,
                "Moderate": 0.5,
                "Aggressive": 0.7
            }[risk_profile]
            
            mf_allocation = 1 - stock_allocation
            
            # Calculate monetary allocations
            stock_total = amount_needed * stock_allocation
            mf_total = amount_needed * mf_allocation
            
            # Fetch data for recommendations
            stock_data = {}
            for ticker in recommended_stocks:
                try:
                    stock_data[ticker] = fetch_stock_data(ticker, period="2y")
                except Exception as e:
                    st.error(f"Error fetching data for {ticker}: {e}")
            
            mf_data = {}
            for ticker in recommended_mutual_funds:
                try:
                    mf_data[ticker] = fetch_mutual_fund_data(ticker, period="2y")
                except Exception as e:
                    st.error(f"Error fetching data for {ticker}: {e}")
        
        # Display tabs for different views
        tab1, tab2, tab3 = st.tabs(["Recommendations", "Growth Projections", "Historical Performance"])
        
        with tab1:
            st.subheader("Investment Recommendations")
            st.write(f"Based on your {risk_profile.lower()} risk profile and {goal['type'].lower()} goal")
            
            # Stock recommendations
            st.write("### Recommended Stocks")
            st.write(f"Allocation: {stock_allocation*100:.1f}% (₹{stock_total:,.2f})")
            
            if recommended_stocks:
                # Create stock allocation table
                stock_weights = np.array([1/len(recommended_stocks)] * len(recommended_stocks))
                stock_allocation_amounts = stock_total * stock_weights
                stock_one_time_allocations = one_time_investment * stock_allocation * stock_weights
                stock_monthly_allocations = monthly_investment * stock_allocation * stock_weights
                
                stocks_df = pd.DataFrame({
                    "Stock": recommended_stocks,
                    "Allocation %": [f"{w*100:.1f}%" for w in stock_weights],
                    "Amount (₹)": [f"{a:,.2f}" for a in stock_allocation_amounts],
                    "One-time Investment (₹)": [f"{a:,.2f}" for a in stock_one_time_allocations],
                    "Monthly Investment (₹)": [f"{a:,.2f}" for a in stock_monthly_allocations]
                })
                
                # Stock info
                stock_info = []
                for ticker in recommended_stocks:
                    info = get_stock_info(ticker)
                    stock_info.append(info)
                
                stock_info_df = pd.DataFrame(stock_info)
                
                # Display both tables
                st.dataframe(stocks_df, use_container_width=True)
                st.dataframe(stock_info_df, use_container_width=True)
            else:
                st.info("No stock recommendations available for this profile")
            
            # Mutual fund recommendations
            st.write("### Recommended Mutual Funds")
            st.write(f"Allocation: {mf_allocation*100:.1f}% (₹{mf_total:,.2f})")
            
            if recommended_mutual_funds:
                # Create mutual fund allocation table
                mf_weights = np.array([1/len(recommended_mutual_funds)] * len(recommended_mutual_funds))
                mf_allocation_amounts = mf_total * mf_weights
                mf_one_time_allocations = one_time_investment * mf_allocation * mf_weights
                mf_monthly_allocations = monthly_investment * mf_allocation * mf_weights
                
                mf_df = pd.DataFrame({
                    "Mutual Fund": recommended_mutual_funds,
                    "Allocation %": [f"{w*100:.1f}%" for w in mf_weights],
                    "Amount (₹)": [f"{a:,.2f}" for a in mf_allocation_amounts],
                    "One-time Investment (₹)": [f"{a:,.2f}" for a in mf_one_time_allocations],
                    "Monthly Investment (₹)": [f"{a:,.2f}" for a in mf_monthly_allocations]
                })
                
                # MF info
                mf_info = []
                for ticker in recommended_mutual_funds:
                    info = get_mutual_fund_info(ticker)
                    mf_info.append(info)
                
                mf_info_df = pd.DataFrame(mf_info)
                
                # Display both tables
                st.dataframe(mf_df, use_container_width=True)
                st.dataframe(mf_info_df, use_container_width=True)
            else:
                st.info("No mutual fund recommendations available for this profile")
        
        with tab2:
            st.subheader("Year-by-Year Growth Projections")
            
            # Create projection data
            years = list(range(datetime.now().year, details["target_year"] + 1))
            values_with_inflation = [
                calculate_future_value(details["target_amount"], inflation_rate, i) 
                for i in range(len(years))
            ]
            
            # Calculate growth of investments
            current_amount = details["current_amount"]
            one_time_values = [current_amount + one_time_investment]
            monthly_values = [current_amount]
            
            for i in range(1, len(years)):
                # One-time investment growth
                prev_value = one_time_values[-1]
                new_value = prev_value * (1 + expected_return)
                one_time_values.append(new_value)
                
                # Monthly investment growth
                prev_value = monthly_values[-1]
                new_value = prev_value * (1 + expected_return) + monthly_investment * 12
                monthly_values.append(new_value)
            
            # Create dataframe for the growth table
            projection_df = pd.DataFrame({
                "Year": years,
                "Age of Investment (Years)": list(range(len(years))),
                "Goal Value (₹)": [f"{v:,.2f}" for v in values_with_inflation],
                "One-time Investment Value (₹)": [f"{v:,.2f}" for v in one_time_values],
                "Monthly Investment Value (₹)": [f"{v:,.2f}" for v in monthly_values]
            })
            
            st.dataframe(projection_df, use_container_width=True)
            
            # Create growth chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=years,
                y=values_with_inflation,
                mode='lines+markers',
                name='Goal Value with Inflation',
                line=dict(color='red', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=years,
                y=one_time_values,
                mode='lines+markers',
                name='One-time Investment Growth',
                line=dict(color='green', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=years,
                y=monthly_values,
                mode='lines+markers',
                name='Monthly Investment Growth',
                line=dict(color='blue', width=2)
            ))
            
            fig.update_layout(
                title="Projected Growth vs. Goal Value",
                xaxis_title="Year",
                yaxis_title="Value (₹)",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display investment comparison
            st.subheader("Investment Returns Comparison")
            
            final_goal_value = values_with_inflation[-1]
            final_one_time_value = one_time_values[-1]
            final_monthly_value = monthly_values[-1]
            
            one_time_total_invested = one_time_investment + current_amount
            one_time_returns = final_one_time_value - one_time_total_invested
            one_time_roi = (one_time_returns / one_time_total_invested) * 100
            
            monthly_total_invested = monthly_investment * 12 * years_to_goal + current_amount
            monthly_returns = final_monthly_value - monthly_total_invested
            monthly_roi = (monthly_returns / monthly_total_invested) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### One-time Investment")
                st.metric("Total Invested", f"₹{one_time_total_invested:,.2f}")
                st.metric("Final Value", f"₹{final_one_time_value:,.2f}")
                st.metric("Total Returns", f"₹{one_time_returns:,.2f}")
                st.metric("ROI", f"{one_time_roi:.2f}%")
            
            with col2:
                st.write("### Monthly Investment")
                st.metric("Total Invested", f"₹{monthly_total_invested:,.2f}")
                st.metric("Final Value", f"₹{final_monthly_value:,.2f}")
                st.metric("Total Returns", f"₹{monthly_returns:,.2f}")
                st.metric("ROI", f"{monthly_roi:.2f}%")
        
        with tab3:
            st.subheader("Historical Performance Analysis")
            
            # Create tab for stocks vs mutual funds
            stock_tab, mf_tab = st.tabs(["Stocks", "Mutual Funds"])
            
            with stock_tab:
                if recommended_stocks and stock_data:
                    # Create selector for individual stocks
                    selected_stock = st.selectbox(
                        "Select a stock to view detailed performance", 
                        recommended_stocks
                    )
                    
                    if selected_stock in stock_data:
                        data = stock_data[selected_stock]
                        
                        # Price chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Close'],
                            mode='lines',
                            name='Close Price',
                            line=dict(color='#1E88E5', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_stock} - Historical Price (2 Years)",
                            xaxis_title="Date",
                            yaxis_title="Price (₹)",
                            template="plotly_dark"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Volume chart
                        fig = px.bar(
                            data, 
                            x=data.index, 
                            y='Volume',
                            title=f"{selected_stock} - Trading Volume"
                        )
                        
                        fig.update_layout(template="plotly_dark")
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Calculate returns
                        data['Daily Return'] = data['Close'].pct_change()
                        data['Cumulative Return'] = (1 + data['Daily Return']).cumprod() - 1
                        
                        # Returns chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Cumulative Return'] * 100,
                            mode='lines',
                            name='Cumulative Return (%)',
                            line=dict(color='#4CAF50', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_stock} - Cumulative Returns (%)",
                            xaxis_title="Date",
                            yaxis_title="Return (%)",
                            template="plotly_dark"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Performance metrics
                        total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
                        annualized_return = (1 + total_return/100) ** (1/(len(data)/252)) - 1
                        daily_returns = data['Daily Return'].dropna()
                        volatility = daily_returns.std() * np.sqrt(252) * 100
                        sharpe = (annualized_return / (volatility/100)) if volatility != 0 else 0
                        max_drawdown = (data['Close'] / data['Close'].cummax() - 1).min() * 100
                        
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        
                        with metrics_col1:
                            st.metric("Total Return (2Y)", f"{total_return:.2f}%")
                            st.metric("Annualized Return", f"{annualized_return*100:.2f}%")
                        
                        with metrics_col2:
                            st.metric("Volatility (Annual)", f"{volatility:.2f}%")
                            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
                        
                        with metrics_col3:
                            st.metric("Maximum Drawdown", f"{max_drawdown:.2f}%")
                            st.metric("Current Price", f"₹{data['Close'].iloc[-1]:.2f}")
                    else:
                        st.error(f"No data available for {selected_stock}")
                else:
                    st.info("No stock data available for analysis")
            
            with mf_tab:
                if recommended_mutual_funds and mf_data:
                    # Create selector for individual mutual funds
                    selected_mf = st.selectbox(
                        "Select a mutual fund to view detailed performance", 
                        recommended_mutual_funds
                    )
                    
                    if selected_mf in mf_data:
                        data = mf_data[selected_mf]
                        
                        # NAV chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Close'],
                            mode='lines',
                            name='NAV',
                            line=dict(color='#1E88E5', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_mf} - Historical NAV (2 Years)",
                            xaxis_title="Date",
                            yaxis_title="NAV (₹)",
                            template="plotly_dark"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Calculate returns
                        data['Daily Return'] = data['Close'].pct_change()
                        data['Cumulative Return'] = (1 + data['Daily Return']).cumprod() - 1
                        
                        # Returns chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Cumulative Return'] * 100,
                            mode='lines',
                            name='Cumulative Return (%)',
                            line=dict(color='#4CAF50', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_mf} - Cumulative Returns (%)",
                            xaxis_title="Date",
                            yaxis_title="Return (%)",
                            template="plotly_dark"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Performance metrics
                        total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
                        annualized_return = (1 + total_return/100) ** (1/(len(data)/252)) - 1
                        daily_returns = data['Daily Return'].dropna()
                        volatility = daily_returns.std() * np.sqrt(252) * 100
                        sharpe = (annualized_return / (volatility/100)) if volatility != 0 else 0
                        max_drawdown = (data['Close'] / data['Close'].cummax() - 1).min() * 100
                        
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        
                        with metrics_col1:
                            st.metric("Total Return (2Y)", f"{total_return:.2f}%")
                            st.metric("Annualized Return", f"{annualized_return*100:.2f}%")
                        
                        with metrics_col2:
                            st.metric("Volatility (Annual)", f"{volatility:.2f}%")
                            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
                        
                        with metrics_col3:
                            st.metric("Maximum Drawdown", f"{max_drawdown:.2f}%")
                            st.metric("Current NAV", f"₹{data['Close'].iloc[-1]:.2f}")
                    else:
                        st.error(f"No data available for {selected_mf}")
                else:
                    st.info("No mutual fund data available for analysis")
                    
        # Add button to go back to edit goal
        if st.button("Back to Goal Details"):
            st.session_state.view_recommendations = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Financial Goal Planner | Data sourced from Yahoo Finance | Not financial advice</p>
    </div>
    """,
    unsafe_allow_html=True
)
