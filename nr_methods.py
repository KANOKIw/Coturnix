import requests
import json
import datetime
import re
import time
import http.server
import discord

from discord.ext import commands
from python_aternos import Client


client: discord.Client = None

def set_client3(cli: discord.Client):
    global client
    client = cli
    

def ElapsedTime(view: int=2):
    def wrapper(func: function):
        def _wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"Function '{func.__name__}' took {(end-start)*1000:.{view}f} milliseconds to execute.")
            return result
        return _wrapper
    return wrapper


def current_time() -> str:
    timestr = datetime.datetime.now().replace(microsecond=0)
    timestr = timestr + datetime.timedelta(hours=9)
    return f'[{str(timestr).replace("2023-", "")}] '


def is_minecraft_player_name(player_name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def contains_japanese(text):
    pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uFF65-\uFF9F]+')
    return bool(re.search(pattern, text))


def timestr() -> any:
    timestr = datetime.datetime.now().replace(microsecond=0)
    timestr = timestr + datetime.timedelta(hours=7)
    return timestr


def make_number_clear(number: str) -> str:
    literable_number = ""
    number = number[::-1]
    for i in str(number):
        literable_number = literable_number + i
        if (len(literable_number.replace(",", "")) % 3) == 0:
            literable_number = literable_number + ","

    literable_number = literable_number[::-1]

    if literable_number[0] == ",":
        literable_number = literable_number[1:]
    return literable_number


def count(name, key) -> None:
    """ register count of user """
    try:
        with open("Counts/usercounts.json") as f:
            counts = json.load(f)
    except Exception:
        counts = {}

    try:
        currentusercounts = counts[name]
    except (KeyError):
        currentusercounts = {}


    try:
        currentusercnt = currentusercounts[key]
    except KeyError:
        currentusercnt = 0
    
    currentusercnt += 1
    currentusercounts[key] = currentusercnt
    counts[name] = currentusercounts

    with open("Counts/usercounts.json", "w") as f:
        json.dump(counts, f, ensure_ascii=False, indent=4)