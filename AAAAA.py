import requests, json, inspect, sys, datetime, asyncio, io
import discord, discord.utils, subprocess, os, time, random, cv2
import numpy as np

from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client
from PIL import Image


galist=[0]
dt = datetime.datetime.today()

# Make sure that the user is running Python 3.8 or higher
if sys.version_info < (3, 8):
    exit("Python 3.8 or higher is required to run this bot!")

# Now make sure that the discord.py library is installed or/and is up to date
try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Either discord.py is not installed or you are running an older and unsupported version of it."
        "Please make sure to check that you have the latest version of discord.py! (try reinstalling the requirements?)"
    )

# ASCII logo, uses Colorama for coloring the logo.
logo = f"""
{Fore.LIGHTBLUE_EX}       {Fore.GREEN}cclloooooooooooooo.
{Fore.LIGHTBLUE_EX},;;;:{Fore.GREEN}oooooooooooooooooooooo.
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}kKXK{Fore.GREEN}ooo{Fore.WHITE}NMMWx{Fore.GREEN}ooooo:..
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}XMMN{Fore.GREEN}oooo{Fore.WHITE}XNK0x{Fore.GREEN}dddddoo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}looo{Fore.WHITE}kNMMWx{Fore.GREEN}ooood{Fore.BLUE}xxxxxxxxxxxxxo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}ld{Fore.WHITE}kXXXXK{Fore.GREEN}ddddd{Fore.BLUE}xxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.BLUE}ldxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{Fore.RESET}
"""

# inspect.cleandoc() is used to remove the indentation from the message
# when using triple quotes (makes the code much cleaner)
# Typicly developers woudln't use cleandoc rather they move the text
# all the way to the left
print(logo + inspect.cleandoc(f"""
    Hey, welcome to the active developer badge bot.
    Please enter your bot's token below to continue.

    {Style.DIM}Don't close this application after entering the token
    You may close it after the bot has been invited and the command has been ran{Style.RESET_ALL}
"""))

# Try except block is useful for when you'd like to capture errors
try:
    with open("Coturnix\Config\config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    # You can in theory also do "except:" or "except Exception:", but it is not recommended
    # unless you want to suppress all errors
    config = {}


while True:
    # If no token is stored in "config" the value defaults to None
    token = config.get("token", None)
    if token:
        print(f"\n--- Detected token in {Fore.GREEN}./config.json{Fore.RESET} (saved from a previous run). Using stored token. ---\n")
    else:
        # Take input from the user if no token is detected
        token = "MTA4MjYxMDg2OTc1NTcwNzQ0Mg.GN2pqW._CK_5stEYGOlTktRqcHLg8Q6MXQAtkWjpaOYzA"

    # Validates if the token you provided was correct or not
    # There is also another one called aiohttp.ClientSession() which is asynchronous
    # However for such simplicity, it is not worth playing around with async
    # and await keywords outside of the event loop
    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bot {token}"
        }).json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
            exit(f"{Fore.RED}ConnectionError{Fore.RESET}: Discord is commonly blocked on public networks, please make sure discord.com is reachable!")

        elif e.__class__ == requests.exceptions.Timeout:
            exit(f"{Fore.RED}Timeout{Fore.RESET}: Connection to Discord's API has timed out (possibly being rate limited?)")

        # Tells python to quit, along with printing some info on the error that occured
        exit(f"Unknown error has occurred! Additional info:\n{e}")

    # If the token is correct, it will continue the code
    if data.get("id", None):
        break  # Breaks out of the while loop

    # If the token is incorrect, an error will be printed
    # You will then be asked to enter a token again (while Loop)
    print(f"\nSeems like you entered an {Fore.RED}invalid token{Fore.RESET}. Please enter a valid token (see Github repo for help).")

    config.clear()

with open("config.json", "w") as f:
    config["token"] = token
    json.dump(config, f, indent=2)


class Coturnix(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        await self.tree.sync()


client = Coturnix(intents=Intents.none())


@client.event
async def on_ready():
    """ This is called when the bot is ready and has a connection with Discord
        It also prints out the bot's invite URL that automatically uses your
        Client ID to make sure you invite the correct bot with correct scopes.
    """
    print(inspect.cleandoc(f"""
        Logged in as {client.user} (ID: {client.user.id})

        Use this URL to invite {client.user} to your server:
        {Fore.LIGHTBLUE_EX}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot{Fore.RESET}
    """), end="\n\n")
    

@client.tree.command()
async def sendasbot(interaction: Interaction, content: str, cmd: bool=None):
    """ nothing to explain """

@client.tree.command()
async def avater(interaction: Interaction, userid: str):
    """ avater """

@client.tree.command()
async def vc(interaction: Interaction, vcid: str=None, disconnect: str=None):
    """ connect to vc """

@client.tree.command()
async def playmusic(interaction: Interaction, name: str, buttons: bool=None):
    """ plays music in connected vc! """

@client.tree.command()
async def stop(interaction: Interaction):
    """ stop """

@client.tree.command()
async def ban(interaction: Interaction, user: discord.Member):
    """ ban with a message """

@client.tree.command()
async def toggle(interaction: Interaction, censor: bool):
    """ toggle censorship """

@client.tree.command()
async def speak(interaction: Interaction, contents: str, allowed: bool=None):
    """ speak """

@client.tree.command()
async def survey(interaction: Interaction, title: str, description: str, anonymous: bool=False):
    """ make new survey on currentchannel
    
    title: :class:`str`
        アンケートのタイトル
    description: :class: `str`
        アンケートの説明
    """

@client.tree.command()
async def getfile(interaction: Interaction, filename: str):
    """ get file from server dir """

@client.tree.command()
async def reset(interaction: Interaction, setagaquest: bool=False, shishiji: bool=False):
    """ about register """

@client.tree.command()
async def getresult(interaction: Interaction, title: str, add_coop: discord.Member=None, remove_coop: discord.Member=None):
    """ get survey result
    
    title: :class:`str`
        #アンケートのID, もしくはアンケートのタイトル
    add_coop: :class:`discord.Member`
        結果を閲覧可能なユーザーを追加する
    remove_coop: :class:`discord.Member`
        結果を閲覧可能なユーザーを削除する
    """
    
@client.tree.command()
async def poll(interaction: Interaction, question: str, option1: str, option2: str, option3: str=None, option4: str=None):
    """ create a poll(options up to 4) """

@client.tree.command()
async def poll_end(interaction: Interaction, question: str):
    """ end a poll """
    print("a")

@client.tree.command()
async def absentcontact(interaction: Interaction, title: str, description: str, year: str, month: str, date: str, hour: str, minute: str, url: str="", message: str=None):
    """ 欠席連絡をさせるボタンを送信します 
    
    title: :class:`str`
        イベントのタイトル
    description: :class:`str`
        イベントの説明
    year: :class:`str`
        イベントの年(西暦, > 1970, < 2030)
    month: :class:`str`
        イベントの月(> 0, < 13)
    date: :class:`str`
        イベントの日にち(> 0, < 31)
    hour: :class:`str`
        イベントの時刻(24時間制, > 0, < 25)
    minute: :class: `str`
        イベントの分(> 0, < 60)
    url: :class: `class`
        イベントのURL(Optional) - 規定値: ""
    message: :class:`str`
        添付するメッセージ - 規定値: `None`
    """

@client.tree.command()
async def setagaquest(interaction: Interaction, invurl: str, rolemention: discord.Role=None, usermention: discord.Member=None):
    """ send a Embed """
    print("a")

@client.tree.command()
async def solve(interaction: Interaction, ticket_category: discord.CategoryChannel, support_role: discord.Role, content: str, cache_channel: discord.TextChannel=None):...

@client.tree.command()
async def send_role_button(interaction: Interaction, message: str=None, label: str="選択する"):...

@client.tree.command()
async def record(interaction: Interaction, message: str=None, label: str="選択する"):...

@client.tree.command()
async def shishiji_absentcontact(interaction: Interaction, title: str, description: str, year: str, month: str, date: str, hour: str, minute: str, url: str="", message: str=None):...

client.run(token)
