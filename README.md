# 📊 Quantitative Risk Dashboard

## Overview

The **Quantitative Risk Dashboard** is a modular, institutional-style portfolio risk monitoring system built using Python, Streamlit, and Plotly. It is designed to simulate the core analytical framework used by risk management desks to monitor market risk exposure in real time.

This project implements multiple Value at Risk (VaR) methodologies, Expected Shortfall (ES), rolling backtesting, portfolio analytics, and asset-level risk contribution analysis within a clean and interactive dashboard interface.

---

## 🎯 Objectives

* Implement multiple VaR methodologies (Historical, Monte Carlo, Parametric)
* Compute Expected Shortfall (ES)
* Perform rolling VaR backtesting and breach analysis
* Visualize portfolio return distributions
* Analyze cumulative returns and drawdowns
* Evaluate asset-level risk contribution
* Present results through a professional interactive dashboard

---

## 🏗 Project Architecture

```
Quantitative_Risk_Dashboard/
│
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   └── sample_data.csv
│   │
│   ├── engine/
│   │   └── var_engine.py
│   │
│   └── dashboard/
│       ├── app.py
│       └── plots.py
│
├── requirements.txt
└── README.md
```

The system follows a clean separation of concerns:

* **Data Layer** → Market and portfolio ingestion
* **Risk Engine** → Statistical computation
* **Dashboard Layer** → Visualization and interaction

---

## 📈 Implemented Risk Methodologies

### 1️⃣ Historical VaR

Non-parametric method using empirical return distribution.

### 2️⃣ Monte Carlo VaR

Simulated return distribution assuming normal dynamics.

### 3️⃣ Parametric (Variance-Covariance) VaR

Closed-form VaR assuming normally distributed returns.

### 4️⃣ Expected Shortfall (ES)

Conditional tail expectation beyond VaR threshold.

---

## 🔍 Advanced Analytics

* Rolling VaR (configurable window)
* VaR breach detection
* PnL distribution visualization with VaR cutoff
* Asset-level component risk contribution
* Cumulative portfolio returns
* Maximum drawdown analysis
* Correlation heatmap

---

## 🖥 Dashboard Features

### 📊 Risk Overview Tab

* VaR & ES metrics
* Interactive confidence level slider
* Method selection toggle
* PnL distribution with VaR line
* Asset risk contribution bar chart

### 📈 Backtesting Tab

* Rolling VaR visualization
* Actual returns overlay
* Breach count monitoring

### 📉 Portfolio Analytics Tab

* Cumulative return curve
* Drawdown time series
* Asset correlation matrix

---

## ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/SiddharthJogdand/Quantitative_Risk_Dashboard.git
cd Quantitative_Risk_Dashboard
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run src/dashboard/app.py
```

---

## 📊 Data Sources

* Market Data: Yahoo Finance (via `yfinance`)
* Portfolio Data: Static CSV (`sample_data.csv`) simulating position management export

---

## 🧠 Key Concepts Demonstrated

* Portfolio aggregation and weighting
* Covariance matrix risk modeling
* Simulation-based risk estimation
* Tail risk measurement
* Time-series backtesting
* Risk decomposition
* Visualization of distributional and path-dependent risk

---

## 🚀 Potential Extensions

* Stress testing scenarios
* GARCH-based volatility modeling
* Extreme Value Theory (EVT) VaR
* Multi-asset derivatives support
* Database integration (PostgreSQL)
* Real-time streaming updates

---

## 📌 Author

Hrushikesh Mahdi
Quantitative Finance & Risk Analytics Enthusiast

---

## 📜 License

This project is for academic and portfolio purposes.
