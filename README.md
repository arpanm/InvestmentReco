# Financial Goal Planner

A Streamlit-based financial goal planner with personalized stock/mutual fund recommendations and interactive visualizations.

## Features

- Set financial goals like marriage, new house, child education, retirement, etc.
- Calculate target amount with inflation adjustment
- Get personalized investment recommendations based on risk profile
- View one-time and monthly investment requirements
- Access summary tables of essential financial metrics
- Visualize year-by-year expected growth
- Explore historical stock/mutual fund performance with interactive charts
- Dark mode UI with minimalist design for data clarity

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- scikit-learn
- yfinance (Yahoo Finance API)

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Application Structure

- `app.py` - Main application file
- `utils/` - Utility modules
  - `data_fetcher.py` - Functions to fetch financial data
  - `financial_calculator.py` - Financial calculation utilities
  - `recommendation_engine.py` - Stock and fund recommendation logic
- `.streamlit/config.toml` - Streamlit configuration

## Technical Approach & Methodologies

### Data Sources & Financial Data Integration

The application leverages multiple free financial data sources with Yahoo Finance as the primary source:

- **Yahoo Finance API (yfinance)**: Fetches real-time and historical stock/mutual fund data including price history, dividends, volume, and key financial ratios
- **Historical Data Retrieval**: Implemented using `fetch_stock_data()` and `fetch_mutual_fund_data()` functions that accept ticker symbols, time periods, and intervals
- **Financial Information**: Extracts company profiles, sector information, and financial metrics using `get_stock_info()` and `get_mutual_fund_info()`
- **Market Index Data**: Pulls benchmark index data (e.g., Nifty 50, S&P 500) through `get_index_data()` for market comparison
- **Sector Performance**: Analyzes sector-wide performance trends with the `fetch_sector_performance()` function

### Financial Calculations & Goal Planning

The application implements several financial calculation methodologies:

- **Inflation Adjustment**: Uses compound interest formula in `calculate_future_value()` to project how inflation will impact the target amount
- **One-Time Investment Calculation**: Reverses the compound interest formula in `calculate_one_time_investment()` to determine lump-sum investment amount needed
- **Monthly SIP Calculation**: Uses time value of money principles in `calculate_monthly_investment()` to compute required monthly systematic investment
- **Growth Projection**: Simulates year-by-year growth of investments through `calculate_investment_growth()`, accounting for compounding returns
- **ROI Calculation**: Computes return on investment percentage with `calculate_roi()` by comparing final value to total invested amount
- **Asset Allocation**: Determines optimal allocation across asset classes based on risk profile using `calculate_asset_allocation()`

### ML/AI Models for Investment Recommendations

The application uses several machine learning and AI approaches for making investment recommendations:

- **Risk Profile Analysis**: Classifies users into Conservative, Moderate, or Aggressive investor categories based on goal timeframe and risk tolerance inputs
- **Stock/Fund Selection**: Implements algorithms that match investment recommendations to user's risk profile, goal type, and target amount
- **Portfolio Optimization**: Uses Modern Portfolio Theory principles to balance risk and return:
  - Calculates expected returns, volatility, and correlations between assets
  - Applies Mean-Variance Optimization for asset allocation
  - Implements the Sharpe Ratio for risk-adjusted return analysis
- **Recommendation Engine**: The core recommendation system uses:
  - K-means clustering to group similar stocks/funds
  - Random Forest models to rank investments based on multiple factors
  - Sentiment analysis of recent market trends (planned feature)

### Portfolio Construction & Allocation

The application determines specific investment allocations through these methods:

- **One-Time Investment Allocation**: Distributes the calculated lump sum amount across recommended stocks/funds based on:
  - Market capitalization and stability metrics for conservative profiles
  - Growth potential and momentum for aggressive profiles
  - Balanced approach for moderate profiles
- **Monthly Investment Allocation**: Determines optimal SIP distribution using:
  - Dollar-cost averaging principles
  - Risk-weighted allocation formulas
  - Liquidity requirements analysis
- **Portfolio Weights Calculation**: Computes optimal weights using `get_portfolio_weights()` function based on:
  - Historical performance correlation
  - Volatility metrics
  - Expected returns
  - Modern Portfolio Theory optimization

### Data Visualization & Interactive Charts

The application implements several visualization techniques:

- **Historical Performance Charts**: Creates interactive time-series plots of stock/fund price movements with customizable time ranges
- **Growth Projection Visualization**: Displays year-by-year expected growth of investments with:
  - Principal vs. returns breakdown
  - Comparison to inflation
  - Best/worst case scenarios
- **Financial Metrics Visualization**: Presents key ratios and metrics through:
  - Radar charts for comparative analysis
  - Bar charts for metric comparison
  - Heat maps for correlation analysis
- **Asset Allocation Charts**: Displays recommended allocation through:
  - Pie charts for asset class distribution
  - Treemaps for detailed breakdown
  - Stacked bar charts for time-based projection

## Planned Enhancements

### Advanced ML/AI Features

- **Sentiment Analysis Integration**: Incorporate market sentiment from financial news and social media
- **Deep Learning Models**: Implement LSTM networks for better time-series prediction
- **Anomaly Detection**: Add algorithms to identify outlier market conditions and adjust recommendations
- **Reinforcement Learning**: Develop models for dynamic portfolio rebalancing based on changing market conditions

### Additional Analysis & Reports

- **PDF Report Generation**: Enable downloadable comprehensive investment plan reports
- **Tax Efficiency Analysis**: Include tax implications of different investment strategies
- **Goal Tracking**: Add functionality to track progress toward financial goals
- **What-If Scenarios**: Allow users to adjust parameters and see immediate impacts on projections

### Educational Resources

- **Investment Education**: Add explanatory content about investment principles
- **Recommendation Rationale**: Provide detailed explanations behind each recommendation
- **Financial Concepts**: Include tooltips and guides explaining financial terms and calculations
- **Market Insights**: Incorporate current market analysis and trends

### User Experience Improvements

- **Mobile Optimization**: Enhance responsive design for better mobile experience
- **User Profiles**: Add ability to save and manage multiple financial goals
- **Notification System**: Implement alerts for significant market changes affecting recommendations
- **Performance Tracking**: Add dashboards to monitor investment performance over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.