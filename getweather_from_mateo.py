import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "start_date": "2016-01-01",
    "end_date": "2019-12-31",
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
             "precipitation_sum,rain_sum,snowfall_sum,"
             "wind_speed_10m_max,wind_gusts_10m_max",
    "timezone": "America/New_York",
}

data = requests.get(url, params=params).json()
weather = pd.DataFrame(data["daily"])
print(weather.shape)
print(weather.head())

weather.to_csv("/Users/Manas/Desktop/ITC510/openmeteo_daily.csv", index=False)