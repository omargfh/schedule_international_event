import pandas as pd
import re

class Time(object):

    def __init__(self, *args):

        if len(args) == 2:
            self.hour, self.minute = args[0], args[1]
        elif len(args) == 1:
            if type(args[0]) == type(""):
                self.hour = int(re.match("(\d\d?):(\d\d)", args[0]).groups()[0])
                self.minute = int(re.match("(\d\d?):(\d\d)", args[0]).groups()[1])
            elif type(args[0]) == type(0) or type(args[0]) == type(0.0):
                self.hour = args[0] - (args[0] % 1)
                self.minute = (args[0] % 1) * 60

        self.floatminute = self.minute/60

        self.value = self.hour + self.floatminute

        self.formatted = f"{int(self.hour)}:" + str(int(self.minute)) if self.minute > 10 else f"{int(self.hour)}:0{int(self.minute)}"

class InputParser(object):

    def __init__(self, user_input):

        self.day = int(user_input["day"])
        self.month = int(user_input["month"])
        self.year = int(user_input["year"])
        self.start = Time(user_input["start"]).value
        self.end = Time(user_input["end"]).value
        self.offset = int(user_input["offset"])/60
        self.users = 0
        
        for country, users in user_input["entries"].items():
            self.users = self.users + users

class Statistics():
    
    def __init__(self, local_time, users, weight, MAX_USERS):
        self.local_time = local_time
        self.users = users
        self.weight = weight
        self.timezones = dict()
        self.MAX_USERS = MAX_USERS

    def __repr__(self):
        
        self.timezone_breakdown = ""
        for timezone_value, timezone  in self.timezones.items():
            self.timezone_breakdown = f"{self.timezone_breakdown}\n{timezone_value} - Users: {timezone['users']}, Weight: {timezone['weight']} - Local Time: {timezone['local-time']}, {'Preferrable' if timezone['preferrable'] else 'Not Preferable'}"

        return f"\nThe total number of available users at {Time(float(self.local_time)).formatted} is {self.users} out of {self.MAX_USERS} users with a total weight of {self.weight}.\nBreakdown of inputted timezones at this time:\n{self.timezone_breakdown}\n"
    
    def addTimezone(self, timezone, users, weight, loc_t, isPreferrable):
        if timezone in self.timezones.keys():
            self.timezones[timezone] = {"users":  self.timezones[timezone]["users"] + users, "weight": self.timezones[timezone]["weight"] + weight}
        else:
            self.timezones[timezone] = {"users": users, "weight": weight, "local-time": Time(loc_t).formatted, "preferrable": isPreferrable}

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