'''
Assigns each taxi pickup in each 2hr segment to a cluster
Produces ungrouped and grouped by day/cluster
'''

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

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_0_2.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 0

# Save to Pickle for easy access
grouped.to_pickle("taxi_0_2.pkl")

print("done1")

# Load Taxi Pickups for 2AM to 4AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('02:00:00')
        AND time(p_datetime) < time('04:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('02:00:00')
        AND time(p_datetime) < time('04:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_2_4.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 1

# Save to Pickle for easy access
grouped.to_pickle("taxi_2_4.pkl")

print("done2")

# Load Taxi Pickups for 4AM to 6AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('04:00:00')
        AND time(p_datetime) < time('06:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('04:00:00')
        AND time(p_datetime) < time('06:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_4_6.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 2

# Save to Pickle for easy access
grouped.to_pickle("taxi_4_6.pkl")

print("done3")

# Load Taxi Pickups for 6AM to 8AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('06:00:00')
        AND time(p_datetime) < time('08:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('06:00:00')
        AND time(p_datetime) < time('08:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_6_8.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 3

# Save to Pickle for easy access
grouped.to_pickle("taxi_6_8.pkl")

print("done4")

# Load Taxi Pickups for 8AM to 10AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('08:00:00')
        AND time(p_datetime) < time('10:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('08:00:00')
        AND time(p_datetime) < time('10:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_8_10.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 4

# Save to Pickle for easy access
grouped.to_pickle("taxi_8_10.pkl")

print("done5")

# Load Taxi Pickups for 10AM to 12PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('10:00:00')
        AND time(p_datetime) < time('12:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('10:00:00')
        AND time(p_datetime) < time('12:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_10_12.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 5

# Save to Pickle for easy access
grouped.to_pickle("taxi_10_12.pkl")

print("done6")

# Load Taxi Pickups for 12PM to 2PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('12:00:00')
        AND time(p_datetime) < time('14:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('12:00:00')
        AND time(p_datetime) < time('14:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_12_14.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 6

# Save to Pickle for easy access
grouped.to_pickle("taxi_12_14.pkl")

print("done7")

# Load Taxi Pickups for 2PM to 4PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('14:00:00')
        AND time(p_datetime) < time('16:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('14:00:00')
        AND time(p_datetime) < time('16:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_14_16.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 7

# Save to Pickle for easy access
grouped.to_pickle("taxi_14_16.pkl")

print("done8")

# Load Taxi Pickups for 4PM to 6PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('16:00:00')
        AND time(p_datetime) < time('18:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('16:00:00')
        AND time(p_datetime) < time('18:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_16_18.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 8

# Save to Pickle for easy access
grouped.to_pickle("taxi_16_18.pkl")

print("done9")

# Load Taxi Pickups for 6PM to 8PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('18:00:00')
        AND time(p_datetime) < time('20:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('18:00:00')
        AND time(p_datetime) < time('20:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_18_20.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 9

# Save to Pickle for easy access
grouped.to_pickle("taxi_18_20.pkl")

print("done10")

# Load Taxi Pickups for 8PM to 10PM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('20:00:00')
        AND time(p_datetime) < time('22:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('20:00:00')
        AND time(p_datetime) < time('22:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_20_22.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 10

# Save to Pickle for easy access
grouped.to_pickle("taxi_20_22.pkl")

print("done11")

# Load Taxi Pickups for 10PM to 12AM
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE time(p_datetime) >= time('22:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE time(p_datetime) >= time('22:00:00')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)

# Get Day vars
df['day'] = pd.to_datetime(df['p_datetime'], format='%Y-%m-%d %H:%M:%S').dt.day

# Assign Clusters
df['cluster'] = df.apply(assign_clu, axis=1)

df.to_pickle("ungroup_22_24.pkl")

# Collapse by Cluster
agg_funcs = {'num_pass':np.sum, 'dist':np.mean}
grouped = df.groupby(['day', 'cluster']).agg(agg_funcs).reset_index()
grouped['interval'] = 11

# Save to Pickle for easy access
grouped.to_pickle("taxi_22_24.pkl")

print("done12")