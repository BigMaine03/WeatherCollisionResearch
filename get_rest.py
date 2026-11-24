import cdsapi
import os

client = cdsapi.Client()
folder = "/Users/Manas/Desktop/ITC510/weathercdc/"

YEARS = [2016]   # start with just 2016, add 2017, 2018, 2019 later

for year in YEARS:
    for month in range(1, 13):
        filename = folder + "weather_" + str(year) + "_" + str(month).zfill(2) + ".nc"

        # skip months we already downloaded
        if os.path.exists(filename) and os.path.getsize(filename) > 100000:
            print("Skipping", filename)
            continue

        request = {
            "variable": [
                "2m_temperature",
                "total_precipitation",
                "snowfall",
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
        try:
            client.retrieve("reanalysis-era5-land", request).download(filename)
            print("Done", filename)
        except Exception as e:
            print("FAILED", filename, e)