import cdsapi

client = cdsapi.Client()

for year in range(2016, 2020):
    for month in range(1, 13):
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
            "month": [str(month).zfill(2)],
            "day": [str(d).zfill(2) for d in range(1, 32)],
            "time": [str(h).zfill(2) + ":00" for h in range(24)],
            "area": [41.0, -74.3, 40.4, -73.6],
            "data_format": "netcdf",
            "download_format": "unarchived",
        }
        filename = "weather_" + str(year) + "_" + str(month).zfill(2) + ".nc"
        client.retrieve("reanalysis-era5-land", request).download(filename)
        print("Done", filename)