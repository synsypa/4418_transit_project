'''
Use K-Means Clustering (k=45) on Taxi Pickup Locations
To create demand areas for analysis.
Outputs cluster ID and Lat/Lon of Center
'''

import sqlite3
import pandas as pd
import numpy as np
import csv
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Pull data from sqlite
con = sqlite3.connect('taxi.sqlite')
query = """
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM yellow
        WHERE date(p_datetime) == date('2015-04-15')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        UNION ALL
        SELECT p_datetime, p_long as lon, p_lat as lat, num_pass, dist
        FROM green
        WHERE date(p_datetime) == date('2015-04-15')
        AND lon <= -73.89 AND lon >= -74.02
        AND lat <= 40.84 AND lat >= 40.70
        AND dist < 10
        AND num_pass < 3
        """
df = pd.read_sql_query(query, con)
con.close()

# Pickle Dataframe for faster access
df.to_pickle("taxi_data.pkl")

# Cluster on lat/lon
cl_df = df[['lon', 'lat']]

# Find good k using silhouette score
#k_range = range(20,50)

#for k in k_range:
#    km_checks = KMeans(n_clusters = k, init='k-means++', n_jobs=2)
#    cluster_lab = km_checks.fit_predict(cl_df)
#    silhouette_avg = silhouette_score(cl_df, cluster_lab, sample_size=1000)
#    print("For n_clusters =", k,
#          "The average silhouette_score is :", silhouette_avg)

# Cluster and create dataset of center of each cluster
km = KMeans(n_clusters = 45, init='k-means++', n_jobs=2)
clusters = km.fit(cl_df) 
np.savetxt('cluster_centers.csv', clusters.cluster_centers_, delimiter=",")