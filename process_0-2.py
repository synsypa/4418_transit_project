import sqlite3
import pandas as pd
import numpy as np
import csv
from geopy.distance import great_circle

# Load cluster centroids
clus = pd.read_csv('cluster_centers.csv', names=['lon', 'lat'])
clu_list = clus.values.tolist()

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
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('00:00:00')
        AND time(p_datetime) < time('02:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        """
df = pd.read_sql_query(query, con)

# Function for finding nearest cluster
def assign_clu(row):
    dists = [great_circle([row['lon'], row['lat']], clu).miles for clu in clu_list]
    return dists.index(min(dists))

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)