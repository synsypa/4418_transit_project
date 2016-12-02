import sqlite3
import pandas as pd
import numpy as np
import csv
from geopy.distance import great_circle

# Load cluster centroids
clus = pd.read_csv('cluster_centers.csv', names=['lon', 'lat'])
clus = clus[['lat', 'lon']] #Switch to Lat/Lon for Geopy
clu_list = clus.values.tolist()


# Function for finding nearest cluster
def assign_clu(row):
    dists = [great_circle([row['lat'], row['lon']], clu).km for clu in clu_list]
    return dists.index(min(dists))

# Load Taxi Pickups for 12AM to 2AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('00:00:00')
        AND time(p_datetime) < time('02:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('00:00:00')
        AND time(p_datetime) < time('02:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day and Weekday vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day
df['weekend'] = np.where(
                        pd.to_datetime(df['p_datetime'], 
                                        format='%Y-%m-%d %H:%M:%S').dt.weekday <= 5
                , 0, 1)

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean, 'weekend':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()

# Save to Pickle for easy access
grouped.to_pickle("taxi_0_2.pkl")