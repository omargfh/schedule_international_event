import pandas as pd

data = pd.read_csv("geolite2-city-ipv4.csv", dtype={
    "ip_range_start":"string",
    "ip_range_end":"string",
    "country_code":"string",
    "state1":"string",
    "state2":"string",
    "postcode":"string",
    "city":"string",
    "latitude":"string",
    "longitude":"string",
    "timezone":"string"
})
data = data.drop(["ip_range_start","ip_range_end","state1","state2","postcode","latitude","longitude"], axis=1)
data.dropna(subset = ["city"], inplace=True)
data.drop_duplicates(subset=["city"], inplace=True)
data.sort_values(by=['country_code'], inplace=True)
data.to_csv("geolite-2-city-updated-NaN.csv", index=False)
