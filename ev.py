import requests, json, inspect, sys, datetime, asyncio
import discord, discord.utils, subprocess, os, time, random

from enum import Enum
from subprocess import PIPE
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands

token = "MTA4MjYxMDg2OTc1NTcwNzQ0Mg.GN2pqW._CK_5stEYGOlTktRqcHLg8Q6MXQAtkWjpaOYzA"
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    st = client.get_guild(1101399573991268374)
    print(st.get_member(805680950238642188).status)
    class Roles:
        class SetagaQuest:
            @staticmethod
            def gr(id: int) -> discord.Role:
                return st.get_role(id)

            programmer = gr(1105789722657304678)
            web_designer = gr(1118902886714331197)
            motion_effect = gr(1118934733108297879)
            illustrator = gr(1105790371100897453)
            AR_3D = gr(1118900539028148367)
            movie_creator = gr(1111149742542565456)
            scenario_writer = gr(1118936362700247050)
            level_designer = gr(1105787037409361972)
            voice_actor = gr(1118901236335386655)
            sound_designer = gr(1119173669214760970)
            free_agent = gr(1118903186233761873)
            member = gr(1101419218253131846)
            real_agent = gr(1119577850652143626)

    _st_roles = [
        Roles.SetagaQuest.programmer,
        Roles.SetagaQuest.web_designer,
        Roles.SetagaQuest.motion_effect,
        Roles.SetagaQuest.illustrator,
        Roles.SetagaQuest.AR_3D,
        Roles.SetagaQuest.movie_creator,
        Roles.SetagaQuest.scenario_writer,
        Roles.SetagaQuest.level_designer,
        Roles.SetagaQuest.voice_actor,
        Roles.SetagaQuest.sound_designer,
        Roles.SetagaQuest.real_agent
    ]
    t = client.get_guild(971597070303625268).get_member(1080464218110832660)
    print(t.color)
    return
    for mem in st.members:
        if Roles.SetagaQuest.free_agent in mem.roles:
            for r in _st_roles:
                if r in mem.roles:
                    break
            else:
                print(mem.nick if mem.nick is not None else mem.global_name)



client.run(token)
