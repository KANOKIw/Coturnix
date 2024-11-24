import discord
import pydub
import ffmpeg
import subprocess
import sqlite3
import json
import requests

from colorama import Fore
from discord.ext import commands


intents = discord.Intents.all()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix="!", intents=intents)


#START
try:
    with open("Config/config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

while True:
    token = config.get("token", None)
    if token:
        print(f"\n--- TOKEN loaded from {Fore.GREEN}./config.json{Fore.RESET}\n")
    else:
        token = input(f"Input TOKEN\n> ")

    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bot {token}"
        }).json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
            exit(f"{Fore.RED}ConnectionError{Fore.RESET}: Discord is commonly blocked on public networks, please make sure discord.com is reachable!")

        elif e.__class__ == requests.exceptions.Timeout:
            exit(f"{Fore.RED}Timeout{Fore.RESET}: Connection to Discord's API has timed out (possibly being rate limited?)")

        exit(f"Unknown error has occurred! Additional info:\n{e}")

    
    if data.get("id", None):
        break  

    print(f"\n{Fore.RED}TOKENが間違っています{Fore.RESET}. TOKENは英数字で書かれています。囲ったりしないでください")

    config.clear()


with open("Config/config.json", "w") as f:
    config["token"] = token

    json.dump(config, f, indent=2)
#END



@client.event
async def on_ready():
    print(f"ready,\nupdating users' name")
    
    connection = sqlite3.connect("./SHISHIJI/db/Latest_nametable.db")
    cursor = connection.cursor()
    guild = client.get_guild(1153884392448606238)
    
    role_updated = guild.get_role(1228371737025056791)
    role_latest_dat = guild.get_role(1237402978525253752)
    channel_log = guild.get_channel(1153952454346559508)
    print(role_latest_dat.mention)
    for member in guild.members:
        if role_updated not in member.roles and role_latest_dat not in member.roles:
            print(member.nick)

    for member in guild.members:
        if not member.nick:
            continue

        prev_nick = member.nick
        nicknamedat = prev_nick.split(" ")
        
        last_datw = nicknamedat[0]
        last_dat = ""
        for dat in last_datw.split("-"):
            if dat.startswith("0"):
                dat = dat[1:]
            last_dat += dat

        realname = nicknamedat[-1]
        row = cursor.execute("SELECT * FROM NAME_TABLE WHERE name=?", (realname, )).fetchone()
        
        if not row or last_dat != row[7]:
            continue
        else:
            latest_dat = row[8]
            latest_dat = latest_dat[:2] + "-" + latest_dat[2:] + " " + realname
            print(prev_nick, latest_dat)
            try:
                await member.edit(nick=latest_dat)
                await member.add_roles(role_updated, role_latest_dat)
            except Exception:
                await channel_log.send(f"```diff\n- Failed to execute 'chNick' on {prev_nick}```")

        

client.run("MTA4MjYxMDg2OTc1NTcwNzQ0Mg.GN2pqW._CK_5stEYGOlTktRqcHLg8Q6MXQAtkWjpaOYzA")
