# 4418_transit_project
Project for IEOR 4418 Transportation Analytics

## Scripts for pulling and processing data for Citibike Project
`weather_scrape.py`: Collects hourly weather data for April 2015 for NYC using the Weather Underground API

`taxi_load.py`: Loads .csv files of NYC taxi pickups/dropoffs for April 2015

`taxi_cluster.py`: Use K-means clustering to designate areas of interest, Assume a single pickup is representative of some set transit demand, clusters denote an area of demand. Produces a dataset of Cluster, Centroid (Location only), Pickups in Cluster 

## Model (Subject to Change)
For each 2 hour segment:
Citibike Pickups = B\_1\*Temperature + B\_2\*Precipitation + B\_3\*DayOfWeek + B\_4\*Taxi Demand in Cluster