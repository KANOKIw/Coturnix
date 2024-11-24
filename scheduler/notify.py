import requests, json, inspect, sys, datetime, asyncio
import discord, discord.utils, subprocess, os, time, random

from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client


try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Discord.pyがインストールされていません"
    )
logo = f"""
なにかあれば "かのき#7777" にDMしてください
"""

#START
try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}


while True:
    token = config.get("token", None)
    if token:
        print(f"\n--- {Fore.GREEN}./config.json{Fore.RESET} よりTOKENをとってきました...\n")
    else:
        token = input("> ")

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


with open("config.json", "w") as f:
    config["token"] = token

    json.dump(config, f, indent=2)
#END


class Coturnix(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        await self.tree.sync()



#intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents) 

@client.event
async def on_ready():
    """ 
    bot起動==
    """
    print(inspect.cleandoc(f"""
        ログインしたのは {client.user} (ID: {client.user.id})のbotです

        以下のURLをブラウザで開けば、 {client.user} をサーバーに追加できます:
        {Fore.LIGHTBLUE_EX}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot{Fore.RESET}
    """), end="\n\n")

    
