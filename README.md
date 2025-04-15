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