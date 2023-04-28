from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS
import pandas as pd
from pybaseball import playerid_lookup
app = Flask(__name__)
CORS(app)

b_data = pd.read_csv('backend/flask/b_curr.csv')
p_data = pd.read_csv('backend/flask/p_curr.csv')

# Load the trained models
pitching_models = {}
pitching_stats_to_predict = ['p_era', 'p_opp_batting_avg', 'woba']
for stat in pitching_stats_to_predict:
    model = joblib.load('backend/flask/models/' + stat + '_model.joblib')
    pitching_models[stat] = model

batting_models = {}
batting_stats_to_predict = ['batting_avg', 'on_base_percent', 'slg_percent']
for stat in batting_stats_to_predict:
    model = joblib.load('backend/flask/models/' + stat + '_model.joblib')
    batting_models[stat] = model

# Define endpoint for getting player projections
@app.route('/projections', methods=['POST'])
def get_projections():
    # Get the player name and flag from the request
    player_stats = pd.DataFrame()

    player_name = request.json['player_name']
    firstName, lastName = player_name.split(' ')
    if firstName == 'Shohei' and lastName == 'Ohtani':
        pID = b_data.loc[(b_data['first_name'] == firstName) & (b_data['last_name'] == lastName), 'player_id'].iloc[0]
        # Get pitching and hitting projections for Shohei Ohtani. Dude breaks this
        player_stats = b_data[b_data['player_id'] == pID]
        player_stats = pd.DataFrame({
            'last_name': [lastName],
            'first_name': [firstName],
            'player_id': [player_stats['player_id'].iloc[0]],
            'year': [player_stats['year'].iloc[0]],
            'b_ab': [player_stats['b_ab'].iloc[0]],
            'batting_avg': [player_stats['batting_avg'].iloc[0]],
            'slg_percent': [player_stats['slg_percent'].iloc[0]],
            'on_base_percent': [player_stats['on_base_percent'].iloc[0]],
            'xba': [player_stats['xba'].iloc[0]],
            'xslg': [player_stats['xslg'].iloc[0]],
            'xwoba': [player_stats['xwoba'].iloc[0]],
            'xobp': [player_stats['xobp'].iloc[0]],
            'xiso': [player_stats['xiso'].iloc[0]],
            'xwobacon': [player_stats['xwobacon'].iloc[0]],
            'xbacon': [player_stats['xbacon'].iloc[0]],
            'exit_velocity_avg': [player_stats['exit_velocity_avg'].iloc[0]],
            'launch_angle_avg': [player_stats['launch_angle_avg'].iloc[0]],
            'barrel_batted_rate': [player_stats['barrel_batted_rate'].iloc[0]],
            'hard_hit_percent': [player_stats['hard_hit_percent'].iloc[0]]
        })
        pID = p_data.loc[(p_data['first_name'] == firstName) & (p_data['last_name'] == lastName), 'player_id'].iloc[0]
        player_stats_p = p_data[p_data['player_id'] == pID]
        player_stats_p = pd.DataFrame({
            'last_name': [lastName],
            'first_name': [firstName],
            'player_id': [player_stats_p['player_id'].iloc[0]],
            'year': [player_stats_p['year'].iloc[0]],
            'p_era': [player_stats_p['p_era'].iloc[0]],
            'p_opp_batting_avg': [player_stats_p['p_opp_batting_avg'].iloc[0]],
            'xba': [player_stats_p['xba'].iloc[0]],
            'xslg': [player_stats_p['xslg'].iloc[0]],
            'woba': [player_stats_p['woba'].iloc[0]],
            'xwoba': [player_stats_p['xwoba'].iloc[0]],
            'xobp': [player_stats_p['xobp'].iloc[0]],
            'xiso': [player_stats_p['xiso'].iloc[0]],
            'exit_velocity_avg': [player_stats_p['exit_velocity_avg'].iloc[0]],
            'launch_angle_avg': [player_stats_p['launch_angle_avg'].iloc[0]],
            'sweet_spot_percent': [player_stats_p['sweet_spot_percent'].iloc[0]],
            'barrel_batted_rate': [player_stats_p['barrel_batted_rate'].iloc[0]],
            'groundballs_percent': [player_stats_p['groundballs_percent'].iloc[0]],
            'flyballs_percent': [player_stats_p['flyballs_percent'].iloc[0]],
            'linedrives_percent': [player_stats_p['linedrives_percent'].iloc[0]]

        })

        # Make predictions for pitching stats
        pitching_predictions = {}
        for stat, model in pitching_models.items():
            X = player_stats_p.drop(columns=['last_name', 'first_name', 'player_id', 'year', 'p_era', 'p_opp_batting_avg', 'woba'])
            y_pred = model.predict(X)
            pitching_predictions[stat] = float(y_pred[0])

        # Make predictions for batting stats
        batting_predictions = {}
        for stat, model in batting_models.items():
            X = player_stats.drop(columns=['last_name','first_name',
        'player_id','year', 'batting_avg', 'slg_percent', 'on_base_percent'])
            y_pred = model.predict(X)
            batting_predictions[stat] = float(y_pred[0])

        # Combine pitching and batting predictions
        combined_predictions = {**pitching_predictions, **batting_predictions}

        # Send back the combined predictions
        return jsonify(combined_predictions)
    
    batter_true = 0
    if (b_data['first_name'] == firstName).any() and (b_data['last_name'] == lastName).any():
        batter_true = 1
        pID = b_data.loc[(b_data['first_name'] == firstName) & (b_data['last_name'] == lastName), 'player_id'].iloc[0]
    else:
        batter_true = 0
        pID = p_data.loc[(p_data['first_name'] == firstName) & (p_data['last_name'] == lastName), 'player_id'].iloc[0]

    # Pull player stats from online (for testing purposes, use sample data)
    if batter_true:
        player_stats = b_data[b_data['player_id'] == pID]

        player_stats = pd.DataFrame({
            #last_name,first_name,player_id,year,b_ab,batting_avg,slg_percent,on_base_percent,xba,xslg,xwoba,xobp,xiso,xwobacon,xbacon,exit_velocity_avg,launch_angle_avg,barrel_batted_rate,hard_hit_percent
            'last_name': [lastName],
            'first_name': [firstName],
            'player_id': [player_stats['player_id'].iloc[0]],
            'year': [player_stats['year'].iloc[0]],
            'b_ab': [player_stats['b_ab'].iloc[0]],
            'batting_avg': [player_stats['batting_avg'].iloc[0]],
            'slg_percent': [player_stats['slg_percent'].iloc[0]],
            'on_base_percent': [player_stats['on_base_percent'].iloc[0]],
            'xba': [player_stats['xba'].iloc[0]],
            'xslg': [player_stats['xslg'].iloc[0]],
            'xwoba': [player_stats['xwoba'].iloc[0]],
            'xobp': [player_stats['xobp'].iloc[0]],
            'xiso': [player_stats['xiso'].iloc[0]],
            'xwobacon': [player_stats['xwobacon'].iloc[0]],
            'xbacon': [player_stats['xbacon'].iloc[0]],
            'exit_velocity_avg': [player_stats['exit_velocity_avg'].iloc[0]],
            'launch_angle_avg': [player_stats['launch_angle_avg'].iloc[0]],
            'barrel_batted_rate': [player_stats['barrel_batted_rate'].iloc[0]],
            'hard_hit_percent': [player_stats['hard_hit_percent'].iloc[0]]
        })
       
        # Make predictions for batting stats
        batting_predictions = {}
        for stat, model in batting_models.items():
            X = player_stats.drop(columns=['last_name','first_name',
        'player_id','year', 'batting_avg', 'slg_percent', 'on_base_percent'])
            y_pred = model.predict(X)
            batting_predictions[stat] = float(y_pred[0])

        # Send back the predictions for batting stats
        return jsonify(batting_predictions)
    
    else:
        #last_name,first_name,player_id,year,p_era,p_opp_batting_avg,xba,xslg,woba,xwoba,xobp,xiso,exit_velocity_avg,launch_angle_avg,sweet_spot_percent,barrel_batted_rate,groundballs_percent,flyballs_percent,linedrives_percent
        player_stats = p_data[p_data['player_id'] == pID]
        player_stats = pd.DataFrame({
            'last_name': [lastName],
            'first_name': [firstName],
            'player_id': [player_stats['player_id'].iloc[0]],
            'year': [player_stats['year'].iloc[0]],
            'p_era': [player_stats['p_era'].iloc[0]],
            'p_opp_batting_avg': [player_stats['p_opp_batting_avg'].iloc[0]],
            'xba': [player_stats['xba'].iloc[0]],
            'xslg': [player_stats['xslg'].iloc[0]],
            'woba': [player_stats['woba'].iloc[0]],
            'xwoba': [player_stats['xwoba'].iloc[0]],
            'xobp': [player_stats['xobp'].iloc[0]],
            'xiso': [player_stats['xiso'].iloc[0]],
            'exit_velocity_avg': [player_stats['exit_velocity_avg'].iloc[0]],
            'launch_angle_avg': [player_stats['launch_angle_avg'].iloc[0]],
            'sweet_spot_percent': [player_stats['sweet_spot_percent'].iloc[0]],
            'barrel_batted_rate': [player_stats['barrel_batted_rate'].iloc[0]],
            'groundballs_percent': [player_stats['groundballs_percent'].iloc[0]],
            'flyballs_percent': [player_stats['flyballs_percent'].iloc[0]],
            'linedrives_percent': [player_stats['linedrives_percent'].iloc[0]]

        })

        # Make predictions for pitching stats
        pitching_predictions = {}
        
        for stat, model in pitching_models.items():
            X = player_stats.drop(columns=['last_name', 'first_name', 'player_id', 'year', 'p_era', 'p_opp_batting_avg', 'woba'])
            y_pred = model.predict(X)
            pitching_predictions[stat] = float(y_pred[0])

        # Send back the predictions for pitching stats
        return jsonify(pitching_predictions)


if __name__ == '__main__':
    app.run(debug=True)


