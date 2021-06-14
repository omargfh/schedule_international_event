from datetime import datetime
import time
import pytz

import numpy as np
import pandas as pd
import re

import matplotlib.pyplot as plt

from PIL import Image, ImageDraw, ImageFont, ImageOps
from pycountry import countries
from tzlocal import get_localzone

from models.input import user_input, user_input_cities
from models.headers import Statistics, cities, strict_countries, InputParser, TimezoneBreakdown, Time, get_concat_h, get_concat_v

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

def calculate_weight(loc_t, c_weight, pref_start, pref_end, users, returnPref=False):
    score, pref = 4, False
    country_weight = 0 if c_weight is None else c_weight
    weight = country_weight if users * 10 < country_weight else users * score
    if pref_start == None or pref_start == 0:
        weight = weight + (users * score)
    elif Time(pref_start).value <= loc_t and Time(pref_end).value >= loc_t:
        weight = weight + (users * (score + 1))
        pref = True
    
    if returnPref:
        return pref
    else:
        return weight if not weight == None else 0


def calculate_time_weight(user_input, timezones):

    timezone_obj = dict()
    for key, value in timezones.items():
        timezone_obj[pytz.timezone(key)] = value
    
    t, time_list = InputParser(user_input), list()
    local_tz = pytz.timezone(user_input["local_timezone"]) if user_input["local_timezone"] else get_localzone()
    for i in list(np.arange(t.start, t.end + 0.001, t.offset)):
        hour, minute = int(i) if i % 1 == 0 else int(i - i % 1), int(i % 1 * 60)
        ls = TimezoneBreakdown(i, 0, 0, t.users)
        for timezone, users in timezone_obj.items():
            loc = local_tz.localize(datetime(t.year, t.month, t.day, hour, minute, 0)).astimezone(timezone)
            loc_t = int(loc.strftime("%H")) + ( int(loc.strftime("%M")) ) / 60
            if loc_t >= t.start and loc_t <= t.end:
                weight = calculate_weight(loc_t, user_input["country-weight"], user_input["preferrable-start"], user_input["preferrable-end"], users)
                isPreferrable = calculate_weight(loc_t, user_input["country-weight"], user_input["preferrable-start"], user_input["preferrable-end"], users, True)
                ls.addTimezone(timezone, users, weight, loc_t, isPreferrable)
                ls.changeSum(users, weight)
            else:
                ls.addTimezone(timezone, 0, 0, loc_t, False)
        time_list.append(ls)
    
    return sorted(time_list, key=lambda k:k.users, reverse=True)


def group_data(time_list):

    data = Statistics(time_list[0].MAX_USERS)
    for timezone_breakdown in time_list:
        loc_t = Time(float(timezone_breakdown.local_time)).value
        data.addTime(loc_t, timezone_breakdown.users, timezone_breakdown.weight)
    
    data.organize_data()
    return data

def output_data(data, output_id):

    # Users Graph
    timesByUsers = [data.listToTime(x).formattedTime() for x in sorted(data.allTimesByUsers, key=lambda k:k[1])]
    valueByUsers = [x[0] for x in sorted(data.allTimesByUsers, key=lambda k:k[1])]
    fig1, ax1 = plt.subplots()
    ax1.plot(timesByUsers, valueByUsers, 'co', timesByUsers, valueByUsers, 'k')
    ax1.set_title("Available Users by Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Available Users")
    fig1.savefig('models/output/users.png')

    # Weight Graph
    timesByWeight = [data.listToTime(x).formattedTime() for x in sorted(data.allTimesByWeight, key=lambda k:k[1])]
    valueByWeight = [x[0] for x in sorted(data.allTimesByWeight, key=lambda k:k[1])]
    fig2, ax2 = plt.subplots()
    ax2.plot(timesByWeight, valueByWeight, 'co', timesByWeight, valueByWeight, 'k')
    ax2.set_title("Time Weight")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Weight")
    fig2.savefig('models/output/weight.png')

    # Concatenate Graphs
    graphs = get_concat_h(Image.open('models/output/users.png'), Image.open('models/output/weight.png'))
    subtext = Image.new('RGB', (graphs.width, 100), color=(256, 256, 256))
    draw = ImageDraw.Draw(subtext, 'RGB')
    font = ImageFont.truetype("models/data/Font.ttf", 18)
    msg1 = f"Optimal time (by users): {data.optimalTimeUsers.formattedTime()}"
    msg2 = f"Optimal time (by weight): {data.optimalTimeWeight.formattedTime()}"
    w1, h1 = draw.textsize(msg1, font=font)
    w2, h2 = draw.textsize(msg2, font=font)
    draw.text(( (graphs.width / 2 - w1)/2, (100-h1)/2 ), msg1, (0, 0, 0, 255),font=font)
    draw.text(( (graphs.width / 2 - w2)/2 + graphs.width/2, (100-h2)/2 ), msg2, (0, 0, 0, 255),font=font)
    conc = get_concat_v(graphs, subtext).save(f'static/{output_id}-light.png')
    dark = ImageOps.invert(Image.open(f'static/{output_id}-light.png')).save(f'static/{output_id}-dark.png')


def input_to_graphs(u_in, output_id):
    validate_user_input(u_in)
    timezones = collect_timezones(u_in)
    time_list = calculate_time_weight(u_in, timezones)
    data = group_data(time_list)
    output_data(data, output_id)
