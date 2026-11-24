import xarray as xr

# April, from the extracted folder
w = xr.open_dataset("/Users/Manas/Desktop/ITC510/weathercdc/weather_2016_04/data_0.nc")
df = w.to_dataframe().reset_index()

print(df.shape)       # expect (40320, ...)
print(df.columns)
print(df.head())

# May, only if `file` said it's a real NetCDF
w5 = xr.open_dataset("/Users/Manas/Desktop/ITC510/weathercdc/weather_2016_05.nc")
print(w5)