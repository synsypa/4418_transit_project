import pandas as pd
import numpy as np

# Function to assign 2 hour intervals
def twohour(row):
    if (row['hour'] >= 0 and row['hour'] < 2):
        return 0
    if (row['hour'] >= 2 and row['hour'] < 4):
        return 1
    if (row['hour'] >= 4 and row['hour'] < 6):
        return 2
    if (row['hour'] >= 6 and row['hour'] < 8):
        return 3
    if (row['hour'] >= 8 and row['hour'] < 10):
        return 4
    if (row['hour'] >= 10 and row['hour'] < 12):
        return 5
    if (row['hour'] >= 12 and row['hour'] < 14):
        return 6
    if (row['hour'] >= 14 and row['hour'] < 16):
        return 7
    if (row['hour'] >= 16 and row['hour'] < 18):
        return 8
    if (row['hour'] >= 18 and row['hour'] < 20):
        return 9
    if (row['hour'] >= 20 and row['hour'] < 22):
        return 10
    if (row['hour'] >= 22 and row['hour'] < 24):
        return 11
    return None

# Load Weather Data
w_df = pd.read_csv("april_wu1.csv")

# Fix bad preciptation data
w_df['precipitation_in'] = np.where(w_df['precipitation_in'] < 0, 0, w_df['precipitation_in']) 

# Assign 2 hr intervals
w_df['interval'] = w_df.apply(twohour, axis=1)

# Cut down and collapse dataset by day/interval
w_df = w_df[['day', 'precipitation_in', 'temp_f', 'humidity', 'interval']]

agg_funcs = {'precipitation_in':np.sum, 'temp_f':np.mean, 'humidity':np.mean}
grouped = w_df.groupby(['day', 'interval']).agg(agg_funcs).reset_index()

# Save to pickle
grouped.to_pickle("weather_april.pkl")