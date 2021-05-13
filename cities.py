import pandas as pd

cities = pd.read_csv("geolite-2-city-updated-NaN.csv")

strict_countries = {
    "FR":"Europe/Paris",
    "RU":"Europe/Moscow",
    "US":"America/New_York",
    "AQ":"Europe/Berlin",
    "CH":"Asia/Shanghai",
    "AU":"Australia/Sydney",
    "GB":"Europe/London",
    "CA":"America/Toronto",
    "DK":"Europe/Copenhagen",
    "NZ":"Pacific/Auckland",
    "BR":"America/Sao_Paulo",
    "MX":"America/Mexico_City",
    "CL":"America/Santiago",
    "ID":"Asia/Makassar",
    "KI":"Pacific/Tarawa",
    "CD":"Africa/Kinshasa",
    "EC":"America/Guayaquil",
    "FM":"Pacific/Kosrae",
    "MN":"Asia/Ulaanbaatar",
    "PG":"Pacific/Port_Moresby", 
    "PT":"Europe/Lisbon",
    "ZA":"Africa/Johannesburg",
    "ES":"Europe/Madrid",
    "UA":"Europe/Kiev"
}