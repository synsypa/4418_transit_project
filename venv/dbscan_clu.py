import sqlite3
import pandas as pd
import numpy as np
import csv
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

## NOTE: This must be run with sklearn v0.15.2 for a faster implemenation of DBSCAN

# Load from pickle
df = pd.read_pickle("../taxi_data.pkl")

# Get Coordinates
cl_df = df[['lon', 'lat']]
coords = cl_df.as_matrix(columns=['lon', 'lat'])

# Cluster Parameters
mi_rad = 3958.76133381 # Miles per Radian on Earth
epsilon = 5 / mi_rad # Min Distance between Points

db = DBSCAN(eps=epsilon, min_samples=6, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

cl_labels = db.labels_
num_clusters = len(set(cl_labels))
clusters = pd.Series([coords[cl_labels == n] for n in range(num_clusters)])
print('Number of clusters: {}'.format(num_clusters))

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)
centermost_points = clusters.map(get_centermost_point)

lats, lons = zip(*centermost_points)
rep_points = pd.DataFrame({'lon':lons, 'lat':lats})

rep_points.to_csv("db_clusters.csv")