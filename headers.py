import pandas as pd
import re

class Date(object):

    def __init__(self, user_input):
        self.day = int(user_input["day"])
        self.month = int(user_input["month"])
        self.year = int(user_input["year"])
        self.start = int(re.match("(\d\d?):(\d\d)", user_input["start"]).groups()[0]) + int(re.match("(\d\d?):(\d\d)", user_input["start"]).groups()[1])/60
        self.end = int(re.match("(\d\d?):(\d\d)", user_input["end"]).groups()[0]) + int(re.match("(\d\d?):(\d\d)", user_input["end"]).groups()[1])/60
        self.offset = int(user_input["offset"])/60

class Statistics():
    
    def __init__(self, local_time, users, weight):
        self.local_time = local_time
        self.users = users
        self.weight = weight
        self.timezones = list()

    def __repr__(self):
        
        hour = int(self.local_time - self.local_time % 1)
        minute = int(self.local_time % 1*60) if (self.local_time % 1) * 60 > 10 else f"0{int(self.local_time % 1*60)}"
        
        self.timezone_breakdown = ""
        for timezone in self.timezones:
            self.timezone_breakdown = f"{self.timezone_breakdown}\n{timezone['timezone']} - Users: {timezone['users']}, Weight: {timezone['weight']}"

        return f"\nThe total number of available users at {hour}:{minute} is {self.users} with a total weight of {self.weight}.\nBreakdown of inputted timezones at this time:\n{self.timezone_breakdown}\n"
    
    def addTimezone(self, timezone, users, weight):
        self.timezones.append({"timezone": timezone, "users": users, "weight": weight})

    def changeSum(self, users, weight):
        self.users = self.users + users
        self.weight = self.weight + weight


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