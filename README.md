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

- **Yahoo Finance API (yfinance)**: Fetches real-time and historical stock/mutual fund data including price history, dividends, volume, and key financial ratios (`utils/data_fetcher.py`, lines 1-3)
- **Historical Data Retrieval**: Implemented using `fetch_stock_data()` (`utils/data_fetcher.py`, lines 9-31) and `fetch_mutual_fund_data()` (`utils/data_fetcher.py`, lines 35-53) functions that accept ticker symbols, time periods, and intervals
- **Financial Information**: Extracts company profiles, sector information, and financial metrics using `get_stock_info()` (`utils/data_fetcher.py`, lines 56-99) and `get_mutual_fund_info()` (`utils/data_fetcher.py`, lines 102-141)
- **Market Index Data**: Pulls benchmark index data (e.g., Nifty 50, S&P 500) through `get_index_data()` (`utils/data_fetcher.py`, lines 143-159) for market comparison
- **Sector Performance**: Analyzes sector-wide performance trends with the `fetch_sector_performance()` function (`utils/data_fetcher.py`, lines 161-198)
- **Implementation**: Data fetching is integrated throughout the app in the main visualization tabs (`app.py`, lines 280-315)

### Financial Calculations & Goal Planning

The application implements several financial calculation methodologies:

- **Inflation Adjustment**: Uses compound interest formula in `calculate_future_value()` (`utils/financial_calculator.py`, lines 3-15) to project how inflation will impact the target amount
- **One-Time Investment Calculation**: Reverses the compound interest formula in `calculate_one_time_investment()` (`utils/financial_calculator.py`, lines 17-32) to determine lump-sum investment amount needed
- **Monthly SIP Calculation**: Uses time value of money principles in `calculate_monthly_investment()` (`utils/financial_calculator.py`, lines 34-60) to compute required monthly systematic investment
- **Growth Projection**: Simulates year-by-year growth of investments through `calculate_investment_growth()` (`utils/financial_calculator.py`, lines 62-88), accounting for compounding returns
- **ROI Calculation**: Computes return on investment percentage with `calculate_roi()` (`utils/financial_calculator.py`, lines 90-104) by comparing final value to total invested amount
- **Asset Allocation**: Determines optimal allocation across asset classes based on risk profile using `calculate_asset_allocation()` (`utils/financial_calculator.py`, lines 106-141)
- **Implementation**: These calculations are applied in the main app to generate recommendations (`app.py`, lines 231-248) and projections (`app.py`, lines 391-449)

### ML/AI Models for Investment Recommendations

The application uses several machine learning and AI approaches for making investment recommendations:

- **Risk Profile Analysis**: Classifies users into Conservative, Moderate, or Aggressive investor categories based on goal timeframe and risk tolerance inputs (`app.py`, lines 186-190)
- **Stock/Fund Selection**: Implements algorithms that match investment recommendations to user's risk profile, goal type, and target amount:
  - Stock recommendation logic: `recommend_stocks()` (`utils/recommendation_engine.py`, lines 10-114)
  - Mutual fund recommendation logic: `recommend_mutual_funds()` (`utils/recommendation_engine.py`, lines 118-201)
- **Portfolio Optimization**: Uses Modern Portfolio Theory principles to balance risk and return:
  - Calculates expected returns, volatility, and correlations between assets (`utils/recommendation_engine.py`, lines 224-252)
  - Applies Mean-Variance Optimization for asset allocation via `calculate_portfolio_metrics()` (`utils/recommendation_engine.py`, lines 224-252)
  - Implements the Sharpe Ratio for risk-adjusted return analysis (`utils/recommendation_engine.py`, lines 296-298)
- **Recommendation Engine**: The core recommendation system uses:
  - K-means clustering to group similar stocks/funds (planned implementation in `simple_ml_recommendation()`, `utils/recommendation_engine.py`, lines 255-349)
  - Random Forest models to rank investments based on multiple factors (feature weighting in `utils/recommendation_engine.py`, lines 329-336)
  - Sentiment analysis of recent market trends (planned feature)
- **Implementation**: ML models are called from the app to generate personalized recommendations (`app.py`, lines 286-287)

### Portfolio Construction & Allocation

The application determines specific investment allocations through these methods:

- **One-Time Investment Allocation**: Distributes the calculated lump sum amount across recommended stocks/funds based on:
  - Market capitalization and stability metrics for conservative profiles (`utils/recommendation_engine.py`, lines 23-29)
  - Growth potential and momentum for aggressive profiles (`utils/recommendation_engine.py`, lines 37-41)
  - Balanced approach for moderate profiles (`utils/recommendation_engine.py`, lines 30-36)
  - Implementation in app: (`app.py`, lines 330-334) for stocks and (`app.py`, lines 364-366) for mutual funds
- **Monthly Investment Allocation**: Determines optimal SIP distribution using:
  - Dollar-cost averaging principles
  - Risk-weighted allocation formulas (via equal weight distribution in current implementation)
  - Liquidity requirements analysis
  - Implementation in app: (`app.py`, lines 334, 366-367)
- **Portfolio Weights Calculation**: Computes optimal weights using `get_portfolio_weights()` function (`utils/recommendation_engine.py`, lines 203-222) based on:
  - Historical performance correlation
  - Volatility metrics
  - Expected returns
  - Modern Portfolio Theory optimization
  - Currently implemented with simple equal weighting (`app.py`, lines 330, 363) with framework for future optimization

### Data Visualization & Interactive Charts

The application implements several visualization techniques:

- **Historical Performance Charts**: Creates interactive time-series plots of stock/fund price movements with customizable time ranges (`app.py`, lines 501-590)
  - Uses Plotly for interactive charts (`app.py`, lines 4-5)
  - Implements line charts for price trends (`app.py`, lines ~520-540)
  - Adds range selector for time period analysis
- **Growth Projection Visualization**: Displays year-by-year expected growth of investments (`app.py`, lines 391-449) with:
  - Principal vs. returns breakdown
  - Comparison to inflation
  - Best/worst case scenarios
  - Uses interactive area charts for visual clarity
- **Financial Metrics Visualization**: Presents key ratios and metrics through:
  - Data tables of stock info (`app.py`, lines 344-353)
  - Data tables of mutual fund info (`app.py`, lines 377-386)
  - Metric cards for key financial values (`app.py`, lines 253-281)
- **Asset Allocation Charts**: Displays recommended allocation through:
  - Visual indicators of allocation percentages (`app.py`, lines 326, 359)
  - Detailed breakdowns in data tables (`app.py`, lines 335-342, 368-374)

## Planned Enhancements

### Advanced ML/AI Features

- **Sentiment Analysis Integration**: 
  - Incorporate market sentiment from financial news and social media
  - Implementation path: Extend `utils/recommendation_engine.py` with a new function `analyze_market_sentiment(ticker)` around line 350
  - Integration point: Update `simple_ml_recommendation()` (line 255) to include sentiment scores in the ranking algorithm
  - Dependencies: Add NLTK or TextBlob for sentiment analysis

- **Deep Learning Models**: 
  - Implement LSTM networks for better time-series prediction
  - Implementation path: Create new file `utils/deep_learning.py` with function `lstm_price_prediction(ticker, days_to_predict)`
  - Integration point: Import in `app.py` and add predictions to the Historical Performance tab (line ~590)
  - Dependencies: Add TensorFlow or PyTorch

- **Anomaly Detection**: 
  - Add algorithms to identify outlier market conditions and adjust recommendations
  - Implementation path: Add function `detect_market_anomalies()` to `utils/recommendation_engine.py` around line 350
  - Integration point: Call from stock/fund recommendation functions (lines 10, 118)
  - Use isolation forests or autoencoders for detection

- **Reinforcement Learning**: 
  - Develop models for dynamic portfolio rebalancing based on changing market conditions
  - Implementation path: Create new file `utils/reinforcement_learning.py` with a portfolio rebalancing agent
  - Integration point: Add rebalancing suggestions to the Recommendations tab (line ~320)
  - Dependencies: Add stable-baselines3 or TensorFlow RL

### Additional Analysis & Reports

- **PDF Report Generation**: 
  - Enable downloadable comprehensive investment plan reports
  - Implementation path: Add new file `utils/report_generator.py` with function `generate_pdf_report(goal, recommendations)`
  - Integration point: Add download button to `app.py` in Recommendations tab (line ~320)
  - Dependencies: Add ReportLab or FPDF

- **Tax Efficiency Analysis**: 
  - Include tax implications of different investment strategies
  - Implementation path: Add `calculate_tax_implications()` to `utils/financial_calculator.py` around line 142
  - Integration point: Display tax metrics in the Recommendations tab (line ~320)
  - Consider short-term vs. long-term capital gains

- **Goal Tracking**: 
  - Add functionality to track progress toward financial goals
  - Implementation path: Extend `app.py` with a new tab for tracking (add after line 318)
  - Add progress charts and milestone tracking
  - Store historical data in session state or database

- **What-If Scenarios**: 
  - Allow users to adjust parameters and see immediate impacts on projections
  - Implementation path: Add sliders in Growth Projections tab (line ~391)
  - Enable dynamic recalculation of projections when parameters change
  - Use Streamlit callbacks for interactivity

### Educational Resources

- **Investment Education**: 
  - Add explanatory content about investment principles
  - Implementation path: Create new tab in `app.py` after line 318
  - Display educational content with expandable sections
  - Include external resources and references

- **Recommendation Rationale**: 
  - Provide detailed explanations behind each recommendation
  - Implementation path: Extend recommendation functions in `utils/recommendation_engine.py` (lines 10, 118) to return rationales
  - Integration point: Add info buttons beside each recommendation in `app.py` (lines ~335, ~368)
  - Implement tooltips or expandable sections for details

- **Financial Concepts**: 
  - Include tooltips and guides explaining financial terms and calculations
  - Implementation path: Add Streamlit tooltips throughout the app using st.help in `app.py`
  - Create a glossary component around line 590
  - Link financial terms to explanations

- **Market Insights**: 
  - Incorporate current market analysis and trends
  - Implementation path: Add function `get_market_insights()` to `utils/data_fetcher.py` around line 200
  - Integration point: Display insights in a new dashboard section in `app.py` after line 590
  - Pull from financial news APIs or economic indicators

### User Experience Improvements

- **Mobile Optimization**: 
  - Enhance responsive design for better mobile experience
  - Implementation path: Update layout in `app.py` with responsive Streamlit columns
  - Use dynamic resizing based on viewport size
  - Optimize charts for smaller screens

- **User Profiles**: 
  - Add ability to save and manage multiple financial goals
  - Implementation path: Implement user authentication in `app.py` around line 33
  - Store user profiles and goals in a database
  - Enable goal comparison and portfolio view

- **Notification System**: 
  - Implement alerts for significant market changes affecting recommendations
  - Implementation path: Add function `check_portfolio_alerts()` to `utils/data_fetcher.py` around line 200
  - Integration point: Display alerts at the top of the app in `app.py` (line ~45)
  - Define alert thresholds based on risk profile

- **Performance Tracking**: 
  - Add dashboards to monitor investment performance over time
  - Implementation path: Create performance tracking tab in `app.py` after line 318
  - Implement portfolio performance metrics in `utils/financial_calculator.py` around line 142
  - Generate visualizations of historical performance vs projections

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.