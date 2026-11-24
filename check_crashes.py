import pandas as pd

crashes = pd.read_csv("/Users/Manas/Desktop/ITC510/nyc_crashes_2012_2020.csv", low_memory=False)
print(crashes.shape)
print(crashes.columns)
print(crashes[["crash_date", "crash_time", "latitude", "longitude"]].head())