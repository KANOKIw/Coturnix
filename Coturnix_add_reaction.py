import requests, json, inspect, sys, datetime, asyncio
import discord, discord.utils, subprocess, os, time, random

from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client


print(f"\n{Fore.GREEN}loading Aternos...{Fore.RESET}\n")

tickets = 0
current_unix_time = time.time()
dt = datetime.datetime.today()

reactions = {
    1: "👍", 2: "👎", 3: "🤮", 4: "🔴", 5: "✅",
    6: "✖", 7: "🎉", 8: "🚮"
    }

#giveawaylist
galist = [0]

#/cmd
cmdlist = ["True", "true", "T", "t"]

def timestr():
    timestr = datetime.datetime.now().replace(microsecond=0)
    return timestr

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
なにかあれば "かのき#7777" にDMしてください
"""

print(logo + inspect.cleandoc(f"""
    Discord BotのTOKENを貼り付けてenterを押してください

    {Style.DIM}このコンソール画面は閉じないでください
    {Style.RESET_ALL}
"""))

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



#custom emojis
javaicon = "<:java:1084395558233444362>"
bedrockicon = "<:bedrock:1084395920306737193>"
switchicon = "<:switch:1084397372580319242>"
aternosicon = "<:aternos:1084397727087087626>"

#intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents) 

#ipembed
ipembed = discord.Embed(title=aternosicon + " サーバーの入り方",description="統合版とjava版どちらでも参加できます",color=0x00ff00)
ipembed.add_field(name=bedrockicon + " 統合版",value="遊ぶ➤サーバー➤下のサーバー追加で下のipを入力➤サーバーに接続")
ipembed.add_field(name=javaicon + " java版",value="下のサーバーipを入力")
ipembed.add_field(name=bedrockicon + " 統合版のip",value=(inspect.cleandoc(f"""**サーバーIP**: SetasabaForEvent.aternos.me
_**ポート**_: 46306""")),inline=False)
ipembed.add_field(name=javaicon + " java版のip",value="SetasabaForEvent.aternos.me:46306")
ipembed.add_field(name=switchicon + " **注意**:Switch版",value=(inspect.cleandoc(f"""Switch版ではデフォルトで**サーバー追加**がないです
[こちら](https://kotoyasyou.work/archives/4873)を参考にしてください""")),inline=False)
ipembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/971597070811168770/1082284879061979178/MOJANG.gif")


async def get_user_input(msg):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, msg)


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


    while True:
        channel_id = await get_user_input(f"input channel_id\n> ")
        if channel_id == "break":
            pass
        else:
            try:
                channel_id = int(channel_id)
                try:
                    channel = client.get_channel(channel_id)
                    if channel.name == None:
                        raise AttributeError("get_channel")
                except Exception:
                    raise AttributeError("get_channel")
            except Exception as e:
                if e.__class__ == ValueError:
                    print("couldn't int(channel_id)")
                elif e.__class__ == AttributeError:
                    print("couldn't get_channel(channel_id)")
                else:
                    print("unknown error")

                while True:
                    channel_id = await get_user_input(f"input channel_id again\n> ")
                    if channel_id == "break":
                        break
                    else:
                        try:
                            channel_id = int(channel_id)
                            try:
                                channel = client.get_channel(channel_id)
                                if channel.name == None:
                                    raise AttributeError("get_channel")
                                break
                            except Exception:
                                raise AttributeError("what??")
                        except Exception as e:
                            if e.__class__ == ValueError:
                                print("couldn't int(channel_id)")
                            elif e.__class__ == AttributeError:
                                print("couldn't get_channel(channel_id)")
                            else:
                                print("unknown error")

            if channel_id == "break":
                pass
            else:
                message_id = await get_user_input(f"input message_id\n> ")
                try:
                    message_id = int(message_id)
                    try:
                        message = await channel.fetch_message(message_id)
                    except Exception:
                        raise AttributeError("fetch_message")
                except Exception as e:
                    if e.__class__ == ValueError:
                        print("couldn't int(message_id)")
                    elif e.__class__ == AttributeError:
                        print("couldn't fetch_message(message_id)")
                    else:
                        print("unknown error")

                    while True:
                        message_id  = await get_user_input(f"input message_id again\n> ")
                        if message_id == "break" or channel_id == "break":
                            break
                        else:
                            try:
                                message_id = int(message_id)
                                try:
                                    message = await channel.fetch_message(message_id)
                                    break
                                except Exception:
                                    raise AttributeError("fetch_message")
                            except Exception as e:
                                if e.__class__ == ValueError:
                                    print("couldn't int(message_id)")
                                elif e.__class__ == AttributeError:
                                    print("couldn't fetch_message(message_id)")
                                else:
                                    print("unknown error")
        
                
                while True:
                    if  message_id == "break" or channel_id == "break":
                        break
                    else:
                        reactionnum = await get_user_input(f"input reaction\n{reactions}\n> ")
                        if reactionnum == "break":
                            break
                        else:
                            try:
                                reactionnum = int(reactionnum)
                                if reactions.get(reactionnum, None):
                                    emoji = reactions.get(reactionnum)
                                    await message.add_reaction(emoji)
                                    attachments = len(message.attachments)
                                    embeds = len(message.embeds)
                                    if attachments > 0:
                                        if embeds > 0:
                                            print(f"reacted {emoji} to {message.author.name}'s message({message.content}, att: {attachments}, embeds: {embeds})")
                                        else:
                                            print(f"reacted {emoji} to {message.author.name}'s message({message.content}, {attachments})")
                                    else:
                                        print(f"reacted {emoji} to {message.author.name}'s message({message.content})")
                                    break
                                else:
                                    raise Exception("だめだね")
                            except Exception as e:
                                if e.__class__ == AttributeError:
                                    print(f"input intable value")
                                if e.__class__ == Exception:
                                    print(f"input included number")
                                else:
                                    print(e)









































































































































































































































































































































































































































































client.run(token)