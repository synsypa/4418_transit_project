'''
This file takes a .pkl of taxi pickups in 2 hr intervals
and merges them with weather and bike data
Fits Random Forest, Lasso, and Linear Regression Model
Reports Adjusted R^2 and RMSE of each
'''

import pandas as pd
import numpy as np
import dill

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import r2_score, mean_squared_error

# Load Data
taxi_df = pd.read_pickle("taxi_6_8.pkl")
weather_df = pd.read_pickle("weather_april.pkl")
bike_df = pd.read_pickle("bikes_april.pkl")

# Combine Dataframes
all_df = bike_df.merge(taxi_df, on=['day', 'cluster', 'interval'], how='right')
all_df = all_df.merge(weather_df, on=['day', 'interval'], how='inner')
all_df['log_taxi'] = np.log1p(all_df['num_pass'])
all_df['log_bike'] = np.log1p(all_df['pick'])

# Prep Dataframe for Fitting
df = all_df[['log_bike', 'pick', 'weekday', 
             'temp_f', 'precipitation_in', 'humidity',
             'log_taxi', 'num_pass', 'dist']]

# Drop missing bike pickups 
df = df[np.isnan(df['pick'])!=1]

# Plots
#f1 = df.plot(x="log_taxi", y="log_bike", style='o',xlim=(2,9))
#fig1 = f1.get_figure()
#fig1.savefig('logbike_logtaxi.png')

#f2 = df.plot(x="temp_f", y="log_bike", style='o')
#fig2 = f2.get_figure()
#fig2.savefig('logbike_temp.png')

#f3 = df.plot(x="dist", y="log_bike", style='o')
#fig3 = f3.get_figure()
#fig3.savefig('logbike_dist.png')

# Get points with no bike data
test_df = all_df[['day', 'cluster', 'log_bike', 'pick', 'weekday', 
             'temp_f', 'precipitation_in', 'humidity',
             'log_taxi', 'num_pass', 'dist']]
test_df = test_df[np.isnan(test_df['pick'])==1]
test_df.to_pickle('to_pred_6_8.pkl')

# Fitting (use metrics on 5 fold CV)
X_df = df[['weekday', 'dist',
           'temp_f', 'precipitation_in', 'humidity',
           'log_taxi']].values
y_df = df['log_bike'].values

# Divide into 5 folds
kf = KFold(n_splits=5, random_state=322)
kf.get_n_splits(X_df)

# Random Forest Model (Parameters tuned manually)
rf_pipe = Pipeline([
        ('scale', StandardScaler()),
        ('rf', RandomForestRegressor(random_state=322, min_samples_leaf=3))
    ])

aR2 = []
mse = []
for train_index, test_index in kf.split(X_df):
    X_train, X_test = X_df[train_index], X_df[test_index]
    y_train, y_test = y_df[train_index], y_df[test_index]
    model0 = rf_pipe.fit(X_train, y_train)
    y_pred = rf_pipe.predict(X_test)
    aR2.append(1 - float(len(y_test)-1)/(len(y_test)-6-1)*(1 - r2_score(y_test,y_pred)))
    mse.append(np.sqrt(mean_squared_error(y_test, y_pred)))

adj_r2 = sum(aR2)/5
rmse = sum(mse)/5

print('Adjusted R^2 = ' + str(adj_r2))
print('RMSE = ' + str(rmse))

# Dill the Model
rf_pipe.fit(X_df, y_df)
dill.dump(rf_pipe, open('rf_pipe_6_8', 'wb'), recurse=True)

# Lasso CV
lasso_pipe = Pipeline([
        ('scale', StandardScaler()),
        ('lasso', LassoCV(random_state=322))
    ])

aR2 = []
mse = []
for train_index, test_index in kf.split(X_df):
    X_train, X_test = X_df[train_index], X_df[test_index]
    y_train, y_test = y_df[train_index], y_df[test_index]
    model0 = lasso_pipe.fit(X_train, y_train)
    y_pred = lasso_pipe.predict(X_test)
    aR2.append(1 - float(len(y_test)-1)/(len(y_test)-6-1)*(1 - r2_score(y_test,y_pred)))
    mse.append(np.sqrt(mean_squared_error(y_test, y_pred)))

adj_r2 = sum(aR2)/5
rmse = sum(mse)/5

# Linear Regression
lr_pipe = Pipeline([
            ('standard', StandardScaler()),
            ('linreg', LinearRegression())
            ])

aR2 = []
mse = []
for train_index, test_index in kf.split(X_df):
    X_train, X_test = X_df[train_index], X_df[test_index]
    y_train, y_test = y_df[train_index], y_df[test_index]
    model0 = lr_pipe.fit(X_train, y_train)
    y_pred = lr_pipe.predict(X_test)
    aR2.append(1 - float(len(y_test)-1)/(len(y_test)-6-1)*(1 - r2_score(y_test,y_pred)))
    mse.append(np.sqrt(mean_squared_error(y_test, y_pred)))

adj_r2 = sum(aR2)/5
rmse = sum(mse)/5