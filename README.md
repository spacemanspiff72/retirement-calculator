# 🧮 Interactive Retirement Calculator

This project is a full-stack web application that models retirement savings and spending paths, built using **Python (Flask, NumPy, Pandas)** on the backend and **HTML/CSS/JavaScript (Chart.js)** on the frontend.

It calculates both deterministic retirement paths and probabilistic Monte Carlo simulations, offering users a dynamic way to assess sustainability and legacy goals under uncertainty.

---

## 📈 What It Does

- Projects year-by-year **savings evolution** based on user inputs: age, savings, contributions, spending, expected return, and inflation.
- Adjusts spending during retirement for **inflation**.
- Computes **whether your retirement plan is sustainable** (i.e., never runs out of money before your death age).
- Estimates **legacy value** at end of life and whether it meets your target.
- Runs **Monte Carlo simulations** with randomized market returns to assess the **probability of success** and distribution of final outcomes.

---

## 📊 Financial Assumptions & Logic

### 1. **Projection Phases**

The model separates the retirement journey into two phases:

#### 🔹 Pre-Retirement (Accumulation)
- Contributions added annually for the number of *pre-pension years* (can be less than years until retirement).
- Portfolio grows using compounded **expected return**.

#### 🔹 Retirement (Decumulation)
- Withdrawals start at retirement and increase annually with **inflation**.
- Withdrawals continue until *death age*, or until funds are depleted.

---

### 2. **Inputs Used**

| Parameter             | Description                                   |
|----------------------|-----------------------------------------------|
| `current_age`         | Starting point for the simulation             |
| `retirement_age`      | When income stops, and withdrawals begin      |
| `death_age`           | Simulation endpoint                           |
| `current_savings`     | Initial portfolio balance                     |
| `pre_pension_years`   | How many years you'll contribute pre-retirement |
| `annual_contribution` | Fixed contribution per year                   |
| `desired_spend`       | Retirement annual spending target (inflation-adjusted) |
| `annual_return`       | Expected portfolio growth rate (mean)         |
| `inflation_rate`      | Assumed annual inflation rate                 |
| `legacy_percent`      | Target end-of-life wealth, as % of starting savings |

---

## 📐 Retirement Calculation Logic (Deterministic)

Each year:

- Pre-retirement:  
savings[i] = savings[i-1] * (1 + return) + contribution

- Retirement:
withdrawal = desired_spend * (1 + inflation) ^ years_from_start savings[i] = savings[i-1] * (1 + return) - withdrawal

yaml

Edge case handling:
- If savings go negative during retirement, the model caps them at 0 and adjusts the final withdrawal downward.

---

## 🎲 Monte Carlo Simulation Logic

Simulates multiple future paths (default: 500) by randomizing annual returns:

- **Returns follow a normal distribution** with:
- Mean = `annual_return`
- Std dev = `return_std_dev` (default: 10%)

For each path:
- Pre-retirement: apply random return + contributions
- Retirement: apply random return - inflation-adjusted withdrawals

At the end, we compute:

| Metric                         | Meaning                                           |
|-------------------------------|---------------------------------------------------|
| `Probability of Success`       | % of simulations where savings ≥ 0 at death       |
| `Average Final Value`          | Mean ending portfolio balance                     |
| `Median Final Value`           | 50th percentile outcome                           |
| `10th / 90th Percentiles`      | Show range of uncertainty                         |

---

## 🔧 Tech Stack

| Layer       | Tools                                     |
|------------|-------------------------------------------|
| Backend     | Python, Flask, NumPy, Pandas              |
| Frontend    | HTML, CSS, JavaScript, Chart.js           |
| Visualization | Interactive charts + summary stats       |
| Deployment (suggested) | Heroku, PythonAnywhere, or Docker  |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/retirement-calculator.git
cd retirement-calculator
