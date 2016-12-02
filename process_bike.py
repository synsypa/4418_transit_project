import pandas as pd
import numpy as np
from geopy.distance import great_circle

# Load bike pickup and station location data
bike_pd = pd.read_csv('citibike_reform_201504.csv')
station_loc = pd.read_csv('citibike_station.csv')

# Merge station locations
bike_df = bike_pd.merge(station_loc, on='station id')

# 0 index intervals, consistent column names
bike_df['interval'] = bike_df['interval']-1
bike_df=bike_df.rename(columns = {'date':'day'})

# Assign Cluster
def assign_clu(row):
    dists = [great_circle([row['lat'], row['lon']], clu).km for clu in clu_list]
    return dists.index(min(dists))

## Load Cluster Centroids
clus = pd.read_csv('cluster_centers.csv', names=['lon', 'lat'])
clus = clus[['lat', 'lon']]
clu_list = clus.values.tolist()

bike_df['cluster'] = bike_df.apply(assign_clu, axis=1)

# Groupby day/interval
agg_funcs = {'pick':np.sum, 'drop':np.sum, 'weekday':np.mean}
grouped = bike_df.groupby(['day', 'interval', 'cluster']).agg(agg_funcs).reset_index()
grouped.to_pickle("bikes_april.pkl")