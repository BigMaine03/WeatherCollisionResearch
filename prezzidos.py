import numpy as np
import pandas as pd
import requests
from importlib import import_module

'''# going to use an api call to fetch data cause its too big of a csv file 
#gonna pull data from the nyc open data api for motor vehicle collisions'''

url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"
#datasets ID is h9gi-nx95, and the data is from 2012-2020, so we will filter for that
where = "crash_date between '2012-07-01T00:00:00' and '2020-12-31T23:59:59'"

pieces = []
offset = 0

while True:
    #talking to the api via sql-like query parameters, we will fetch 50k rows at a time until we get all the data
    #We need a loop because the server won't send 1.7 million rows at once.
    params = {"$where": where, "$limit": 50000, "$offset": offset, "$order": "crash_date"}
    data = requests.get(url, params=params).json()
    if len(data) == 0:
        break
    pieces.append(pd.DataFrame(data))
    #Turns this batch into a pandas table and adds it to the pieces list.
    offset = offset + 50000
    print("Fetched", offset, "rows")

crashes = pd.concat(pieces)





'''#going to pull data from cds for weather data'''
import cdsapi

client = cdsapi.Client()

for year in range(2012, 2021):
    request = {
        "variable": [
            "2m_temperature",
            "total_precipitation",
            "snowfall",
            "snow_depth",
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
        ],
        "year": [str(year)],
        "month": [str(m).zfill(2) for m in range(1, 13)],
        "day": [str(d).zfill(2) for d in range(1, 32)],
        "time": [str(h).zfill(2) + ":00" for h in range(24)],
        "area": [41.0, -74.3, 40.4, -73.6],
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    client.retrieve("reanalysis-era5-land", request).download("weather_" + str(year) + ".nc")
    print("Done", year)
#cleaning the data:
# Turn text columns into numbers
for col in ["latitude", "longitude", "number_of_persons_injured", "number_of_persons_killed"]:
    crashes[col] = pd.to_numeric(crashes[col])

# Build one datetime column, rounded down to the hour
crashes["datetime"] = pd.to_datetime(crashes["crash_date"].str[:10] + " " + crashes["crash_time"])
crashes["hour"] = crashes["datetime"].dt.floor("h")

# Drop rows with no location, and bad locations outside NYC
crashes = crashes.dropna(subset=["latitude", "longitude", "hour"])
crashes = crashes[crashes["latitude"].between(40.4, 41.0)]
crashes = crashes[crashes["longitude"].between(-74.3, -73.6)]

print(len(crashes), "crashes kept")


'''need to install a reader for the netcdf files, gonna use xarray'''
#installed using pip install xarray netcdf4


import xarray as xr
weather = xr.open_dataset("/Users/Manas/Desktop/weatherdoc/weather_2016_01.nc")
print(weather)