# 4418_transit_project
Project for IEOR 4418 Transportation Analytics

## Scripts for pulling and processing data for Citibike Project
`weather_scrape.py`: Collects hourly weather data for April 2015 for NYC using the Weather Underground API

`load_taxi.py`: Loads .csv files of NYC taxi pickups/dropoffs for April 2015 in SQLite database. (Table Schemas pre-defined in SQLite CLI)

`taxi_clusters.py`: Use K-means clustering to divide city into demand areas. Assume a single pickup is representative of some set transit demand features, then a cluster denotes an "organic" area of demand. Produces a dataset of Cluster, Centroid (Location only) (k=45)

`process_single_taxi.py`: Processes single interval (12AM-2AM) of taxi pickups in April. Assigns cluster to each pickup and aggregates on day and cluster. Final Dataframe is [day, cluster, total passengers, average trip distance]

`process_taxi.py`: Same as single taxi for all 2 hr intervals.

`process_weather.py`: Condenses weather data into 2 hour intervals. Output Dataframe is [day, interval, temp_f, humidity, precipitation_in] 

`process_bike.py`: Merges Bike Station location with demand datat and assigns cluster. Output Dataframe is [day, interval, cluster, pickups, weekday/end] 

`cut_for_csv.py`: Create .csv files of pickup locations for use in CARTO maps.

`model_single.py`: Fits a Random Forest, Lasso, and Linear regression to given time interval. Applies Random Forest model to the test point.

`predict_pickups.py`: Takes dilled models from `model_single.py` and uses them to predict pickups in clusters without any bike stations. outputs to csv

`venv/dbscan.clu.py`: NOT IN USE. Implements DBSCAN clustering on taxi pickups using Virtual Env and sklearn version 0.15.2's implementation. Incomplete, not working.

https://kjiang.carto.com/viz/3184256e-b857-11e6-aa3b-0ee66e2c9693/public_map

## Model (Subject to Change)
For each 2 hour segment:
Citibike Pickups = B\_1\*Temperature + B\_2\*Precipitation + B\_3\*Humidity + B\_4\*Weekend + B\_5\*Taxi Demand