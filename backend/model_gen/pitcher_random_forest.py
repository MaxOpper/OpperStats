from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
import pandas as pd
import joblib
import os

# Load the data from the CSV files
pitchers_agg = pd.read_csv('backend/cleaned_data/p_agg.csv')
pitchers_test_agg = pd.read_csv('backend/cleaned_data/p_val.csv')

# Train random forest models for each stat
pitching_stats_to_predict = ['p_era', 'p_opp_batting_avg', 'woba']
pitching_models = {}

for stat in pitching_stats_to_predict:
    X = pitchers_agg.drop(columns=['last_name', 'first_name', 'player_id', 'year', 'p_era', 'p_opp_batting_avg', 'woba'])
    y = pitchers_agg[stat]

    model = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=0)

    # Use cross-validation to train the model and get the mean squared error
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    mean_score = -scores.mean()
    print(f"Mean squared error for {stat}: {mean_score:.4f}")

    # Fit the model on the full training set
    model.fit(X, y)
    pitching_models[stat] = model

    # Save the trained model as a joblib file
    joblib.dump(model, f'backend/flask/models/{stat}_model.joblib')

# Predict using the validation set
X_val = pitchers_test_agg.drop(columns=['last_name', 'first_name', 'player_id', 'year', 'p_era', 'p_opp_batting_avg', 'woba'])
pitching_predictions = {}

for stat, model in pitching_models.items():
    y_val = pitchers_test_agg[stat]
    y_pred = model.predict(X_val)

    # Calculate mean squared error
    mse = mean_squared_error(y_val, y_pred)
    print(f'Mean squared error for {stat}:', mse)

    pitching_predictions[stat] = y_pred

# Store predictions in a DataFrame
pitchers_predictions = pitchers_test_agg[['player_id', 'first_name', 'last_name']].copy()
for stat, pred in pitching_predictions.items():
    pitchers_predictions[f'Predicted_{stat}'] = pred

# Save predictions to a CSV file
pitchers_predictions.to_csv('frontend/public/p_forest_pred.csv', index=False)
