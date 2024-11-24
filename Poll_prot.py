import json
import discord
import discord.utils
import os
import matplotlib.pyplot as plt
import time
import threading
import random
import urllib.parse

from typing import List
from typing import Callable as function
from colorama import Fore
from nr_methods import *


client: discord.Client = None

def set_client2(cli: discord.Client):
    global client
    client = cli


_white_list: List[int] = []

def _set_on_cooldown(id: int, /) -> None:
    global _white_list
    _white_list.append(id)
    time.sleep(5)
    if _is_on_cooldown(id):
        _white_list.remove(id)


def _is_on_cooldown(id: int, /) -> bool:
    global _white_list
    return id in _white_list


def _rm_on_cooldown(id: int, /) -> bool:
    global _white_list
    if _is_on_cooldown(id):
        _white_list.remove(id)


async def start_thread_async(func: function, *args) -> threading.Thread:
    a = threading.Thread(target=func, args=args)
    a.daemon = True
    a.start()
    return a


class PollSelect(discord.ui.View):
    def __init__(self, question: str, option1: str, option2: str, message: discord.Message, madeby: discord.User, tag: str):
        super().__init__(timeout=None)
        self.question = question; self.option1 = option1; self.option2 = option2; self.message = message; self.madeby = madeby;self.tag = tag
        self.KUMANKEN = client.get_user(1080464218110832660)
        
        
    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #1 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id): 
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        voted = self.votes[3]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
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
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "options": {
                "#1": self.option1,
                "#2": self.option2
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)


        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


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
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)    
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        voted = self.votes[3]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "2":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
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
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        

        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "options": {
                "#1": self.option1,
                "#2": self.option2
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)      
            
        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")

        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect(question=self.question, option1=self.option1, option2=self.option2, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#2 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()



class Disabled_PollSelect_three(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectsecond(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#3", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectthird(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    


class PollSelect_three(discord.ui.View):
    def __init__(self, question: str, option1: str, option2: str, message: discord.Message, option3: str, madeby: discord.User, tag: str):
        super().__init__(timeout=None)
        self.question = question; self.option1 = option1; self.option2 = option2; self.option3 = option3; self.message = message; self.madeby = madeby;self.tag = tag

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #1 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        voted = self.votes[4]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
            elif voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[0] += 1
            else:
                self.votes[2] -= 1
                self.votes[0] += 1
        else:
            changes = 0
            change = False
            self.votes[0] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2]

        
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
        third_rate = f"{(self.votes[2] / all)*100:.1f}"
        labels = [f"#3 {third_rate}%", f"#2 {second_rate}%", f"#1 {first_rate}%"]
        if self.votes[0] == 0 and self.votes[1] == 0:
            labels = [f"#3 {third_rate}%", "others 0%", "others 0%"]
        if self.votes[0] == 0 and self.votes[2] == 0:
            labels = ["others 0%", f"#2 {second_rate}%", "others 0%"]
        if self.votes[1] == 0 and self.votes[2] == 0:
            labels = ["others 0%", "others 0%", f"#1 {first_rate}%"]

        colors = ["#ff9700", "#504464", "#30746c"]

        x = [self.votes[2], self.votes[1], self.votes[0]]

        if self.votes[1] > self.votes[0]:
            if self.votes[2] > self.votes[1]:
                embedcolor = 0xff9700
            else:
                embedcolor = 0x504464
        elif self.votes[2] > self.votes[0]:
            if self.votes[1] > self.votes[2]:
                embedcolor = 0x504464
            else:
                embedcolor = 0xff9700
        else:
            embedcolor = 0x30746c

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_three(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#1 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()



    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary)
    async def selectsecond(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #2 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        voted = self.votes[4]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[1] += 1
            elif voted[str(interaction.user.id)]["voted"] == "2":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
            else:
                self.votes[2] -= 1
                self.votes[1] += 1
        else:
            changes = 0
            change = False
            self.votes[1] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2]

        
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
        third_rate = f"{(self.votes[2] / all)*100:.1f}"
        labels = [f"#3 {third_rate}%", f"#2 {second_rate}%", f"#1 {first_rate}%"]
        if self.votes[0] == 0 and self.votes[1] == 0:
            labels = [f"#3 {third_rate}%", "others 0%", "others 0%"]
        if self.votes[0] == 0 and self.votes[2] == 0:
            labels = ["others 0%", f"#2 {second_rate}%", "others 0%"]
        if self.votes[1] == 0 and self.votes[2] == 0:
            labels = ["others 0%", "others 0%", f"#1 {first_rate}%"]
        colors = ["#ff9700", "#504464", "#30746c"]

        x = [self.votes[2], self.votes[1], self.votes[0]]

        if self.votes[1] > self.votes[0]:
            if self.votes[2] > self.votes[1]:
                embedcolor = 0xff9700
            else:
                embedcolor = 0x504464
        elif self.votes[2] > self.votes[0]:
            if self.votes[1] > self.votes[2]:
                embedcolor = 0x504464
            else:
                embedcolor = 0xff9700
        else:
            embedcolor = 0x30746c

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_three(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#2 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()

    @discord.ui.button(label = "#3", style = discord.ButtonStyle.secondary)
    async def selectthird(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #3 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        voted = self.votes[4]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[2] += 1
            elif voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[2] += 1
            else:
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
        else:
            changes = 0
            change = False
            self.votes[2] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2]

        
        if change is True:
            changes += 1
            print("-> change")
        user_info = {
            "voted": "3",
            "name": interaction.user.name,
            "last": str(timestr()),
            "changes": changes
        }



        voted[str(interaction.user.id)] = user_info
    

        first_rate = f"{(self.votes[0] / all)*100:.1f}"
        second_rate = f"{(self.votes[1] / all)*100:.1f}"
        third_rate = f"{(self.votes[2] / all)*100:.1f}"
        labels = [f"#3 {third_rate}%", f"#2 {second_rate}%", f"#1 {first_rate}%"]
        if self.votes[0] == 0 and self.votes[1] == 0:
            labels = [f"#3 {third_rate}%", "others 0%", "others 0%"]
        if self.votes[0] == 0 and self.votes[2] == 0:
            labels = ["others 0%", f"#2 {second_rate}%", "others 0%"]
        if self.votes[1] == 0 and self.votes[2] == 0:
            labels = ["others 0%", "others 0%", f"#1 {first_rate}%"]
        colors = ["#ff9700", "#504464", "#30746c"]

        x = [self.votes[2], self.votes[1], self.votes[0]]

        if self.votes[1] > self.votes[0]:
            if self.votes[2] > self.votes[1]:
                embedcolor = 0xff9700
            else:
                embedcolor = 0x504464
        elif self.votes[2] > self.votes[0]:
            if self.votes[1] > self.votes[2]:
                embedcolor = 0x504464
            else:
                embedcolor = 0xff9700
        else:
            embedcolor = 0x30746c

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_three(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#3 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()
    


class Disabled_PollSelect_four(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectsecond(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#3", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectthird(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
    @discord.ui.button(label = "#4", style = discord.ButtonStyle.secondary, disabled=True)
    async def selectfour(self, interaction: discord.Interaction, button: discord.ui.Button):
        return



class PollSelect_four(discord.ui.View):
    def __init__(self, question: str, option1: str, option2: str, message: discord.Message, option3: str, option4: str, madeby: discord.User, tag: str):
        super().__init__(timeout=None)
        self.question = question; self.option1 = option1; self.option2 = option2; self.option3 = option3; self.option4 = option4; self.message = message; self.madeby = madeby;self.tag = tag

    @discord.ui.button(label = "#1", style = discord.ButtonStyle.secondary)
    async def selectfirst(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #1 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        self.votes[3] = int(self.votes[3])
        voted = self.votes[5]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
            elif voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[0] += 1
            elif voted[str(interaction.user.id)]["voted"] == "3":
                self.votes[2] -= 1
                self.votes[0] += 1
            else:
                self.votes[3] -= 1
                self.votes[0] += 1
        else:
            changes = 0
            change = False
            self.votes[0] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2] + self.votes[3]

        
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
    

        first_rate = f"#1 {(self.votes[0] / all)*100:.1f}%" if f"{(self.votes[0] / all)*100:.1f}" != "0.0" else "others 0%"
        second_rate = f"#2 {(self.votes[1] / all)*100:.1f}%" if f"{(self.votes[1] / all)*100:.1f}" != "0.0" else "others 0%"
        third_rate = f"#3 {(self.votes[2] / all)*100:.1f}%" if f"{(self.votes[2] / all)*100:.1f}" != "0.0" else "others 0%"
        fourth_rate = f"#4 {(self.votes[3] / all)*100:.1f}%" if f"{(self.votes[3] / all)*100:.1f}" != "0.0" else "others 0%"

        labels = [f"{fourth_rate}", f"{third_rate}", f"{second_rate}", f"{first_rate}"]
        inds = []
        for k in range(len(labels)):
            if labels[k] == "others 0%":
                inds.append(k)
        for i in range(len(inds)):
            if i == 0:
                continue
            else:
                labels[inds[i]] = ""

        colors = ["#ff58aa", "#ff9700", "#504464", "#30746c"]

        x = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list.sort()

        color_mapping_dict = {
            self.votes[0]: 0x30746c,
            self.votes[1]: 0x504464,
            self.votes[2]: 0xff9700,
            self.votes[3]: 0xff58aa
            }

        embedcolor = color_mapping_dict[tmp_list[-1]]

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "#4": self.votes[3],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3,
                "#4": self.option4
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2] + votes_list[3]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}\n[**#4**] {self.option4}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_four(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, option4=self.option4, message=self.message, madeby=self.madeby, tag=self.tag))        
        await interaction.followup.send("#1 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()

    @discord.ui.button(label = "#2", style = discord.ButtonStyle.secondary)
    async def selectsecond(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #2 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        self.votes[3] = int(self.votes[3])
        voted = self.votes[5]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[1] += 1
            elif voted[str(interaction.user.id)]["voted"] == "2":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
            elif voted[str(interaction.user.id)]["voted"] == "3":
                self.votes[2] -= 1
                self.votes[1] += 1
            else:
                self.votes[3] -= 1
                self.votes[1] += 1
        else:
            changes = 0
            change = False
            self.votes[1] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2] + self.votes[3]

        
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
    

        first_rate = f"#1 {(self.votes[0] / all)*100:.1f}%" if f"{(self.votes[0] / all)*100:.1f}" != "0.0" else "others 0%"
        second_rate = f"#2 {(self.votes[1] / all)*100:.1f}%" if f"{(self.votes[1] / all)*100:.1f}" != "0.0" else "others 0%"
        third_rate = f"#3 {(self.votes[2] / all)*100:.1f}%" if f"{(self.votes[2] / all)*100:.1f}" != "0.0" else "others 0%"
        fourth_rate = f"#4 {(self.votes[3] / all)*100:.1f}%" if f"{(self.votes[3] / all)*100:.1f}" != "0.0" else "others 0%"

        labels = [f"{fourth_rate}", f"{third_rate}", f"{second_rate}", f"{first_rate}"]
        inds = []
        for k in range(len(labels)):
            if labels[k] == "others 0%":
                inds.append(k)
        for i in range(len(inds)):
            if i == 0:
                continue
            else:
                labels[inds[i]] = ""

        colors = ["#ff58aa", "#ff9700", "#504464", "#30746c"]

        x = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list.sort()

        color_mapping_dict = {
            self.votes[0]: 0x30746c,
            self.votes[1]: 0x504464,
            self.votes[2]: 0xff9700,
            self.votes[3]: 0xff58aa
            }

        embedcolor = color_mapping_dict[tmp_list[-1]]

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "#4": self.votes[3],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3,
                "#4": self.option4
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2] + votes_list[3]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}\n[**#4**] {self.option4}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_four(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, option4=self.option4, message=self.message, madeby=self.madeby, tag=self.tag))        
        await interaction.followup.send("#2 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()

    @discord.ui.button(label = "#3", style = discord.ButtonStyle.secondary)
    async def selectthird(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #3 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        self.votes[3] = int(self.votes[3])
        voted = self.votes[5]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[2] += 1
            elif voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[2] += 1
            elif voted[str(interaction.user.id)]["voted"] == "3":
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
            else:
                self.votes[3] -= 1
                self.votes[2] += 1
        else:
            changes = 0
            change = False
            self.votes[2] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2] + self.votes[3]

        
        if change is True:
            changes += 1
            print("-> change")
        user_info = {
            "voted": "3",
            "name": interaction.user.name,
            "last": str(timestr()),
            "changes": changes
        }



        voted[str(interaction.user.id)] = user_info
    

        first_rate = f"#1 {(self.votes[0] / all)*100:.1f}%" if f"{(self.votes[0] / all)*100:.1f}" != "0.0" else "others 0%"
        second_rate = f"#2 {(self.votes[1] / all)*100:.1f}%" if f"{(self.votes[1] / all)*100:.1f}" != "0.0" else "others 0%"
        third_rate = f"#3 {(self.votes[2] / all)*100:.1f}%" if f"{(self.votes[2] / all)*100:.1f}" != "0.0" else "others 0%"
        fourth_rate = f"#4 {(self.votes[3] / all)*100:.1f}%" if f"{(self.votes[3] / all)*100:.1f}" != "0.0" else "others 0%"

        labels = [f"{fourth_rate}", f"{third_rate}", f"{second_rate}", f"{first_rate}"]
        inds = []
        for k in range(len(labels)):
            if labels[k] == "others 0%":
                inds.append(k)
        for i in range(len(inds)):
            if i == 0:
                continue
            else:
                labels[inds[i]] = ""

        colors = ["#ff58aa", "#ff9700", "#504464", "#30746c"]

        x = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list.sort()

        color_mapping_dict = {
            self.votes[0]: 0x30746c,
            self.votes[1]: 0x504464,
            self.votes[2]: 0xff9700,
            self.votes[3]: 0xff58aa
            }

        embedcolor = color_mapping_dict[tmp_list[-1]]

        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "#4": self.votes[3],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3,
                "#4": self.option4
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2] + votes_list[3]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}\n[**#4**] {self.option4}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_four(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, option4=self.option4, message=self.message, madeby=self.madeby, tag=self.tag))        
        await interaction.followup.send("#3 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()

    @discord.ui.button(label = "#4", style = discord.ButtonStyle.secondary)
    async def selectfourth(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.CYAN}{interaction.user.name}{Fore.RESET} selected #4 at {self.question}")

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            with open(f"poll/{self.question}_poll.json") as f:
                self.votes: dict = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("ファイルが破損しているか削除されています。", ephemeral=True)
            return

        if _is_on_cooldown(interaction.user.id):
            await interaction.followup.send("選択のクールダウン中です！", ephemeral=True)
            return
        thre = await start_thread_async(_set_on_cooldown, interaction.user.id)
        n = self.votes.get("n", 0)         
        self.votes = list(self.votes.values())

        self.votes[0] = int(self.votes[0])
        self.votes[1] = int(self.votes[1])
        self.votes[2] = int(self.votes[2])
        self.votes[3] = int(self.votes[3])
        voted = self.votes[5]

        if str(interaction.user.id) in voted.keys():
            changes = voted[str(interaction.user.id)]["changes"]
            change = True
            if voted[str(interaction.user.id)]["voted"] == "1":
                self.votes[0] -= 1
                self.votes[3] += 1
            elif voted[str(interaction.user.id)]["voted"] == "2":
                self.votes[1] -= 1
                self.votes[3] += 1
            elif voted[str(interaction.user.id)]["voted"] == "3":
                self.votes[2] -= 1
                self.votes[3] += 1
            else:
                await interaction.followup.send("選択中の選択肢です！", ephemeral=True)
                print("-> same")
                _rm_on_cooldown(interaction.user.id)
                return
        else:
            changes = 0
            change = False
            self.votes[3] += 1
        all = self.votes[0] + self.votes[1] + self.votes[2] + self.votes[3]

        
        if change is True:
            changes += 1
            print("-> change")
        user_info = {
            "voted": "4",
            "name": interaction.user.name,
            "last": str(timestr()),
            "changes": changes
        }



        voted[str(interaction.user.id)] = user_info
    

        first_rate = f"#1 {(self.votes[0] / all)*100:.1f}%" if f"{(self.votes[0] / all)*100:.1f}" != "0.0" else "others 0%"
        second_rate = f"#2 {(self.votes[1] / all)*100:.1f}%" if f"{(self.votes[1] / all)*100:.1f}" != "0.0" else "others 0%"
        third_rate = f"#3 {(self.votes[2] / all)*100:.1f}%" if f"{(self.votes[2] / all)*100:.1f}" != "0.0" else "others 0%"
        fourth_rate = f"#4 {(self.votes[3] / all)*100:.1f}%" if f"{(self.votes[3] / all)*100:.1f}" != "0.0" else "others 0%"

        labels = [f"{fourth_rate}", f"{third_rate}", f"{second_rate}", f"{first_rate}"]
        inds = []
        for k in range(len(labels)):
            if labels[k] == "others 0%":
                inds.append(k)
        for i in range(len(inds)):
            if i == 0:
                continue
            else:
                labels[inds[i]] = ""

        colors = ["#ff58aa", "#ff9700", "#504464", "#30746c"]

        x = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list = [self.votes[3], self.votes[2], self.votes[1], self.votes[0]]
        tmp_list.sort()

        color_mapping_dict = {
            self.votes[0]: 0x30746c,
            self.votes[1]: 0x504464,
            self.votes[2]: 0xff9700,
            self.votes[3]: 0xff58aa
            }

        embedcolor = color_mapping_dict[tmp_list[-1]]
        
        textprops = {
            "color": "white",
            "size": "large",
            "backgroundcolor": "#102001"
        }


        plt.figure(facecolor="#303434")
        
        
        plt.pie(x=x, colors=colors, labels=labels, startangle=90, textprops=textprops)
        plt.savefig(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n}_pie.png")
        
        
        n += 1
        self.votes = {
            "#1": self.votes[0],
            "#2": self.votes[1],
            "#3": self.votes[2],
            "#4": self.votes[3],
            "options": {
                "#1": self.option1,
                "#2": self.option2,
                "#3": self.option3,
                "#4": self.option4
            },
            "voted": voted,
            "madeby": str(self.madeby.id),
            "n": n
        }



        with open(f"poll/{self.question}_poll.json", "w") as f:
            json.dump(self.votes, f, ensure_ascii=False, indent=4)

        image_url = f"http://cdn.kanokiw.com:8443/tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-1}_pie.png?{random.randint(0, 1000*1000)}"
        

        votes_list = list(self.votes.values())
        _voted = votes_list[0] + votes_list[1] + votes_list[2] + votes_list[3]
        _voted = make_number_clear(str(_voted))
        embed = discord.Embed(title=self.question, color=embedcolor)
        embed.add_field(name=f"Options [{_voted} Votes]", value=f"[**#1**] {self.option1}\n[**#2**] {self.option2}\n[**#3**] {self.option3}\n[**#4**] {self.option4}")
        embed.add_field(name=f"Status", value=f"__**Active**__\n**ID: {self.tag}**")
        embed.set_image(url=image_url)
        
        if os.path.exists(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png"):
            os.remove(f"tmp/{urllib.parse.quote(self.question.replace(' ', '-').replace('　', '-').replace('?', '_').replace('&', '_'))}{n-2}_pie.png")


        try:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url=self.madeby.avatar.url)
        except Exception:
            embed.set_footer(text=f"Poll created by {self.madeby}", icon_url="https://static.vecteezy.com/system/resources/previews/006/892/625/original/discord-logo-icon-editorial-free-vector.jpg")


        await self.message.edit(embed=embed, view=PollSelect_four(question=self.question, option1=self.option1, option2=self.option2, option3=self.option3, option4=self.option4, message=self.message, madeby=self.madeby, tag=self.tag))
        await interaction.followup.send("#4 に投票しました", ephemeral=True)

        plt.clf()
        plt.close()

