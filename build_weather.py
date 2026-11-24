import pandas as pd
import xarray as xr
import glob

pieces = []
for path in sorted(glob.glob("/Users/Manas/Desktop/ITC510/weathercdc/weather_2016_0*/data_0.nc")):
    pieces.append(xr.open_dataset(path).to_dataframe().reset_index())
    print("loaded", path)

weather = pd.concat(pieces)
print(weather.shape)