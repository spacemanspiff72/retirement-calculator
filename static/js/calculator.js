// static/js/calculator.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('calculator-form');
    const resultsSection = document.getElementById('results');
    let savingsChart;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        document.querySelector('.calculate-btn').textContent = 'Calculating...';
        
        // Collect form data
        const formData = new FormData(form);
        
        // Send data to server
        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Display results
            displayResults(data);
            document.querySelector('.calculate-btn').textContent = 'Calculate Retirement Plan';
        })
        .catch(error => {
            console.error('Error:', error);
            document.querySelector('.calculate-btn').textContent = 'Calculate Retirement Plan';
        });
    });
    
    function displayResults(data) {
        // Show results section
        resultsSection.classList.remove('hidden');
        
        // Display summary data
        const summaryContainer = document.getElementById('summary-data');
        summaryContainer.innerHTML = '';
        
        // Add each summary item
        for (const [key, value] of Object.entries(data.summary)) {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'summary-item';
            
            let displayValue = value;
            if (typeof value === 'number') {
                // Format currency values
                if (key.includes('Savings') || key.includes('Contributions') || 
                    key.includes('Withdrawals') || key.includes('Target')) {
                    displayValue = '$' + value.toLocaleString('en-US', {maximumFractionDigits: 0});
                }
                // Format percentage values
                else if (key.includes('Percentage')) {
                    displayValue = value.toFixed(1) + '%';
                }
                // Format boolean values
                else if (typeof value === 'boolean') {
                    displayValue = value ? '✅ Yes' : '❌ No';
                }
            }
            
            itemDiv.innerHTML = `
                <div class="summary-label">${key}</div>
                <div class="summary-value">${displayValue}</div>
            `;
            summaryContainer.appendChild(itemDiv);
        }
        
        // Display Monte Carlo results
        const monteCarloContainer = document.getElementById('monte-carlo-data');
        monteCarloContainer.innerHTML = '';
        
        for (const [key, value] of Object.entries(data.monte_carlo)) {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'summary-item';
            
            let displayValue = value;
            if (typeof value === 'number') {
                if (key.includes('Probability')) {
                    displayValue = value.toFixed(1) + '%';
                } else if (key.includes('Value')) {
                    displayValue = '$' + value.toLocaleString('en-US', {maximumFractionDigits: 0});
                }
            }
            
            itemDiv.innerHTML = `
                <div class="summary-label">${key}</div>
                <div class="summary-value">${displayValue}</div>
            `;
            monteCarloContainer.appendChild(itemDiv);
        }
        
        // Create chart
        createOrUpdateChart(data.chart_data);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function createOrUpdateChart(chartData) {
        const ctx = document.getElementById('savingsChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (savingsChart) {
            savingsChart.destroy();
        }
        
        // Create new chart
        savingsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [
                    {
                        label: 'Savings Balance',
                        data: chartData.savings,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        fill: true
                    },
                    {
                        label: 'Contributions',
                        data: chartData.contributions,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5]
                    },
                    {
                        label: 'Withdrawals',
                        data: chartData.withdrawals,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Age'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Amount ($)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += '$' + context.parsed.y.toLocaleString();
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
});