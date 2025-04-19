# app.py
from flask import Flask, render_template, request, jsonify
from retirement_calculator import RetirementCalculator
import numpy as np  # For NumPy type conversion

app = Flask(__name__)

# Convert NumPy or pandas types to JSON-safe Python types
def make_json_safe(d):
    return {
        k: (
            v.item() if hasattr(v, "item") 
            else bool(v) if isinstance(v, np.bool_) 
            else v
        )
        for k, v in d.items()
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get data from form
    current_age = int(request.form.get('current_age'))
    retirement_age = int(request.form.get('retirement_age'))
    death_age = int(request.form.get('death_age'))
    current_savings = float(request.form.get('current_savings'))
    pre_pension_years = int(request.form.get('pre_pension_years'))
    annual_contribution = float(request.form.get('annual_contribution'))
    desired_spend = float(request.form.get('desired_spend'))
    annual_return = float(request.form.get('annual_return'))
    inflation_rate = float(request.form.get('inflation_rate'))
    legacy_percent = float(request.form.get('legacy_percent'))

    # Create calculator instance
    calculator = RetirementCalculator(
        current_age, retirement_age, death_age, current_savings,
        pre_pension_years, annual_contribution, desired_spend,
        annual_return, inflation_rate, legacy_percent
    )

    # Run projections
    results, summary = calculator.calculate_projection()
    monte_carlo = calculator.run_monte_carlo(num_simulations=500)

    # Format chart data
    chart_data = {
        'labels': results['Age'].tolist(),
        'savings': results['Savings'].tolist(),
        'contributions': results['Contributions'].tolist(),
        'withdrawals': results['Withdrawals'].tolist(),
        'spending': results['Inflation_Adjusted_Spending'].tolist()
    }

    # Ensure JSON-safe return
    summary = make_json_safe(summary)
    monte_carlo = make_json_safe(monte_carlo)

    return jsonify({
        'summary': summary,
        'monte_carlo': monte_carlo,
        'chart_data': chart_data
    })

if __name__ == '__main__':
    app.run(debug=True)
