import datetime

import numpy as np
import pandas as pd

from pycountry import countries

from external import user_input, user_input_cities
from cities import cities, strict_countries

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

    global timezones; timezones = dict()
    for key, value in user_input["entries"].items():
        if user_input["type"] == "countries":
            exec(f"global alpha; alpha = countries.get({user_input['format']}=key).alpha_2")
            timezone = cities.loc[cities['country_code'] == alpha]["timezone"].tolist()[0] if alpha not in [country_code for country_code, value in strict_countries.items()] else strict_countries[alpha]
        elif user_input["type"] == "cities":
            timezone = cities.loc[cities["city"] == key]["timezone"].tolist()[0]
        timezones[timezone] = timezones[timezone] + value if timezone in timezones.keys() else value