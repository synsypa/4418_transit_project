'''
This script takes ungrouped taxi and bike pickup locations 
and exports Cluster 3 and Cluster 43 to .csv for use in
CARTO.net maps
'''

import pandas as pd
import csv

# Subset of Taxi Pickups on April 16, 2015 from 8AM - 10AM
df = pd.read_pickle("ungroup_8_10.pkl")

# Cluster 3 (Roughly Koreatown)
df3 = df[df['cluster'] == 3]
df3 = df3[df['day'] == 16]

df3.to_csv("cluster3_0416_taxis.csv")

# Cluster 42 (Roughly Morningside Heights)
df43 = df[df['cluster'] == 42]
df43 = df43[df['day'] == 16]

df43.to_csv("cluster42_0416_taxis.csv")

# Bike Stations in Cluster 3 and 42 (Should be none in 42)
df = pd.read_pickle('ungroup_bike.pkl')

dfb = df[(df['cluster'] == 3) | ((df['cluster'] == 42))]
dfb = dfb[df['day'] == 16]
dfb = dfb[df['interval'] == 4]

dfb[['cluster', 'pick', 'lat', 'lon']].to_csv("bikes_st.csv")