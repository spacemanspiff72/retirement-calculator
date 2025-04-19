# retirement_calculator.py
import numpy as np
import pandas as pd

class RetirementCalculator:
    def __init__(self, current_age, retirement_age, death_age, current_savings,
                 pre_pension_years, annual_contribution, desired_spend,
                 annual_return, inflation_rate, legacy_percent):
        # Initialize with user inputs
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.death_age = death_age
        self.current_savings = current_savings
        self.pre_pension_years = pre_pension_years
        self.annual_contribution = annual_contribution
        self.desired_spend = desired_spend
        self.annual_return = annual_return / 100  # Convert percentage to decimal
        self.inflation_rate = inflation_rate / 100  # Convert percentage to decimal
        self.legacy_percent = legacy_percent / 100  # Convert percentage to decimal
        
    def calculate_projection(self):
        # Calculate total years for the projection
        total_years = self.death_age - self.current_age
        
        # Initialize arrays to store yearly data
        years = np.arange(self.current_age, self.death_age + 1)
        savings = np.zeros(total_years + 1)
        contributions = np.zeros(total_years + 1)
        withdrawals = np.zeros(total_years + 1)
        inflation_adjusted_spend = np.zeros(total_years + 1)
        
        # Set initial values
        savings[0] = self.current_savings
        
        # Calculate year-by-year projection
        for i in range(1, total_years + 1):
            current_year = self.current_age + i
            
            # Pre-retirement phase: contributions
            if current_year < self.retirement_age:
                if i <= self.pre_pension_years:
                    contributions[i] = self.annual_contribution
                savings[i] = savings[i-1] * (1 + self.annual_return) + contributions[i]
            
            # Retirement phase: withdrawals
            else:
                # Calculate inflation-adjusted withdrawal
                years_from_start = i
                inflation_factor = (1 + self.inflation_rate) ** years_from_start
                inflation_adjusted_spend[i] = self.desired_spend * inflation_factor
                
                withdrawals[i] = inflation_adjusted_spend[i]
                savings[i] = savings[i-1] * (1 + self.annual_return) - withdrawals[i]
                
                # Ensure savings don't go negative
                if savings[i] < 0:
                    savings[i] = 0
                    withdrawals[i] = savings[i-1] * (1 + self.annual_return)
        
        # Calculate legacy target
        legacy_target = self.current_savings * self.legacy_percent
        legacy_achieved = savings[-1] >= legacy_target
        
        # Check if retirement plan is sustainable
        sustainable = all(s >= 0 for s in savings[self.retirement_age - self.current_age:])
        
        # Create a DataFrame for clearer data representation
        results = pd.DataFrame({
            'Age': years,
            'Savings': savings,
            'Contributions': contributions,
            'Withdrawals': withdrawals,
            'Inflation_Adjusted_Spending': inflation_adjusted_spend
        })
        
        summary = {
            'Final Savings': savings[-1],
            'Legacy Target': legacy_target,
            'Legacy Achieved': legacy_achieved,
            'Plan Sustainable': sustainable,
            'Years of Retirement': self.death_age - self.retirement_age,
            'Total Contributions': contributions.sum(),
            'Total Withdrawals': withdrawals.sum()
        }
        
        return results, summary
    
    def run_monte_carlo(self, num_simulations=1000, return_std_dev=0.1):
        """Optional: Run Monte Carlo simulations with variable returns"""
        success_count = 0
        final_values = []
        
        for _ in range(num_simulations):
            # Reset initial savings
            savings = self.current_savings
            
            # Pre-retirement phase
            for year in range(self.current_age, self.retirement_age):
                # Generate random return based on mean and std deviation
                year_return = np.random.normal(self.annual_return, return_std_dev)
                
                # Add contribution if in pre-pension years
                contribution = self.annual_contribution if year - self.current_age < self.pre_pension_years else 0
                
                # Update savings
                savings = savings * (1 + year_return) + contribution
            
            # Retirement phase
            sustainable = True
            for year in range(self.retirement_age, self.death_age + 1):
                # Generate random return
                year_return = np.random.normal(self.annual_return, return_std_dev)
                
                # Calculate inflation-adjusted withdrawal
                years_from_start = year - self.current_age
                inflation_factor = (1 + self.inflation_rate) ** years_from_start
                withdrawal = self.desired_spend * inflation_factor
                
                # Update savings
                savings = savings * (1 + year_return) - withdrawal
                
                # Check if we've run out of money
                if savings < 0:
                    sustainable = False
                    break
            
            # Count successful simulations and record final value
            if sustainable:
                success_count += 1
            final_values.append(savings)
        
        # Calculate probability of success and statistics
        probability_of_success = success_count / num_simulations * 100
        average_final_value = np.mean(final_values)
        
        return {
            'Probability of Success': probability_of_success,
            'Average Final Value': average_final_value,
            'Median Final Value': np.median(final_values),
            'Final Value 10th Percentile': np.percentile(final_values, 10),
            'Final Value 90th Percentile': np.percentile(final_values, 90)
        }