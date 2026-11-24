import cdsapi

client = cdsapi.Client()

request = {
    "variable": [
        "2m_temperature",
        "total_precipitation",
        "snowfall",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
    ],
    "year": ["2016"],
    "month": ["05"],
    "day": [str(d).zfill(2) for d in range(1, 32)],
    "time": [str(h).zfill(2) + ":00" for h in range(24)],
    "area": [41.0, -74.3, 40.4, -73.6],
    "data_format": "netcdf",
    "download_format": "unarchived",
}

client.retrieve("reanalysis-era5-land", request).download("weather_2016_05.nc")
print("Done")