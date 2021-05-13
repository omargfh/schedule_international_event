from datetime import datetime
import time
import pytz

import numpy as np
import pandas as pd
import re as re

from pycountry import countries
from tzlocal import get_localzone

from external import user_input, user_input_cities
from headers import cities, strict_countries, Date, Statistics

def validate_user_input(user_input):

    labels = [label.lower() for label in user_input["entries"]]
    if user_input["type"] == "countries":
        if user_input["format"] in ["name", "alpha_2", "alpha_3", "official_name"]:
            exec(f"global valid_entries; valid_entries = [country.{user_input['format']}.lower() for country in countries];")
        else:
            raise Exception("Illegal input: ISO country name format. Abort.")
    elif user_input["type"] == "cities":
        global valid_entries; valid_entries = [city.lower() for city in cities["city"].to_list()]
    if not all(item in valid_entries for item in labels):
        errors = ', '.join([labels[i].capitalize() for i, error in enumerate(np.in1d(labels, valid_entries)) if error == False])
        raise Exception(f"Errors detected in the values: ({errors}). Country names does not follow the ISO 3166 standard for the given format: {user_input['format']}.")

def collect_timezones(user_input):

    timezones = dict()
    for key, value in user_input["entries"].items():
        if user_input["type"] == "countries":
            exec(f"global alpha; alpha = countries.get({user_input['format']}=key).alpha_2")
            timezone = cities.loc[cities['country_code'] == alpha]["timezone"].tolist()[0] if alpha not in [country_code for country_code, value in strict_countries.items()] else strict_countries[alpha]
        elif user_input["type"] == "cities":
            timezone = cities.loc[cities["city"] == key]["timezone"].tolist()[0]
        timezones[timezone] = timezones[timezone] + value if timezone in timezones.keys() else value
        timezones[timezone] > 0 or timezones.pop(timezone, None)
    return timezones

timezones = collect_timezones(user_input_cities) # TODO: delete

def calculate_time_weight(user_input, timezones):

    timezone_obj = dict()
    for key, value in timezones.items():
        timezone_obj[pytz.timezone(key)] = value
    
    t, time_list = Date(user_input), list()
    local_tz = pytz.timezone(user_input["local_timezone"]) if user_input["local_timezone"] else get_localzone()
    for i in list(np.arange(t.start, t.end + 0.001, t.offset)):
        hour, minute = int(i) if i % 1 == 0 else int(i - i % 1), int(i % 1 * 60)
        ls = Statistics(i, 0, 0)
        for timezone, users in timezone_obj.items():
            loc = local_tz.localize(datetime(t.year, t.month, t.day, hour, minute, 0)).astimezone(timezone)
            loc_t = int(loc.strftime("%H")) + ( int(loc.strftime("%M")) ) / 60
            if loc_t >= t.start and loc_t <= t.end:
                weight = 100 if users < 10 else users * 10
                ls.addTimezone(timezone, users, weight)
                ls.changeSum(users, weight)
            else:
                ls.addTimezone(timezone, 0, 0)
        time_list.append(ls)
    
    return sorted(time_list, key=lambda k:k.users, reverse=True)

time_list = calculate_time_weight(user_input_cities, timezones) # TODO: delete
print(f'{[item.users for item in time_list]}\n{[item.weight for item in time_list]}')
print(time_list)