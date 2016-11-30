import csv
import sqlite3
import pandas as pd

# tables in taxi.sqlite created prior using Sqlite3 CLI

with open('yellow_tripdata_2015-04.csv') as f, sqlite3.connect('taxi.sqlite') as cnx:
    reader = csv.reader(f)
    next(reader) # Skip header
    c = cnx.cursor()
    c.executemany('insert into yellow values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', reader)

c.close()

with open('green_tripdata_2015-04.csv') as f, sqlite3.connect('taxi.sqlite') as cnx:
    reader = csv.reader(f)
    next(reader) # Skip header
    c = cnx.cursor()
    c.executemany('insert into green values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', reader)

c.close()