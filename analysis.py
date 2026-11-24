import pandas as pd
import matplotlib.pyplot as plt

folder = "/Users/Manas/Desktop/ITC510/"

# ---------- 1. WEATHER ----------
weather = pd.read_csv(folder + "openmeteo_daily.csv")
weather["date"] = pd.to_datetime(weather["time"])
weather = weather.set_index("date")

# ---------- 2. CRASHES (all crashes, no coordinates needed) ----------
crashes = pd.read_csv(folder + "nyc_crashes_2012_2020.csv", low_memory=False,
                      usecols=["crash_date", "number_of_persons_injured", "number_of_persons_killed"])
crashes["date"] = pd.to_datetime(crashes["crash_date"].str[:10])
crashes = crashes[(crashes["date"] >= "2016-01-01") & (crashes["date"] <= "2019-12-31")]
for col in ["number_of_persons_injured", "number_of_persons_killed"]:
    crashes[col] = pd.to_numeric(crashes[col], errors="coerce")

crash_daily = crashes.groupby("date").agg(
    crashes=("date", "count"),
    injured=("number_of_persons_injured", "sum"),
    killed=("number_of_persons_killed", "sum"),
)

# ---------- 3. MERGE: one row per day ----------
df = weather.join(crash_daily, how="inner")
print(df.shape)
print(df.head())
df.to_csv(folder + "daily_merged.csv")

# ---------- 4. WEATHER FLAGS ----------
df["rain"] = df["rain_sum"] >= 1                   # at least 1 mm of rain
df["snow"] = df["snowfall_sum"] >= 1               # at least 1 cm of snow
df["freezing"] = df["temperature_2m_min"] <= 0
df["hot"] = df["temperature_2m_max"] >= 30
df["windy"] = df["wind_speed_10m_max"] >= df["wind_speed_10m_max"].quantile(0.90)
df["clear"] = ~(df["rain"] | df["snow"])

# ---------- 5. COMPARE ----------
rows = [{
    "condition": "all days",
    "days": len(df),
    "crashes_per_day": df["crashes"].mean(),
    "injured_per_day": df["injured"].mean(),
    "killed_per_day": df["killed"].mean(),
    "injuries_per_crash": df["injured"].sum() / df["crashes"].sum(),
}]
for f in ["rain", "snow", "freezing", "hot", "windy", "clear"]:
    d = df[df[f]]
    rows.append({
        "condition": f,
        "days": len(d),
        "crashes_per_day": d["crashes"].mean(),
        "injured_per_day": d["injured"].mean(),
        "killed_per_day": d["killed"].mean(),
        "injuries_per_crash": d["injured"].sum() / d["crashes"].sum(),
    })

results = pd.DataFrame(rows).round(2)
print(results)
results.to_csv(folder + "daily_results.csv", index=False)

# ---------- 6. CHART ----------
plt.bar(results["condition"], results["crashes_per_day"])
plt.ylabel("Average crashes per day")
plt.title("Daily crashes by weather condition (NYC, 2016-2019)")
plt.savefig(folder + "daily_crash_rate.png")
plt.show()