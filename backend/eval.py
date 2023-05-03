import matplotlib.pyplot as plt
import pandas as pd
# Load data
batters_test_agg = pd.read_csv('frontend/public/b_forest_pred.csv')
batters_predictions = pd.read_csv('frontend/public/p_forest_pred.csv')

# Plot scatter plot for each stat
stats_to_predict = ['batting_avg', 'on_base_percent', 'slg_percent']

for stat in stats_to_predict:
    # Get true and predicted values
    y_true = batters_test_agg[stat]
    y_pred = batters_predictions[f'Predicted_{stat}']

    # Calculate residuals
    residuals = y_pred - y_true

    # Plot scatter plot
    plt.figure()
    plt.scatter(y_true, y_pred, c=residuals, cmap='coolwarm', alpha=0.8)
    plt.xlabel('True values')
    plt.ylabel('Predicted values')
    plt.title(f'{stat} scatter plot')
    
    # Add colorbar for residuals
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Residuals', rotation=270)
    
    plt.show()

