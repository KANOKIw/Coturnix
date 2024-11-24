import requests, json, inspect, sys, datetime, asyncio, io
import discord, discord.utils, subprocess, os, time, random

from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client
from PIL import Image
from typing import List, Optional
from discord.components import SelectOption
from discord.interactions import Interaction
from discord.utils import MISSING as MS
import matplotlib.pyplot as plt


print(f"[{Fore.BLUE}loading Aternos...{Fore.RESET}]\n")

#aternos
aternos = Client.from_credentials('SETASABA', 'SETASABA')
servs = aternos.list_servers()
eventserv = servs[1]

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


async def roll_hand(message: discord.message, hand_is: int) -> None:
    """
    Parameter
    -----
    hand_is:
    1 = Gu,
    2 = Tyoki,
    3 = Pa
    """

    if message.content == "✊":
        previous_content = "gu"
    elif message.content == "✌🏼":
        previous_content = "tyoki"
    else:
        previous_content = "pa"
    
    if hand_is == 1:
        await message.edit(view=Disabled_Gu_Tyoki_Pa_is_Gu())
    elif hand_is == 2:
        await message.edit(view=Disabled_Gu_Tyoki_Pa_is_Tyoki())
    else:
        await message.edit(view=Disabled_Gu_Tyoki_Pa_is_Pa())

    """
    for i in range(0, 1):
        if previous_content == "gu":
            await message.edit(content="✌🏼")
            await asyncio.sleep(7)
            await message.edit(content="✋")
            await asyncio.sleep(7)
            await message.edit(content="✊")
            await asyncio.sleep(7)
        elif previous_content == "tyoki":
            await message.edit(content="✋")
            await asyncio.sleep(7)
            await message.edit(content="✊")
            await asyncio.sleep(7)
            await message.edit(content="✌🏼")
            await asyncio.sleep(7)
        else:
            await message.edit(content="✊")
            await asyncio.sleep(7)
            await message.edit(content="✌🏼")
            await asyncio.sleep(7)
            await message.edit(content="✋")
            await asyncio.sleep(7)
    for i in range(0, 1):
        if previous_content == "gu":
            await asyncio.sleep(6)
            await message.edit(content="✌🏼")
            await asyncio.sleep(6)
            await message.edit(content="✋")
            await asyncio.sleep(6)
            await message.edit(content="✊")
        elif previous_content == "tyoki":
            await asyncio.sleep(6)
            await message.edit(content="✋")
            await asyncio.sleep(6)
            await message.edit(content="✊")
            await asyncio.sleep(6)
            await message.edit(content="✌🏼")
        else:
            await asyncio.sleep(6)
            await message.edit(content="✊")
            await asyncio.sleep(6)
            await message.edit(content="✌🏼")
            await asyncio.sleep(6)
            await message.edit(content="✋")
    
    
    for i in range(0, 1):
        if previous_content == "gu":
            await asyncio.sleep(1)
            await message.edit(content="✌🏼")
            await asyncio.sleep(1)
            await message.edit(content="✋")
            await asyncio.sleep(1)
            await message.edit(content="✊")
        elif previous_content == "tyoki":
            await asyncio.sleep(1)
            await message.edit(content="✋")
            await asyncio.sleep(1)
            await message.edit(content="✊")
            await asyncio.sleep(1)
            await message.edit(content="✌🏼")
        else:
            await asyncio.sleep(1)
            await message.edit(content="✊")
            await asyncio.sleep(1)
            await message.edit(content="✌🏼")
            await asyncio.sleep(1)
            await message.edit(content="✋")
    """


async def roll_to_selected_hand(message: discord.message, hand_message: str, user_hand: str) -> str:
    now_message_content = message.content
    win_map = {"✊": "✌🏼", "✌🏼": "✋", "✋": "✊"}

    if "✊" in now_message_content:
        if hand_message == "✊":
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        elif "✌🏼" in hand_message:
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        else:
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
    elif "✌🏼" in now_message_content:
        if hand_message == "✊":
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        elif hand_message == "✌🏼":
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        else:
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
    else:
        if hand_message == "✊":
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        elif hand_message == "✌🏼":
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return  f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"
        else:
            if user_hand == hand_message:
                await message.edit(content=f"{hand_message}\n**あいこ**", view=Gu_Tyoki_Pa())
                return f"{Fore.YELLOW}あいこ{Fore.RESET}"
            elif win_map.get(hand_message, None) == user_hand:
                await message.edit(content=f"{hand_message}\n**BOTの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.RED}Coturnixの勝ち{Fore.RESET}"
            else:
                await message.edit(content=f"{hand_message}\n**あなたの勝ち**", view=Gu_Tyoki_Pa())
                return f"{Fore.BLUE}ユーザーの勝ち{Fore.RESET}"


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

with open("Config/init_tuple.json") as f:
    yurusanaiwords = json.load(f)

damewords = ("町田", "まちだ")
eandro = ("え")
myhomes = {"https://cdn.discordapp.com/attachments/971597070811168770/1093867985028010044/IMG_7471.png": "かのきの家の全体像"
}

#Python version
if sys.version_info < (3, 8):
    exit("Python 3.8 以上で実行してください")

try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Discord.pyがインストールされていません"
    )
logo = f"""
Succesfully running Coturnix.py
"""

print(logo + inspect.cleandoc(f"""
    Discord BotのTOKENを貼り付けてください

    {Style.DIM}このコンソール画面は閉じないでください
    {Style.RESET_ALL}
"""))

#START

try:
    with open("Config/config.json") as f:
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


#名誉サバイバル市民ボタン+1
class meiyorole(discord.ui.View):                                      
    def __init__(self):
        super().__init__(timeout = None)                               

    @discord.ui.button(label = "名誉サバイバル市民", style = discord.ButtonStyle.green, custom_id = "meiyorole")
    async def meiyorole(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.user.guild
        role = guild.get_role(1076411397816201246)
        role1 = guild.get_role(1081485314276728842)
        
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("名誉サバイバル市民になりました！", ephemeral=True)

            print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} got their role(meiyo)")
            
            if role1 not in interaction.user.roles:
                await interaction.user.add_roles(role1)
        
        else:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("名誉サバイバル市民から離脱しました", ephemeral=True)

            print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} removed their role(meiyo)")
            
            if role1 not in interaction.user.roles:
                await interaction.user.add_roles(role1)


#giveawayボタン
class giveawaybutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "参加する", style = discord.ButtonStyle.green, custom_id = "giveawaybutton")
    async def giveawaybutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} participated in the giveaway.")
        
        usernick = interaction.user.name
        galist = [0]
        
        try:
            with open("giveawaylist.json") as f:
                galist = json.load(f)
        except Exception:
            pass

        if galist is not None:  
            if usernick in galist:
                await interaction.response.send_message("既に参加しています", ephemeral=True)
        
            else:
                galist.append(usernick)
                await interaction.response.send_message("参加しました", ephemeral=True)
                print(galist)
                with open("giveawaylist.json", "w") as f:
                    json.dump(galist, f, ensure_ascii=False, indent=4)
        else:
            galist.append(usernick)
            await interaction.response.send_message("参加しました", ephemeral=True)
            print(galist)
            with open("giveawaylist.json", "w") as f:
                json.dump(galist, f, ensure_ascii=False, indent=4)


#チケットを作成
class makeaticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "チケットを作成", style = discord.ButtonStyle.green, custom_id = "makeaticket")
    async def makeaticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} made a ticket.")

        await interaction.response.defer(thinking=True, ephemeral=True)

        guild = interaction.user.guild
        role = guild.get_role(1085461267176755252)  #Support

        global tickets
        tickets += 1

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }
        
        KANOKI = guild.get_member(805680950238642188)       #file送信用
        mochi = guild.get_member(723448498879463425)

        userid = interaction.user.id

        opennerid = interaction.user.id

        openner = interaction.user

        category = await guild.create_category(name="SUPPORT LINE", overwrites=overwrites, position=3)

        ticketchannel = await category.create_text_channel(name=interaction.user.name + " " + str(int(userid)))

        ticketchannel_id = ticketchannel.id

        await interaction.followup.send("チケットを作成しました (" + ticketchannel.mention + ")", ephemeral=True)

        ticketfile = inspect.cleandoc(f"""{interaction.user.name}ticketmsgcache.txt""")      #チケットメッセージキャッシュ.txtの作成

        with open(ticketfile, "w"):
            pass

        @client.event
        async def on_message(message):
            if message.channel.id == ticketchannel_id:
                with open(ticketfile, 'a') as f:
                    f.write(f'[{timestr()}]\n{message.author.name}:{message.content}\n\n')


        mention = role.mention
        opennermention = interaction.user.mention
        nowtime = time.time()

        ticketembed = discord.Embed(title=interaction.user.name + "のチケット", color=0xfffff)
        ticketembed.add_field(name="作成日時", value=(inspect.cleandoc(f"""<t:{int(nowtime)}:F>""")))
        ticketembed.add_field(name="メンバー", value=opennermention)
        ticketembed.add_field(name="メモ", value=(inspect.cleandoc(f"""**解決**したり間違えて開いたチケットだったりした場合は
        下のボタンを使ってチケットを閉じてください""")))

        try:
            with open("usercounts.json") as f:
                counts = json.load(f)
        except Exception:
            counts = {}

        try:
            currentusercounts = counts[interaction.user.name]
        except (KeyError):
            currentusercounts = {}


        try:
            currentusercnt = currentusercounts["ticket"]
        except KeyError:
            currentusercnt = 0
        
        currentusercnt += 1
        currentusercounts["ticket"] = currentusercnt
        counts[interaction.user.name] = currentusercounts

        with open("usercounts.json", "w") as f:
            json.dump(counts, f, ensure_ascii=False, indent=4)
        

        class closeaticket(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)

            @discord.ui.button(label = "はい、閉じます", emoji="✖", style = discord.ButtonStyle.red, custom_id = "closeaticket")
            async def closeaticket(self, interaction: discord.Interaction, button: discord.ui.Button):

                print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} closed the ticket.")
                
                if str(int(opennerid)) in str(int(interaction.user.id)):
                    await interaction.response.send_message(inspect.cleandoc(f"""チケットを閉じています...
                    DMをご確認ください
                    """), ephemeral=True)

                else:
                    await interaction.response.send_message("他人のチケットを閉じています...", ephemeral=True)


                class feedback(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout = None)

                    @discord.ui.button(label="★", style = discord.ButtonStyle.red, custom_id = "1star")
                    async def onestar(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_message("フィードバックありがとうございました", ephemeral=True)
                        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} feedbacked ⭐.")
                        await feedbackmsg.edit(content="フィードバックありがとうございました", view=None)
                        count("feedbacks", "1")

                    @discord.ui.button(label="★★", style = discord.ButtonStyle.red, custom_id = "2stars")
                    async def twostars(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_message("フィードバックありがとうございました", ephemeral=True)
                        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} feedbacked ⭐⭐.")
                        await feedbackmsg.edit(content="フィードバックありがとうございました", view=None)
                        count("feedbacks", "2")

                    @discord.ui.button(label="★★★", style = discord.ButtonStyle.secondary, custom_id = "3stars")
                    async def threestars(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_message("フィードバックありがとうございました", ephemeral=True)
                        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} feedbacked ⭐⭐⭐.")
                        await feedbackmsg.edit(content="フィードバックありがとうございました", view=None)
                        count("feedbacks", "3")

                    @discord.ui.button(label="★★★★", style = discord.ButtonStyle.green, custom_id = "4stars")
                    async def fourstars(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_message("フィードバックありがとうございました", ephemeral=True)
                        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} feedbacked ⭐⭐⭐⭐.")
                        await feedbackmsg.edit(content="フィードバックありがとうございました", view=None)
                        count("feedbacks", "4")
                              
                    @discord.ui.button(label="★★★★★", style = discord.ButtonStyle.green, custom_id = "5stars")
                    async def fivestars(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_message("フィードバックありがとうございました", ephemeral=True)
                        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} feedbacked ⭐⭐⭐⭐⭐.")
                        await feedbackmsg.edit(content="フィードバックありがとうございました", view=None)
                        count("feedbacks", "5")

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    dm = await interaction.user.create_dm()
                    kanokidm = await KANOKI.create_dm()
                    mochidm = await mochi.create_dm()

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        await kanokidm.send(inspect.cleandoc(f"""{openner.name}'s Ticket cache(Created at <t:{int(nowtime)}:F>)"""), file=file)

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        feedbackmsg = await dm.send(inspect.cleandoc(f"""チケットのご利用ありがとうございました
                        よければOPの対応についての総合評価をお願いします
                        (チケットのメッセージを見返すことができます)"""), view=feedback(), file=file)

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        await mochidm.send(inspect.cleandoc(f"""{openner.name}'s Ticket cache(Created at <t:{int(nowtime)}:F>)
                        (このメッセージを受信したくない場合はご連絡ください)"""), file=file)

                    os.remove(ticketfile)

                    await asyncio.sleep(3)

                    await ticketchannel.delete()
                    await category.delete()

                
                else:
                    dm = await interaction.user.create_dm()
                    opennerdm = await openner.create_dm()
                    kanokidm = await KANOKI.create_dm()
                    mochidm = await mochi.create_dm()

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        await kanokidm.send(inspect.cleandoc(f"""{openner.name}'s Ticket msg cache(Created at <t:{int(nowtime)}:F>)"""), file=file)

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        feedbackmsg = await opennerdm.send(inspect.cleandoc(f"""チケットが閉じられました
                        よければOPの対応についての総合評価をお願いします
                        (チケットのメッセージを見返すことができます)"""), view=feedback(), file=file)

                    with open(ticketfile, 'rb') as f:
                        file = discord.File(f)
                        await mochidm.send(inspect.cleandoc(f"""{openner.name}'s Ticket msg cache(Created at <t:{int(nowtime)}:F>)
                        (このメッセージを受信したくない場合はご連絡ください)"""), file=file)

                    await dm.send("他人のチケットを閉じました...")

                    os.remove(ticketfile)
                    
                    await asyncio.sleep(3)
                    
                    await ticketchannel.delete()
                    await category.delete()
                    

        class closeaticketconfirm(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)

            @discord.ui.button(label = "チケットを閉じる", emoji="✖", style = discord.ButtonStyle.red, custom_id = "closeaticketconfirm")
            async def closeaticketconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                
                print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} wants to close the ticket.")

                global tickets
                tickets -= 1

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    await interaction.response.send_message("本当にこのチケットを閉じますか？", view=closeaticket(), ephemeral=True)

                else:
                    await interaction.response.send_message(inspect.cleandoc(f"""本当にこのチケットを閉じますか？
                    **警告:あなたはこのチケットの所有者ではありません**"""), view=closeaticket(), ephemeral=True)


        await ticketchannel.send(opennermention, embed=ticketembed, view=closeaticketconfirm())

        class ticketoption(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)

            @discord.ui.button(label = "Erea(土地)に関して", style = discord.ButtonStyle.green, custom_id = "erea")
            async def ereaticket(self, interaction: discord.Interaction, button: discord.ui.Button):

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET}'s ticket reason was Erea(土地)に関して.")

                    reasonembed = discord.Embed(title=interaction.user.name + "'s Ticket reason", description="Erea(土地)に関して", color=0x008000)

                    await interaction.response.send_message("理由を送信しました", ephemeral=True)
                    await message.delete()
                    
                    await ticketchannel.send(embed=reasonembed)
                    await ticketchannel.send(mention)
                    await ticketchannel.send(inspect.cleandoc(f"""{opennermention}現在の土地所有状況をこちらから確認できます
                    https://twitter.com/SGMinecraf9192?s=20"""))

                else:
                    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} tried selecting ticket reason Erea(土地)に関して.")

                    await interaction.response.send_message("あなたはチケット所有者ではないです", ephemeral=True)

            @discord.ui.button(label = "提案・要求", style = discord.ButtonStyle.primary, custom_id = "suggestion")
            async def suggestion(self, interaction: discord.Interaction, button: discord.ui.Button):

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET}'s ticket reason was 提案・要求.")

                    reasonembed = discord.Embed(title=interaction.user.name + "'s Ticket reason", description="提案・要求", color=0x0000ff)

                    await interaction.response.send_message("理由を送信しました", ephemeral=True)
                    await message.delete()

                    await ticketchannel.send(embed=reasonembed)
                    await ticketchannel.send(mention)

                else:
                    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} tried selecting ticket reason 提案・要求.")
                    await interaction.response.send_message("あなたはチケットの所有者ではないです", ephemeral=True)

            @discord.ui.button(label = "バグ・不具合", style = discord.ButtonStyle.red, custom_id = "bug")
            async def bug(self, interaction: discord.Interaction, button: discord.ui.Button):

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET}'s ticket reason was バグ・不具合")

                    reasonembed = discord.Embed(title=interaction.user.name + "'s Ticket reason", description="バグ・不具合", color=0xff0000)

                    await interaction.response.send_message("理由を送信しました", ephemeral=True)
                    await message.delete()

                    await ticketchannel.send(embed=reasonembed)
                    await ticketchannel.send(mention)

                else:
                    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} tried selecting ticket reason バグ・不具合")

                    await interaction.response.send_message("あなたはチケット所有者ではないです", ephemeral=True)

            @discord.ui.button(label = "訴訟", style = discord.ButtonStyle.red, custom_id = "sosyou")
            async def sosyou(self, interaction: discord.Interaction, button: discord.ui.Button):

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET}'s ticket reason was 訴訟")

                    reasonembed = discord.Embed(title=interaction.user.name + "'s Ticket reason", description="訴訟", color=0xff0000)

                    await interaction.response.send_message("理由を送信しました", ephemeral=True)
                    await message.delete()

                    await ticketchannel.send(embed=reasonembed)
                    await ticketchannel.send(mention)

                else:
                    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} tried selecting ticket reason バグ・不具合")

                    await interaction.response.send_message("あなたはチケット所有者ではないです", ephemeral=True)

            @discord.ui.button(label = "その他", style = discord.ButtonStyle.secondary, custom_id = "others")
            async def others(self, interaction: discord.Interaction, button: discord.ui.Button):

                if str(int(opennerid)) in str(int(interaction.user.id)):
                    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET}'s ticket reason was その他")

                    reasonembed = discord.Embed(title=interaction.user.name + "'s Ticket reason", description="その他", color=0x808080)

                    await interaction.response.send_message("理由を送信しました", ephemeral=True)
                    await message.delete()

                    await ticketchannel.send(embed=reasonembed)
                    await ticketchannel.send(mention)

                else:
                    print(f"\n[{timestr()}] {Fore.RED}{interaction.user.name}{Fore.RESET} tried selecting ticket reason その他")
                    await interaction.response.send_message("あなたはチケット所有者ではないです", ephemeral=True)


        message = await ticketchannel.send(inspect.cleandoc(f"""チケットをご利用いただきありがとうございます{opennermention}
        チケットを開いた理由を選んでください"""), view=ticketoption())
        

class MCmusic(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "Disconnect", style = discord.ButtonStyle.red, custom_id = "Disconnect")
    async def Disconnect(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} disconnected Coturnix")

        guild = interaction.user.guild
        count(interaction.user.name, "B.disconnect")
        
        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            await guild.voice_client.disconnect()
            await interaction.followup.send(inspect.cleandoc(f"""Disconnected!!"""), ephemeral=True)

        except Exception:
            await interaction.followup.send(inspect.cleandoc(f"""No vc was connected"""), ephemeral=True)


    @discord.ui.button(label = "Minecraft", style = discord.ButtonStyle.green, custom_id = "Minecraft")
    async def Minecraft(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Minecraft")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Minecraft.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Minecraft**..."""), ephemeral=True)


    @discord.ui.button(label = "Beginning", style = discord.ButtonStyle.green, custom_id = "Beginning")
    async def Beginning(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Beginning")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Beginning.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Beginning**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Beginning 2", style = discord.ButtonStyle.green, custom_id = "Beginning2")
    async def Beginning2(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Beginning 2")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")
        
        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Beginning2.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Beginning2**..."""), ephemeral=True)


    @discord.ui.button(label = "Clark", style = discord.ButtonStyle.green, custom_id = "Clark")
    async def Clark(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Clark")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Clark.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Clark**..."""), ephemeral=True)


    @discord.ui.button(label = "Mutation", style = discord.ButtonStyle.green, custom_id = "Mutation")
    async def Mutation(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Sweden")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Mutation.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Mutation**..."""), ephemeral=True)


    @discord.ui.button(label = "Sweden", style = discord.ButtonStyle.green, custom_id = "Sweden")
    async def Sweden(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Sweden")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Sweden.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Sweden**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Subwoofer Lullaby", style = discord.ButtonStyle.green, custom_id = "SubwooferLullaby")
    async def SubwooferLullaby(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Subwoofer Lullaby")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")
        
        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/SubwooferLullaby.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Subwoofer Lullaby**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Living Mice", style = discord.ButtonStyle.green, custom_id = "LivingMice")
    async def LivingMice(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Living Mice")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")
        
        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/LivingMice.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Living Mice**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Haggstrom", style = discord.ButtonStyle.green, custom_id = "Haggstrom")
    async def Haggstrom(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Haggstrom")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Haggstrom.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Haggstrom**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Danny", style = discord.ButtonStyle.green, custom_id = "Danny")
    async def Danny(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Danny")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")
        
        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Danny.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Danny**..."""), ephemeral=True)


    @discord.ui.button(label = "Dry Hands", style = discord.ButtonStyle.green, custom_id = "DryHands")
    async def DryHands(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Dry Hands")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/DryHands.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Dry Hands**..."""), ephemeral=True)


    @discord.ui.button(label = "Wet Hands", style = discord.ButtonStyle.green, custom_id = "WetHands")
    async def WetHands(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Wet Hands")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/WetHands.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Wet Hands**..."""), ephemeral=True)


    @discord.ui.button(label = "Mice On Venus", style = discord.ButtonStyle.green, custom_id = "MiceOnVenus")
    async def MiceOnVenus(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Mice On Venus")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/MiceOnVenus.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Mice On Venus**..."""), ephemeral=True)


    @discord.ui.button(label = "Stal", style = discord.ButtonStyle.green, custom_id = "Stal")
    async def Stal(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Stal")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Stal.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Stal**..."""), ephemeral=True)


    @discord.ui.button(label = "otherside", style = discord.ButtonStyle.green, custom_id = "otherside")
    async def otherside(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played otherside")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/otherside.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **otherside**..."""), ephemeral=True)


    @discord.ui.button(label = "Trailer", style = discord.ButtonStyle.green, custom_id = "Trailer")
    async def Trailer(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Trailer")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Trailer.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Trailer**..."""), ephemeral=True)


class FGmusic(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Final Fall", style = discord.ButtonStyle.primary, custom_id = "Final Fall")
    async def FinalFall(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Final Fall")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/FinalFall.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Final Fall**..."""), ephemeral=True)


    @discord.ui.button(label = "Everybody Falls", style = discord.ButtonStyle.primary, custom_id = "Everybody Falls")
    async def EverybodyFalls(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Everybody Falls")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/EverybodyFalls.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Everybody Falls**..."""), ephemeral=True)
    

    @discord.ui.button(label = "Fall for the Team", style = discord.ButtonStyle.primary, custom_id = "Fall for the Team")
    async def FallfortheTeam(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Fall for the Team")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/FallfortheTeam.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Fall for the Team**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Skis on Beans", style = discord.ButtonStyle.primary, custom_id = "Skis on Beans")
    async def SkisonBeans(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Skis on Beans")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/SkisonBeans.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Skis on Beans**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Falling Stars Chugu Bam Bam", style = discord.ButtonStyle.primary, custom_id = "Falling Stars Chugu Bam Bam")
    async def FallingStarsChuguBamBam(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Falling Stars Chugu Bam Bam")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/FallingStarsChuguBamBam.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Falling Stars Chugu Bam Bam**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Rumbling Waterfall", style = discord.ButtonStyle.primary, custom_id = "Rumbling Waterfall")
    async def RumblingWaterfall(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Rumbling Waterfall")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/RumblingWaterfall.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Rumbling Waterfall**..."""), ephemeral=True)


    @discord.ui.button(label = "Temple Tumble", style = discord.ButtonStyle.primary, custom_id = "Temple Tumble")
    async def TempleTumble(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Temple Tumble")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/TempleTumble.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Temple Tumble**..."""), ephemeral=True)


    @discord.ui.button(label = "Carousel Stumble", style = discord.ButtonStyle.primary, custom_id = "Carousel Stumble")
    async def CarouselStumble(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Carousel Stumble")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/CarouselStumble.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Carousel Stumble**..."""), ephemeral=True)


    @discord.ui.button(label = "Grand Festifall", style = discord.ButtonStyle.primary, custom_id = "Grand Festifall")
    async def GrandFestifall(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Grand Festifall")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/GrandFestifall.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Grand Festifall**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Fall Guys in the House", style = discord.ButtonStyle.primary, custom_id = "Fall Guys in the House")
    async def FallGuysintheHouse(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Fall Guys in the House")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/FallGuysintheHouse.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Fall Guys in the House**..."""), ephemeral=True)


    @discord.ui.button(label = "Main Room Beanstep", style = discord.ButtonStyle.primary, custom_id = "Main Room Beanstep")
    async def MainRoomBeanstep(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Main Room Beanstep")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/MainRoomBeanstep.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Main Room Beanstep**..."""), ephemeral=True)


    @discord.ui.button(label = "Everybody Falls HD", style = discord.ButtonStyle.secondary, custom_id = "Everybody Falls HD")
    async def EverybodyFallsHD(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Everybody Falls HD")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/EverybodyFallsHD.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Everybody Falls HD**..."""), ephemeral=True)


    @discord.ui.button(label = "Falling in Love on the Dancefloor", style = discord.ButtonStyle.secondary, custom_id = "Falling in Love on the Dancefloor")
    async def FallinginLoveontheDancefloor(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Falling in Love on the Dancefloor")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/FallinginLoveontheDancefloor.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Falling in Love on the Dancefloor**..."""), ephemeral=True)


    @discord.ui.button(label = "Satellite Scramble", style = discord.ButtonStyle.secondary, custom_id = "Satellite Scramble")
    async def SatelliteScramble(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Satellite Scramble")

        guild = interaction.user.guild
        count(interaction.user.name, "B.fall_guys")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/SatelliteScramble.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Satellite Scramble**..."""), ephemeral=True)


    @discord.ui.button(label = "高音jtr", style = discord.ButtonStyle.red, custom_id = "kouonjtr")
    async def kouonjtr(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played 高音jtr")

        guild = interaction.user.guild
        count(interaction.user.name, "B.高音jtr")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/singingwatabe.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **高音jtr**..."""), ephemeral=True)
    

    @discord.ui.button(label = "低音ども", style = discord.ButtonStyle.red, custom_id = "teionguys")
    async def teionguys(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played 低音ども")

        guild = interaction.user.guild
        count(interaction.user.name, "B.低音ども")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=True, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/teionguys.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **低音ども**..."""), ephemeral=True)


#サーバー停止確認ボタン
class stopconfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 7)

    @discord.ui.button(label = "はい、停止します", style = discord.ButtonStyle.red, custom_id = "stopconfirm")
    async def stopconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} stopped the evserver.")

        try:
            eventserv.stop()
            await interaction.response.send_message("サーバーは停止されました", ephemeral=True)

        except Exception:
            await interaction.response.send_message("サーバーは停止されています", ephemeral=True)


#サーバー再起動確認ボタン
class restartconfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 7)

    @discord.ui.button(label = "はい、再起動します", style = discord.ButtonStyle.red, custom_id = "restartconfirm")
    async def restartconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} restarted the evserver.")

        try:
            eventserv.restart()
            await interaction.response.send_message("サーバーは再起動されました", ephemeral=True)
            channel = client.get_channel(1076880460069752872)
            await channel.send(":octagonal_sign:➤➤➤:white_check_mark: **サーバーは再起動されています**")

        except Exception:
            await interaction.response.send_message("サーバーは停止されています", ephemeral=True)


#サーバーボタン
class eventservbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "サーバーを起動", style = discord.ButtonStyle.green, custom_id = "eventstarter")
    async def eventstarter(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} is trying to start the evserver.")

        channel = client.get_channel(1076880460069752872)

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            print('running Aternos_start.py')
            proc = subprocess.run(['python', 'Aternos_start.py'], stdout=PIPE, stderr=PIPE)
            status = proc.stdout.decode('utf-8')
            print(status)

            if "starting" in status:
                await interaction.followup.send("起動します", ephemeral=True)
                await channel.send(":fire: **サーバーの起動が始まりました**")

                print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} started the evserver.")

            else:
                await interaction.followup.send("既に起動されています", ephemeral=True)
            
                print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} couldn't start the evserver.")

        except Exception:
            await interaction.response.send_message(inspect.cleandoc(f"""サブプロセス(Aternos_start.py)の実行に失敗しました。
            スクショを かのき#7777 に送ってほしいです[-1]"""), ephemeral=True)

        try:
            with open("usercounts.json") as f:
                counts = json.load(f)
        except Exception:
            counts = {}

        try:
            currentusercounts = counts[interaction.user.name]
        except (KeyError):
            currentusercounts = {}


        try:
            currentusercnt = currentusercounts["start"]
        except KeyError:
            currentusercnt = 0
        
        currentusercnt += 1
        currentusercounts["start"] = currentusercnt
        counts[interaction.user.name] = currentusercounts

        with open("usercounts.json", "w") as f:
            json.dump(counts, f, ensure_ascii=False, indent=4)


    @discord.ui.button(label = "サーバーを停止", style = discord.ButtonStyle.red, custom_id = "eventstopper")
    async def eventstopper(self, interaction: discord.Interaction, button: discord.ui.Button):

        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} is trying to stop the evserver.")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            print('running Aternos_status.py')
            proc = subprocess.run(['python', 'Aternos_status.py'], stdout=PIPE, stderr=PIPE)
            status = proc.stdout.decode('utf-8')
            print(status)

            if "online" in status:
                await interaction.followup.send(inspect.cleandoc(f"""**本当にサーバーを停止しますか？**
                ボタンはたぶん10秒後に無効になります"""), view = stopconfirm(), ephemeral=True)
            
            elif "starting" in status:
                await interaction.followup.send(inspect.cleandoc(f"""**本当にサーバーを停止しますか？**
                __サーバーは起動中です。停止しないほうがいいと思います__
                ボタンはたぶん10秒後に無効になります"""), view = stopconfirm(), ephemeral=True)

            elif "loading" in status:
                await interaction.followup.send(inspect.cleandoc(f"""サーバーは起動準備中です。停止できません"""), ephemeral=True)

            elif "restarting" in status:
                await interaction.followup.send(inspect.cleandoc(f"""サーバーは再起動中です。停止できません"""), ephemeral=True)

            else:
                await interaction.followup.send("サーバーはオフラインです", ephemeral=True)

        except Exception:
            await interaction.response.send_message(inspect.cleandoc(f"""サブプロセス(Aternos_status.py)の実行に失敗しました。
            スクショを かのき#7777 に送ってほしいです[0]"""), ephemeral=True)

        try:
            with open("usercounts.json") as f:
                counts = json.load(f)
        except Exception:
            counts = {}

        try:
            currentusercounts = counts[interaction.user.name]
        except (KeyError):
            currentusercounts = {}


        try:
            currentusercnt = currentusercounts["stop"]
        except KeyError:
            currentusercnt = 0
        
        currentusercnt += 1
        currentusercounts["stop"] = currentusercnt
        counts[interaction.user.name] = currentusercounts

        with open("usercounts.json", "w") as f:
            json.dump(counts, f, ensure_ascii=False, indent=4)

    
    @discord.ui.button(label = "再起動", style = discord.ButtonStyle.gray, custom_id = "eventrestarter")
    async def eventrestarter(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} is trying to restart the evserver.")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            print('running Aternos_status.py')
            proc = subprocess.run(['python', 'Aternos_status.py'], stdout=PIPE, stderr=PIPE)
            status = proc.stdout.decode('utf-8')
            print(status)

            if "online" in status:
                await interaction.followup.send(inspect.cleandoc(f"""**本当にサーバーを再起動しますか？**
                ボタンはたぶん10秒後に無効になります"""), view = restartconfirm(), ephemeral=True)
            
            elif "starting" in status:
                await interaction.followup.send(inspect.cleandoc(f"""サーバーは起動中です。再起動できません"""), ephemeral=True)

            elif "loading" in status:
                await interaction.followup.send(inspect.cleandoc(f"""サーバーは起動準備中です。再起動できません"""), ephemeral=True)

            elif "restarting" in status:
                await interaction.followup.send(inspect.cleandoc(f"""サーバーは既に再起動中です。再起動できません"""), ephemeral=True)

            else:
                await interaction.followup.send("サーバーはオフラインです", ephemeral=True)

        except Exception:
            await interaction.response.send_message(inspect.cleandoc(f"""サブプロセス(Aternos_status.py)の実行に失敗しました。
            スクショを かのき#7777 に送ってほしいです[1]"""), ephemeral=True)

        try:
            with open("usercounts.json") as f:
                counts = json.load(f)
        except Exception:
            counts = {}

        try:
            currentusercounts = counts[interaction.user.name]
        except (KeyError):
            currentusercounts = {}


        try:
            currentusercnt = currentusercounts["restart"]
        except KeyError:
            currentusercnt = 0
        
        currentusercnt += 1
        currentusercounts["restart"] = currentusercnt
        counts[interaction.user.name] = currentusercounts

        with open("usercounts.json", "w") as f:
            json.dump(counts, f, ensure_ascii=False, indent=4)


    @discord.ui.button(label = "プレイヤーリスト", style = discord.ButtonStyle.gray, custom_id = "eventplayerslist")
    async def eventplayerslist(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} showed playerslist of the evserver.")

        await interaction.response.defer(thinking=True, ephemeral=True)

        print('running Aternos_playerslist.py')
        proc = subprocess.run(['python', 'Aternos_playerslist.py'], stdout=PIPE, stderr=PIPE)
        playerslist = proc.stdout.decode('utf-8')
        print(playerslist)
                    
        if len(playerslist) <= 4:
            await interaction.followup.send(inspect.cleandoc(f"""サーバーには誰もいません"""), ephemeral=True)
        
        else:
            await interaction.followup.send(inspect.cleandoc(f"""現在のプレイヤー:
                {playerslist}"""), ephemeral=True)
            
        try:
            with open("usercounts.json") as f:
                counts = json.load(f)
        except Exception:
            counts = {}

        try:
            currentusercounts = counts[interaction.user.name]
        except (KeyError):
            currentusercounts = {}


        try:
            currentusercnt = currentusercounts["playerslist"]
        except KeyError:
            currentusercnt = 0
        
        currentusercnt += 1
        currentusercounts["playerslist"] = currentusercnt
        counts[interaction.user.name] = currentusercounts

        with open("usercounts.json", "w") as f:
            json.dump(counts, f, ensure_ascii=False, indent=4)
            

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

        await self.dm.send(f"-------------------------\n登録手続きが開始されました\n-------------------------")

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
            global sent_your_class
            global your_class
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
            # check end

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
        await interaction.response.send_message(f"回答を記録しました\n回答を変更: {coturnix.mention}とのDM", ephemeral=True)



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
                await interaction.response.send_message(f"無効なアンケートです。\nおかしいと思ったら {kanoki.mention} までおねがいします", ephemeral=True)
                print(f"-> ...Error?: {e}")
                return
            else:
                await interaction.response.send_message(f"Unknown error occurred!! Additional info:\n{e}", ephemeral=True)
                print(f"-> Error: {e}")
                return

        if str(self.user.id) in ansed_users.keys():
            await interaction.response.send_message(f"既に回答しています", ephemeral=True, view=CancelAnswer(title=self.title, label=self.description, channel=self.channel))
            print("-> 既に回答している")
            return
        await interaction.response.send_modal(CustomAnswerModal(title=self.title, label=self.description, channel=self.channel))


class Disabled_Gu_Tyoki_Pa_is_Gu(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "グー", emoji="✊", style = discord.ButtonStyle.red, disabled=True)
    async def disabled_gu(self, interaction: discord.Interaction, button: discord.ui.Button):
        return

    @discord.ui.button(label = "チョキ", emoji="✌", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_tyoki(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "パー", emoji="✋", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_pa(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
class Disabled_Gu_Tyoki_Pa_is_Tyoki(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "グー", emoji="✊", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_gu(self, interaction: discord.Interaction, button: discord.ui.Button):
        return

    @discord.ui.button(label = "チョキ", emoji="✌", style = discord.ButtonStyle.red, disabled=True)
    async def disabled_tyoki(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "パー", emoji="✋", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_pa(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
class Disabled_Gu_Tyoki_Pa_is_Pa(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "グー", emoji="✊", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_gu(self, interaction: discord.Interaction, button: discord.ui.Button):
        return

    @discord.ui.button(label = "チョキ", emoji="✌", style = discord.ButtonStyle.green, disabled=True)
    async def disabled_tyoki(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "パー", emoji="✋", style = discord.ButtonStyle.red, disabled=True)
    async def disabled_pa(self, interaction: discord.Interaction, button: discord.ui.Button):
        return


class Gu_Tyoki_Pa(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "グー", emoji="✊", style = discord.ButtonStyle.green)
    async def gu(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} selected グー.")

        count(interaction.user.name, "ジャンケン: グー")

        await interaction.response.defer(ephemeral=True)

        channel = client.get_channel(1102617480599437352)
        message = await channel.fetch_message(1102618442621780110)
        
        await roll_hand(message=message, hand_is=1)


        hand_list = ["✌🏼", "✊", "✊", "✊", "✋", "✋", "✋", "✋"]
        
        hand_message = random.choice(hand_list)

        result = await roll_to_selected_hand(message=message, hand_message=hand_message, user_hand="✊")
        print(result)
        result = str(result).replace("\u001b[3", "").replace("1m", "").replace("3m", "").replace("4m", "").replace("9m", "")
        if result == "Coturnixの勝ち":
            count(interaction.user.name, "負け")
        elif result == "ユーザーの勝ち":
            count(interaction.user.name, "勝ち")
        else:
            count(interaction.user.name, "あいこ")

    @discord.ui.button(label = "チョキ", emoji="✌🏼", style = discord.ButtonStyle.green)
    async def tyoki(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} selected チョキ.")

        count(interaction.user.name, "ジャンケン: チョキ")

        await interaction.response.defer(ephemeral=True)

        channel = client.get_channel(1102617480599437352)
        message = await channel.fetch_message(1102618442621780110)
        
        await roll_hand(message=message, hand_is=2)


        hand_list = ["✋", "✌🏼", "✌🏼", "✌🏼", "✊", "✊", "✊", "✊"]
        
        hand_message = random.choice(hand_list)

        result = await roll_to_selected_hand(message=message, hand_message=hand_message, user_hand="✌🏼")
        print(result)
        result = str(result).replace("\u001b[3", "").replace("1m", "").replace("3m", "").replace("4m", "").replace("9m", "")
        if result == "Coturnixの勝ち":
            count(interaction.user.name, "負け")
        elif result == "ユーザーの勝ち":
            count(interaction.user.name, "勝ち")
        else:
            count(interaction.user.name, "あいこ")

    @discord.ui.button(label = "パー", emoji="✋", style = discord.ButtonStyle.green)
    async def pa(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} selected パー.")

        count(interaction.user.name, "ジャンケン: パー")

        await interaction.response.defer(ephemeral=True)

        channel = client.get_channel(1102617480599437352)
        message = await channel.fetch_message(1102618442621780110)
        
        await roll_hand(message=message, hand_is=3)


        hand_list = ["✊", "✋", "✋", "✋", "✌🏼", "✌🏼", "✌🏼", "✌🏼"]
        
        hand_message = random.choice(hand_list)

        result = await roll_to_selected_hand(message=message, hand_message=hand_message, user_hand="✋")
        print(result)
        result = str(result).replace("\u001b[3", "").replace("1m", "").replace("3m", "").replace("4m", "").replace("9m", "")
        if result == "Coturnixの勝ち":
            count(interaction.user.name, "負け")
        elif result == "ユーザーの勝ち":
            count(interaction.user.name, "勝ち")
        else:
            count(interaction.user.name, "あいこ")


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


class PollSelect(discord.ui.View):
    def __init__(self, question: str, option1: str, option2: str, message: discord.Message, madeby: discord.User, tag: str):
        super().__init__(timeout=None)
        self.question = question; self.option1 = option1; self.option2 = option2; self.message = message; self.madeby = madeby;self.tag = tag

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #1 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return
        
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        voted = self.votes[3]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[0] += 1
            else:
                self.votes[1] -= 1
                self.votes[0] += 1
        else:
            changes = 0
            change = False
            self.votes[0] += 1
        all = self.votes[0] + self.votes[1]

        
        if change is True:
            changes += 1
            print("-> change")
        user_info = {
            "voted": "1",
            "name": interaction.user.name,
            "last": str(timestr()),
            "changes": changes
        }



        voted[str(interaction.user.id)] = user_info
    

        first_rate = f"{(self.votes[0] / all)*100:.1f}"
        second_rate = f"{(self.votes[1] / all)*100:.1f}"
        if self.votes[1] == 0:
            labels = [f"#1 {first_rate}%", ""]
        else:
            labels = [f"#2 {second_rate}%", f"#1 {first_rate}%"]
        colors = ["#504464", "#30746c"]

        x = [self.votes[1], self.votes[0]]
        if self.votes[1] > self.votes[0]:
            embedcolor = 0x504464
        else:
            embedcolor = 0x30746c

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{self.question}_pie.png")
        

        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "options": {
                "#1": self.option1,
                "#2": self.option2
            },
            "voted": voted,
            "madeby": str(self.madeby.id)
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)


        with open(f"tmp/{self.question}_pie.png", "rb") as f:
            file = discord.File(f)


        KUMANKEN = client.get_user(1104729250285756447)
        dm = await KUMANKEN.create_dm()
        msg = await dm.send(file=file)


        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1]
        _voted = make_number_clear(str(_voted))
        image_url = msg.attachments[0].url
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect(question=self.question, option1=self.option1, option2=self.option2, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#1 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()



    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary)
    async def selectsecondt(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #2 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        voted = self.votes[3]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[1] += 1
            else:
                self.votes[0] -= 1
                self.votes[1] += 1
        else:
            changes = 0
            change = False
            self.votes[1] += 1
        all = self.votes[0] + self.votes[1]

        
        if change is True:
            changes += 1
            print("-> change")
        user_info = {
            "voted": "2",
            "name": interaction.user.name,
            "last": str(timestr()),
            "changes": changes
        }



        voted[str(interaction.user.id)] = user_info
    

        first_rate = f"{(self.votes[0] / all)*100:.1f}"
        second_rate = f"{(self.votes[1] / all)*100:.1f}"
        if self.votes[0] == 0:
            labels = ["", f"#2 {second_rate}%"]
        else:
            labels = [f"#2 {second_rate}%", f"#1 {first_rate}%"]
        colors = ["#504464", "#30746c"]

        x = [self.votes[1], self.votes[0]]
        if self.votes[1] > self.votes[0]:
            embedcolor = 0x504464
        else:
            embedcolor = 0x30746c

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }

        

        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{self.question}_pie.png")


        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "options": {
                "#1": self.option1,
                "#2": self.option2
            },
            "voted": voted,
            "madeby": str(self.madeby.id)
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)


        with open(f"tmp/{self.question}_pie.png", "rb") as f:
            file = discord.File(f)


        KUMANKEN = client.get_user(1104729250285756447)
        dm = await KUMANKEN.create_dm()
        msg = await dm.send(file=file)

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1]
        _voted = make_number_clear(str(_voted))
        image_url = msg.attachments[0].url
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)

        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect(question=self.question, option1=self.option1, option2=self.option2, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#2 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()




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

    #サーバーボタン
    channel = client.get_channel(1082650639676477540)
    message = await channel.fetch_message(1087918892623613994)
    await message.edit(content=inspect.cleandoc(f"""
            サーバーへようこそ！
            サーバーは5分間誰もいないと自動で閉鎖されます。下のボタンを使うとこでサーバーを操作することができます
            (ボタンの処理には数秒かかります。我慢してください)
            `Last update`: <t:{int(current_unix_time)}:R>
            """), view = eventservbuttons())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed server buttons")
    
    #名誉サバイバル市民
    channel = client.get_channel(1077140061394571315)
    message = await channel.fetch_message(1085185734912266321)

    await message.edit(content=inspect.cleandoc(f"""読み終わったら押してください！"""), view = meiyorole())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed meiyorole button")

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
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed Make a Ticket")

    #MCmusic------
    #SGマイクラ---
    #MCmusic
    channel = client.get_channel(1086972254811869284)
    message = await channel.fetch_message(1091303466292478103)
    
    await message.edit(content=inspect.cleandoc(f"""Minecraft"""), view=MCmusic())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed MCmusic\n(SGマイクラ)")

    #FGmusic
    channel = client.get_channel(1086972254811869284)
    message = await channel.fetch_message(1091303488786538536)
    
    await message.edit(content=inspect.cleandoc(f"""Fall Guys"""), view=FGmusic())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed FGmusic\n(SGマイクラ)")

    #Dancing Disco---
    #MCmusic
    channel = client.get_channel(1078252040200912928)
    message = await channel.fetch_message(1091301220364324975)

    await message.edit(content="Minecraft", view=MCmusic())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed MCmusic\n(Dancing Disco)")

    #FGmusic
    channel = client.get_channel(1078252040200912928)
    message = await channel.fetch_message(1091302293493784576)

    await message.edit(content="Fall Guys", view=FGmusic())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed FGmusic\n(Dancing Disco)")

    channel = client.get_channel(1098507125266858106)
    message = await channel.fetch_message(1098884369692762113)
    channel_for_mention = client.get_channel(1099721782732275773)
    await message.edit(content=inspect.cleandoc(f"""このボタンをおしたあと、DMを確認してください
    <登録の仕方: {channel_for_mention.mention}>"""), view=RegisterWithDM())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed RegisterWithDM\n(登録)")

    # セタガクエスト
    # 登録
    channel = client.get_channel(1101755461876842507)
    message = await channel.fetch_message(1101756183251013682)
    admin_role = channel.guild.get_role(1101414407860396074)

    await message.edit(content=f"{admin_role.mention}: 「名前がわかりづらい」\nということで名前を登録してください", view=RegisterWithDmOnSETAGAQUEST())
    print(f"\n[{timestr()}] {Fore.GREEN}<Coturnix system>{Fore.RESET} Fixed セタガクエスト\n(登録)")


    
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(name="Latest: http://coturnixbot.html.xdomain.jp/", type=discord.ActivityType.listening))

        #SGS
        channel = client.get_channel(1096698328139444306)
        members = channel.guild.member_count
        if channel.name != f"Member Count: {members}":
            await channel.edit(name=f"Member Count: {members}")

        #Dancing Disco
        channel = client.get_channel(1096452435750428732)
        members = channel.guild.member_count
        if channel.name != f"Member Count: {members}":
            await channel.edit(name=f"Member Count: {members}")

        #世田学四年
        channel = client.get_channel(1098512932339470408)
        members = channel.guild.member_count
        if channel.name != f"Member Count: {members}":
            await channel.edit(name=f"Member Count: {members}")

        #セタガクエスト
        channel = client.get_channel(1102101129095032832)
        members = channel.guild.member_count
        if channel.name != f"多分{int(members) -3}人":
            await channel.edit(name=f"多分{int(members) -3}人")

        await asyncio.sleep(15)


@client.event
async def on_member_join(member):
    global censorship
    if censorship is True:
        if member.guild.id == 1078251724801847326:
            if member.id == 856826942967906314:
                await member.kick(reason="あほ")
                return
        
    
    if member.guild.id == 1098507124532842588:
        channel = client.get_channel(1098507125266858106)
        dm = await member.create_dm()
        kanoki = client.get_user(805680950238642188)
        helloembed = discord.Embed(title=f"ようこそ！{member.mention}さん", description=inspect.cleandoc(f"""[チャンネル](https://discord.gg/GCnUmwDght)
        {channel.mention}
        ↑ のチャンネルで登録を完了してください
        このBOTは世田谷学園の生徒({kanoki.mention})によって作成されています
        情報が外部に漏洩することはありません"""), color=0x98765)
        helloembed.add_field(name="サーバー参加日時", value=f"<t:{int(time.time())}:F>")
        await dm.send(embed=helloembed)

    if member.guild.id == 1101399573991268374:
        channel = client.get_channel(1101755461876842507)
        dm = await member.create_dm()
        kanoki = client.get_user(805680950238642188)
        helloembed = discord.Embed(title=f"ようこそ！{member.mention}", description=inspect.cleandoc(f"""[チャンネル](https://discord.gg/Qp4Rhej5Q7)
        {channel.mention}
        ↑ のチャンネルで登録を完了してください"""), color=0x98765)
        helloembed.add_field(name="サーバー参加日時", value=f"<t:{int(time.time())}:F>")
        await dm.send(embed=helloembed)


@client.event
async def on_member_remove(member):
    global censorship
    if censorship is True:
        if member.guild.id == 1078251724801847326:
            if member.id == 856826942967906314:
                channel = client.get_channel(1078251725250646047)
                banembed = discord.Embed(title=f"✅ {member.name} was banned", color=0x98765)
                await channel.send(embed=banembed)
                return
            
        
    if member.guild.id == 1098507124532842588:
        channel = client.get_channel(1098579941714579516)
        await channel.send(f"```diff\n- <@{member.id} '{member.name}'> left the server\n```")

    if member.guild.id == 1101399573991268374:
        channel = client.get_channel(1101747278722641970)
        await channel.send(f"```diff\n- <@{member.id} '{member.name}'> left the server\n```")


@client.event
async def on_voice_state_update(member, before, after):
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
        1101399574897250377
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



class Class_disabled(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "A", style = discord.ButtonStyle.green, custom_id = "AGUMI")
    async def AGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "B", style = discord.ButtonStyle.green, custom_id = "BGUMI")
    async def BGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "C", style = discord.ButtonStyle.green, custom_id = "CGUMI")
    async def CGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "D", style = discord.ButtonStyle.green, custom_id = "DGUMI")
    async def DGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "E", style = discord.ButtonStyle.green, custom_id = "EGUMI")
    async def EGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "F", style = discord.ButtonStyle.green, custom_id = "FGUMI")
    async def FGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "G", style = discord.ButtonStyle.green, custom_id = "GGUMI")
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
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "B", style = discord.ButtonStyle.green, custom_id = "BGUMI")
    async def BGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"B_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "C", style = discord.ButtonStyle.green, custom_id = "CGUMI")
    async def CGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"C_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "D", style = discord.ButtonStyle.green, custom_id = "DGUMI")
    async def DGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"D_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "E", style = discord.ButtonStyle.green, custom_id = "EGUMI")
    async def EGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"E_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "F", style = discord.ButtonStyle.green, custom_id = "FGUMI")
    async def FGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"F_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")


    @discord.ui.button(label = "G", style = discord.ButtonStyle.green, custom_id = "GGUMI")
    async def GGUMI(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("pushed!!")
        nickname = f"G_{self.name}"
        user = client.get_guild(1101399573991268374).get_member(interaction.user.id)
        until = datetime.datetime.now()
        await user.edit(nick=nickname, timed_out_until=until)
        await self.message.edit(view=Class_disabled())
        await interaction.response.send_message(f"You have changed your nickname `{nickname}` successfully.\nYour timeout was lifted, thank you for taking the time for this")





@client.event
async def on_message(message):
    if message.author.id == 1080464218110832660:
        if message.author.nick.startswith("output"):
            await message.author.timeout()
            dm = await message.author.create_dm()
            message = await dm.send("Hey! Your nick seems to be invailed, please rename yourself.")
            await message.edit(view=Class_again("KUMANKEN", message=message))
            current_time = datetime.datetime.now()
            until = current_time + datetime.timedelta(minutes=33)
            await message.author.edit(timed_out_until=until)


        
    global censorship
    if censorship is True:
        if message.author.id == 899562089725710377:
            await message.delete()
            return
    
    gid = int(); cid = int()
    if message.channel.__class__ == discord.channel.DMChannel:
        if message.author.bot:
            pass
        else:
            print(f"\n[{timestr()}] {Fore.BLUE}{message.author.name}{Fore.RESET} {Fore.LIGHTGREEN_EX}DM{Fore.RESET} {Fore.CYAN}<normal>{Fore.RESET} {message.content}\n")
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    print(f"    attachment_url: {Fore.LIGHTBLUE_EX}{attachment.url}{Fore.RESET}")
                

    try:
        gid = message.channel.guild.id
    except Exception:
        pass
    
    try:
        cid = message.channel.id
    except Exception:
        pass
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

    if gid == 1098507124532842588:
        return

    if message.author.bot:
        return

    if censorship is False and message.author.id == 805680950238642188:
        return
    
    await check_everychat_iscrime(message)
        



#send as bot
@client.tree.command()
async def sendasbot(interaction: Interaction, content: str, cmd: bool=None):
    """ nothing to explain """

    channel = interaction.channel
    count(interaction.user.name, "/sendasbot")

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
                
        else:
            await interaction.response.send_message(inspect.cleandoc(f"""This command does not exists
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
    await dm.send(embed=createdembed, view=EndCustomAnswer_Conf(title=title, description=description, madeby=interaction.user, message=message))

    try:
        with open(f"Config/Survey/{title}_ansed_users.json", "w") as f:
            madeby = json.load(f)
    except Exception:
        madeby = {}


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
        
    await interaction.response.send_message(f"{answers_for_send}", ephemeral=True)



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
async def poll(interaction: Interaction, question: str, option1: str, option2: str):
    """ create a poll """

    print(f"\n[{timestr()}] {Fore.YELLOW}{interaction.user.name}{Fore.RESET} used /poll,\n    question: {question}\n    option1: {option1}\n    option2: {option2}")

    if option1 == option2:
        await interaction.response.send_message("選択肢が重複しています", ephemeral=True)
        return
    
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
    embed.add_field(name="Options [0 Votes]", value=f"[**#1**] {option1}\n[**#2**] {option2}")
    embed.add_field(name="Status", value=f"__**Active**__\n**ID: {new_tag}**")
    embed.set_image(url="https://cdn.discordapp.com/attachments/905028183424892929/1104761789410971719/image.png")
    try:
        embed.set_footer(text=f"Poll created by {interaction.user}", icon_url=interaction.user.avatar.url)
    except Exception:
        embed.set_footer(text=f"Poll created by {interaction.user}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")

    message = await interaction.channel.send("[ @everyone ]", embed=embed)
    await message.edit(view=PollSelect(question=question, option1=option1, option2=option2, message=message, madeby=interaction.user, tag=new_tag))
    
    details = {
        "question": question,
        "channel_id": str(message.channel.id),
        "message_id": str(message.id)
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
        await interaction.response.send_message("Use this command in the poll channel or sumbit a correct message ID", ephemeral=True)
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
    await message_to_edit.edit(embed=embed, view=Disabled_PollSelect())
    await interaction.response.send_message(f"Succesfully ended **{question}**\ncheck it now -> {channel.mention}", ephemeral=True)




# Fluid Nodes server cpu sucks
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





client.run(token)