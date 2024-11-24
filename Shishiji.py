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

from discord.utils import MISSING
from typing import Optional, Tuple
from discord.ui.item import Item
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client
from PIL import Image
from discord.interactions import Interaction
from discord.ui import Select, View


client: commands.Bot = None

def set_client6(cli: commands.Bot):
    global client
    client = cli

class RegisterBtn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="実行委員になる", style=discord.ButtonStyle.green)
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        role = interaction.guild.get_role(1153900714301587527)
        if role in interaction.user.roles:
            await interaction.followup.send(f"**あなたは登録されています。**\n間違いだと思われる場合は<@805680950238642188>にお問い合わせください", ephemeral=True)
            return
        await interaction.followup.send("学年を選択してください", view=GradeSelect(), ephemeral=True)


class GradeSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.pressed = False

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="学年を選択して下さい",
        options=[
            discord.SelectOption(label="5 年生", value="5"),
            discord.SelectOption(label="4 年生", value="4"),
            discord.SelectOption(label="先生", value="teacher")
        ]
    )
    async def callback(self, interaction: Interaction, select: Select):
        teacher = False
        info_path = "./SHISHIJI/user_info.json"
        user_id = str(interaction.user.id)
        user_info = {}
        if os.path.exists(info_path):
            with open(info_path, encoding="utf-8") as f:
                user_info: dict = json.load(f)
        if self.pressed:
            return
        user_info[user_id] = {
            "grade": select.values[0]
        }
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(user_info, f, indent=4, ensure_ascii=False)
        options = [
            discord.SelectOption(label="A 組", value="a"),
            discord.SelectOption(label="B 組", value="b"),
            discord.SelectOption(label="C 組", value="c"),
            discord.SelectOption(label="D 組", value="d"),
            discord.SelectOption(label="E 組", value="e"),
            discord.SelectOption(label="F 組", value="f")
        ]
            
        class ClassSelect(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.pressed = False

            @discord.ui.select(
                cls=discord.ui.Select,
                placeholder="クラスを選択して下さい",
                options=options
            )
            async def callback(self, interaction: Interaction, select: Select):
                info_path = "./SHISHIJI/user_info.json"
                user_info = {}
                user_id = str(interaction.user.id)
                if os.path.exists(info_path):
                    with open("./SHISHIJI/user_info.json", encoding="utf-8") as f:
                        user_info = json.load(f)
                if self.pressed:
                    return
                
                user_info[user_id]["class"] = select.values[0]

                with open(info_path, "w", encoding="utf-8") as f:
                    json.dump(user_info, f, indent=4, ensure_ascii=False)
                
                await interaction.response.send_modal(NameModal())
                self.pressed = True

        if not teacher:
            await interaction.response.send_message("次にクラスを選択してください", view=ClassSelect(), ephemeral=True)
        else:
            await interaction.response.send_modal(T_NameModal())
        self.pressed = True




class T_NameModal(discord.ui.Modal, title="フルネームを入力してください"):
    answer = discord.ui.TextInput(label="フルネーム", style=discord.TextStyle.short, placeholder="(例) 山本耕大", required=True, min_length=1)
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        name = str(self.answer).replace(" ", "").replace("　", "")
        re_kanji = re.compile(r'^[\u4E00-\u9FD0]+$')
        status_kanji = re_kanji.fullmatch(name)
        
        if not status_kanji:
            class Submit(discord.ui.View):
                def __init__(self, *, name: str, real: str):
                    super().__init__(timeout=None)
                    self.name = name
                    self.real = real
                    self.pressed = False

                @discord.ui.button(style=discord.ButtonStyle.green, label="間違いありません")
                async def dn(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    await interaction.response.defer()
                    if self.pressed:
                        return
                    await t_register(interaction, self.name, self.real)
                    self.pressed = True

                @discord.ui.button(style=discord.ButtonStyle.red, label="修正します")
                async def rel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    if self.pressed:
                        await interaction.response.defer()
                        return
                    await interaction.response.send_modal(T_NameModal())

            await interaction.followup.send(f"名前(`{name}`)に漢字以外の文字が含まれている可能性がありますが、間違いありませんか？",
                                            view=Submit(name=name, real=str(self.answer)), ephemeral=True)
            return
        
        await t_register(interaction, name, str(self.answer))



class NameModal(discord.ui.Modal, title="出席番号とフルネームを入力してください"):
    answer = discord.ui.TextInput(label="出席番号とフルネーム", style=discord.TextStyle.short, placeholder="(例) 36山本耕大", required=True, min_length=1)
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.d = {
            "１": "1", "２": "2",
            "３": "3", "４": "4",
            "５": "5", "６": "6",
            "７": "7", "８": "8",
            "９": "9", "０": "0"
        }
    
    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        ans = str(self.answer)
        for k in self.d.keys():
            ans = ans.replace(k, self.d[k])
        nump = r"[0-9]+"
        _number = re.findall(nump, ans)
        mlin = "https://discord.com/channels/1153884392448606238/1153910708816318574/1153925069828010054"
        if not len(_number) > 0:
            await interaction.followup.send(f"**出席番号が見つかりませんでした。**初めからやり直してください", ephemeral=True)
            return
        elif int(_number[0]) > 50:
            await interaction.followup.send(f"**出席番号が範囲外です！**初めからやり直してください", ephemeral=True)
            return
        number = int(_number[0])
        name = str(ans).replace("0"+str(number), "").replace(str(number), "").replace(" ", "").replace("　", "")
        re_kanji = re.compile(r'^[\u4E00-\u9FD0]+$')
        status_kanji = re_kanji.fullmatch(name)
        
        if not status_kanji:
            class Submit(discord.ui.View):
                def __init__(self, *, name: str, number: str, answer: str, real: str):
                    super().__init__(timeout=None)
                    self.name = name
                    self.number = number
                    self.answer = answer
                    self.real = real
                    self.pressed = False

                @discord.ui.button(style=discord.ButtonStyle.green, label="間違いありません")
                async def dn(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    await interaction.response.defer()
                    if self.pressed:
                        return
                    await register(interaction, self.name, self.number, self.answer, self.real)
                    self.pressed = True

                @discord.ui.button(style=discord.ButtonStyle.red, label="修正します")
                async def rel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    if self.pressed:
                        await interaction.response.defer()
                        return
                    await interaction.response.send_modal(NameModal())

            await interaction.followup.send(f"名前(`{name}`)に漢字以外の文字が含まれている可能性がありますが、間違いありませんか？",
                                            view=Submit(name=name, number=str(number), answer=ans, real=str(self.answer)), ephemeral=True)
            return
        
        await register(interaction, name, str(number), ans, str(self.answer))



async def register(interaction: discord.Interaction, name: str, number: str, answer: str, real: str, /):
    """Defer the response before call"""

    g_roles = [interaction.guild.get_role(m) for m in [
        1154287629743955978, 1154287764859265024, 1154287812468817981,
        1154287854529294366, 1154287916575629353, 1154287978634555403
    ]]
    role = interaction.guild.get_role(1153900714301587527)
    info_path = "./SHISHIJI/user_info.json"
    user_id = str(interaction.user.id)
    mlin = "https://discord.com/channels/1153884392448606238/1153910708816318574/1153925069828010054"
    with open(info_path, encoding="utf-8") as f:
        user_info: dict = json.load(f)
    
    user_info[user_id]["name"] = name
    user_info[user_id]["number"] = number
    user_info[user_id]["modal"] = {
        "answer": real,
        "detected": {
            "processed": answer,
            "num": number,
            "name": name
        }
    }
    grade: str = user_info[user_id]["grade"]
    g_role = g_roles[int(grade) -1]

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(user_info, f, indent=4, ensure_ascii=False)

    _number = "number"
    info = user_info[user_id]
    nick = f"{info['grade']}{info['class'].upper()}-{info['number'] if len(info['number']) == 2 else f'0{info[_number]}'} {name}"
    role_nr = interaction.guild.get_role(1158538895017902081)
    role_latest = interaction.guild.get_role(1237402978525253752)
    bumonsentakuzumi = interaction.guild.get_role(1161599033152913448)
    upmost = f"\n<#1162643708005584916> __**で部門登録もしてね**__" if not bumonsentakuzumi in interaction.user.roles else ""

    try:
        await interaction.user.edit(nick=nick)
        await interaction.user.add_roles(role, g_role, role_latest)
        await interaction.user.remove_roles(role_nr)
        await interaction.followup.send(f"実行委員に登録しました。全てのチャンネルを閲覧いただけます。{upmost}", ephemeral=True)
    except Exception as e:
        if e.__class__ == discord.errors.Forbidden:
            await interaction.followup.send(f"管理者だったのでニックネームを変更できませんでした(set: {nick}, +{role.mention}, +{g_role.mention}, +{role_latest.mention}, -{role_nr.mention})", ephemeral=True)
        else:
            await interaction.user.remove_roles(role)
            await interaction.followup.send(f"不明なエラーです。初めからやり直してください", ephemeral=True)
        return
    log = interaction.guild.get_channel(1153952454346559508)
    await log.send(f"{interaction.user.mention}```diff\n+ <@{interaction.user.id} {nick}> has just arrived.```")


async def t_register(interaction: discord.Interaction, name: str, real: str, /):
    """Defer the response before call"""

    role = interaction.guild.get_role(1153900714301587527)
    info_path = "./SHISHIJI/user_info.json"
    user_id = str(interaction.user.id)
    mlin = "https://discord.com/channels/1153884392448606238/1153910708816318574/1153925069828010054"
    with open(info_path, encoding="utf-8") as f:
        user_info: dict = json.load(f)
    
    user_info[user_id]["name"] = name
    user_info[user_id]["modal"] = {
        "answer": real,
        "detected": {
            "name": name
        }
    }

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(user_info, f, indent=4, ensure_ascii=False)

    nick = f"{name}"
    t_role = interaction.guild.get_role(1159813381218373693)
    role_nr = interaction.guild.get_role(1158538895017902081)

    try:
        await interaction.user.edit(nick=nick)
        await interaction.user.add_roles(role, t_role)
        await interaction.user.remove_roles(role_nr)
        await interaction.followup.send("先生として登録しました。", ephemeral=True)
    except Exception as e:
        if e.__class__ == discord.errors.Forbidden:
            await interaction.followup.send(f"管理者だったのでニックネームを変更できませんでした(set: {nick}, +{role.mention}, +{t_role.mention}, -{role_nr.mention})", ephemeral=True)
        else:
            await interaction.user.remove_roles(role)
            await interaction.followup.send(f"不明なエラーです。初めからやり直してください", ephemeral=True)
        return
    log = interaction.guild.get_channel(1153952454346559508)
    await log.send(f"**先生が来たぞー！**{interaction.user.mention}```diff\n+ <@{interaction.user.id} {nick}> has just arrived.```")




class Shishiji_Roles:
    def __init__(self):
        self.guild = client.get_guild(1153884392448606238)
        self.done = self.guild.get_role(1161599033152913448)

    def create_select(self, client: commands.Bot) -> discord.ui.View:
        GOT_ROLES = []
        options = []
        ignore = [1161599033152913448, 1161200196374503477]

        for role in self.guild.roles:
            if "部門" in role.name and "副" not in role.name and "長" not in role.name and role.id not in ignore:
                options.append(discord.SelectOption(label=role.name.replace("員", ""), value=str(role.id)))
        
        class SelectRole(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.pressed = False
                self.guild = client.get_guild(1153884392448606238)
                self.done = self.guild.get_role(1161599033152913448)
                self.selected = False

            @discord.ui.select(
                cls=discord.ui.Select,
                placeholder="あなたの部門を選択してください",
                options=options
            )
            async def callback(self, interaction: Interaction, select: Select):
                async def _callback(interaction: Interaction, select: Select):
                    if self.selected:
                        return
                    self.selected = not self.selected
                    value = select.values[0]
                    memb_role = self.guild.get_role(int(value))
                    await interaction.user.add_roles(memb_role)
                    GOT_ROLES.append(memb_role)

                    leader_role_name = memb_role.name.replace("員", "") + "長"
                    sub_leader_role_name = memb_role.name.replace("員", "").replace("部門", "副部門") + "長"
                    next_select_options = []

                    for role in self.guild.roles:
                        if role.name == leader_role_name or role.name == sub_leader_role_name:
                            next_select_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                    if len(next_select_options) == 0:
                        await interaction.user.add_roles(self.done)
                        await interaction.response.send_message(f"完了しました。\n付与: {mention_string(*GOT_ROLES)}", ephemeral=True)
                    else:
                        next_select_options.append(discord.SelectOption(label="上記に該当なし", value="-1"))
                        class _Substance(discord.ui.View):
                            def __init__(self):
                                super().__init__(timeout=None)
                                self.pressed = False
                                self.guild = client.get_guild(1153884392448606238)
                                self.done = self.guild.get_role(1161599033152913448)
                                self.selected = False

                            @discord.ui.select(
                                cls=discord.ui.Select,
                                placeholder="御前の細かい役職を選んでください",
                                options=next_select_options
                            )
                            async def callback(self, interaction: Interaction, select: Select):
                                async def _last_callback(interaction: Interaction, select: Select):
                                    if self.selected:
                                        return
                                    self.selected = not self.selected
                                    value = int(select.values[0])
                                    if value != -1:
                                        rs = []
                                        rs.append(self.guild.get_role(value))
                                        if "長" in role.name:
                                            rs.append(self.guild.get_role(1161210252616794203))
                                        await interaction.user.add_roles(*rs, self.done)
                                        GOT_ROLES.extend(rs)
                                    else:
                                        await interaction.user.add_roles(self.done)
                                    await interaction.response.send_message(f"完了しました。", ephemeral=True)
                                # run
                                await _last_callback(interaction, select)
                    if not interaction.response.is_done():
                        await interaction.response.send_message(view=_Substance(), ephemeral=True)
                # run
                await _callback(interaction, select)
        return SelectRole
    

def mention_string(*roles: discord.Role):
    string = ""
    for role in roles:
        string += ", "+role.mention
    return string[2:]


class MemberVisibleInfoUpdater(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="アップデート！！", style=discord.ButtonStyle.green)
    async def update_my_detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        updated_role = interaction.guild.get_role(1228371737025056791)
        if updated_role in interaction.user.roles:
            await interaction.response.defer()
            return
        info_path = "./SHISHIJI/user_info.json"
        user_id = str(interaction.user.id)
        user_info = {}
        if os.path.exists(info_path):
            with open(info_path, encoding="utf-8") as f:
                user_info: dict = json.load(f)
                
        grade = user_info[user_id]["grade"]

        if not grade:
            if interaction.user.nick.__class__ == str.__class__:
                grade = interaction.user.nick[0]
            else:
                await interaction.response.send_message("Who are you?", ephemeral=True)
                return

        grade = int(grade) + 1
        options = [
            discord.SelectOption(label="A 組", value="a"),
            discord.SelectOption(label="B 組", value="b"),
            discord.SelectOption(label="C 組", value="c"),
            discord.SelectOption(label="D 組", value="d"),
            discord.SelectOption(label="E 組", value="e"),
        ]
        if grade >= 4:
            options.append(discord.SelectOption(label="(F) 組", value="f"))

        class SelectClass(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.pressed = False
                self.guild = client.get_guild(1153884392448606238)
                self.done = self.guild.get_role(1161599033152913448)
                self.selected = False

            @discord.ui.select(
                cls=discord.ui.Select,
                placeholder="あなたの今年度のクラスを選択してください",
                options=options
            )
            async def callback(self, interaction: Interaction, select: Select):
                if self.pressed:
                    await interaction.response.defer()
                    return
                new_class = select.values[0]
                user_info = {}
                if os.path.exists(info_path):
                    with open(info_path, encoding="utf-8") as f:
                        user_info: dict = json.load(f)
                if user_info.get(str(interaction.user.id), None):
                    user_info[str(interaction.user.id)]["class"] = new_class
                else:
                    user_info[str(interaction.user.id)] = { "class": new_class }
                self.pressed = True
                class NameModal(discord.ui.Modal, title="出席番号を入力してください"):
                    answer = discord.ui.TextInput(label="出席番号", style=discord.TextStyle.short, placeholder="(例) 3", required=True, min_length=1, max_length=2)
                    def __init__(self) -> None:
                        super().__init__(timeout=None)
                        self.d = {
                            "１": "1", "２": "2",
                            "３": "3", "４": "4",
                            "５": "5", "６": "6",
                            "７": "7", "８": "8",
                            "９": "9", "０": "0"
                        }
                    
                    async def on_submit(self, interaction: Interaction) -> None:
                        await interaction.response.defer()
                        ans = str(self.answer)
                        for k in self.d.keys():
                            ans = ans.replace(k, self.d[k])
                        try:
                            ans = int(ans)
                            if ans > 55:
                                raise ValueError()
                        except ValueError:
                            await interaction.followup.send("Unexpected number", ephemeral=True)
                            return
                        ans = str(ans)
                        if len(ans) == 1:
                            ans = f"0{ans}"
                        new_name = f"{grade}{new_class.upper()}-{ans} {interaction.user.nick.split(' ')[1]}"
                        updated_role = interaction.guild.get_role(1228371737025056791)
                        try:
                            await interaction.user.edit(nick=new_name)
                            await interaction.user.add_roles(updated_role)
                        except Exception:...
                        with open(info_path, "w", encoding="utf-8") as f:
                            json.dump(user_info, f, indent=4, ensure_ascii=False)
                        log = interaction.guild.get_channel(1153952454346559508)
                        await log.send(f"{interaction.user.mention}```diff\n+ <@{interaction.user.id} {new_name}> has just updated.```")
                        await interaction.followup.send("Done", ephemeral=True)

                await interaction.response.send_modal(NameModal())
        
        await interaction.response.send_message(view=SelectClass(), ephemeral=True)

