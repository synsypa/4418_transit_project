'''
This file loads the model from `model_single.py`
and uses it to predict pickups for a given
2 hours interval and cluster where we don't
have bike stations
'''

import pandas as pd
import numpy as np
import dill

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load Test Data
test_df = pd.read_pickle('to_pred_6_8.pkl')
test_df = test_df[test_df['day'] == 1]
test_df['weekday'] = 1.0

test_clusters = test_df['cluster'].values.tolist()
test_df = test_df[['weekday', 'dist',
                    'temp_f', 'precipitation_in', 'humidity',
                    'log_taxi']]

# Load Model
rf_mod = dill.load(open('rf_pipe_6_8', 'rb'))

# Prediction
result = rf_mod.predict(test_df)
preds = [np.exp(i)+1 for i in result.tolist()]
clu_pred = list(zip(test_clusters, preds))

with open("predictions_6_8.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(clu_pred)