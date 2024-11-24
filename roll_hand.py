import discord
import discord.utils
import random
import re
import datetime
import json

from colorama import Fore
from nr_methods import *


client: discord.Client = None

def set_client1(cli: discord.Client):
    global client
    client = cli
    print(client)

def contains_japanese(text):
    pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uFF65-\uFF9F]+')
    return bool(re.search(pattern, text))


def timestr() -> any:
    timestr = datetime.datetime.now().replace(microsecond=0)
    timestr = timestr + datetime.timedelta(hours=7)
    return timestr


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

