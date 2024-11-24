import requests
import json
import inspect
import sys
import datetime
import asyncio
import io
import re
import discord
import discord.utils
import subprocess
import os
import time
import random
import matplotlib.pyplot as plt
import http.server
import socketserver
import threading
import Shishiji
import functools
import typing
import a_client

from typing import Optional
from discord.ui.item import Item
from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client
from PIL import Image
from discord.interactions import Interaction
from discord.ui import Select, View
from Te import TicketModal, TicketCloseConfirm
from roll_hand import *
from atbuttons import *
from Poll_prot import *
from musicbtns import *



# fluid nodes
PORT = 2293
HTTPHandler = http.server.SimpleHTTPRequestHandler

#aternos
tickets = 0
current_unix_time = time.time()
dt = datetime.datetime.today()

credential_path = "./crypto-pulsar-382609-4ec0295085ca.json"
present_emoji = "<:event_present01_01:1102521654447439923>"

#giveawaylist
galist = [0]

#/cmd
cmdlist = ["True", "true", "T", "t"]
censorship = False

srcs = ["javascript"]



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


def start(port, handler):
    """with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"HTTPserver has started on port: {port}")
        httpd.serve_forever()"""
    server_address = ('', port)  # Change port as needed
    print(f"HTTPserver has started on port: {port}")

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


async def embedban(message, reason) -> None:
    channel = message.channel
    try:
        await message.author.ban(reason="あほ", delete_message_seconds=0)
        banembed = discord.Embed(title=f"✅ {message.author.name} was banned", description=reason, color=0x98765)
        await channel.send(embed=banembed)
    except AttributeError:
        banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}", description=f"ErrorType: {{channel: DM}}, {reason}", color=0xff0000)
        await channel.send(embed=banembed)
    except discord.errors.Forbidden:
        banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}", description=f"ErrorType: {{roles: administrator}}, {reason}", color=0xff0000)
        await channel.send(embed=banembed)


def compare_images(image_url_1, image_url_2) -> bool:
    response_1 = requests.get(image_url_1)
    response_2 = requests.get(image_url_2)
    image_1 = Image.open(io.BytesIO(response_1.content)).convert('RGB')
    image_2 = Image.open(io.BytesIO(response_2.content)).convert('RGB')
    if image_1.size != image_2.size:
        return False
    pairs = zip(image_1.getdata(), image_2.getdata())
    if len(image_1.getbands()) == 1:
        # grayscale image
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    n_components = image_1.size[0] * image_1.size[1] * 3
    difference = (dif / 255.0 * 100) / n_components
    return difference < 20.0


async def check_everychat_iscrime(message: discord.Message) -> None:
    """
    Parameter
    ----------
    message: discord.Message

    Checks if message.content is crimery
    This method also contains checking with five continuous word crimery

    If detected crimery, message.author will be banned
    Above activity will send unofficial BanEmbed explaining who was banned
    If the ban target has ADMIN permissons, BanEmbed will become ErrorEmbed
    
    Returns
    ----------
    None
    """
    return

    channel = message.channel

    if len(message.content) >= 50:
        return

    for i in damewords:
        if i in message.content:
            try:
                await message.delete()
            except Exception:
                pass
            print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{message.content}{Fore.RESET} {Fore.MAGENTA}(author:{message.author.name}, detected: {i}){Fore.RESET}")

            try:
                with open("Counts/usercounts.json") as f:
                    counts = json.load(f)
            except Exception:
                counts = {}

            try:
                currentusercounts = counts[message.author.name]
            except (KeyError):
                currentusercounts = {}

            try:
                currentusercnt = currentusercounts["deleted"]
            except KeyError:
                currentusercnt = 0
            
            currentusercnt += 1
            if currentusercnt >= 1:
                try:
                    await message.author.ban(reason="あほ", delete_message_seconds=0)
                    banembed = discord.Embed(title=f"✅ {message.author.name} was banned", color=0x98765)
                    await channel.send(embed=banembed)
                except Exception as e:
                    if e.__class__ == AttributeError:
                        banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}",
                            description="ErrorType: {{Channel: DM}} , 下ネタ: {}".format(message.content),
                            color=0xff0000)
                        await channel.send(embed=banembed)
                    else:
                        banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}", description="ErrorType: administrator", color=0xff0000)
                        await channel.send(embed=banembed)

            currentusercounts["deleted"] = currentusercnt
            counts[message.author.name] = currentusercounts

            with open("Counts/usercounts.json", "w") as f:
                json.dump(counts, f, ensure_ascii=False, indent=4)

            break

    for i in yurusanaiwords:
        if i in message.content:
            print(f"\n[{timestr()}] {Fore.RED}Detected {i}: {Fore.RESET} {Fore.CYAN}{message.content}{Fore.RESET} {Fore.MAGENTA}(author:{message.author.name}){Fore.RESET}")
            count(message.author.name, "下ネタ")
            try:
                await message.author.ban(reason="あほ", delete_message_seconds=0)
                banembed = discord.Embed(title=f"✅ {message.author.name} was banned", description="下ネタ: {}".format(message.content), color=0x98765)
                await channel.send(embed=banembed)
            except Exception as e:
                if e.__class__ == AttributeError:
                    banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}",
                        description="ErrorType: {{Channel: DM}} , 下ネタ: {}".format(message.content),
                        color=0xff0000)
                    await channel.send(embed=banembed)
                else:
                    banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}",
                        description="ErrorType: administrator, 下ネタ: {}".format(message.content),
                        color=0xff0000)
                    await channel.send(embed=banembed)
            return

    fivemsgs = "a"
    try:
        with open(".d_crime/rentou.json") as f:
            rentou = json.load(f)
    except Exception:
        rentou = ["a", "a", "a", "a", "a"]

    rentou.pop(0)
    rentou.append(message.content)

    for messages in rentou:
        fivemsgs += str(messages)

    for word in yurusanaiwords:
        if word in fivemsgs:
            print(f"\n[{timestr()}] {Fore.RED}Detected {Fore.CYAN}{word}{Fore.RESET} in {Fore.RESET}{Fore.CYAN}{fivemsgs}{Fore.RESET} {Fore.MAGENTA}(author:{message.author.name}){Fore.RESET}")
            count(message.author.name, "下ネタ")
            try:
                await message.author.ban(reason="あほ", delete_message_seconds=0)
                if "a" in fivemsgs:
                    fivemsgs = fivemsgs.replace("a", "")
                banembed = discord.Embed(title=f"✅ {message.author.name} was banned", description="下ネタ: {}, 連投タイプ".format(fivemsgs), color=0x98765)
                await channel.send(embed=banembed)
            except Exception:
                if "a" in fivemsgs:
                    fivemsgs = fivemsgs.replace("a", "")
                banembed = discord.Embed(title=f"❌ Couldn't ban {message.author.name}",
                    description="ErrorType: administrator, 下ネタ: {}, 連投タイプ".format(fivemsgs),
                    color=0xff0000)
                await channel.send(embed=banembed)
            rentou = ["a", "a", "a", "a", "a"]
            break

    with open(".d_crime/rentou.json", "w") as f:
        json.dump(rentou, f, ensure_ascii=False, indent=4)

yurusanaiwords = ("IOshda(U)TYUSJIOGHDA)7ujwadhsJBAFiOYUATW(Ojsdhbajiluwa{D}aw)")

damewords = ("町田IAHDSIUYgw89a7dUIJSHDuijaSHDigusha")
eandro = ("えUIHADIOWuuisdhaiUYWGHD(798dgs9ad0uujshf8ifsjkvhnkAWD-Ds-aok)")
myhomes = {"https://cdn.discordapp.com/attachments/971597070811168770/1093867985028010044/IMG_7471.png": "かのきの家の全体像"}

if sys.version_info < (3, 8):
    exit("Python 3.8 以上で実行してください")

try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Discord.pyがインストールされていません"
    )

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


class Coturnix(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        await self.tree.sync()



class RegisterWithDM(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "登録する", style = discord.ButtonStyle.green, custom_id = "registerwithdm")
    async def eventstopper(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.BLUE}{interaction.user.name}{Fore.RESET} interacted register(4年-獅子師たち) button.")

        self.user = interaction.user; guild = interaction.guild
        self.dm = await self.user.create_dm()
        coturnix = guild.get_member(1082610869755707442)
        role_registered = guild.get_role(1098532985629839441)
        if role_registered in self.user.roles:
            await interaction.response.send_message("既に登録済みです", ephemeral=True)
            return
        register_channel = client.get_channel(1098507125266858106)
        register_message = await register_channel.fetch_message(1098884369692762113)
        await register_message.edit(content=f"ただいま{interaction.user.mention}が手続きを行っています。\n完了するまで少しだけお待ちください", view=None)

        await interaction.response.send_message(inspect.cleandoc(f"""{self.user.mention}、こんにちは
        続行するには私({coturnix.mention})とのダイレクトメッセージをご確認ください
        """), ephemeral=True)
        await self.dm.send("あなたのクラスを**__半角__アルファベット**で送信してください")
        self.sent_your_class = False
        self.sent_your_name = False

        @client.event
        async def on_message(message):
            if message.author.bot:
                return
            
            try:
                cid = message.channel.id
            except Exception:
                pass

            global censorship
            if censorship is True:
                if cid == 1098507125266858106:
                    try:
                        await message.delete()
                        print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{message.content}{Fore.RESET}(登録)")
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")
                    except Exception:
                        pass
            
            await check_everychat_iscrime(message)

            if self.sent_your_class is False:
                if message.channel.id == self.dm.id:
                    print(f"\n[{timestr()}] {Fore.BLUE}{self.user.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.YELLOW}<class>{Fore.RESET} {message.content}")
            if self.sent_your_class is True and self.sent_your_name is False:
                if message.channel.id == self.dm.id:
                    print(f"\n[{timestr()}] {Fore.BLUE}{self.user.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.YELLOW}<name>{Fore.RESET} {message.content}")
                    
            if message.channel.id == self.dm.id:
                if self.sent_your_class is False:
                    pass
                
                elif self.sent_your_class is True and self.sent_your_name is False:
                    pass
                else:
                    if message.author.bot:
                        pass
                    else:
                        print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}")

            elif message.channel.__class__ == discord.channel.DMChannel:
                if message.author.bot:
                    pass
                else:
                    print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}")
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")
            
            if message.channel.id != self.dm.id:
                return

            self.userid = self.user.id; self.username = self.user.name

            if self.sent_your_class is False:
                self.your_class = message.content
                self.your_class = self.your_class.replace("　", "")
                self.your_class = self.your_class.replace(" ", "")
                self.your_class = self.your_class.replace("4", "")
                self.your_class = self.your_class.replace("４", "")

                if "a" in self.your_class:
                    self.your_class = "A"
                elif "b" in self.your_class:
                    self.your_class = "B"
                elif "c" in self.your_class:
                    self.your_class = "C"
                elif "d" in self.your_class:
                    self.your_class = "D"
                elif "e" in self.your_class:
                    self.your_class = "E"
                elif "f" in self.your_class:
                    self.your_class = "F"
                elif "g" in self.your_class:
                    self.your_class = "G"

                classes = ("A", "B", "C", "D", "E", "F", "G")
                if self.your_class not in classes:
                    await self.dm.send("**正確なクラス**を送信してください")
                    return
            
                self.sent_your_class = True
                await self.dm.send("次に**本名__(フルネーム)__**を送信してください")
                return
            
            if self.sent_your_class is True and self.sent_your_name is False:
                self.your_name = message.content
                self.your_name = self.your_name.replace("　", "")
                self.your_name = self.your_name.replace(" ", "")
                try:
                    with open("Config/Config_username.json") as f:
                        users = json.load(f)
                except Exception:
                    users = {}

                intera_user_info = {}

                intera_user_info["discord_name"] = self.username
                intera_user_info["name"] = self.your_name
                intera_user_info["class"] = self.your_class
                users[self.userid] = intera_user_info
                
                with open("Config/Config_username.json", "w") as f:
                    json.dump(users, f, ensure_ascii=False, indent=4)
                self.sent_your_name = True
    
                try:
                    channel_for_mention = client.get_channel(1099721782732275773)
                    await register_message.edit(content=inspect.cleandoc(f"""このボタンをおしたあと、DMを確認してください
                    <登録の仕方: {channel_for_mention.mention}>"""), view=RegisterWithDM())

                    await self.user.add_roles(role_registered)
                    await self.user.edit(nick=f"{self.your_class}_{self.your_name}")

                    role_class_A = guild.get_role(1098607173308780686)
                    role_class_B = guild.get_role(1098607662511423709)
                    role_class_C = guild.get_role(1098607729775493132)
                    role_class_D = guild.get_role(1098607764873420921)
                    role_class_E = guild.get_role(1098607800642449550)
                    role_class_F = guild.get_role(1098607852723118101)
                    role_class_G = guild.get_role(1098608577612091523)

                    if self.your_class == "A":
                        await self.user.add_roles(role_class_A)
                    elif self.your_class == "B":
                        await self.user.add_roles(role_class_B)
                    elif self.your_class == "C":
                        await self.user.add_roles(role_class_C)
                    elif self.your_class == "D":
                        await self.user.add_roles(role_class_D)
                    elif self.your_class == "E":
                        await self.user.add_roles(role_class_E)
                    elif self.your_class == "F":
                        await self.user.add_roles(role_class_F)
                    elif self.your_class == "G":
                        await self.user.add_roles(role_class_G)

                    channel = client.get_channel(1098507125266858109)
                    await self.dm.send(inspect.cleandoc(f"""登録が完了しました!!
                    サーバーに戻ってみてください
                    {channel.mention}
                    https://discord.gg/gtTbasKVRm"""))
                    channel = guild.get_channel(1098579941714579516)
                    await channel.send(f"{interaction.user.mention}が登録されました")
                except Exception:
                    await self.dm.send("貴様は管理者や")
                

class RegisterWithDmOnSETAGAQUEST(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "| いますぐ無料で登録！！", emoji=present_emoji, style = discord.ButtonStyle.success, custom_id = "registerwithdmOnSETAGAQUEST")
    async def eventstopper(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.BLUE}{interaction.user.name}{Fore.RESET} interacted register(セタガクエスト) button.")

        # セタガクエスト -> メンバー
        guild = interaction.guild
        self.user = interaction.user
        role_registered = guild.get_role(1101419218253131846)
        if role_registered in self.user.roles:
            await interaction.response.send_message("既に登録されています", ephemeral=True)
            print("-> 既に登録されている")
            return

        channel = client.get_channel(1101755461876842507)
        coturnix_register_message = await channel.fetch_message(1101756183251013682)
        await coturnix_register_message.edit(content=f"ただいま{interaction.user.mention}が手続きを行っています。\n完了するまで少しだけお待ちください", view=None)

        self.dm = await self.user.create_dm()
        coturnix = guild.get_member(1082610869755707442)


        global sent_your_class
        global your_class
        self.sent_your_name = False
        sent_your_class = False

        await interaction.response.send_message(inspect.cleandoc(f"""{self.user.mention}、こんにちは
        続行するには({coturnix.mention})とのダイレクトメッセージをご確認ください
        """), ephemeral=True)

        await self.dm.send(f"-------------------------\nここからは登録の手続きです")

        class CLASS_SETAGAKU(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)

            @discord.ui.button(label = "A", style = discord.ButtonStyle.green, custom_id = "AGUMI")
            async def AGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "A"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "B", style = discord.ButtonStyle.green, custom_id = "BGUMI")
            async def BGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "B"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "C", style = discord.ButtonStyle.green, custom_id = "CGUMI")
            async def CGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "C"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "D", style = discord.ButtonStyle.green, custom_id = "DGUMI")
            async def DGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "D"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "E", style = discord.ButtonStyle.green, custom_id = "EGUMI")
            async def EGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "E"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "F", style = discord.ButtonStyle.green, custom_id = "FGUMI")
            async def FGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "F"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()

            @discord.ui.button(label = "G", style = discord.ButtonStyle.green, custom_id = "GGUMI")
            async def GGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("pushed!!")
                global sent_your_class
                global your_class
                sent_your_class = True
                your_class = "G"
                await interaction.response.send_message("次に名前をフルネームで送信してください")
                await msg.delete()


        msg = await self.dm.send("あなたのクラスを選択してください", view=CLASS_SETAGAKU())
        

        @client.event
        async def on_message(message):
            if sent_your_class is True and self.sent_your_name is False:
                if message.channel.id == self.dm.id:
                    print(f"\n[{timestr()}] {Fore.BLUE}{self.user.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.YELLOW}<name>{Fore.RESET} {message.content}")
                    
            if message.channel.id == self.dm.id:
                if sent_your_class is True and self.sent_your_name is False:
                    pass
                else:
                    if message.author.bot:
                        pass
                    else:
                        print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}")
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")

            elif message.channel.__class__ == discord.channel.DMChannel:
                if message.author.bot:
                    pass
                else:
                    print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}")
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")
            
            if message.channel.id != self.dm.id:
                return

            self.userid = self.user.id; self.username = self.user.name

            if sent_your_class is True and self.sent_your_name is False:
                self.your_name = message.content
                self.your_name = self.your_name.replace("　", "")
                self.your_name = self.your_name.replace(" ", "")
                try:
                    with open("Config/Config_username_SETAGAQUEST.json") as f:
                        users = json.load(f)
                except Exception:
                    users = {}

                if str(self.userid) in users.keys():
                    users.pop(str(self.userid))

                intera_user_info = {}

                intera_user_info["discord_name"] = self.username
                intera_user_info["name"] = self.your_name
                intera_user_info["class"] = your_class
                users[self.userid] = intera_user_info
                
                with open("Config/Config_username_SETAGAQUEST.json", "w") as f:
                    json.dump(users, f, ensure_ascii=False, indent=4)
                self.sent_your_name = True
    
                try:
                    await self.user.add_roles(role_registered)

                    await self.user.edit(nick=f"{your_class}_{self.your_name}")

                    nowtime = time.time()

                    announce = client.get_channel(1101415964442112030)
                    general = client.get_channel(1101399574897250376)
                    endembed = discord.Embed(title="登録の手続きが完了しました", description=inspect.cleandoc(f"""**進行中のアンケートに回答してください:**\n    {announce.mention}\n
                    一般チャット:\n    {general.mention}"""), color=0x008000)
                    endembed.add_field(name="完了日時", value=(inspect.cleandoc(f"""<t:{int(nowtime)}:F>""")))
                    endembed.add_field(name="ついでに", value=(inspect.cleandoc(f"""https://forms.gle/r1LSdhHG5opnBJPe7
                    を`@shishiji` のメールアドレスで回答してください
                    **してくれないと僕がくびにされます**""")))

                    # General
                    await self.dm.send(embed=endembed)

                    # hist
                    guild = client.get_guild(1101399573991268374)
                    channel = guild.get_channel(1101747278722641970)
                    await channel.send(f"{interaction.user.mention}が登録されました")
                except Exception as e:
                    if e.__class__ == discord.errors.Forbidden:
                        await self.dm.send(f"管理者に変更を加えることはできません。じぶんでやっといて！\nメンバーロールを外すとまたボタンが押せるようになります")
                    else:
                        await self.dm.send(f"unknown error occurred!! additional info: \n`{e}`")
                finally:
                    guild = client.get_guild(1101399573991268374)
                    admin_role = guild.get_role(1101414407860396074)
                    await coturnix_register_message.edit(content=f"{admin_role.mention}: 名前わかりづらい\nということで名前を登録してください", view=RegisterWithDmOnSETAGAQUEST())


class CancelAnswer(discord.ui.View):
    def __init__(self, title: str, label: str, channel: discord.channel) -> None:
        super().__init__(timeout = None)
        self.title = title; self.label = label; self.channel = channel

    @discord.ui.button(label = "回答を変更する", style = discord.ButtonStyle.red, custom_id = "Change Answer")
    async def changeanswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} changed his answer\n")

        try:
            with open("Config/Survey/" + self.title + "_ansed_users.json") as f:
                ansed_users = json.load(f)
        except Exception:
            ansed_users = {}
            
        if str(interaction.user.id) in ansed_users.keys():
            ansed_users.pop(str(interaction.user.id))

        with open("Config/Survey/" + self.title + "_ansed_users.json", "w") as f:
            json.dump(ansed_users, f, ensure_ascii=False, indent=4)

        await interaction.response.send_modal(CustomAnswerModal(title=self.title, label=self.label, channel=self.channel))


class CustomAnswerModal(discord.ui.Modal, title = "回答を記入してください"):
    answer = discord.ui.TextInput(label="複数回答する場合は空白などで区切ってください", style=discord.TextStyle.long, placeholder="回答を記入してください", required=True, min_length=1)
    def __init__(self, title: str, label: str, channel: discord.channel) -> None:
        super().__init__(timeout=None)
        self.title = title; self.label = label; self.channel = channel

    async def on_submit(self, interaction: Interaction) -> None:
        print(f"[{timestr()}] {Fore.BLUE}{interaction.user.name} {Fore.CYAN}Modal{Fore.RESET} {Fore.YELLOW}<{self.title}>{Fore.RESET} {str(self.answer)}")

        user = interaction.user
        dm  = await user.create_dm(); nowtime = time.time()
        embed = discord.Embed(title="回答を記録しました", description=f"回答日時: <t:{int(nowtime)}:F>", color=0x0000FF)
        if interaction.channel.__class__ == discord.channel.DMChannel or interaction.channel.__class__ == discord.channel.PartialMessageable:
            embed.add_field(name="回答を変更する場合は下のボタンからできます", value=f"反応しないときは\n**ここ**からやり直してください", inline=True)
        else:
            embed.add_field(name="回答を変更する場合は下のボタンからできます", value=f"反応しないときは\n{self.channel.mention}からやり直してください", inline=True)
        embed.add_field(name=f"質問: {self.title}", value=f"回答: {str(self.answer)}", inline=True)
        await dm.send(embed=embed, view=CancelAnswer(title=self.title, label=self.label, channel=self.channel))
        self.user = interaction.user; self.userid = interaction.user.id; self.username = interaction.user.name

        try:
            with open("Answers/" + self.title + "_answers.json") as f:
                users = json.load(f)
        except Exception:
            users = {}

        if str(self.userid) in users.keys():
            users.pop(str(self.userid))

        intera_user_info = {}

        intera_user_info["discord_name"] = self.username
        intera_user_info[self.title] = str(self.answer)
        users[self.userid] = intera_user_info
        
        with open("Answers/" + self.title + "_answers.json", "w") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

        try:
            with open("Config/Survey/" + self.title + "_ansed_users.json") as f:
                ansed_users = json.load(f)
        except Exception:
            ansed_users = {}
        
        if str(self.userid) in ansed_users.keys():
            ansed_users.pop(str(self.userid))
        
        ansed_user_info = {}
        ansed_user_info["discord_name"] = self.username
        ansed_user_info["time_stamp"] = str(timestr())
        ansed_users[str(self.userid)] = ansed_user_info

        with open("Config/Survey/" + self.title + "_ansed_users.json", "w") as f:
            json.dump(ansed_users, f, ensure_ascii=False, indent=4)
        coturnix = client.get_user(1082610869755707442)
        await interaction.response.send_message(f"回答を記録しました", ephemeral=True)



class CustomAnswer(discord.ui.View):
    def __init__(self, title: str, description: str, madeby: discord.User, channel: discord.channel) -> None:
        super().__init__(timeout = None)
        self.title = title; self.description = description; self.madeby = madeby; self.channel = channel

    @discord.ui.button(label = "| 回答する", emoji="📋", style = discord.ButtonStyle.green)
    async def customanswer(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.BLUE}{interaction.user.name}{Fore.RESET} interacted {self.title} button.")

        self.user = interaction.user; guild = interaction.guild
        self.dm = await self.user.create_dm()
        kanoki = client.get_user(805680950238642188)

        try:
            with open("Config/Survey/" + self.title + "_ansed_users.json") as f:
                ansed_users = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"無効なアンケートです。", ephemeral=True)
                print(f"-> ...Error?: {e}")
                return
            else:
                await interaction.response.send_message(f"Unknown error occurred!!\nPlease report to <@805680950238642188>.", ephemeral=True)
                print(f"-> Error: {e}")
                return

        if str(self.user.id) in ansed_users.keys():
            await interaction.response.send_message(f"既に回答しています", ephemeral=True, view=CancelAnswer(title=self.title, label=self.description, channel=self.channel))
            print("-> 既に回答している")
            return
        await interaction.response.send_modal(CustomAnswerModal(title=self.title, label=self.description, channel=self.channel))


class SMGnicknameModal(discord.ui.Modal, title="マイクラのユーザー名を入力してください"):
    answer = discord.ui.TextInput(label="マイクラのユーザー名をdiscordのニックネームに設定します", style=discord.TextStyle.short, placeholder="正確に答えてください！", required=True, min_length=1, max_length=16)
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def on_submit(self, interaction: Interaction) -> None:
        print(f"[{timestr()}] {Fore.YELLOW}{interaction.user.global_name} {Fore.CYAN}Modal{Fore.RESET} {Fore.YELLOW}<SMGnicknameModal>{Fore.RESET} {str(self.answer)}")

        self.answer = str(self.answer).replace(" ", "").replace("　", "")
        check = repr(self.answer.encode("shift_jis")).replace("\\", "/")
        if "/x" in check:
            await interaction.response.send_message(f"**日本語が混じっています。\n正確に入力してください**", ephemeral=True)
            return

        if self.answer[0] != ".":
            result = is_minecraft_player_name(self.answer)
            if not result:
                await interaction.response.send_message(f"**__存在しないマインクラフターです。__\n正確に入力してください**", ephemeral=True)
                return
        
        SMG = interaction.guild
        role = SMG.get_role(1127590883664072744)
        await interaction.user.add_roles(role)
        try:
            await interaction.user.edit(nick=self.answer)
        except Exception:
            await interaction.response.send_message("**いつものごとく管理者です**", ephemeral=True)
            return
        
        await interaction.response.send_message(f"Discordニックネームを{self.answer}に変更しました", ephemeral=True)


class SMGnickname(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label = "ニックネームを登録する", style = discord.ButtonStyle.success)
    async def idontattendlol(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"[{timestr()}] {interaction.user.display_name} interacted [SMGnickname]")

        SMG = interaction.guild
        role = SMG.get_role(1127590883664072744)
        if role in interaction.user.roles:
            await interaction.response.send_message("あなたは既に登録されています", ephemeral=True)
            return
        await interaction.response.send_modal(SMGnicknameModal())



class CancelAbsent(discord.ui.View):
    def __init__(self, fp, title, color, timeoutunix):
        super().__init__(timeout=None)
        self.fp = fp
        self.title = title
        self.color = color
        self.timeoutunix = timeoutunix
    
    @discord.ui.button(label="欠席通知を取り消す", style=discord.ButtonStyle.primary)
    async def show_absentusers(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"[{timestr()}] {interaction.user.display_name} interacted [CancelAbsent({self.fp})]")

        with open(self.fp) as f:
            data = json.load(f)
        data = list(map(int, data))

        if not interaction.user.id in data:
            await interaction.response.send_message("**あなたは出席することになっています！**", ephemeral=True)
            return
        
        data = list(map(str, data))
        data.remove(str(interaction.user.id))
        data = list(map(int, data))
        with open(self.fp, "w") as f:
            json.dump(data, f, indent=4)
        
        await interaction.response.send_message(f"**欠席通知を取り消しました。**", ephemeral=True)


class AbsentUsersSoFar(discord.ui.View):
    def __init__(self, fp, title, color, timeoutunix):
        super().__init__(timeout=None)
        self.fp = fp
        self.title = title
        self.color = color
        self.timeoutunix = timeoutunix

    @discord.ui.button(label="このイベントの欠席者一覧", style=discord.ButtonStyle.success)
    async def show_absentusers(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"[{timestr()}] {interaction.user.display_name} interacted [show_absentusers({self.fp})]")

        await interaction.response.defer()

        with open(self.fp) as f:
            data = json.load(f)
            absentuserlist = list(map(int, data))
        details = f"**開催日時:** <t:{int(str(self.timeoutunix))}:F>\n"
        r = False
        for userid in absentuserlist:
            user = client.get_user(userid)
            details += f"{user.mention}, "
            r = True
        if r:
            details = details[:-2]
        else:
            details += "__なし__"
        embed = discord.Embed(title=f"{self.title} イベントの欠席者", description=details, color=self.color)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        

class IDontAttendTodayModal(discord.ui.Modal, title="理由を入力してください"):
    answer = discord.ui.TextInput(label="ユーザー名と欠席する理由が管理者に送信されます。", style=discord.TextStyle.long, placeholder="Beware; Unjustfied reasons enrage 山本耕大!!", required=True, min_length=1)
    def __init__(self, eventTitle: str, filenumber: str, color, timeoutunix) -> None:
        super().__init__(timeout=None)
        self.eventTitle = eventTitle
        self.filenumber = filenumber
        self.color = color
        self.timeoutunix = timeoutunix
        self.fp = "absent/config.cfg"
        
    
    async def on_submit(self, interaction: Interaction) -> None:
        print(f"[{timestr()}] {Fore.YELLOW}{interaction.user.global_name} {Fore.CYAN}Modal{Fore.RESET} {Fore.YELLOW}<IDontAttendTodayModal>{Fore.RESET} {str(self.answer)}")

        with open(self.fp) as f:
            config = json.load(f)
            absent_channel_id_list = list(map(int, config["absent-notify-channel_id"]))
        
        with open(self.filenumber) as f:
            alrUsers = json.load(f)
        alrUsers = list(map(int, alrUsers))
        alrUsers.append(interaction.user.id)
        with open(self.filenumber, "w") as f:
            json.dump(alrUsers, f, indent=4)
        
        for absent_channel_id in absent_channel_id_list:
            absent_channel = client.get_channel(absent_channel_id)
            embed = discord.Embed(title=f"欠席連絡({self.eventTitle})", description=f"**From:** {interaction.user.mention}\n**開催日時:** <t:{int(str(self.timeoutunix))}:F>", color=self.color)
            embed.add_field(name="理由", value=f"**{str(self.answer)}**")
            
            await absent_channel.send(embed=embed, view=AbsentUsersSoFar(self.filenumber, self.eventTitle, self.color, self.timeoutunix))

        await interaction.response.send_message("欠席理由を送信しました。", ephemeral=True)



class IDontAttendToday(discord.ui.View):
    def __init__(self, createdDate, filenumber, eventTitle, color):
        super().__init__(timeout=None)
        self.timeoutunix = int(createdDate)
        self.filenumber = filenumber
        self.eventTitle = eventTitle
        self.color = color
    
    @discord.ui.button(label = "欠席を連絡する", style = discord.ButtonStyle.success)
    async def idontattendlol(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"[{timestr()}] {interaction.user.display_name} interacted [IDontAttendToday]")

        nowunix = time.time()
        if nowunix > self.timeoutunix:
            await interaction.response.send_message("期限切れのイベントです。", ephemeral=True)
            return
        
        with open(self.filenumber) as f:
            alrUsers = json.load(f)
        alrUsers = list(map(int, alrUsers))
        if interaction.user.id in alrUsers:
            await interaction.response.send_message("あなたは既にこの会議の欠席連絡をしています。", view=CancelAbsent(self.filenumber, self.eventTitle, self.color, self.timeoutunix), ephemeral=True)
            return
        
        await interaction.response.send_modal(IDontAttendTodayModal(self.eventTitle, self.filenumber, self.color, self.timeoutunix))



class SETAGAQUESTRegisterNickName(discord.ui.View):
    def _init_(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label = "今すぐ登録する", emoji=present_emoji, style = discord.ButtonStyle.success)
    async def sendRegisterModal(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"[{timestr()}] {interaction.user.display_name} interacted [SETAGAQUESTRegisterNickName]")

        member = interaction.guild.get_role(1101419218253131846)
        selected = interaction.guild.get_role(1118870578519089233)
        
        if selected in interaction.user.roles:
            await interaction.response.send_message(f"既に登録されています\n間違いだと思う場合は <@805680950238642188> に問い合わせてください", ephemeral=True)
            return
        if member in interaction.user.roles:
            await interaction.response.send_message("**所属したい班を選んでください**", view=OrgList(), ephemeral=True)
            return
        await interaction.response.send_modal(SETAGAQUESTRegisterModal())


class OrgList(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="なりたい役職を選択してください",
        options=[
            discord.SelectOption(label="プログラマー", value="programmer", description=" ゲーム開発を行います(javascript, ブラック)"),
            discord.SelectOption(label="ウェブデザイナー", value="webdesigner", description="表示されるサイトのデザインを行います。(css)"),
            discord.SelectOption(label="モーション・エフェクトクリエイター", value="PVmaker", description="ムービーや戦闘など様々な場面での演出制作を担当します。"),
            discord.SelectOption(label="イラストレーター", value="designer", description="キャラクターや背景素材などグラフィックスの制作を担当します。"),
            discord.SelectOption(label="AR・3Dモデラー", value="ARand3D", description="ARマーカーやAR上の演出、3Dグラフィックスの制作を担当します。"),
            discord.SelectOption(label="ムービークリエイター", value="movieCreator", description="企画内や広報で使用するムービーを制作を担当します。"),
            discord.SelectOption(label="クイズ・ミッションスクリプター", value="questioner", description="ゲーム内でプレイヤーに解かせるクイズやミッションを作成します。"),
            discord.SelectOption(label="声優", value="voiceactor", description="ボイスを担当します。"),
            discord.SelectOption(label="サウンドデザイナー", value="soundDesigner", description="ゲーム内やムービー内で使用するBGMや効果音を担当します。"),
            discord.SelectOption(label="フリーエージェント(なんでも屋)", value="freeagent", description="必要な時にマネージャーや各ルームリーダーの指示に従って補佐を行います。また、デバッカーを担当します。")
        ]
    )

    async def callback(self, interaction: Interaction, select: Select):
        selected = interaction.guild.get_role(1118870578519089233)
        channel = interaction.guild.get_channel(1101747278722641970)

        if selected in interaction.user.roles:
            print("alr")
            await interaction.response.defer(ephemeral=True)
            return

        if select.values[0] == "designer":
            role = interaction.guild.get_role(1105790371100897453)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**イラストレーターに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "questioner":
            role = interaction.guild.get_role(1105787037409361972)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**クイズ・ミッションスクリプターに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "PVmaker":
            role = interaction.guild.get_role(1111149742542565456)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**エフェクト・モーションクリエーターに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "programmer":
            role = interaction.guild.get_role(1105789722657304678)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**プログラマーに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "webdesigner":
            role = interaction.guild.get_role(1118902886714331197)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**ウェブデザイナーに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "ARand3D":
            role = interaction.guild.get_role(1118900539028148367)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**AR, 3Dモデリングに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "voiceactor":
            role = interaction.guild.get_role(1118901236335386655)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**ウェブデザイナーに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "movieCreator":
            role = interaction.guild.get_role(1111149742542565456)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**ムービークリエイターに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "soundDesigner":
            role = interaction.guild.get_role(1119173669214760970)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**サウンドデザイナーに加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        elif select.values[0] == "freeagent":
            role = interaction.guild.get_role(1118903186233761873)
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"**フリーエージェント(なんでも屋)に加入しました。\n変更したい場合は<#1119203403571134515>のボタンをどうぞ**", ephemeral=True)
        if interaction.user.id != 805680950238642188:
            await channel.send(f"{interaction.user.mention}が{role.mention}として登録されました")
        await interaction.user.add_roles(selected)



class SETAGAQUESTRegisterModal(discord.ui.Modal, title="名前を入力してください"):
    answer = discord.ui.TextInput(label="学年クラス_名前のように入力してください(例: 4F_宋嘉軒)", style=discord.TextStyle.short, placeholder="(例: 4F_山本耕大)", required=True, min_length=5)
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    async def on_submit(self, interaction: Interaction) -> None:
        print(f"[{timestr()}] {Fore.YELLOW}{interaction.user.name} {Fore.CYAN}Modal{Fore.RESET} {Fore.YELLOW}<セタガクエスト名前登録>{Fore.RESET} {str(self.answer)}")
        self.user = interaction.user
        grades = ["1", "2", "3", "4", "5", "6"]
        classes = ["A", "B", "C", "D", "E", "F", "G"]
        nick = str(self.answer).replace("＿", "_").replace("１", "1").replace("２", "2").replace("３", "3").replace("４", "4").replace("５", "5").replace("６", "6")
        
        print(nick)
        Arraynick = list(nick)
        member = interaction.guild.get_role(1101419218253131846)

        if not Arraynick[0] in grades:
            await interaction.response.send_message(f'学年は["1", "2", "3", "4", "5", "6"]のうちのどれかです。\n__やり直してください__', ephemeral=True)
            print("grade miss")
            return
        if not Arraynick[1] in classes:
            await interaction.response.send_message(f'クラスは["A", "B", "C", "D", "E", "F", "G"]のうちのどれかです。\n__やり直してください__', ephemeral=True)
            print("class miss")
            return
        if Arraynick[2] != "_":
            await interaction.response.send_message(f'2文字目は「 _ 」(アンダーバー)でお願いします。\n__やり直してください__', ephemeral=True)
            print("_ (under bar) miss")
            return
        
        try:
            await interaction.user.edit(nick=nick)
        except Exception:
            dm = await interaction.user.create_dm()
            await dm.send(f"Ignoring exception in Coturnix.py, line 2575> 管理者だったため、ニックネームをつけることができませんでした")
        
        await interaction.user.add_roles(member)
        await interaction.response.send_message("**次に所属したい班を選んでください**", view=OrgList(), ephemeral=True)

        try:
            with open("Config/Config_username_SETAGAQUEST.json") as f:
                users = json.load(f)
        except Exception:
            users = {}

        if str(self.user.id) in users.keys():
            users.pop(str(self.user.id))

        intera_user_info = {}

        intera_user_info["discord_name"] = self.user.name
        intera_user_info["nickName"] = str(self.answer)
        users[self.user.id] = intera_user_info
        
        with open("Config/Config_username_SETAGAQUEST.json", "w") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)




class Disabled_CustomAnswer(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "| 回答する", emoji="📋", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_customanswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        return


class EndCustomAnswer_Conf(discord.ui.View):
    def __init__(self, title: str, description: str, madeby: discord.user, message: discord.Message) -> None:
        super().__init__(timeout = None)
        self.title = title; self.description = description; self.madeby = madeby; self.message = message

    @discord.ui.button(label = "| アンケートを終了する", emoji="<:greenpeke:1104032167656439899>", style = discord.ButtonStyle.red)
    async def end_custom_survey_conf(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} trying ending {self.title} survey.")

        try:
            with open("Config/Survey/" + self.title + "_ansed_users.json"):
                pass
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"そのアンケートは既に終了されています", ephemeral=True)
                print("-> 既に終了されいる")
                return
            else:
                await interaction.response.send_message(f"Unknown error occurred!! Additional info:\n{e}")
                print(f"-> Error: {e}")
                return


        await interaction.response.send_message(
            f"本当に **{self.title}** アンケートを終了しますか？\n__**この操作は取り消すことができません**__\n(引き続き結果を閲覧することは可能です。)",
            view=EndCustomAnswer(title=self.title, description=self.description, madeby=self.madeby, message=self.message),
            ephemeral=True)




class EndCustomAnswer(discord.ui.View):
    def __init__(self, title: str, description: str, madeby: discord.user, message: discord.Message) -> None:
        super().__init__(timeout = None)
        self.title = title; self.description = description; self.madeby = madeby; self.message = message

    @discord.ui.button(label = "| アンケートを終了する", emoji="<:greenpeke:1104032167656439899>", style = discord.ButtonStyle.red)
    async def end_cutom_survey(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} closed {self.title} survey.")

        try:
            with open("Config/Survey/" + self.title + "_ansed_users.json") as f:
                ansed_users = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"そのアンケートは既に終了されています", ephemeral=True)
                print("-> 既に終了されいる")
                return
            else:
                await interaction.response.send_message(f"Unknown error occurred!! Additional info:\n{e}")
                print(f"-> Error: {e}")
                return
        else:
            os.remove("Config/Survey/" + self.title + "_ansed_users.json")
        
        cnt = 0
        while True:
            try:
                if cnt == 0:
                    with open("Cache/Survey/cache_" + self.title + "_ansed_users.json"):
                        pass
                else:
                    with open("Cache/Survey/cache_" + self.title + "_ansed_users_" + str(cnt) + ".json"):
                        pass
            except Exception as e:
                if e.__class__ == FileNotFoundError:
                    break
                else:
                    await interaction.response.send_message(f"Unknown error occurred!! Additional info:\n{e}")
                    print(f"-> Error: {e}")
                    return
            cnt += 1


        if cnt == 0:
            with open("Cache/Survey/cache_" + self.title + "_ansed_users.json", "w") as f:
                json.dump(ansed_users, f, ensure_ascii=False, indent=4)
        else:
            with open("Cache/Survey/cache_" + self.title + "_ansed_users_" + str(cnt) + ".json", "w") as f:
                json.dump(ansed_users, f, ensure_ascii=False, indent=4)

        try:
            with open("Answers/" + self.title + "_answers.json") as f:
                answers = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                pass
            else:
                await interaction.response.send_message(f"Unknown error occurred!! Additional info:\n{e}")
                print(f"-> Error: {e}")
                return
        else:
            os.remove("Answers/" + self.title + "_answers.json")

            if cnt == 0:
                with open("Cache/Survey/cache_" + self.title + "_answers.json", "w") as f:
                    json.dump(answers, f, ensure_ascii=False, indent=4)
            else:
                with open("Cache/Survey/cache_" + self.title + "_answers_" + str(cnt) + ".json", "w") as f:
                    json.dump(answers, f, ensure_ascii=False, indent=4)

        embed = self.message.embeds[0]
        embed.add_field(name="このアンケートは終了されました", value=f"<t:{int(time.time())}:F>")

        await self.message.edit(embed=embed, view=Disabled_CustomAnswer())
        if self.message.channel.__class__ == discord.channel.DMChannel or self.message.channel.__class__ == discord.channel.PartialMessageable:
            await interaction.response.send_message(f"**{self.title}** アンケートを終了しました。\n<t:{int(time.time())}:F>")
        else:
            await interaction.response.send_message(f"**{self.title}** アンケートを終了しました。\n{self.message.channel.mention}\n<t:{int(time.time())}:F>")



class Disabled_PollSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary, disabled=True)
    async def disabled_first(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary, disabled=True)
    async def disabled_second(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    

class ChatModal(discord.ui.Modal, title="返信します"):
    answer = discord.ui.TextInput(label="返信を入力してください", style=discord.TextStyle.long, placeholder="必須...", required=True, min_length=1)
    def __init__(self, user: discord.User) -> None:
        super().__init__(timeout=None)
        self.user = user
    
    async def on_submit(self, interaction: Interaction) -> None:
        answer = str(self.answer)
        dm = await self.user.create_dm()
        await dm.send(f"**{interaction.user.mention}からの返信(役職変更希望)**\n```\n{answer}\n```", view=ResponceBtn(user=interaction.user))
        await interaction.response.send_message("返信しました", ephemeral=True)
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Replay({answer})")


class RejectModal(discord.ui.Modal, title="却下する理由を返信します"):
    answer = discord.ui.TextInput(label="理由を入力してください(任意)", style=discord.TextStyle.long, placeholder="任意...", required=False)
    def __init__(self, user: discord.User) -> None:
        super().__init__(timeout=None)
        self.user = user
    
    async def on_submit(self, interaction: Interaction) -> None:
        answer = str(self.answer)
        
        try:
            with open("Config/rejected.json") as f:
                rejectedusers = json.load(f)
        except Exception:
            rejectedusers = []
        
        rejectedusers.append(self.user.id)
        with open("Config/rejected.json", "w") as f:
            json.dump(rejectedusers, f, indent=4)

        dm = await self.user.create_dm()
        if len(answer) < 1:
            answer = "(提供された理由なし)"
        await dm.send(f"__**{interaction.user.mention}より、役職変更希望の却下の通知**__\n```\n{answer}\n```")
        await interaction.response.send_message("却下しました")
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Reject({answer})")


class ResponceBtn(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label = "返信する", style = discord.ButtonStyle.green)
    async def replay(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            with open("Config/rejected.json") as f:
                rejectedusers = json.load(f)
        except Exception:
            rejectedusers = []
        if interaction.user.id in rejectedusers:
            await interaction.response.send_message("これ以上返信できません", ephemeral=True)
            return
        if self.user.id in rejectedusers:
            await interaction.response.send_message("これ以上返信できません", ephemeral=True)
            return
        await interaction.response.send_modal(ChatModal(user=self.user))
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Replay()")
    
    @discord.ui.button(label = "却下する", style = discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            with open("Config/rejected.json") as f:
                rejectedusers = json.load(f)
        except Exception:
            rejectedusers = []
        
        if not interaction.user.id in [805680950238642188, 723448498879463425]:
            await interaction.response.send_message("Oops! This is a wrong button!", ephemeral=True)
            return
        if self.user.id in rejectedusers:
            await interaction.response.send_message("既に却下されています", ephemeral=True)
            return

        await interaction.response.send_modal(RejectModal(user=self.user))
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Reject()")


class ChangeRoleModal(discord.ui.Modal, title="役職変更の希望を管理者に送信します"):
    answer = discord.ui.TextInput(label="役職となりたい理由を入力してください", style=discord.TextStyle.long, placeholder="役職, なりたい理由...", required=True, min_length=1)
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    async def on_submit(self, interaction: Interaction) -> None:
        answer = str(self.answer)
        mochi = client.get_user(723448498879463425)
        kanoki = client.get_user(805680950238642188)
        
        try:
            with open("Config/rejected.json") as f:
                rejectedusers = json.load(f)
        except Exception:
            rejectedusers = []

        if interaction.user.id in rejectedusers:
            rejectedusers.remove(interaction.user.id)

        with open("Config/rejected.json", "w") as f:
            json.dump(rejectedusers, f, indent=4)
        
        dm = await mochi.create_dm()
        await dm.send(f"**{interaction.user.mention}の役職変更希望**\n```\n{answer}\n```", view=ResponceBtn(user=interaction.user))
        dm = await kanoki.create_dm()
        await dm.send(f"**{interaction.user.mention}の役職変更希望**\n```\n{answer}\n```", view=ResponceBtn(user=interaction.user))

        await interaction.response.send_message("要望の送信に成功しました", ephemeral=True)
        embed = discord.Embed(title="管理者たちに役職変更の希望を送信しました", description="このBOTから、彼らからの返信が届きます", color=0xff00ff)
        dm = await interaction.user.create_dm()
        await dm.send(embed=embed)
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => ResponceBtn(answer={answer})")


class ShowRoleDes(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label = "ルームリーダー一覧", style = discord.ButtonStyle.secondary)
    async def roomleaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        global Ldescription

        Lembed = discord.Embed(title="ルームリーダー一覧", description=Ldescription, color=0x228b22)

        await interaction.response.send_message(embed=Lembed, ephemeral=True)
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => ShowRoleDes().roomleaderboard()")

    @discord.ui.button(label = "役職一覧", style = discord.ButtonStyle.secondary)
    async def roleleaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        global description
        embed = discord.Embed(title="役職一覧", description=description, color=0x8a2be2)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => ShowRoleDes().roleleaderboard()")

    @discord.ui.button(label = "役職変更のお問い合わせ", style = discord.ButtonStyle.red)
    async def changerolesubmit(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(1118870578519089233)
        if not role in interaction.user.roles: 
            await interaction.response.send_message("まだ役職がありません", ephemeral=True)
            return
            
        await interaction.response.send_modal(ChangeRoleModal())
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => ChangeRoleModal()")






class Replytocreativeapproval(discord.ui.View):
    def __init__(self, to: discord.Member, msg: discord.Message):
        super().__init__(timeout=None)
        self.to = to
        self.msg = msg

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def createticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Replytocreativeapproval_Accept()")

        try:
            with open("creative_approval.json") as f:
                j = json.load(f)
        except FileNotFoundError:
            j = {}

        if self.msg.id in list(map(int, j.keys())):
            by = j[str(self.msg.id)]
            await interaction.response.send_message(f"The replyed appication has already been responded by {client.get_user(int(by)).mention}.")
            return
        j[str(self.msg.id)] = interaction.user.id
        with open("creative_approval.json", "w") as f:
            json.dump(j, f, indent=4)
        dm = await self.to.create_dm()
        await dm.send("クリエイティブ申請が受理され、オペレーターにより承認されました！")
        await interaction.response.send_message(f"The replyed appication has been approved by {interaction.user.mention}.")

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def createticketr(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => Replytocreativeapproval_Reject()")

        try:
            with open("creative_approval.json") as f:
                j = json.load(f)
        except FileNotFoundError:
            j = {}

        if self.msg.id in list(map(int, j.keys())):
            by = j[str(self.msg.id)]
            await interaction.response.send_message(f"The replyed appication has already been responded by {client.get_user(int(by)).mention}.")
            return
        j[str(self.msg.id)] = interaction.user.id
        with open("creative_approval.json", "w") as f:
            json.dump(j, f, indent=4)
        dm = await self.to.create_dm()
        await dm.send("クリエイティブ申請が受理されましたが、オペレーターにより拒否されました。")
        await interaction.response.send_message(f"The replyed appication has been rejected by {interaction.user.mention}.")




class MITcreativeapprovalModal(discord.ui.Modal, title="クリエイティブを使用するにあたって"):
    answer = discord.ui.TextInput(label="理由(用途)を記述してください", style=discord.TextStyle.long, placeholder=None, required=True, min_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        self.answer = str(self.answer)
        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} made a ticket. at MIT reason: {self.answer}")

        channel = interaction.guild.get_channel(1129061838496202802)
        embed = discord.Embed(title="件名: クリエイティブ申請", description=f"From: {interaction.user.mention}\n理由:\n```{self.answer}```")
        msg = await channel.send(embed=embed)
        await msg.edit(view=Replytocreativeapproval(interaction.user, msg))
        await interaction.response.send_message(f"管理者に送信されました。\n結果までしばらくお待ちください", ephemeral=True)


class MITcreativeapproval(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="申請をする", style=discord.ButtonStyle.green)
    async def buttonwww(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(MITcreativeapprovalModal())


class MITcreateticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Make a Ticket", style=discord.ButtonStyle.green)
    async def createticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} => MITticketModal()")

        await interaction.response.send_modal(MITticketModal())




class MITticketModal(discord.ui.Modal, title="Write down your reason"):
    answer = discord.ui.TextInput(label="write your reason here (required)", style=discord.TextStyle.long, placeholder=None, required=True, min_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        self.answer = str(self.answer)
        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} made a ticket. at MIT reason: {self.answer}")

        await interaction.response.defer(thinking=True, ephemeral=True)

        guild = interaction.user.guild
        role = guild.get_role(1127590580910829608)  #Support

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        
        KANOKI = guild.get_member(805680950238642188)
        mochi = guild.get_member(723448498879463425)

        userid = interaction.user.id

        opennerid = interaction.user.id

        openner = interaction.user

        category = guild.get_channel(1129093089605206177)
        na = interaction.user.nick
        if not na:
            na = interaction.user.global_name

        ticketchannel = await category.create_text_channel(name=na.replace(".", "") + "-" + str(int(userid)), overwrites=overwrites)

        ticketchannel_id = ticketchannel.id

        ticketfile = inspect.cleandoc(f"""tickets/{ticketchannel.id}_ticketmsgcache.txt""")

        with open("ticket_channelids.json") as f:
            po = list(map(int, json.load(f)))
            if ticketchannel.id not in po:
                po.append(ticketchannel.id)
        with open("ticket_channelids.json", "w") as f:
            json.dump(po, f, indent=4)

        with open(ticketfile, "w"):
            pass

        mention = role.mention
        opennermention = interaction.user.mention
        nowtime = time.time()

        ticketembed = discord.Embed(title=f"Ticket | {na}", description=f"Hello {openner.mention}! Thank you for contacting support.", color=0xffaa00)
        ticketembed.add_field(name="Reason:", value=f"```{self.answer}```\nIf you wants to close this ticket, use the button below.")

        await ticketchannel.send(embed=ticketembed, view=MITcloseaticketconfirm(openner, ticketfile, nowtime, ticketchannel))

        await interaction.followup.send("Created a new ticket at " + ticketchannel.mention, ephemeral=True)


class MITcloseaticketconfirm(discord.ui.View):
    def __init__(self, openner: discord.Member, filename: str, nowtime: float, ticket_channel: discord.channel):
        super().__init__(timeout = None)
        self.openner = openner
        self.filename = filename
        self.nowtime = nowtime
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="Close", emoji="<:trashbox:1129096572098060469>", style=discord.ButtonStyle.red)
    async def closeaticketconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} wants to close the ticket.")

        if str(int(self.openner.id)) in str(int(interaction.user.id)):
            await interaction.response.send_message("__close ticket confirmation__", view=MITcloseaticket(self.openner, self.filename, self.nowtime, self.ticket_channel))

        else:
            await interaction.response.send_message(inspect.cleandoc(f"""__close ticket confirmation__
            **You aren't this ticket's owner**"""), view=MITcloseaticket(self.openner, self.filename, self.nowtime, self.ticket_channel))


class MITcloseaticket(discord.ui.View):
    def __init__(self, openner: discord.Member, filename: str, nowtime: float, ticket_channel: discord.channel):
        super().__init__(timeout = None)
        self.openner = openner
        self.filename = filename
        self.nowtime = nowtime
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="Yes, close", emoji="<:trashbox:1129096572098060469>", style=discord.ButtonStyle.red)
    async def closeaticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} closed the ticket. at MIT")
        
        if str(int(self.openner.id)) in str(int(interaction.user.id)):
            await interaction.response.send_message(inspect.cleandoc(f"""Closing your ticket, please wait..."""))

        else:
            await interaction.response.send_message(f"Closing {self.openner.mention}'s ticket, please wait...")

        dm = await interaction.user.create_dm()
        KANOKI = interaction.guild.get_member(805680950238642188)
        mochi = interaction.guild.get_member(723448498879463425)

        with open("ticket_channelids.json") as f:
            po = list(map(int, json.load(f)))
            if self.ticket_channel.id in po:
                po.remove(self.ticket_channel.id)
        with open("ticket_channelids.json", "w") as f:
            json.dump(po, f, indent=4)

        with open(self.filename, 'rb') as f:
            file = discord.File(f)
            await KANOKI.send(inspect.cleandoc(f"""{self.openner.name}'s ticket cache(created at <t:{int(self.nowtime)}:F>)"""), file=file)
        with open(self.filename, 'rb') as f:
            file = discord.File(f)
            await dm.send(inspect.cleandoc(f"""**Thank you for using ticket and you can read ticket message contents with the attached file**"""), file=file)
        with open(self.filename, 'rb') as f:
            file = discord.File(f)
            await mochi.send(inspect.cleandoc(f"""{self.openner.name}'s Ticket cache(created at <t:{int(self.nowtime)}:F>)"""), file=file)

        with open(self.filename, "r") as f:
            d = f.read()
        with open(f"Cache/Ticket/cache-{self.filename}", "w") as f:
            f.write(str(d))

        os.remove(self.filename)

        await asyncio.sleep(3)

        await self.ticket_channel.delete()






#custom emojis
javaicon = "<:java:1084395558233444362>"
bedrockicon = "<:bedrock:1084395920306737193>"
switchicon = "<:switch:1084397372580319242>"
aternosicon = "<:aternos:1084397727087087626>"

#intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.presences = True

client = commands.Bot(command_prefix="!", intents=intents)

#ipembed
ipembed = discord.Embed(title=aternosicon + " サーバーの入り方",description="統合版とjava版どちらでも参加できます", color=0x00ff00)
ipembed.add_field(name=bedrockicon + " 統合版",value="遊ぶ➤サーバー➤下のサーバー追加で下のipを入力➤サーバーに接続")
ipembed.add_field(name=javaicon + " java版",value="下のサーバーipを入力")
ipembed.add_field(name=bedrockicon + " 統合版のip",value=(inspect.cleandoc(f"""**サーバーIP**: SetasabaForEvent.aternos.me
_**ポート**_: 46306""")),inline=False)
ipembed.add_field(name=javaicon + " java版のip",value="SetasabaForEvent.aternos.me:46306")
ipembed.add_field(name=switchicon + " **注意**:Switch版",value=(inspect.cleandoc(f"""Switch版ではデフォルトで**サーバー追加**がないです
[こちら](https://kotoyasyou.work/archives/4873)を参考にしてください""")),inline=False)
ipembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/971597070811168770/1082284879061979178/MOJANG.gif")

Ldescription = inspect.cleandoc(f"""
    <@&1119182179273027655>
        ➤<@805680950238642188>
    
    <@&1119209600386863115>
        ➤<@1065256151056396300>
                                
    <@&1119209874656604210>
        ➤<@967738166318608384>
                                
    <@&1119210349577654362>
        ➤<@723448498879463425>
                                
    <@&1119210635415265392>
        ➤<@762554401054523392>
""")

description = inspect.cleandoc(f"""
    <@&1101414407860396074>
        本団体の代表であり、本企画の最高責任者です。
    
    <@&1105785994369839106>
        本団体の副代表であり、進行管理やマネジメントを行います。
                                
    <@&1105789722657304678>
        ゲーム開発を行います
                                
    <@&1118902886714331197>
        表示されるサイトのデザインを行います。
    
    <@&1118934733108297879>
        ムービーや戦闘など様々な場面での演出制作を担当します。   

    <@&1105790371100897453>
        キャラクターや背景素材などグラフィックスの制作を担当します。

    <@&1118900539028148367>
        ARマーカーやAR上の演出、3Dグラフィックスの制作を担当します。

    <@&1111149742542565456>
        企画内や広報で使用するムービーを制作を担当します。

    <@&1118936362700247050>
        ゲームのシナリオを作成します。        

    <@&1118901236335386655>
        ボイスを担当します。

    <@&1119173669214760970>  
        ゲーム内やムービー内で使用するBGMや効果音を担当します。 

    <@&1118903186233761873>
        必要な時にマネージャーや各ルームリーダーの指示に従って補佐を行います。また、デバッカーを担当します。                                                                                                                                                     
""")

@client.event
async def on_ready():
    """bot hired"""

    print(f"[{timestr()}] {Fore.GREEN}<Coturnix system> Processinigon_ready...{Fore.RESET}")

    a_client.set_client(client)
    for func in (set_client1, set_client2, set_client3, set_client4, set_client5, Shishiji.set_client6):
        func(client)

    global PORT, HTTPHandler
    server_thread = threading.Thread(target=start, args=(PORT, HTTPHandler))
    server_thread.daemon = True
    server_thread.start()

    print(f"[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} {Fore.YELLOW}Updating preserved buttons...{Fore.RESET}")

    class G(discord.ui.View):
        def __init__(self, *, ticket_line: discord.CategoryChannel, support_role: discord.Role, cache_channel: discord.channel.TextChannel | None = None):
            super().__init__(timeout=None)
            self.ticket_line, self.support_role, self.cache_channel = ticket_line, support_role, cache_channel

        @discord.ui.button(label="Create Ticket", emoji="<:ticket_:1129107340415733770>", style=discord.ButtonStyle.primary)
        async def _o(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(TicketModal(ticket_line=self.ticket_line, support_role=self.support_role, cache_channel=self.cache_channel))

    #try:
    path = "./SHISHIJI/role_btn_preserved.json"
    try:
        with open(path) as f:
            AKK: typing.List[typing.Dict[str, str | int]] = json.load(f)
        for dic in AKK:
            guild_id: int = dic["guild_id"]
            channel_id: int = dic["channel_id"]
            message_id: int = dic["message_id"]
            message_: str = dic["message"]
            label: str = dic["label"]
            channel = client.get_guild(guild_id).get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            class b(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                    self.guild = client.get_guild(1153884392448606238)
                    self.done = self.guild.get_role(1161599033152913448)

                @discord.ui.button(label=label, style=discord.ButtonStyle.blurple)
                async def e(self, interaction: Interaction, button: discord.Button):
                    if self.done in interaction.user.roles:
                        await interaction.response.send_message(f"あなたは選択を済ませています。\n間違いだと思われる場合は<@805680950238642188>へお問い合わせください。", ephemeral=True)
                        return
                    await interaction.response.send_message(view=Shishiji.Shishiji_Roles().create_select(client)(), ephemeral=True)
            await message.edit(content=message_, view=b())
    except Exception:...

    try:
        with open("./ticket_createButtons.json") as f:
            j = json.load(f)
        for l in j:
            try:
                category = client.get_channel(l["category"])
                role = category.guild.get_role(l["role"])
                channel = client.get_channel(l["channel"])
                message = await channel.fetch_message(l["message"])
                cache_channel = None
                if l.get("cache", None):
                    cache_channel = client.get_channel(l["cache"])
                await message.edit(view=G(ticket_line=category, support_role=role, cache_channel=cache_channel))
            except Exception as e:
                continue
    except FileNotFoundError:
        pass

    try:
        with open("./ticket_closers.json") as f:
            p = json.load(f)
        for u in p:
            try:
                channel = client.get_channel(u["channel"])
                message = await channel.fetch_message(u["message"])
                creator = channel.guild.get_member(u["creator"])
                await message.edit(view=TicketCloseConfirm(channel=channel, creator=creator))
            except Exception:
                continue
    except FileNotFoundError:
        pass

    try:
        with open("absents.json") as f:
            p = json.load(f)
        for u in p:
            try:
                channel = client.get_channel(u["channel"])
                message = await channel.fetch_message(u["message"])
                await message.edit(view=IDontAttendToday(u["date"], u["fp"], u["title"], u["color_code"]))
            except Exception:
                continue
    except FileNotFoundError:
        pass

    try:
        with open("Tags/poll_tags.json") as f:
            k: dict = json.load(f)
        for j in k.keys():
            try:
                channel = client.get_channel(int(k[j]["channel_id"]))
                message = await channel.fetch_message(int(k[j]["message_id"]))
                
                with open(f"poll/{k[j]['question']}_poll.json") as f:
                    vals: dict = json.load(f)
                if k[j]["isthree"]:
                    await message.edit(
                        view=
                        PollSelect_three(
                            question=k[j]["question"],
                            option1=vals["options"]["#1"],
                            option2=vals["options"]["#2"],
                            option3=vals["options"]["#3"],
                            message=message,
                            madeby=client.get_user(k[j]["madeby"]),
                            tag=j
                        ))
                elif k[j]["isfour"]: 
                    await message.edit(
                        view=
                        PollSelect_four(
                            question=k[j]["question"],
                            option1=vals["options"]["#1"],
                            option2=vals["options"]["#2"],
                            option3=vals["options"]["#3"],
                            option4=vals["options"]["#4"],
                            message=message,
                            madeby=client.get_user(k[j]["madeby"]),
                            tag=j
                        ))
                else:
                    await message.edit(
                        view=
                        PollSelect(
                            question=k[j]["question"],
                            option1=vals["options"]["#1"],
                            option2=vals["options"]["#2"],
                            message=message,
                            madeby=client.get_user(k[j]["madeby"]),
                            tag=j
                        ))
            except Exception as e:
                continue
    except FileNotFoundError:
        pass

    try:
        with open("survey_messages.json") as f:
            datas = json.load(f)
            for data in datas:
                title = data["title"]
                _description = data["description"]
                anonymous = data["anonymous"]
                channel = client.get_channel(int(data["channel_id"]))
                message = await channel.fetch_message(int(data["message_id"]))
                madeby = client.get_user(int(data["madeby"]))
                dm = await madeby.create_dm()
                dmmsg = await dm.fetch_message(data["dmmsg"])

                await message.edit(view=CustomAnswer(title=title, description=_description, madeby=madeby, channel=channel))
                await dmmsg.edit(view=EndCustomAnswer_Conf(title=title, description=_description, madeby=madeby, message=message))
    except Exception:...

    #サーバーボタン
    channel = client.get_channel(1082650639676477540)
    message = await channel.fetch_message(1087918892623613994)
    await message.edit(content=f"**ただいまトラブルが発生しております。復旧の目処は立っておりません**\n`Last update`: <t:{int(current_unix_time)}:R>", view=Disabled_eventservbuttons())
    '''
    await message.edit(content=inspect.cleandoc(f"""
            サーバーへようこそ！
            サーバーは5分間誰もいないと自動で閉鎖されます。下のボタンを使うとこでサーバーを操作することができます
            (ボタンの処理には数秒かかります。我慢してください)
            
            """), view = eventservbuttons())
    '''

    channel = client.get_channel(1153910708816318574)
    message = await channel.fetch_message(1153925069828010054)
    await message.edit(content="", view=Shishiji.RegisterBtn())


    channel = client.get_channel(1228365649181675570)
    message = await channel.fetch_message(1228374571003019396)
    await message.edit(content="", view=Shishiji.MemberVisibleInfoUpdater())


    channel = client.get_channel(1101755461876842507)
    message = await channel.fetch_message(1101756183251013682)
    admin_role = channel.guild.get_role(1101414407860396074)

    await message.edit(content=f"下のボタンで名前を登録し、なりたい役職を選んでください", view=SETAGAQUESTRegisterNickName())

    #名誉サバイバル市民
    channel = client.get_channel(1077140061394571315)
    message = await channel.fetch_message(1085185734912266321)

    await message.edit(content=inspect.cleandoc(f"""読み終わったら押してください！"""), view = meiyorole())

    #チケットを作成
    channel = client.get_channel(1085437616079523951)
    message = await channel.fetch_message(1085437887052517387)
    guild = client.get_guild(1076379360904364164)
    support = guild.get_role(1085461267176755252)
    mention = support.mention

    await message.edit(content=inspect.cleandoc(f"""サポートへようこそ！
    下のボタンを使ってチケットを作成してください。
    チケットでは__**チャンク購入**__のほか、__どんな問題や質問、訴訟__でも、{mention}が対処します。
    """), view = makeaticket())

    #MCmusic------
    #SGマイクラ---
    #MCmusic
    channel = client.get_channel(1086972254811869284)
    message = await channel.fetch_message(1091303466292478103)

    await message.edit(content=inspect.cleandoc(f"""Minecraft"""), view=MCmusic())

    #FGmusic
    channel = client.get_channel(1086972254811869284)
    message = await channel.fetch_message(1091303488786538536)

    await message.edit(content=inspect.cleandoc(f"""Fall Guys"""), view=FGmusic())

    #Dancing Disco---
    #MCmusic
    channel = client.get_channel(1078252040200912928)
    message = await channel.fetch_message(1091301220364324975)

    await message.edit(content="Minecraft", view=MCmusic())

    #FGmusic
    channel = client.get_channel(1078252040200912928)
    message = await channel.fetch_message(1091302293493784576)

    await message.edit(content="Fall Guys", view=FGmusic())

    channel = client.get_channel(1098507125266858106)
    message = await channel.fetch_message(1098884369692762113)
    channel_for_mention = client.get_channel(1099721782732275773)
    await message.edit(content=inspect.cleandoc(f"""このボタンをおしたあと、DMを確認してください
    <登録の仕方: {channel_for_mention.mention}>"""), view=RegisterWithDM())

    channel = client.get_channel(1127591546733211649)
    message = await channel.fetch_message(1127598653255733298)
    await message.edit(
        content=f"[ @everyone ]\n**__MITマインクラフト__へようこそ！\n下のボタンを押してマインクラフトのユーザー名を登録してください。\n__統合版の方__は___マイクロソフトアカウントのゲーマータグ___の前に「.」(ドット)をつけてください**\n※登録すると利用可能な全てのチャンネルが閲覧できるようになります",
        view=SMGnickname()
    )

    channel = client.get_channel(1118877099487408178)
    message = await channel.fetch_message(1127915346452545578)
    d = "イベント内容: イベント内容: イベント内容: ・一週間の成果報告 ・情報共有 を行います。 全員出席するようにお願いします。"
    url = "https://discord.gg/N7Na7R9t?event=1127576142614908978"
    color_code = discord.Color.random()
    embed = discord.Embed(title=f"第二回 総会 イベントに関して", description=f"欠席連絡をする場合は以下からお願いします\n※必ずイベントが始まる前に連絡してください", color=color_code)
    embed.add_field(name="詳細", value=f"開始日時: <t:1689508800:F>\nイベント内容: {d}\n{url}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1083021323967672421/1126034721462300772/logo.png")
    await message.edit(content="[ @everyone ]", embed=embed, view=IDontAttendToday(1689508800, "./absent/1689508800_第二回 総会_3_userIDs.json", "第二回 総会", color_code))

    channel = client.get_channel(1129061298064326656)
    message = await channel.fetch_message(1129394034461397072)
    await message.edit(content="**下のボタンを押して申請をしてください**", view=MITcreativeapproval())

    channel = client.get_channel(1130153447560327198)
    message = await channel.fetch_message(1130153848388976670)
    #await message.edit(content=f"Welcome to MIT Minecraft Support.\n\
#Use the button below to get help with any issues or questions you have.", view=MITcreateticket())
    print(f"[{timestr()}] {Fore.GREEN}<Coturnix system> All Updates were done.{Fore.RESET}")
    
   
    def _ask():
        while "hello":
            try:
                requests.get("http://tickets.kanokiw.com:2293/")
                requests.get("http://code.kanokiw.com:2293/")
            except Exception as e:
                print(inspect.cleandoc(
                    f"""{Fore.RED}http://tickets.kanokiw.com:2293/: connection timeout, please solve this issue.
                    Retrying in 120 seconds.
                    exc: {e.__class__} --{e}{Fore.RESET}"""
                ))
            time.sleep(30)

    while True:
        """
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="寝返り",
                assets={
                    "large_image": "cleanix",
                    "large_text": "Coturnix",
                    "small_image": "coturnix_craft",
                    "small_text": "KANOKIw"
                }
            )
        )"""

        channel = client.get_channel(1101755461876842507)
        message = await channel.fetch_message(1101756183251013682)

        await message.edit(content=f"下のボタンで名前を登録し、なりたい役職を選んでください", view=SETAGAQUESTRegisterNickName())

        channel = client.get_channel(1119203403571134515)
        message = await channel.fetch_message(1119259756742312007)

        global Ldescription
        global description
            
        embed = discord.Embed(title="役職一覧", description=description, color=0x8a2be2)
        Lembed = discord.Embed(title="ルームリーダー一覧", description=Ldescription, color=0x228b22)

        await message.edit(embeds=(Lembed, embed), view=ShowRoleDes())

        await asyncio.sleep(120)


@client.event
async def on_member_join(member: discord.Member):
    global censorship
    if censorship is True:
        if member.guild.id == 1078251724801847326:
            if member.id == 856826942967906314:
                await member.kick(reason="あほ")
                return
    
    if member.guild.id == 1153884392448606238:
        channel = client.get_channel(1153952454346559508)
        await channel.send(f"```diff\n+ <@{member.id} '{member.global_name}'> joined the server\n```")
        role = member.guild.get_role(1158538895017902081)
        await member.add_roles(role)
    
    if member.guild.id == 1098507124532842588:
        channel = client.get_channel(1098507125266858106)
        dm = await member.create_dm()
        kanoki = client.get_user(805680950238642188)
        helloembed = discord.Embed(title=f"ようこそ！{member.mention}さん", description=inspect.cleandoc(f"""[チャンネル](https://discord.gg/GCnUmwDght)
        {channel.mention}
        ↑ のチャンネルで登録を完了してください"""), color=0x98765)
        helloembed.add_field(name="サーバー参加日時", value=f"<t:{int(time.time())}:F>")
        await dm.send(embed=helloembed)

    if member.guild.id == 1101399573991268374:
        channel = client.get_channel(1101755461876842507)
        dm = await member.create_dm()
        mochi = client.get_user(723448498879463425)
        message = inspect.cleandoc(f"""
            こんにちは {member.mention}。セタガクエストプロジェクトマネージャーの山本耕大({mochi.mention})です。
            この度は本企画にご参加頂きまして誠にありがとうございます。
            サーバーにて名前登録ボタンを押し、名前と自分の役職を選択するようにお願い申し上げます。
            企画の成功に向けてご協力を賜わりますようお願い申し上げます。
            """)
        
        await dm.send(f"{message}")
    


@client.event
async def on_member_remove(member: discord.Member):
    global censorship
    if censorship is True:
        if member.guild.id == 1078251724801847326:
            if member.id == 856826942967906314:
                channel = client.get_channel(1078251725250646047)
                banembed = discord.Embed(title=f"✅ {member.name} was banned", color=0x98765)
                await channel.send(embed=banembed)
                return
    if member.guild.id == 1153884392448606238:
        channel = client.get_channel(1153952454346559508)
        await channel.send(f"```diff\n- {member.mention} <@{member.id} {member.global_name}> left the server.```")
            
        
    if member.guild.id == 1098507124532842588:
        channel = client.get_channel(1098579941714579516)
        await channel.send(f"```diff\n- <@{member.id} '{member.global_name}'> left the server\n```")

    if member.guild.id == 1101399573991268374:
        channel = client.get_channel(1101747278722641970)
        await channel.send(f"```diff\n- <@{member.id} '{member.global_name}'> left the server\n```")


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceChannel, after: discord.VoiceChannel):
    try:
        after.channel.id
    except AttributeError:
        return
    
    guild = after.channel.guild
    role_registered = guild.get_role(1098532985629839441)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role_registered: discord.PermissionOverwrite(view_channel=True, speak=True)
        }
    
    role_member = guild.get_role(1101419218253131846)
    overwrites_setagaquest = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role_member: discord.PermissionOverwrite(view_channel=True, speak=True)
        }
        
    no_limit_room_id = (
        1092800303419621447,
        1092810253789306890,
        1098508217027412008,
        1101399574897250377,
        1153961409953153044
        )
    
    if after.channel.id in no_limit_room_id:
        new_vc_name = f"{member.display_name}'s Room"
        if after.channel.id == 1098508217027412008:
            category = after.channel.guild.get_channel(1098507125266858112)
            new_vc = await category.create_voice_channel(name=new_vc_name, overwrites=overwrites)
        elif after.channel.id == 1101399574897250377:
            new_vc = await after.channel.category.create_voice_channel(name=new_vc_name, overwrites=overwrites_setagaquest)
        else:
            new_vc = await after.channel.category.create_voice_channel(name=new_vc_name)
        await member.move_to(new_vc)
        print(f"\n[{timestr()}] {Fore.LIGHTBLUE_EX}Created VC{Fore.RESET} {Fore.CYAN}{new_vc_name}{Fore.RESET} in {guild.name}")

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)

    try:
        after.channel.id
    except AttributeError:
        return
    
    if after.channel.id == 1093069431074197534 or after.channel.id == 1093072187218481214:
        new_vc_name = f"Chilling {member.display_name}"
        new_vc = await after.channel.category.create_voice_channel(name=new_vc_name, user_limit=1, overwrites=overwrites)
        print(f"\n[{timestr()}] {Fore.LIGHTBLUE_EX}Created Chill{Fore.RESET} {Fore.CYAN}{new_vc_name}{Fore.RESET} in {guild.name}")
        
        await member.move_to(new_vc)

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)

    try:
        after.channel.id
    except AttributeError:
        return

    if after.channel.id == 1098509049642889236:
        new_vc_name = f"{member.display_name}'s Room"
        category = after.channel.guild.get_channel(1098508677029314580)
        new_vc = await category.create_voice_channel(name=new_vc_name, user_limit=2, overwrites=overwrites)
        await member.move_to(new_vc)
        print(f"\n[{timestr()}] {Fore.LIGHTBLUE_EX}Created limit: 2 VC{Fore.RESET} {Fore.CYAN}{new_vc_name}{Fore.RESET} in {guild.name}")

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)

    try:
        after.channel.id
    except AttributeError:
        return
    
    if after.channel.id == 1098511657845674075:
        new_vc_name = f"{member.display_name}'s Room"
        category = after.channel.guild.get_channel(1098511598718566411)
        new_vc = await category.create_voice_channel(name=new_vc_name, user_limit=3, overwrites=overwrites)
        await member.move_to(new_vc)
        print(f"\n[{timestr()}] {Fore.LIGHTBLUE_EX}Created limit: 3 VC{Fore.RESET} {Fore.CYAN}{new_vc_name}{Fore.RESET} in {guild.name} in {guild.name}")

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)

    try:
        after.channel.id
    except AttributeError:
        return

    if after.channel.id == 1098511886942732318:
        new_vc_name = f"{member.display_name}'s Room"
        category = after.channel.guild.get_channel(1098511858169823303)
        new_vc = await category.create_voice_channel(name=new_vc_name, user_limit=4, overwrites=overwrites)
        await member.move_to(new_vc)
        print(f"\n[{timestr()}] {Fore.LIGHTBLUE_EX}Created limit: 4 VC{Fore.RESET} {Fore.CYAN}{new_vc_name}{Fore.RESET} in {guild.name}")

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)

    if after.channel.id == 1160137460395815002:
        name = member.nick
        cate = client.get_channel(1160139309425377350)
        if name is None:
            name = member.global_name
        ch_name = f"会議室 - {name}"
        overwrites = {member.guild.get_role(1158538895017902081): discord.PermissionOverwrite(view_channel=False)}
        new_vc = await cate.create_voice_channel(name=ch_name, overwrites=overwrites, user_limit=50)
        await member.move_to(new_vc)
        await asyncio.sleep(1)

        while True:
            if len(new_vc.members) == 0:
                await new_vc.delete()
                print(f"\n[{timestr()}] {Fore.RED}Deleted{Fore.RESET} {Fore.CYAN}{new_vc.name}{Fore.RESET} in {guild.name}")
                break

            await asyncio.sleep(1)





class Class_disabled(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "A", style = discord.ButtonStyle.green, custom_id = "AGUMI", disabled=True)
    async def AGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "B", style = discord.ButtonStyle.green, custom_id = "BGUMI", disabled=True)
    async def BGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "C", style = discord.ButtonStyle.green, custom_id = "CGUMI", disabled=True)
    async def CGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "D", style = discord.ButtonStyle.green, custom_id = "DGUMI", disabled=True)
    async def DGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "E", style = discord.ButtonStyle.green, custom_id = "EGUMI", disabled=True)
    async def EGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "F", style = discord.ButtonStyle.green, custom_id = "FGUMI", disabled=True)
    async def FGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "G", style = discord.ButtonStyle.green, custom_id = "GGUMI", disabled=True)
    async def GGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    


class Class_again(discord.ui.View):
    def __init__(self, name: str, message: discord.Message):
        super().__init__(timeout = None)
        self.name = name; self.message = message

    @discord.ui.button(label = "A", style = discord.ButtonStyle.green, custom_id = "AGUMI")
    async def AGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"A_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "B", style = discord.ButtonStyle.green, custom_id = "BGUMI")
    async def BGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"B_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "C", style = discord.ButtonStyle.green, custom_id = "CGUMI")
    async def CGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"C_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "D", style = discord.ButtonStyle.green, custom_id = "DGUMI")
    async def DGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"D_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "E", style = discord.ButtonStyle.green, custom_id = "EGUMI")
    async def EGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"E_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "F", style = discord.ButtonStyle.green, custom_id = "FGUMI")
    async def FGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"F_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


    @discord.ui.button(label = "G", style = discord.ButtonStyle.green, custom_id = "GGUMI")
    async def GGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"G_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = discord.utils.utcnow()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nThank you for taking the time")


def int_to_rgb(integer_value: int) -> str:
    red = (integer_value >> 16) & 0xFF
    green = (integer_value >> 8) & 0xFF
    blue = integer_value & 0xFF
    return f"rgb({red}, {green}, {blue})"


def replaceWithName(text: str, message: discord.Message):
    if not text:
        return ""
    for i in range(0, len(text)):
        char = text[i]
        if char == "<":
            r = ""
            d = False
            t = text[i+1]
            for u in text[i+2:]:
                if u == ">":
                    break
                r += u
            else:
                continue
            if r[0] == "&":
                d = True
                r = r[1:]
            try:
                r = int(r)
            except ValueError:
                continue
            res = ""
            color = ""
            try:
                if t == "#":
                    name = client.get_channel(r).name
                elif d:
                    rl = message.guild.get_role(r)
                    name = rl.name
                    color = f' style="color: {int_to_rgb(rl.color.value)};"'
                else:
                    name = client.get_user(r).display_name
                res = f'<span class="user--mention pointer-w-hovered"{color}>{"@" if t != "#" else "#"}{name if name else "Unknown"}</span>'
            except Exception:
                res = f'<span class="user--mention pointer-w-hovered">{"@" if t != "#" else "#"}Unknown</span>'
            text = text.replace(f"<@{r}>", res)
            text = text.replace(f"<#{r}>", res)
            text = text.replace(f"<@&{r}>", res)

    return text.replace("@everyone", '<span class="user--mention pointer-w-hovered">@everyone</span>').replace("@here", '<span class="user--mention pointer-w-hovered">@here</span>')


def _replaceWithName(text: str, message: discord.Message):
    if not text:
        return ""
    for i in range(0, len(text)):
        try:
            char = text[i]
        except IndexError:
            break
        if char == "<":
            r = ""
            d = False
            t = text[i+1]
            for u in text[i+2:]:
                if u == ">":
                    break
                r += u
            else:
                continue
            if r[0] == "&":
                d = True
                r = r[1:]
            try:
                r = int(r)
            except ValueError:
                continue
            res = ""
            color = ""
            try:
                if t == "#":
                    name = client.get_channel(r).name
                elif d:
                    rl = message.guild.get_role(r)
                    name = rl.name
                    color = f' style="color: {int_to_rgb(rl.color.value)};"'
                else:
                    name = client.get_user(r).display_name
                res = f'*??++{color}>{"@" if t != "#" else "#"}{name if name else "Unknown"}--??*'
            except Exception:
                res = f'*??++>{"@" if t != "#" else "#"}Unknown--??*'
            text = text.replace(f"<@{r}>", res)
            text = text.replace(f"<#{r}>", res)
            text = text.replace(f"<@&{r}>", res)

    return text.replace("@everyone", '*??++>@everyone--??*').replace("@here", '*??++>@here--??*')


def add_links_to_urls(text: str):
    if not text:
        return ""
    url_regex = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    urls = re.findall(url_regex, text)
    _l = []
    for url in urls:
        if url in _l:
            continue
        _l.append(url)
        link = f'<a href="{url}" target="_blank"><attachment>{url}</attachment></a>'
        text = text.replace(url, link)
    
    return text


def _add_links_to_urls(text: str):
    if not text:
        return ""
    url_regex = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    urls = re.findall(url_regex, text)
    _l = []
    for url in urls:
        if url in _l:
            continue
        _l.append(url)
        link = f'<url>{url}</url>'
        text = text.replace(url, link)
    
    return text


@client.event
async def on_message(message: discord.Message):
    if message.channel.__class__ == discord.channel.DMChannel:
        if message.author.bot:
            pass
        else:
            print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}\n")
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")
    try:
        with open("ticket_channelids.json") as f:
            ids = list(map(int, json.load(f)))
        if message.channel.id in ids:
            ticketfile = f"tickets/{message.channel.id}_ticketmsgcache.json"
            try:
                with open(ticketfile) as f:
                    _data = json.load(f)
                    _l = []
                    for attachment in message.attachments:
                        _l.append(attachment.url)
                    if len(message.embeds) > 0:
                        if message.embeds[0].title == "Close Ticket":
                            _new = {
                                "embed": {
                                    "type": "closer",
                                    "color": 0xed4245,
                                },
                                "role_color": message.author.color.value,
                                "time": (message.created_at + datetime.timedelta(hours=9)).strftime("%Y/%m/%d/%H:%M"),
                                "id": message.id
                            }
                        else:
                            _new = {
                                "embed": {
                                    "type": "any",
                                    "color": message.embeds[0].color.value,
                                    "title": add_links_to_urls(replaceWithName(message.embeds[0].title, message)),
                                    "description": add_links_to_urls(replaceWithName(message.embeds[0].description, message)),
                                    "images": [
                                        message.embeds[0].thumbnail.url,
                                        message.embeds[0].image.url
                                    ]
                                },
                                "author": message.author.display_name,
                                "avater": message.author.avatar.url,
                                "role_color": message.author.color.value,
                                "time": (message.created_at + datetime.timedelta(hours=9)).strftime("%Y/%m/%d/%H:%M"),
                                "id": message.id
                            }
                    else:
                        _new = {
                            "author": {
                                "name": message.author.display_name,
                                "avater": message.author.display_avatar.url,
                                "role_color": message.author.color.value,
                                "bot": message.author.bot
                            },
                            "details": {
                                "content": add_links_to_urls(replaceWithName(message.content, message))
                            },
                            "time": (message.created_at + datetime.timedelta(hours=9)).strftime("%Y/%m/%d/%H:%M"),
                            "id": message.id
                        }
                    if message.reference:
                        msg = await message.channel.fetch_message(message.reference.message_id)
                        ct = _replaceWithName(msg.content, message)
                        match ct:
                            case None:
                                ct = "..."
                            case _:
                                if len(ct) > 50:
                                    if "--??*" in ct:
                                        r = "..."
                                        for i in range(0, len(ct)):
                                            u = ct[i]
                                            r += u
                                            if len(r) > 3: r = r[1:]
                                            if i > 100 and r == "--??*":
                                                ct = ct[:i+1]
                                                break
                                    else:
                                        ct = ct[:51]
                                ct = _add_links_to_urls(ct.replace("*??++", '<span class="user--mention pointer-w-hovered"').replace("--??*", '</span>'))
                        _new["reply"] = {
                            "author": {
                                "name": msg.author.display_name,
                                "avater": msg.author.display_avatar.url,
                                "role_color": msg.author.color.value,
                                "bot": msg.author.bot
                            },
                            "id": msg.id,
                            "content": ct
                        }
                    _new["attachments"] = _l
                    _data.append(_new)
                    if message.author.id not in _data[0]["participants"]:
                        _data[0]["participants"].append(message.author.id)
                with open(ticketfile, "w") as f:
                    json.dump(_data, f, indent=4)
            except Exception as e:...
    except Exception as e:...




#send as bot
@client.tree.command()
async def sendasbot(interaction: Interaction, content: str, cmd: bool=None):
    """ nothing to explain """

    channel = interaction.channel

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /send_ab. content = {content}, cmd = {cmd}")

    if cmd is True:
        if content == "eventservbutton":
            await interaction.response.send_message("sent eventservbutton", ephemeral=True)
            await channel.send(inspect.cleandoc(f"""
            サーバーへようこそ！
            Aternosのサーバーは5分間誰もいないと自動で閉鎖されます
            下のボタンを使うとこでいつでもサーバーを起動することができます
            """), view = eventservbuttons())
    
        elif content == "clearservbutton":
            await interaction.response.send_message("sent eventservbuttons", ephemeral=True)
            await channel.send(view = eventservbuttons())

        elif content == "showip":
            await interaction.response.send_message("sent embed ip", ephemeral=True)
            await channel.send(embed=ipembed)

        elif content == "giveaway":
            await interaction.response.send_message("sent giveawaybutton", ephemeral=True)
            galist = [0]
            with open("giveawaylist.json", "w") as f:
                json.dump(galist, f, ensure_ascii=False)
            await channel.send(view = giveawaybutton())
        
        elif content == "RegisterButton":
            await interaction.channel.send("このボタンをおしたあと、DMを確認してください", view=RegisterWithDM())
            await interaction.response.send_message("sent!!", ephemeral=True)

        elif content == "lottery":
            try:
                with open("giveawaylist.json") as f:
                    galist = json.load(f)
            except Exception:
                with open("giveawaylist.json", "w"):
                    pass
                await interaction.response.send_message("No giveaway was held", ephemeral=True)
                return

            if len(galist) == 1:
                await interaction.response.send_message("No giveaway was held", ephemeral=True)
                return
                
            if 0 in galist:
                galist.pop(0)
                try:
                    lotter = random.choice(galist)
                    member = discord.utils.get(channel.guild.members, name=lotter)
                    mention = member.mention

                    await interaction.response.send_message("did lottery", ephemeral=True)
                    await channel.send(inspect.cleandoc(f"""
                    **{mention}**
                    おめでとうございます
                    """))
                except Exception:
                    await interaction.response.send_message("galist was None", ephemeral=True)

            else:
                try:
                    lotter = random.choice(galist)
                    member = discord.utils.get(channel.guild.members, name=lotter)
                    mention = member.mention

                    await interaction.response.send_message("did lottery", ephemeral=True)
                    await channel.send(inspect.cleandoc(f"""
                    **{mention}**
                    おめでとうございます
                    """))
                except Exception:
                    await interaction.response.send_message("galist was None", ephemeral=True)

        elif content == "cleargalist":
            galist = [0]

            try:
                with open("giveawaylist.json", "w") as f:
                    json.dump(galist, f, indent=4)
            except Exception:
                await interaction.response.send_message("couldn't find giveawaylist.json", ephemeral=True)
                return
        
            await interaction.response.send_message(inspect.cleandoc(f"""Succesfully Cleared **galist**
            {galist}"""), ephemeral=True)

        elif content == "meiyorolebutton":
            await interaction.response.send_message("sent meiyorolebutton", ephemeral=True)
            await channel.send("読み終わったら押してください！", view=meiyorole())

        elif content == "mcmusic":
            await interaction.response.send_message("Sending MCmusic buttons", ephemeral=True)
            await channel.send(view=MCmusic())

        elif content == "fgmusic":
            await interaction.response.send_message("Sending FGmusic buttons", ephemeral=True)
            await channel.send(view=FGmusic())

        elif content == "RegisterWithDmOnSETAGAQUEST":
            await interaction.response.send_message("Sending RegisterWithDmOnSETAGAQUEST button", ephemeral=True)
            await channel.send(view=RegisterWithDmOnSETAGAQUEST())
        
        elif content == "Gu_Tyoki_Pa":
            await interaction.response.send_message("Sending Gu_Tyoki_Pa", ephemeral=True)
            await channel.send("✊", view=Gu_Tyoki_Pa())

        elif content == "makeaticket":
            await interaction.response.send_message("sent makeaticket", ephemeral=True)
            await channel.send(inspect.cleandoc(f"""サポートへようこそ！
            下のボタンを使ってチケットを作成してください。
            チケットでは**チャンク購入**のほか、__どんな問題や質問__に関してもOPがお応えします。
            """), view = makeaticket())

        elif content == "roleDes":
            await interaction.response.send_message("sent roleDes", ephemeral=True)
            global Ldescription
            global description
            
            Lembed = discord.Embed(title="ルームリーダー一覧", description=Ldescription, color=0x228b22)
            embed = discord.Embed(title="役職一覧", description=description, color=0x8a2be2)

            await channel.send(embed=Lembed)
            await channel.send(embed=embed, view=ShowRoleDes())
        elif content == "SMGnickname":
            await interaction.response.send_message("sent SMGnickname", ephemeral=True)
            await interaction.channel.send("どういけてる？", view=SMGnickname())
        elif content == "MIT_ticket":
            await interaction.channel.send("```未定(BETA)```", view=MITcreateticket())
            await interaction.response.send_message("sent MITcreateticket", ephemeral=True)
        elif content == "Shishiji_nick":
            await interaction.channel.send(view=Shishiji.RegisterBtn())
            await interaction.response.send_message("sent Shishiji_nick", ephemeral=True)
        elif content == "Shishiji_update":
            await interaction.channel.send(view=Shishiji.MemberVisibleInfoUpdater())
            await interaction.response.send_message("sent Shishiji_update", ephemeral=True)
        else:
            await interaction.response.send_message(inspect.cleandoc(f"""This command does not exist
            **"{content}"**"""), ephemeral=True)
    else:
        class sendconf(discord.ui.View):         #ほんとに送るか確認ボタン
            def __init__(self):
                super().__init__(timeout = None)

            @discord.ui.button(label = "送信", style = discord.ButtonStyle.green, custom_id = "sendconf")
            async def send_ab(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("sent a message", ephemeral=True)
                await channel.send(content)
            
        await interaction.response.send_message(inspect.cleandoc(f"""
        本当に送信しますか？
        **content = {content}**"""), view = sendconf(), ephemeral=True)



@client.tree.command()
async def avater(interaction: Interaction, userid: str):
    """ avater """
    
    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /avater\n")

    count(interaction.user.name, "/avater")

    user = client.get_user(int(userid))
    avater = user.avatar
    username = user.name
    avaterembed = discord.Embed(title=username + "'s avater", color=0xfffff)
    avaterembed.set_image(url=avater.url)

    await interaction.response.send_message(embed=avaterembed)



@client.tree.command()
async def vc(interaction: Interaction, vcid: str=None, disconnect: str=None):
    """ connect to vc """
   
    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /vc dc = {disconnect}\n")

    guild = interaction.user.guild

    if vcid != None:
        vc = client.get_channel(int(vcid))
        vcname = vc.name
        await vc.connect()
        await interaction.response.send_message(inspect.cleandoc(f"""Connected to **{vcname}**"""), ephemeral=True)

    elif disconnect != None:
        try:
            await guild.voice_client.disconnect()
            await interaction.response.send_message(inspect.cleandoc(f"""Disconnected!!"""), ephemeral=True)

        except Exception:
            await interaction.response.send_message(inspect.cleandoc(f"""No vc was connected"""), ephemeral=True)

    else:
        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.response.send_message("You must connect any vc to use this!!", ephemeral=True)
            return
        
        await vc.connect()
        await interaction.response.send_message(inspect.cleandoc(f"""Connected!!"""), ephemeral=True)



@client.tree.command()
async def playmusic(interaction: Interaction, name: str, buttons: bool=None):
    """ plays music in connected vc! """

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /playmusic name = {name}, buttons = {buttons}\n")

    count(interaction.user.name, "/playmusic")

    guild = interaction.user.guild


    if buttons is True:
        channel = interaction.channel
        await interaction.response.send_message("sending music Buttons...", ephemeral=True)
        await channel.send(view=MCmusic())
        await channel.send(view=FGmusic())
        return
    
    else:
        pass



    guild = interaction.user.guild
    musiclist = [
        "Minecraft", "Beginning", "Beginning2", "Clark", "Mutation", "Sweden", "SubwooferLullaby",
        "LivingMice", "Haggstrom", "Danny", "DryHands", "WetHands", "MiceOnVenus", "Trailer"]
    
    music = name + ".mp3"

    if guild.voice_client is None:
        await interaction.response.send_message("No vc was connected", ephemeral=True)
        return


    try:
        with open(music, "r"):
            pass
        guild.voice_client.play(discord.FFmpegPCMAudio(music))
        await interaction.response.send_message(inspect.cleandoc(f"""Playing **{name}**..."""), ephemeral=True)
    
    except Exception:
        await interaction.response.send_message(inspect.cleandoc(f"""Choose music from below!!
        {musiclist}"""), ephemeral=True)



@client.tree.command()
async def stop(interaction: Interaction):
    """ stop """

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /stop\n")
    
    count(interaction.user.name, "/stop")

    guild = interaction.user.guild

    if guild.voice_client != None:
        guild.voice_client.stop()
        await interaction.response.send_message("Stopped!!", ephemeral=True)
    
    else:
        await interaction.response.send_message("No vc was connected", ephemeral=True)



# もう使わん
#@client.tree.command()
async def register(interaction: Interaction, your_name: str, your_class: str):
    """ ニックネームを名前に変更します """
    
    print(f"\n[{timestr()}] {Fore.BLUE}{interaction.user.name}{Fore.RESET} used /register, name={your_name}, {your_class}\n")

    userid = interaction.user.id; username = interaction.user.name

    your_name = your_name.replace("　", "")
    your_name = your_name.replace(" ", "")
    your_class = your_class.replace("　", "")
    your_class = your_class.replace(" ", "")
    your_class = your_class.replace("4", "")
    your_class = your_class.replace("４", "")

    if "a" in your_class:
        your_class = "A"
    elif "b" in your_class:
        your_class = "B"
    elif "c" in your_class:
        your_class = "C"
    elif "d" in your_class:
        your_class = "D"
    elif "e" in your_class:
        your_class = "E"
    elif "f" in your_class:
        your_class = "F"
    elif "g" in your_class:
        your_class = "G"

    try:
        with open("Config_username.json") as f:
            users = json.load(f)
    except Exception:
        users = {}

    intera_user_info = {}

    intera_user_info["discord_name"] = username
    intera_user_info["name"] = your_name
    intera_user_info["class"] = your_class
    users[userid] = intera_user_info
    
    with open("Config_username.json", "w") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    role = interaction.guild.get_role(1098532985629839441)

    classes = ("A", "B", "C", "D", "E", "F", "G")
    if your_class not in classes:
        await interaction.response.send_message("正確なクラスを入力してください", ephemeral=True)
        return
    if role in interaction.user.roles:
        await interaction.response.send_message("既に登録済みです", ephemeral=True)
        return
    
    await interaction.user.add_roles(role)
    role_class_A = interaction.guild.get_role(1098607173308780686)
    role_class_B = interaction.guild.get_role(1098607662511423709)
    role_class_C = interaction.guild.get_role(1098607729775493132)
    role_class_D = interaction.guild.get_role(1098607764873420921)
    role_class_E = interaction.guild.get_role(1098607800642449550)
    role_class_F = interaction.guild.get_role(1098607852723118101)
    role_class_G = interaction.guild.get_role(1098608577612091523)

    if your_class == "A":
        await interaction.user.add_roles(role_class_A)
    elif your_class == "B":
        await interaction.user.add_roles(role_class_B)
    elif your_class == "C":
        await interaction.user.add_roles(role_class_C)
    elif your_class == "D":
        await interaction.user.add_roles(role_class_D)
    elif your_class == "E":
        await interaction.user.add_roles(role_class_E)
    elif your_class == "F":
        await interaction.user.add_roles(role_class_F)
    elif your_class == "G":
        await interaction.user.add_roles(role_class_G)

    try:
        await interaction.user.edit(nick=f"{your_class}_{your_name}")
        await interaction.response.send_message("ニックネームを変更しました", ephemeral=True)
        channel = interaction.guild.get_channel(1098579941714579516)
        await channel.send(f"{interaction.user.mention}が登録されました")
    except Exception:
        await interaction.response.send_message("貴様は管理者や", ephemeral=True)
    


@client.tree.command()
async def ban(interaction: Interaction, user: discord.Member):
    """ ban with a message """

    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /ban {user.name}\n")

    channel = interaction.channel
    await interaction.response.send_message("trying...", ephemeral=True)

    try:
        await user.ban(reason="あほ", delete_message_seconds=0)
        banembed = discord.Embed(title=f"✅ {user.name} was banned", color=0x98765)
        await channel.send(embed=banembed)
    except discord.errors.Forbidden:
        banembed = discord.Embed(title=f"❌ Couldn't ban {user.name}", description="ErrorType: administrator", color=0xff0000)
        await channel.send(embed=banembed)
    except (AttributeError, discord.app_commands.errors.TransformerError):
        banembed = discord.Embed(title=f"❌ Couldn't ban {user.name}", description="ErrorType: {channel: DM}", color=0xff0000)
        await channel.send(embed=banembed)


@client.tree.command()
async def toggle(interaction: Interaction, censor: bool):
    """ toggle censorship """

    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /toggle, bool: {censor}\n")
    
    if interaction.user.id != 805680950238642188:
        await interaction.response.send_message("死ね", ephemeral=True)
        return

    global censorship
    censorship = censor
    await interaction.response.send_message(f"censorship is now \n```python\n{censorship}\n```")



@client.tree.command()
async def survey(interaction: Interaction, title: str, description: str, anonymous: bool=False):
    """ make new survey on currentchannel
    
    title: :class:`str`
        アンケートのタイトル
    description: :class: `str`
        アンケートの説明
    """

    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} used /survey\n\
    title: {title}\n\
    description: {description}")

    kanoki = client.get_user(805680950238642188)

    if title[0] == "#":
        await interaction.response.send_message('タイトルの先頭に "#" をつけることはできません', ephemeral=True)
        return

    try:
        with open(f"Config/Survey/{title}_ansed_users.json") as f:
            pass
        await interaction.response.send_message(f"**{title}** というアンケートは既に作成されています。どうしても作りたいなら{kanoki.mention}に問い合わせください", ephemeral=True)
        print("-> 既存のタイトル")
        return
    except FileNotFoundError:
        pass

    try:
        with open("Tags/survey_tags.json") as f:
            tag_dict = json.load(f)
    except FileNotFoundError:
        tag_dict = {}
    
    while True:
        new_tag = str(random.randint(1, 9999))
        if len(new_tag) < 4:
            new_tag = new_tag[::-1]
            while True:
                new_tag = str(new_tag)
                new_tag = f"{new_tag}0"
                if len(new_tag) >= 4:
                    new_tag = new_tag[::-1]
                    break

        new_tag = f"#{new_tag}"
        if not new_tag in list(tag_dict.keys()):
            break
    
    tag_dict[new_tag] = title

    with open("Tags/survey_tags.json", "w") as f:
        json.dump(tag_dict, f, ensure_ascii=False, indent=4)


    answerembed = discord.Embed(title=title, description=description, color=0xfffff)
    answerembed.add_field(name="作成者",value=interaction.user.mention)
    if anonymous is True:
        answerembed.add_field(name="詳細",value=f"作成日時: <t:{int(time.time())}:F>\n**ID: {new_tag}**\n匿名回答: __有効__")
    else:
        answerembed.add_field(name="詳細",value=f"作成日時: <t:{int(time.time())}:F>\n**ID: {new_tag}**")


    dm = await interaction.user.create_dm()
    if interaction.channel.__class__ == discord.channel.PartialMessageable or interaction.channel.__class__ == discord.channel.DMChannel:
        createdembed = discord.Embed(title="アンケートを作成しました", description=f"<t:{int(time.time())}:F>\n**ID: {new_tag}**", color=0xff00ff)
    else:
        createdembed = discord.Embed(title="アンケートを作成しました", description=f"{interaction.channel.mention}\n<t:{int(time.time())}:F>\n**ID: {new_tag}**", color=0xff00ff)
    createdembed.add_field(name="タイトル",value=title)
    createdembed.add_field(name="説明",value=description)
    if anonymous is True:
        createdembed.add_field(name="匿名投票", value="__有効__", inline=False)
    createdembed.add_field(name="結果を取得",value=f"`/getresult {title}`\nもしくは `/getresult {new_tag}`", inline=False)
    createdembed.add_field(name="結果を閲覧可能なユーザーを追加する",value=f"`/getresult {title}(もしくは {new_tag}) @USER`")
    

    description = description + "複数回答する場合は空白などで区切ってください"

    message = await interaction.channel.send("[ @everyone ]", embed=answerembed, view=CustomAnswer(title=title, description=description, madeby=interaction.user, channel=interaction.channel))
    dmmsg = await dm.send(embed=createdembed, view=EndCustomAnswer_Conf(title=title, description=description, madeby=interaction.user, message=message))

    try:
        with open(f"Config/Survey/{title}_ansed_users.json", "w") as f:
            madeby = json.load(f)
    except Exception:
        madeby = {}

    g = []
    try:
        with open("survey_messages.json") as f:
            g = json.load(f)
    except Exception:...
    g.append({
        "title": title,
        "description": description,
        "anonymous": anonymous,
        "channel_id": message.channel.id,
        "message_id": message.id,
        "madeby": interaction.user.id,
        "dmmsg": dmmsg.id,
    })
    with open("survey_messages.json", "w") as f:
        json.dump(g, f, indent=4, ensure_ascii=False)


    madeby["madeby"] = [str(interaction.user.id)]

    if anonymous is True:
        madeby["anonymous"] = anonymous


    with open(f"Config/Survey/{title}_ansed_users.json", "w") as f:
        json.dump(madeby, f, ensure_ascii=False, indent=4)

    await interaction.response.send_message(f"作成に成功しました\n`/getresult {title}(もしくは {new_tag})` \
で結果を取得できます\n結果を閲覧可能なユーザーを追加する: `/getresult {title}(もしくは {new_tag}) @USER`\n(DMに説明があります)", ephemeral=True)



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

    if add_coop is None and remove_coop is not None:
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /getresult\n    title: {title}\n    remove_coop: {remove_coop.name}")
    elif add_coop is not None and remove_coop is None:
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /getresult\n    title: {title}\n    add_coop: {add_coop.name}")
    elif add_coop is not None and remove_coop is not None:
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /getresult\n    title: {title}\n    add_coop: {add_coop.name}\n    remove_coop: {remove_coop.name}")
        await interaction.response.send_message("`add_coop` と `remove_coop` を同時に使用しないでください")
        print("-> returned")
        return
    else:
        print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /getresult\n    title: {title}")


    kanoki = client.get_user(805680950238642188)
    survey_tag = f"Fatal Error. Report to {kanoki.mention}"
    if remove_coop is not None:
        if "#" in title:
            title = title.replace(" ", "")
            try:
                with open("Tags/survey_tags.json") as f:
                    tag_dict = json.load(f)
            except Exception as e:
                if e.__class__ == FileNotFoundError:
                    await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                    print("-> アンケートが存在しない")
                    return
                else:
                    kanoki = client.get_user(805680950238642188)
                    await interaction.response.send_message(f"Fatal error occurred!! Report this to {kanoki.mention}. Additional info:\n{e}", ephemeral=True)
                    print(f"-> {Fore.RED}Error: {e}{Fore.RESET}")
                    return
            else:
                if tag_dict.get(title, False):
                    title = tag_dict[title]
                else:
                    await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                    print("-> アンケートが存在しない")
                    return
                
        cached_ = False
        try:
            with open(f"Config/Survey/{title}_ansed_users.json") as f:
                madeby = json.load(f)
        except FileNotFoundError:
            try:
                with open("Cache/Survey/cache_" + title + "_ansed_users.json") as f:
                    madeby = json.load(f)
                cached_ = True
            except FileNotFoundError:
                await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                return
        with open("Tags/survey_tags.json") as f:
            tag_dict = json.load(f)
        kanoki = client.get_user(805680950238642188)
        for tag in list(tag_dict.keys()):
            if tag_dict[tag] == title:
                survey_tag = tag
                break
            else:
                survey_tag = f"Fatal Error Report to {kanoki.mention}"

        id_madeby = madeby["madeby"]
        if id_madeby[0] == str(remove_coop.id):
            await interaction.response.send_message(f"{remove_coop.mention}は **{title}** アンケート(ID: {survey_tag}) のオーナーです", ephemeral=True)
            return
            
        if not str(interaction.user.id) in id_madeby:
            await interaction.response.send_message(f"あなたは **{title}** アンケート(ID: {survey_tag}) の作成者もしくは閲覧可能者ではありません", ephemeral=True)
            return
        
        if str(remove_coop.id) in id_madeby:       
            id_madeby.remove(str(remove_coop.id))
            madeby["madeby"] = id_madeby
        else:
            coop_users = ""
            for user in id_madeby:
                if coop_users != "":
                    coop_users = f"{coop_users}\n\n・{client.get_user(int(user)).mention}"
                else:
                    coop_users = f"・{client.get_user(int(user)).mention}"
            await interaction.response.send_message(f"{remove_coop.mention} は閲覧可能なユーザーではありませんでした。\n\n現在の閲覧可能なユーザー:\n{coop_users}", ephemeral=True)
            return
        if cached_ is True:
            with open(f"Cache/Survey/cache_{title}_ansed_users.json", "w") as f:
                json.dump(madeby, f, ensure_ascii=False, indent=4)
        else:
            with open(f"Config/Survey/{title}_ansed_users.json", "w") as f:
                json.dump(madeby, f, ensure_ascii=False, indent=4)


        coop_users = ""
        for user in id_madeby:
            if coop_users != "":
                coop_users = f"{coop_users}\n\n・{client.get_user(int(user)).mention}"
            else:
                coop_users = f"・{client.get_user(int(user)).mention}"
        
        await interaction.response.send_message(f"{remove_coop.mention} の アンケート: **{title}** (ID: {survey_tag}) の結果を取得する権限を剥奪しました。\n\n現在の閲覧可能なユーザー:\n{coop_users}", ephemeral=True)
        return

    if add_coop is not None and remove_coop is None:
        if "#" in title:
            title = title.replace(" ", "")
            try:
                with open("Tags/survey_tags.json") as f:
                    tag_dict = json.load(f)
            except Exception as e:
                if e.__class__ == FileNotFoundError:
                    await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                    print("-> アンケートが存在しない")
                    return
                else:
                    kanoki = client.get_user(805680950238642188)
                    await interaction.response.send_message(f"Fatal error occurred!! Report this to {kanoki.mention}. Additional info:\n{e}", ephemeral=True)
                    print(f"-> {Fore.RED}Error: {e}{Fore.RESET}")
                    return
            else:
                if tag_dict.get(title, False):
                    title = tag_dict[title]
                else:
                    await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                    print("-> アンケートが存在しない")
                    return
                
        cached_ = False
        try:
            with open(f"Config/Survey/{title}_ansed_users.json") as f:
                madeby = json.load(f)
        except FileNotFoundError:
            try:
                with open("Cache/Survey/cache_" + title + "_ansed_users.json") as f:
                    madeby = json.load(f)
                cached_ = True
            except FileNotFoundError:
                await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                return
        
        with open("Tags/survey_tags.json") as f:
            tag_dict = json.load(f)
        kanoki = client.get_user(805680950238642188)
        for tag in list(tag_dict.keys()):
            if tag_dict[tag] == title:
                survey_tag = tag
                break
            else:
                survey_tag = f"Fatal Error. Report to {kanoki.mention}"

        id_madeby = madeby["madeby"]
        if id_madeby[0] == str(add_coop.id):
            await interaction.response.send_message(f"{add_coop.mention}は **{title}** アンケート(ID: {survey_tag}) のオーナーです", ephemeral=True)
            return

        if not str(interaction.user.id) in id_madeby:
            await interaction.response.send_message(f"あなたは **{title}** アンケート(ID: {survey_tag}) の作成者もしくは閲覧可能者ではありません", ephemeral=True)
            return
        
        if not str(add_coop.id) in id_madeby:
            id_madeby.append(str(add_coop.id))
            madeby["madeby"] = id_madeby
            if add_coop.id != 1082610869755707442:
                dm = await add_coop.create_dm()
                with open("Tags/survey_tags.json") as f:
                    tag_dict = json.load(f)
                kanoki = client.get_user(805680950238642188)
                for tag in list(tag_dict.keys()):
                    if tag_dict[tag] == title:
                        survey_tag = tag
                        break
                    else:
                        survey_tag = f"Fatal Error. Report to {kanoki.mention}"
                if cached_ is True:
                    await dm.send(f"終了した **{title}** (ID: {survey_tag}) のアンケート結果が {interaction.user.mention}により閲覧可能になりました\n結果を取得: `/getresult {title}(もしくは {survey_tag})`")
                else:
                    await dm.send(f"**{title}** (ID: {survey_tag}) のアンケート結果が {interaction.user.mention}により閲覧可能になりました\n結果を取得: `/getresult {title}(もしくは {survey_tag})`")
        else:
            coop_users = ""
            for user in id_madeby:
                if coop_users != "":
                    coop_users = f"{coop_users}\n\n・{client.get_user(int(user)).mention}"
                else:
                    coop_users = f"・{client.get_user(int(user)).mention}"
            await interaction.response.send_message(f"{add_coop.mention} はすでに閲覧可能になっています\n\n現在の閲覧可能なユーザー:\n{coop_users}", ephemeral=True)
            return

        if cached_ is True:
            with open(f"Cache/Survey/cache_{title}_ansed_users.json", "w") as f:
                json.dump(madeby, f, ensure_ascii=False, indent=4)
        else:
            with open(f"Config/Survey/{title}_ansed_users.json", "w") as f:
                json.dump(madeby, f, ensure_ascii=False, indent=4)


        coop_users = ""
        for user in id_madeby:
            if coop_users != "":
                coop_users = f"{coop_users}\n\n・{client.get_user(int(user)).mention}"
            else:
                coop_users = f"・{client.get_user(int(user)).mention}"
        
        await interaction.response.send_message(f"{add_coop.mention} が アンケート: **{title}** (ID: {survey_tag}) の結果を取得することができるようになりました\n\n現在の閲覧可能なユーザー:\n{coop_users}", ephemeral=True)
        return
        
    if "#" in title:
        title = title.replace(" ", "")
        try:
            with open("Tags/survey_tags.json") as f:
                tag_dict = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                print("-> アンケートが存在しない")
                return
            else:
                kanoki = client.get_user(805680950238642188)
                await interaction.response.send_message(f"Unknown error occurred!! Report this to {kanoki.mention}. Additional info:\n{e}", ephemeral=True)
                print(f"-> {Fore.RED}Error: {e}{Fore.RESET}")
                return
        else:
            if tag_dict.get(title, False):
                title = tag_dict[title]
            else:
                await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
                print("-> アンケートが存在しない")
                return


    _cached = False
    try:
        with open(f"Config/Survey/{title}_ansed_users.json") as f:
            madeby = json.load(f)
    except FileNotFoundError:
        try:
            with open("Cache/Survey/cache_" + title + "_ansed_users.json") as f:
                madeby = json.load(f)
            _cached = True
        except FileNotFoundError:
            await interaction.response.send_message(f"**{title}** というアンケートは存在しません", ephemeral=True)
            return

    with open("Tags/survey_tags.json") as f:
        tag_dict = json.load(f)
    kanoki = client.get_user(805680950238642188)
    for tag in list(tag_dict.keys()):
        if tag_dict[tag] == title:
            survey_tag = tag
            break
        else:
            survey_tag = f"Fatal Error. Report to {kanoki.mention}"

    id_madeby = madeby["madeby"]; coop_users = ""
    for user in id_madeby:
        if coop_users != "":
            coop_users = f"{coop_users}\n\n・{client.get_user(int(user)).mention}"
        else:
            coop_users = f"・{client.get_user(int(user)).mention}"
    if not str(interaction.user.id) in madeby["madeby"]:
        await interaction.response.send_message(f"あなたには **{title}** アンケート(ID: {survey_tag}) の結果を閲覧する権限がありません。\n\
{coop_users}のみが閲覧可能であり、**ユーザーに閲覧する権限を付与できます**", ephemeral=True)
        return
    
    try:
        with open(f"Answers/{title}_answers.json") as f:
            answers = json.load(f)
    except FileNotFoundError:
        if _cached is True:
            try:
                with open("Cache/Survey/cache_" + title + "_answers.json") as f:
                    answers = json.load(f)
            except FileNotFoundError:
                await interaction.response.send_message(f"回答がありませんでした", ephemeral=True)
                print("-> 回答がなかった(終了済み)")
                return
        else:
            await interaction.response.send_message(f"まだ回答がありません", ephemeral=True)
            print("-> 回答がまだない")
            return


    answers_for_send = ""; cnt = 0
    for answer in answers.values():
        answer_user = client.get_user(int(list(answers.keys())[cnt]))
        if answers_for_send == "":
            if madeby.get("anonymous", False):
                if _cached is True:
                    answers_for_send = f"終了したアンケート結果: **{title}** (ID: {survey_tag}): __{str(len(list(answers.values())))}件の回答__\n\n> {answer[title]}"
                else:
                    answers_for_send = f"アンケート結果: **{title}** (ID: {survey_tag}): __{str(len(list(answers.values())))}件の回答__\n\n> {answer[title]}"
            else:
                if _cached is True:
                    answers_for_send = f"終了したアンケート結果: **{title}** (ID: {survey_tag}): __{str(len(list(answers.values())))}件の回答__\n\n> {answer[title]} -> {answer_user.mention}"
                else:
                    answers_for_send = f"アンケート結果: **{title}** (ID: {survey_tag}): __{str(len(list(answers.values())))}件の回答__\n\n> {answer[title]} -> {answer_user.mention}"
        else:
            if madeby.get("anonymous", False):
                answers_for_send = f"{answers_for_send}\n\n> {answer[title]}"
            else:
                answers_for_send = f"{answers_for_send}\n\n> {answer[title]} -> {answer_user.mention}"
        cnt += 1
    
    ephemeral = True
    if interaction.channel.__class__ == discord.channel.DMChannel:
        ephemeral = False
    
    await interaction.response.send_message(f"{answers_for_send}", ephemeral=ephemeral)



@client.tree.command()
async def getfile(interaction: Interaction, filename: str):
    """ get file from server dir """
    
    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /getfile, {filename}")

    filename = filename.replace(" ", "")
    found = False

    if "/" in filename:
        pass
    else:
        for file_name in os.listdir():
            if filename.lower() in file_name.lower():
                filename = file_name
                found = True

        if "answers" in filename.lower():
            try:
                with open(f"Answers/{filename}.json", "rb") as f:
                    file = discord.File(f)
                    await interaction.response.send_message(file=file)
                    print(f"responded {filename}")
                    return
            except FileNotFoundError as e:
                await interaction.response.send_message(f"{type(e).__name__}: {e}")
                print("failed")
                return
        
        if not found:
            await interaction.response.send_message(f"{filename} does not exist in os.listdir()")
            print("failed")
            return
    
    with open(filename, 'rb') as f:
        file = discord.File(f)
        await interaction.response.send_message(file=file)
        print(f"responded {filename}")



@client.tree.command()
async def reset(interaction: Interaction, setagaquest: bool=False, shishiji: bool=False):
    """ about register """

    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /reset, setagaquest: {setagaquest}, shishiji: {shishiji}")

    if interaction.user.id != 805680950238642188:
        await interaction.response.send_message("you're not allowed to get returns", ephemeral=True)
        return
    

    if setagaquest is True:
        channel = client.get_channel(1101755461876842507)
        message = await channel.fetch_message(1101756183251013682)
        admin_role = channel.guild.get_role(1101414407860396074)

        await message.edit(content=f"{admin_role.mention}: 名前わかりづらい\nということで名前を登録してください", view=RegisterWithDmOnSETAGAQUEST())
        print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed セタガクエスト\n(登録)")
        await interaction.response.send_message(f"{channel.mention}", ephemeral=True)
        return
    

    if shishiji is True:
        channel = client.get_channel(1098507125266858106)
        message = await channel.fetch_message(1098884369692762113)
        channel_for_mention = client.get_channel(1099721782732275773)

        await message.edit(content=inspect.cleandoc(f"""このボタンをおしたあと、DMを確認してください
        <登録の仕方: {channel_for_mention.mention}>"""), view=RegisterWithDM())
        print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed 獅子師たち-4年\n(登録)")
        await interaction.response.send_message(f"{channel.mention}", ephemeral=True)
        return
    
    

@client.tree.command()
async def poll(interaction: Interaction, question: str, option1: str, option2: str, option3: str=None, option4: str=None):
    """ create a poll(options up to 4) """

    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} used /poll,\n    question: {question}\n    option1: {option1}\n    option2: {option2}\n    option3: {option3}")

    _threeoptions = False; _fouroptions = False
    if option1 == option2 or option1 == option3 or option2 == option3:
        await interaction.response.send_message("選択肢が重複しています", ephemeral=True)
        return

    if option4 is not None:
        if option3 is None:
            await interaction.response.send_message("option3を埋めてください", ephemeral=True)
            return
        else:
            _fouroptions = True
            try:
                with open(f"poll/{question}_poll.json"):
                    pass
                await interaction.response.send_message("既に存在する質問です", ephemeral=True)
                return
            except FileNotFoundError:
                votes = {
                    "#1": 0,
                    "#2": 0,
                    "#3": 0,
                    "#4": 0,
                    "options":{
                        "#1": option1,
                        "#2": option2,
                        "#3": option3,
                        "#4": option4
                    },
                    "voted": {},
                    "madeby": str(interaction.user.id)
                }
                with open(f"poll/{question}_poll.json", "w") as f:
                    json.dump(votes, f, ensure_ascii=False, indent=4)
            
            try:
                with open("Tags/poll_tags.json") as f:
                    tag_dict = json.load(f)
            except FileNotFoundError:
                tag_dict = {}
            
            while True:
                new_tag = str(random.randint(1, 9999))
                if len(new_tag) < 4:
                    new_tag = new_tag[::-1]
                    while True:
                        new_tag = str(new_tag)
                        new_tag = f"{new_tag}0"
                        if len(new_tag) >= 4:
                            new_tag = new_tag[::-1]
                            break

                new_tag = f"#{new_tag}"
                if not new_tag in list(tag_dict.keys()):
                    break
    
    elif option3 is not None:
        _threeoptions = True
        try:
            with open(f"poll/{question}_poll.json"):
                pass
            await interaction.response.send_message("既に存在する質問です", ephemeral=True)
            return
        except FileNotFoundError:
            votes = {
                "#1": 0,
                "#2": 0,
                "#3": 0,
                "options":{
                    "#1": option1,
                    "#2": option2,
                    "#3": option3
                },
                "voted": {},
                "madeby": str(interaction.user.id)
            }
            with open(f"poll/{question}_poll.json", "w") as f:
                json.dump(votes, f, ensure_ascii=False, indent=4)
        
        try:
            with open("Tags/poll_tags.json") as f:
                tag_dict = json.load(f)
        except FileNotFoundError:
            tag_dict = {}
        
        while True:
            new_tag = str(random.randint(1, 9999))
            if len(new_tag) < 4:
                new_tag = new_tag[::-1]
                while True:
                    new_tag = str(new_tag)
                    new_tag = f"{new_tag}0"
                    if len(new_tag) >= 4:
                        new_tag = new_tag[::-1]
                        break

            new_tag = f"#{new_tag}"
            if not new_tag in list(tag_dict.keys()):
                break

    else:
        try:
            with open(f"poll/{question}_poll.json"):
                pass
            await interaction.response.send_message("既に存在する質問です", ephemeral=True)
            return
        except FileNotFoundError:
            votes = {
                "#1": 0,
                "#2": 0,
                "options":{
                    "#1": option1,
                    "#2": option2
                },
                "voted": {},
                "madeby": str(interaction.user.id)
            }
            with open(f"poll/{question}_poll.json", "w") as f:
                json.dump(votes, f, ensure_ascii=False, indent=4)
        
        try:
            with open("Tags/poll_tags.json") as f:
                tag_dict = json.load(f)
        except FileNotFoundError:
            tag_dict = {}
        
        while True:
            new_tag = str(random.randint(1, 9999))
            if len(new_tag) < 4:
                new_tag = new_tag[::-1]
                while True:
                    new_tag = str(new_tag)
                    new_tag = f"{new_tag}0"
                    if len(new_tag) >= 4:
                        new_tag = new_tag[::-1]
                        break

            new_tag = f"#{new_tag}"
            if not new_tag in list(tag_dict.keys()):
                break
           
    
    embed = discord.Embed(title=question, color=0xffffff)
    if _threeoptions:
        embed.add_field(name="Options [0 Votes]", value=f"[**#1**] {option1}\n[**#2**] {option2}\n[**#3**] {option3}")
    elif _fouroptions:
        embed.add_field(name="Options [0 Votes]", value=f"[**#1**] {option1}\n[**#2**] {option2}\n[**#3**] {option3}\n[**#4**] {option4}")
    else:
        embed.add_field(name="Options [0 Votes]", value=f"[**#1**] {option1}\n[**#2**] {option2}")
    embed.add_field(name="Status", value=f"__**Active**__\n**ID: {new_tag}**")
    embed.set_image(url="http://cdn.kanokiw.com:8443/assets/novotesf.png")
    try:
        embed.set_footer(text=f"Poll created by {interaction.user}", icon_url=interaction.user.avatar.url)
    except Exception:
        embed.set_footer(text=f"Poll created by {interaction.user}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")

    message = await interaction.channel.send("[ @everyone ]", embed=embed)
    if _threeoptions:
        await message.edit(view=PollSelect_three(question=question, option1=option1, option2=option2, option3=option3, message=message, madeby=interaction.user, tag=new_tag))
    elif _fouroptions:
        await message.edit(view=PollSelect_four(question=question, option1=option1, option2=option2, option3=option3, option4=option4, message=message, madeby=interaction.user, tag=new_tag))
    else:
        await message.edit(view=PollSelect(question=question, option1=option1, option2=option2, message=message, madeby=interaction.user, tag=new_tag))
    
    details = {
        "question": question,
        "channel_id": str(message.channel.id),
        "message_id": str(message.id),
        "isthree": True if _threeoptions else False,
        "isfour": True if _fouroptions else False,
        "madeby": interaction.user.id
    }
    
    tag_dict[new_tag] = details
    
    with open("Tags/poll_tags.json", "w") as f:
        json.dump(tag_dict, f, ensure_ascii=False, indent=4)
    await interaction.response.send_message("作成しました", ephemeral=True)
    


@client.tree.command()
async def poll_end(interaction: Interaction, question: str):
    """ end a poll """

    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /poll_end,\n    question: {question}")
    
    got_from_tag = False
    if "#" in question:
        question = question.replace(" ", "")
        try:
            with open("Tags/poll_tags.json") as f:
                tag_dict = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"**{question}** というpollは存在しません", ephemeral=True)
                print("-> pollが存在しない")
                return
            else:
                kanoki = client.get_user(805680950238642188)
                await interaction.response.send_message(f"Unknown error occurred!! Report this to {kanoki.mention}. Additional info:\n{e}", ephemeral=True)
                print(f"-> {Fore.RED}Error: {e}{Fore.RESET}")
                return
        else:
            if tag_dict.get(question, False):
                got_from_tag = True
                tag = question
                question = tag_dict[question]["question"]
            else:
                await interaction.response.send_message(f"**{question}** というpollは存在しません", ephemeral=True)
                print("-> pollが存在しない")
                return
    if got_from_tag is False:
        try:
            with open("Tags/poll_tags.json") as f:
                tag_dict = json.load(f)
        except Exception as e:
            if e.__class__ == FileNotFoundError:
                await interaction.response.send_message(f"**{question}** というpollは存在しません", ephemeral=True)
                print("-> pollが存在しない")
                return
        
        found = False
        for values in list(tag_dict.values()):
            if question == values["question"]:
                channel_id = values["channel_id"]
                message_id = values["message_id"]
                found = True
                break
        if found is False:
            await interaction.response.send_message("poll が見つかりませんでした", ephemeral=True)
            return
    else:
        channel_id = tag_dict[tag]["channel_id"]
        message_id = tag_dict[tag]["message_id"]
    
    try:
        with open(f"poll/{question}_poll.json") as f:
            madeby = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("Couldn't find any poll with the question", ephemeral=True)
        return
    
    if str(interaction.user.id) != madeby["madeby"]:
        await interaction.response.send_message("No Permissions on you", ephemeral=True)
        return
    
    
    try:
        channel = client.get_channel(int(channel_id))
        message_to_edit = await channel.fetch_message(int(message_id))
    except Exception:
        await interaction.response.send_message("Something wnet wrong :(", ephemeral=True)
        return
    
    
    with open(f"Cache/Poll/poll_{question}.json", "w") as f:
        json.dump(madeby, f, ensure_ascii=False, indent=4)
    os.remove(f"poll/{question}_poll.json")

    with open("Tags/poll_tags.json") as f:
        tag_dict = json.load(f)

    for key in list(tag_dict.keys()):
        if tag_dict[key]["question"] == question:
            tag = key
            break


    embed = message_to_edit.embeds[0]
    embed.remove_field(index=1)
    embed.add_field(name="Status", value=f"__**Ended**__\n**ID: {tag}**")
    if tag_dict[tag].get("isthree", False):
        await message_to_edit.edit(embed=embed, view=Disabled_PollSelect_three())
    elif tag_dict[tag].get("isfour", False):
        await message_to_edit.edit(embed=embed, view=Disabled_PollSelect_four())
    else:
        await message_to_edit.edit(embed=embed, view=Disabled_PollSelect())
    for key in list(tag_dict.keys()):
        if tag_dict[key]["question"] == question:
            del tag_dict[key]
            with open("Tags/poll_tags.json", "w") as f:
                json.dump(tag_dict, f, indent=4, ensure_ascii=False)
            break
    await interaction.response.send_message(f"Succesfully ended **{question}**\ncheck it now -> {channel.mention}", ephemeral=True)


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
        イベントのURL(Optional) - 規定値: ''
    message: :class:`str`
        添付するメッセージ - 規定値: `None`
    """

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.global_name}{Fore.RESET} used /absentcontact,\n    title: {title}, description: {description}, month: {month}, date: {date}, hour: {hour}, url: {url}")

    await interaction.response.defer(thinking=True, ephemeral=True)

    nick = interaction.user.nick
    if str(nick) == "None":
        nick = interaction.user.global_name
    try:
        await interaction.user.edit(nick=nick)
        await interaction.followup.send("このコマンドを使うには、少なくとも管理者権限が必要です", ephemeral=True)
    except Exception:
        pass

    parms = {year: [1970, 2030], month: [1, 12], date: [1, 31], hour: [0, 24], minute: [0, 59]}
    caution = False
    for parm in parms:
        info = parms[parm]
        if int(parm) < info[0] or int(parm) > info[1]:
            caution = True

    if caution:
        await interaction.followup.send("UnixTime変換における計算対象外の数値があります", ephemeral=True)
        return
    
    #########################
    y = int(year) -1970
    m = int(month) -1
    d = int(date) -1
    h = int(hour) -1
    m = 60 - int(minute)
    
    am = y*365*24*60*60 + m*30
    #########################

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color_code = (r, g, b)
    color_code = discord.Color.random()

    eventDate = datetime.datetime(int(year), int(month), int(date), int(hour), int(minute))
    epoch = datetime.datetime(1970, 1, 1, 9)
    eventDate = eventDate - epoch

    eventDate = str(eventDate.total_seconds())

    d = 0
    for i in list(eventDate):
        if i == ".":
            break
        d += 1
    eventDate = eventDate[:d]

    embed = discord.Embed(title=title, description=f"欠席連絡をする場合は以下からお願いします\n※必ずイベントが始まる前に連絡してください", color=color_code)
    embed.add_field(name="詳細", value=f"開始日時: <t:{int(str(eventDate))}:F>\nイベント内容: {description}\n{url}")

    e = 0
    fp = ""
    while True:
        fp = f"absent/{eventDate}_{title}_{e}_userIDs.json"
        try:
            with open(fp):
                pass
        except Exception:
            break
        e += 1
    with open(fp, "w") as f:
        json.dump([], f, indent=4)
    p = await interaction.channel.send(content=message, embed=embed, view=IDontAttendToday(eventDate, fp, title, color_code))
    await interaction.followup.send(f"成功!!\n一応日時を確認してね!!", ephemeral=True)
    try:    
        with open("absents.json") as f:
            r = json.load(f)
    except FileNotFoundError:
        r = []
    r.append({
        "channel": interaction.channel.id,
        "message": p.id,
        "date": eventDate,
        "fp": fp,
        "title": title,
        "color_code": color_code.value
    })
    with open("absents.json", "w") as f:
        json.dump(r, f, indent=4)



@client.tree.command()
async def setagaquest(interaction: Interaction, invurl: str, rolemention: discord.Role=None, usermention: discord.Member=None):
    """ end a poll """

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} used /setagaquest,\n    invURL: {invurl}")

    class URL_Buttons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            myip = "mitminecraft.f5.si"
            with open("setagaquest.url.json") as f:
                p = json.load(f)
            myip = p["globIP"]
            port = p["port"]
            self.add_item(discord.ui.Button(label="GitHub", url=p["GitHub"]))
            del p["port"]
            del p["globIP"]
            del p["GitHub"]
            for key in p.keys():
                path = p[key]
                self.add_item(discord.ui.Button(label=key, url=f"http://{myip}:{port}/{path}"))
    
    invurl = invurl.replace(" ", "").replace("　", "")
    try:
        requests.get(invurl)
        if not invurl.startswith("https://prod.liveshare.vsengsaas.visualstudio.com/join?"):
            raise Exception()
    except Exception:
        await interaction.response.send_message("Invailed URL", ephemeral=True)
        return
    
    embed = discord.Embed(title=f"VScode Live Share: <t:{int(time.time())}:F>", description=f"`Session: ` {invurl}\nrun `node app.js` on terminal when the server is down", color=0xff00ff)
    
    if rolemention is not None:
        if usermention is not None:
            if str(rolemention) == "@everyone":
                await interaction.channel.send(f"[{usermention.mention} {rolemention}]", embed=embed, view=URL_Buttons())
            else:
                await interaction.channel.send(f"[{usermention.mention} {rolemention.mention}]", embed=embed, view=URL_Buttons())
        else:
            if str(rolemention) == "@everyone":
                await interaction.channel.send(f"[{rolemention}]", embed=embed, view=URL_Buttons())
            else:
                await interaction.channel.send(f"[{rolemention.mention}]", embed=embed, view=URL_Buttons())
    else:
        if usermention is not None:
            await interaction.channel.send(f"[{usermention.mention}]", embed=embed, view=URL_Buttons())
        else:
            await interaction.channel.send(embed=embed, view=URL_Buttons())
    await interaction.response.send_message("Sent!!", ephemeral=True)



@client.tree.command()
async def solve(interaction: Interaction, ticket_category: discord.CategoryChannel, support_role: discord.Role, content: str, cache_channel: discord.TextChannel=None):
    await interaction.response.defer(thinking=True, ephemeral=True)

    categoty = ticket_category
    role = support_role
    
    class G(discord.ui.View):
        def __init__(self, *, ticket_line: discord.CategoryChannel, support_role: discord.Role, cache_channel: discord.channel.TextChannel | None = None):
            super().__init__(timeout=None)
            self.ticket_line, self.support_role, self.cache_channel = ticket_line, support_role, cache_channel

        @discord.ui.button(label="Create Ticket", emoji="<:ticket_:1129107340415733770>", style=discord.ButtonStyle.primary)
        async def _o(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(TicketModal(ticket_line=self.ticket_line, support_role=self.support_role, cache_channel=self.cache_channel))

    content = content.replace("\\n", "\n")
    r: discord.Message = await interaction.channel.send(content=content, view=G(ticket_line=categoty, support_role=role, cache_channel=cache_channel))
    await interaction.followup.send("All went fine.", ephemeral=True)
    try:
        with open("./ticket_createButtons.json") as f:
            j = json.load(f)
    except FileNotFoundError:
        j = []
    j.append({
        "category": ticket_category.id,
        "role": support_role.id,
        "channel": r.channel.id,
        "message": r.id,
        "cache": cache_channel.id
    })
    with open("./ticket_createButtons.json", "w") as f:
        json.dump(j, f, indent=4)
    

@client.tree.command()
async def send_role_button(interaction: Interaction, message: str=None, label: str="選択する"):
    class b(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.guild = client.get_guild(1153884392448606238)
            self.done = self.guild.get_role(1161599033152913448)

        @discord.ui.button(label=label, style=discord.ButtonStyle.blurple)
        async def e(self, interaction: Interaction, button: discord.Button):
            if self.done in interaction.user.roles:
                await interaction.response.send_message(f"あなたは選択を済ませています。\n間違いだと思われる場合は<@805680950238642188>へお問い合わせください。", ephemeral=True)
                return
            await interaction.response.send_message(view=Shishiji.Shishiji_Roles().create_select(client)(), ephemeral=True)
    msg = await interaction.channel.send(content=message, view=b())
    await interaction.response.send_message("`<T>`", ephemeral=True)
    path = "./SHISHIJI/role_btn_preserved.json"
    preserved = []
    if os.path.exists(path):
        with open(path) as f:
            preserved = json.load(f)
    preserved.append({
        "guild_id": msg.guild.id,
        "channel_id": msg.channel.id,
        "message_id": msg.id,
        "message": message,
        "label": label
    })
    with open(path, "w") as f:
        json.dump(preserved, f, indent=4)


# VPN cpu sucks
#@client.tree.command()
async def speak(interaction: Interaction, contents: str):
    """ speak """

    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} used /speak, contents={contents}\n")

    user = interaction.user; guild = interaction.guild
    if user.id != 805680950238642188:
        await interaction.response.send_message("Do Not", ephemeral=True)
        return
    else:
        await interaction.response.send_message(f"speaking {contents}...", ephemeral=True)   
    word_count = len(contents); index = 0; words = list(contents)
    small_word_tuple = ("ゃ", "ゅ", "ょ")

    def speak(filename):
        guild.voice_client.play(discord.FFmpegPCMAudio(filename))

    while index <= word_count -1:
        first_word = words[index]
        spoken = False
        if index < word_count -2:
            second_word = words[index +1]
            third_word = words[index +2]
            index += 3
            combined = f"{first_word}{second_word}{third_word}"
            if "ちょっ" in combined:
                speak("ちょっ.mp3")
                spoken = True
            else:
                spoken = False

        if index < word_count -1:
            if spoken is False:
                second_word = words[index +1]
                index += 2
                if small_word_tuple in second_word:
                    filename = f"{first_word}{second_word}.mp3"
                    speak(filename)
                    spoken = True
                else:
                    spoken = False

        if spoken is False:
            index += 1
            filename = f"{first_word}.mp3"
            speak(filename)
            spoken = True



@client.tree.command()
async def shishiji_absentcontact(interaction: Interaction, title: str, description: str, year: str, month: str, date: str, hour: str, minute: str, url: str="", message: str=None):
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
        イベントのURL*複数ある場合は空白で区切ってください(Optional) - 規定値: ''
    message: :class:`str`
        添付するメッセージ - 規定値: `None`
    """

    print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.global_name}{Fore.RESET} used /shishiji_absentcontact,\n    title: {title}, description: {description}, month: {month}, date: {date}, hour: {hour}, url: {url}")

    await interaction.response.defer(thinking=True, ephemeral=True)

    nick = interaction.user.nick
    if str(nick) == "None":
        nick = interaction.user.global_name
    try:
        await interaction.user.edit(nick=nick)
        await interaction.followup.send("You need Admin or higher to run!", ephemeral=True)
    except Exception:
        pass

    parms = {year: [1970, 2030], month: [1, 12], date: [1, 31], hour: [0, 24], minute: [0, 59]}
    caution = False
    for parm in parms:
        info = parms[parm]
        if int(parm) < info[0] or int(parm) > info[1]:
            caution = True

    if caution:
        await interaction.followup.send("Error occured while handling unixtime convertion!", ephemeral=True)
        return
    
    #########################
    y = int(year) -1970
    m = int(month) -1
    d = int(date) -1
    h = int(hour) -1
    m = 60 - int(minute)
    
    am = y*365*24*60*60 + m*30
    #########################

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color_code = (r, g, b)
    color_code = discord.Color.random()

    eventDate = datetime.datetime(int(year), int(month), int(date), int(hour), int(minute))
    epoch = datetime.datetime(1970, 1, 1, 9)
    eventDate = eventDate - epoch

    eventDate = str(eventDate.total_seconds())

    d = 0
    for i in list(eventDate):
        if i == ".":
            break
        d += 1
    eventDate = eventDate[:d]
    br = "\n"

    embed = discord.Embed(title=title, description=f"**欠席連絡をする場合は以下のボタンを押して行ってください\n※必ずイベントが始まる前に連絡してください**", color=color_code)
    embed.add_field(name="開始日時", value=f"<t:{int(str(eventDate))}:F>")
    embed.add_field(name="イベント詳細", value=f"{interaction.user.mention} が作成\n{description}")
    embed.add_field(name="外部リンク", value=f"{br.join(url.split(' '))}")
    embed.set_thumbnail(url=interaction.guild.icon.url)

    e = 0
    fp = ""
    while True:
        fp = f"absent/{eventDate}_{title}_{e}_userIDs.json"
        try:
            with open(fp):
                pass
        except Exception:
            break
        e += 1
    with open(fp, "w") as f:
        json.dump([], f, indent=4)
    p = await interaction.channel.send(content=message, embed=embed, view=IDontAttendToday(eventDate, fp, title, color_code))
    await interaction.followup.send(f"成功!!\n一応日時を確認してね!!", ephemeral=True)
    try:    
        with open("absents.json") as f:
            r = json.load(f)
    except FileNotFoundError:
        r = []
    r.append({
        "channel": interaction.channel.id,
        "message": p.id,
        "date": eventDate,
        "fp": fp,
        "title": title,
        "color_code": color_code.value
    })
    with open("absents.json", "w") as f:
        json.dump(r, f, indent=4)


client.run(token)
