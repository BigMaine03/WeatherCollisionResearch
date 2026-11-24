import pandas as pd
import xarray as xr
import numpy as np
import glob
import zipfile

folder = "/Users/Manas/Desktop/ITC510/weathercdc/"

# ---------- 1. WEATHER ----------
pieces = []
for path in sorted(glob.glob(folder + "weather_*.nc")):
    if zipfile.is_zipfile(path):
        file = path.replace(".nc", "") + "/data_0.nc"   # unzipped months
    else:
        file = path                                      # plain NetCDF months
    pieces.append(xr.open_dataset(file).to_dataframe().reset_index())
    print("loaded", file)

weather = pd.concat(pieces)
weather = weather.sort_values(["latitude", "longitude", "valid_time"]).reset_index(drop=True)

# Units
weather["temp_c"] = weather["t2m"] - 273.15
weather["wind_speed"] = np.sqrt(weather["u10"] ** 2 + weather["v10"] ** 2)

# Precipitation and snowfall are running totals that reset each day.
# Hour 01 holds the first hour's amount; every other hour = this total minus the last one.
hour = weather["valid_time"].dt.hour
for col in ["tp", "sf"]:
    hourly = weather.groupby(["latitude", "longitude"])[col].diff()
    hourly[hour == 1] = weather.loc[hour == 1, col]
    weather[col + "_mm"] = hourly.clip(lower=0) * 1000   # meters -> mm

# Round the grid coordinates so they match cleanly later
weather["lat_r"] = weather["latitude"].round(1)
weather["lon_r"] = weather["longitude"].round(1)
weather = weather[["valid_time", "lat_r", "lon_r", "temp_c", "wind_speed", "tp_mm", "sf_mm"]]

print("Weather range:", weather["valid_time"].min(), "to", weather["valid_time"].max())

city = weather.groupby("valid_time")[["temp_c", "wind_speed", "tp_mm", "sf_mm"]].mean().reset_index()
city.to_csv("/Users/Manas/Desktop/ITC510/weather_hourly.csv", index=False)

# ---------- 2. CRASHES ----------
crashes = pd.read_csv("/Users/Manas/Desktop/ITC510/nyc_crashes_2012_2020.csv", low_memory=False)
crashes = crashes[crashes["crash_date"] >= "2016-01-01"]   # only years we have weather for

for col in ["latitude", "longitude", "number_of_persons_injured", "number_of_persons_killed"]:
    crashes[col] = pd.to_numeric(crashes[col], errors="coerce")

crashes = crashes.dropna(subset=["latitude", "longitude"])
crashes = crashes[crashes["latitude"].between(40.4, 41.0)]
crashes = crashes[crashes["longitude"].between(-74.3, -73.6)]

# Local NYC time -> UTC (weather is in UTC), then round down to the hour
crashes["datetime"] = pd.to_datetime(crashes["crash_date"].str[:10] + " " + crashes["crash_time"], errors="coerce")
crashes["datetime"] = (crashes["datetime"]
                       .dt.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT")
                       .dt.tz_convert("UTC")
                       .dt.tz_localize(None))
crashes = crashes.dropna(subset=["datetime"])
crashes["hour_utc"] = crashes["datetime"].dt.floor("h")

# Nearest weather grid cell (the grid is every 0.1 degrees)
crashes["lat_r"] = crashes["latitude"].round(1)
crashes["lon_r"] = crashes["longitude"].round(1)

# Keep only crashes inside the weather time range
crashes = crashes[crashes["hour_utc"].between(weather["valid_time"].min(), weather["valid_time"].max())]
print("Crashes in weather range:", len(crashes))

# ---------- 3. MERGE ----------
merged = crashes.merge(weather,
                       left_on=["hour_utc", "lat_r", "lon_r"],
                       right_on=["valid_time", "lat_r", "lon_r"],
                       how="left")

print(merged.shape)
print("Crashes with no weather match:", merged["temp_c"].isna().sum())
print(merged[["datetime", "latitude", "longitude", "temp_c", "wind_speed", "tp_mm", "sf_mm",
              "number_of_persons_injured"]].head())
print(merged[["temp_c", "wind_speed", "tp_mm", "sf_mm"]].describe())

merged.to_csv("/Users/Manas/Desktop/ITC510/merged.csv", index=False)