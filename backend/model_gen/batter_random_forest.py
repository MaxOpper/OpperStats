from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
import pandas as pd
import os
import joblib

#last_name, first_name,player_id,year,b_ab,batting_avg,slg_percent,on_base_percent,xba,xslg,xwoba,xobp,xiso,xwobacon,xbacon,exit_velocity_avg,launch_angle_avg,barrel_batted_rate,hard_hit_percent,
# Load data
batters_agg= pd.read_csv('backend/cleaned_data/b_agg.csv')
batters_test_agg = pd.read_csv('backend/cleaned_data/b_val.csv')
print(batters_agg.isna().sum())
# Train random forest models for each stat
stats_to_predict = ['batting_avg', 'slg_percent', 'on_base_percent']
models = {}

for stat in stats_to_predict:
    X_train = batters_agg.drop(columns=['last_name','first_name',
        'player_id','year', 'batting_avg', 'slg_percent', 'on_base_percent'])
    y_train = batters_agg[stat]

    model = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=0)
    
    # Use cross-validation to train the model and get the mean squared error
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    mean_score = -scores.mean()
    print(f"Mean squared error for {stat}: {mean_score:.4f}")
    
    # Fit the model on the full training set
    model.fit(X_train, y_train)
    models[stat] = model
    
    # Save the trained model as a joblib file in the backend/flask directory
    joblib.dump(model, f'backend/flask/models/{stat}_model.joblib')

# Predict using the validation set
X_val = batters_test_agg.drop(columns=['last_name','first_name',
        'player_id','year', 'batting_avg', 'slg_percent', 'on_base_percent'])
predictions = {}

for stat, model in models.items():
    y_val = batters_test_agg[stat]
    y_pred = model.predict(X_val)

    # Calculate mean squared error
    mse = mean_squared_error(y_val, y_pred)
    print(f'Mean squared error for {stat}:', mse)

    predictions[stat] = y_pred

# Store predictions in a DataFrame
batters_predictions = batters_test_agg[['player_id', 'first_name', 'last_name']].copy()
for stat, pred in predictions.items():
    batters_predictions[f'Predicted_{stat}'] = pred

# Calculate predicted OPS from predicted OBP and SLG
batters_predictions['Predicted_OPS'] = (batters_predictions['Predicted_on_base_percent'] + batters_predictions['Predicted_slg_percent']).round(3)

# Save predictions with calculated OPS to a CSV file
batters_predictions.to_csv('frontend/public/b_forest_pred.csv', index=False)
