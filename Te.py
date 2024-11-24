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
from typing import Optional
from discord.ui.item import Item
from colorama import Fore, Style
from discord.ext import commands
from discord import app_commands
from python_aternos import Client
from PIL import Image
from discord.interactions import Interaction
from discord.ui import Select, View


def _escapeHTML(_str: str):
    return _str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;").replace(" ", "&nbsp;").replace("\n", "<br>")


def int_to_rgb(integer_value: int) -> str:
    red = (integer_value >> 16) & 0xFF
    green = (integer_value >> 8) & 0xFF
    blue = integer_value & 0xFF
    return f"rgb({red}, {green}, {blue})"


class TicketModal(discord.ui.Modal, title="Create Ticket"):
    answer = discord.ui.TextInput(label="REASON:", style=discord.TextStyle.short, placeholder=None, required=True, min_length=1)

    def __init__(self, *, ticket_line: discord.CategoryChannel, support_role: discord.Role, cache_channel: discord.channel.TextChannel | None = None) -> None:
        super().__init__()
        self.category, self.support, self.cache = ticket_line, support_role, cache_channel

    async def on_submit(self, interaction: discord.Interaction):
        self.answer = str(self.answer)
        await interaction.response.defer(thinking=True, ephemeral=True)
        overwrites = {
            interaction.user.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            self.support: discord.PermissionOverwrite(read_messages=True)
        }
        na = interaction.user.nick
        if not na:
            na = interaction.user.global_name

        ticketchannel = await self.category.create_text_channel(name=na.replace(".", "") + "-" + str(int(interaction.user.id)), overwrites=overwrites)
        ticketfile = f"./tickets/{ticketchannel.id}_ticketmsgcache.json"

        with open("ticket_channelids.json") as f:
            po = list(map(int, json.load(f)))
            if ticketchannel.id not in po:
                po.append(ticketchannel.id)
        with open("ticket_channelids.json", "w") as f:
            json.dump(po, f, indent=4)
        
        guide = f"""Hello {interaction.user.mention}! Thank you for contacting support. Please explain your issue below.

**Reason:**
```{self.answer}```"""
        ticketembed = discord.Embed(title=f"Ticket | {na}", description=guide, color=0xffaa00)

        msg: discord.Message = await ticketchannel.send(embed=ticketembed, view=TicketCloseConfirm(channel=ticketchannel, creator=interaction.user, cache=self.cache))
        with open(ticketfile, "w") as f:
            json.dump([
                    {
                    "embed": {
                        "type": "guide",
                        "color": 0xffaa00,
                        "mention": f"@{na}",
                        "reason": self.answer,
                    },
                    "role_color": interaction.guild.get_member(1082610869755707442).top_role.color.value,
                    "time": (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y/%m/%d/%H:%M"),
                    "id": msg.id,
                    "created_at": int(time.time()),
                    "attachments": [],
                    "participants": []
                }
            ], f, indent=4)
        try:
            with open("./ticket_closers.json") as f:
                p = json.load(f)
        except FileNotFoundError:
            p = []
        p.append({
            "channel": ticketchannel.id,
            "message": msg.id,
            "creator": interaction.user.id
        })
        with open("./ticket_closers.json", "w") as f:
            json.dump(p, f, indent=4)

        await interaction.followup.send(f"You have created a new ticket channel: {ticketchannel.mention}", ephemeral=True)


class TicketCloseConfirm(discord.ui.View):
    def __init__(self, *, channel: discord.channel, creator: discord.Member, cache: discord.channel.TextChannel | None = None):
        super().__init__(timeout=None)
        self.channel, self.creator, self.cache = channel, creator, cache

    @discord.ui.button(label="Close", emoji="<:trashbox:1129096572098060469>", style=discord.ButtonStyle.red)
    async def send_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Close Ticket", description="Are you sure you want to close this ticket?", color=0xed4245)
        await interaction.channel.send(embed=embed, view=TicketCloser(channel=self.channel, creator=self.creator, cache=self.cache))
        await interaction.response.defer()


class TicketCloser(discord.ui.View):
    def __init__(self, *, channel: discord.TextChannel, creator: discord.Member, cache: discord.channel.TextChannel | None = None):
        super().__init__(timeout=180)
        self.channel, self.creator, self.cache = channel, creator, cache

    @discord.ui.button(label="Close", emoji="<:trashbox:1129096572098060469>", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        with open("./ticket_channelids.json") as f:
            po = list(map(int, json.load(f)))
            if self.channel.id in po:
                po.remove(self.channel.id)
        with open("./ticket_channelids.json", "w") as f:
            json.dump(po, f, indent=4)

        with open("./ticket_closers.json") as f:
            p: list[dict] = json.load(f)
        for h in p:
            if h.get("channel", 0) == interaction.channel.id:
                p.remove(h)
        with open("./ticket_closers.json", "w") as f:
            json.dump(p, f, indent=4)
            
        html = """<!DOCTYPE html>
    <html lang="ja" original-ticket discord-like>
    <head>
        <title>ticket - ?www.//Opisovasghaw</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://code.jquery.com/jquery-1.9.1.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/markdown-it/8.2.2/markdown-it.min.js"></script>
        <script
            src="https://code.jquery.com/jquery-2.2.4.min.js"
            integrity="sha384-rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB"
            crossorigin="anonymous">
        </script>
        <link rel="stylesheet" href="//cdn.kanokiw.com/assets/ticket/ticket.css">
        <link rel="icon" href="//cdn.kanokiw.com/assets/ticket/Coturnix.ico">
        <script>
var w=[];var g={};$(function(){var f=document.getElementsByClassName("chatlog--message-content");var g=document.getElementsByClassName("chatlog--embed-description");var k=[...f,...g];for(var i=0;i<k.length;i++){var d=k[i];var l=d.innerHTML;try{l=marked(l)}catch(exc){} d.innerHTML=l}}); function e(j){const r=document.getElementById(j);r.scrollIntoView({behavior:'smooth',block:'start',inline:'center'});if(g[j]!=null){for(var k of g[j]){clearTimeout(k);g[j].filter(l=>l!==k)}}else{g[j]=[]} w.push(j);cL=r.classList[0]["/"];r.classList.remove("chatlog-message-block--highlighted");r.classList.remove("fade-out");setTimeout(function(){r.classList.add("chatlog-message-block--highlighted");r.classList.add("fade-out")},0); var e=setTimeout(function(){r.classList.remove("chatlog-message-block--highlighted");r.classList.remove("fade-out");w=w.filter(m=>m!==j)},2000);g[j].push(e)} function jump(k){window.location.href=k} !function(d,l){"use strict";var e=!1,n=!1;if(l.querySelector&&d.addEventListener){e=!0} if(d.wp=d.wp||{},!d.wp.receiveEmbedMessage) if(d.wp.receiveEmbedMessage=function(e){var t=e.data;if(t){if(t.secret||t.message||t.value){if(!/[^a-zA-Z0-9]/.test(t.secret)){for(var r,i,a,s=l.querySelectorAll('iframe[data-secret="'+t.secret+'"]'),n=l.querySelectorAll('blockquote[data-secret="'+t.secret+'"]'),o=new RegExp("^https?:$","i"),c=0;c<n.length;c++) n[c].style.display="none";for(c=0;c<s.length;c++){if(r=s[c],e.source===r.contentWindow){if(r.removeAttribute("style"),"height"===t.message){if(1e3<(a=parseInt(t.value,10))){a=1e3}else if(~~a<200){a=200} r.height=a} if("link"===t.message){if(i=l.createElement("a"),a=l.createElement("a"),i.href=r.getAttribute("src"),a.href=t.value,o.test(a.protocol)){if(a.host===i.host){if(l.activeElement===r){d.top.location.href=t.value}}}}}}}}}},e){d.addEventListener("message",d.wp.receiveEmbedMessage,!1),l.addEventListener("DOMContentLoaded",t,!1),d.addEventListener("load",t,!1)} function t(){if(!n){n=!0;for(var e,t,r=-1!==navigator.appVersion.indexOf("MSIE 10"),i=!!navigator.userAgent.match(/Trident.*rv:11\./),a=l.querySelectorAll("iframe.wp-embedded-content"),s=0;s<a.length;s++){if(!(e=a[s]).getAttribute("data-secret")) t=Math.random().toString(36).substr(2,10),e.src+="#?secret="+t,e.setAttribute("data-secret",t);if(r||i)(t=e.cloneNode(!0)).removeAttribute("security"),e.parentNode.replaceChild(t,e)}}}}(window,document);const s=window.addEventListener("click",function(i){if(i.target.classList.contains("chatlog--replyed-message-content-prefix")&&n){n(i.target.getAttribute("gp"));}else if(i.target.classList.contains("chatlog--replyed-message-content")&&p){p(i.target.children[0].getAttribute("gp"));}else if(i.target.tagName.toUpperCase()==="ATTACHMENT"&&h){h(i.target.innerText);}});const i=window.addEventListener;const n="click dblclick gesturestart resize".split(" ").forEach(function(o){function u(a){a.preventDefault();}i.apply(this,[o,u,{passive:false}]);});window.addEventListener("touchstart", function(e){e.target.classList.add("active");});window.addEventListener("touchend",function(e){e.target.classList.remove("active");});window.addEventListener("DOMContentLoaded",function(){for (const j of document.getElementsByClassName("chatlog-message-block-")){j.addEventListener("click", function(){const t = this.getAttribute("gp");e(String(t));});}});
        </script>
    </head>
    <body>
        <div id="bottom-display-conquester">
            <div id="bottom-display">
                <img class="bottom-display-slave-img" src="https://cdn.kanokiw.com/assets/ticket/coturnix_b.png">
                <h4>Coturnix - ticket transcript</h4>
            </div>
        </div>
        <!-- Message ID digits on discord -->"""     
        html = html.replace("?www.//Opisovasghaw", _escapeHTML(self.creator.name))
        html += f"""
        <div class="chatlog-message-block but-not-a-chatlog">
            <img id="server-icon" src="{self.channel.guild.icon.url}">
            <div id="server-ticket--details">
                <div class="chatlog-text--name-guild">{_escapeHTML(self.channel.guild.name)}</div>
                <div class="chatlog-text--name-ticket">ticket - {_escapeHTML(self.creator.name)}</div>
                <div class="chatlog-text">This is the start of the #ticket-{_escapeHTML(self.creator.name)} channel.</div>
            </div>
        </div>
        <hr class="chatlog-divider">"""
        with open(f"./tickets/{self.channel.id}_ticketmsgcache.json") as f:
            data = json.load(f)
            participants = data[0]["participants"]
            for id in [self.creator.id, 1082610869755707442]:
                try:participants.remove(id)
                except ValueError:...
            for block in data:
                attachments = block.get("attachments", [])
                attr = f"\n".join([f'<a href="{attachment}" target="_blank"><attachment onclick="h(this.innerText)">{attachment}</attachment></a><br>' for attachment in attachments])
                if block.get("embed", None):
                    match block["embed"]["type"]:
                        case "guide":
                            html += f"""
        <div class="chatlog-message-block" id="{block["id"]}">
            <span class="upper-icon"><img class="author-icon" src="https://cdn.discordapp.com/avatars/1082610869755707442/6c1693c65c291e3fb1b80777d14e5611.png?size=1024"></span>
            <div class="not-icon">
                <div class="author-details">
                    <span class="author-name" style="color: {int_to_rgb(block["role_color"])};">Coturnix</span>
                    <span class="author-tag">BOT</span>
                    <span class="authed-datetime">{block.get("time", "Unknown")}</span>
                    <div class="chatlog--embed">
                        <div class="chatlog--emed-color" style="background-color: {int_to_rgb(block["embed"]["color"])};"></div>
                        <div class="chatlog--embed-container">
                            <div class="chatlog--embed-content">
                                <div class="chatlog--embed-text">
                                    <div class="chatlog--embed-title">Ticket | {_escapeHTML(self.creator.name)}</div>
                                    <div class="chatlog--embed-description">Hello 
                                        <span class="user--mention ">{block["embed"]["mention"]}</span>!
                                        Thank you for contacting support. Please explain your issue below.
                                        <br>
                                        <br>
                                        <strong>Reason:</strong>
                                        <div class="pre-multiline">{_escapeHTML(block["embed"]["reason"])}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ticket-options">
                        <!-- We only preserve expected buttons due to being no way to get buttons from messages -->
                        <button class="bot-button">
                            <div class="bot-button-inner">
                                <img src="//cdn.kanokiw.com/assets/ticket/trashbox.webp" draggable="false">
                                <div class="button-content">Close</div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>"""
                        case "closer":
                            html += f"""
        <hr class="chatlog-divider">
        <div class="chatlog-message-block" id="{block["id"]}">
            <span><img class="author-icon" src="https://cdn.discordapp.com/avatars/1082610869755707442/6c1693c65c291e3fb1b80777d14e5611.png?size=1024"></span>
            <div class="not-icon">
                <div class="author-details">
                    <span class="author-name" style="color: {int_to_rgb(block["role_color"])};">Coturnix</span>
                    <span class="author-tag">BOT</span>
                    <span class="authed-datetime">{block.get("time", "Unknown")}</span>
                    <div class="chatlog--embed">
                        <div class="chatlog--emed-color" style="background-color: #ed4245;"></div>
                        <div class="chatlog--embed-container">
                            <div class="chatlog--embed-content">
                                <div class="chatlog--embed-text">
                                    <div class="chatlog--embed-title">Close Ticket</div>
                                    <div class="chatlog--embed-description">
                                        Are you sure you want to close this ticket?
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ticket-options">
                        <!-- We only preserve expected buttons due to being no way to get buttons from messages -->
                        <button class="bot-button">
                            <div class="bot-button-inner">
                                <img src="//cdn.kanokiw.com/assets/ticket/trashbox.webp" draggable="false">
                                <div class="button-content">Close</div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>"""             
                        case _:
                            html += f"""
        <hr class="chatlog-divider">
        <div class="chatlog-message-block" id="{block["id"]}">
            <span class="upper-icon-"><img class="author-icon" src="{block["avater"]}"></span>
            <div class="not-icon">
                <div class="author-details">
                    <span class="author-name" style="color: {int_to_rgb(block["role_color"])};">{block["author"]}</span>
                    <span class="author-tag">BOT</span>
                    <span class="authed-datetime">{block.get("time", "Unknown")}</span>
                    <div class="chatlog--embed">
                        <div class="chatlog--emed-color" style="background-color: {int_to_rgb(block["embed"]["color"])};"></div>
                        <div class="chatlog--embed-container">
                            <div class="chatlog--embed-content">
                                <div class="chatlog--embed-text">
                                    <div class="chatlog--embed-title">{_escapeHTML(block["embed"]["title"])}</div>
                                    <div class="chatlog--embed-description">
                                        {_escapeHTML(block["embed"]["description"]) if block["embed"]["description"] else ""}
                                    </div>{"".join([f'<a href="{image}"><attachment>{image if image else ""}</attachment></a><br>' for image in block["embed"]["images"]])}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""
                else:
                    html += f'\n        <hr class="chatlog-divider">'
                    if block.get("reply", None):
                        html += f"""
        <div class="chatlog--block-contains-replyer" id="{block["id"]}">
            <div class="chatlog-message-block-" gp="{block["reply"]["id"]}">
                <!-- replyer -->
                <div class="replyer--symbol"></div>
                <div class="replyer--replyed-message">
                    <img class="replyed--message-author-avater" src="{block["reply"]["author"]["avater"]}">
                    {'<span class="author-tag">BOT</span>' if block["reply"]["author"].get("bot", None) else ""}
                    <span class="replyed--message-author-name" style="color: {int_to_rgb(block["reply"]["author"]["role_color"])};">{'&nbsp;@' if block["reply"]["author"].get("bot", None) else ""}{block["reply"]["author"]["name"]}</span>
                    <div class="chatlog--replyed-message-content">
                        <span class="chatlog--replyed-message-content-prefix">
                            {_escapeHTML(block["reply"]["content"]) if len(block["reply"]["content"]) > 0 else "<span class='no-content-replyGuide'>クリックして添付ファイルを表示</span>"}
                            {'<svg class="repliedTextContentIcon-1LQXRB" aria-hidden="true" role="img" width="20" height="20" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M6 2C3.79086 2 2 3.79086 2 6V18C2 20.2091 3.79086 22 6 22H18C20.2091 22 22 20.2091 22 18V6C22 3.79086 20.2091 2 18 2H6ZM10 8C10 6.8952 9.1032 6 8 6C6.8944 6 6 6.8952 6 8C6 9.1056 6.8944 10 8 10C9.1032 10 10 9.1056 10 8ZM9 14L6 18H18L15 11L11 16L9 14Z" fill="currentColor"></path></svg>' if len(block["reply"]["content"]) == 0 else '<span></span>'}
                        </span>
                    </div>
                </div>
                <!-- replyer end -->
            </div>
            <div class="chatlog-message-block--replyer">
                <span class=""><img class="author-icon" src="{block["author"]["avater"]}"></span>
                <div class="not-icon">
                    <div class="author-details">
                        <span class="author-name" style="color: {int_to_rgb(block["author"]["role_color"])};">{_escapeHTML(block["author"]["name"])}</span>
                        {'<span class="author-tag">BOT</span>' if block["author"].get("bot", None) else ""}
                        <span class="authed-datetime">{block.get("time", "Unknown")}</span>
                        <div class="chatlog--message">
                            <div class="markdown">
                                <span class="chatlog--message-content">
                                    {_escapeHTML(block["details"]["content"])}
                                </span>
                            </div>{attr}
                        </div>
                    </div>
                </div>
            </div>
        </div>"""
                    else:
                        html += f"""
        <div class="chatlog-message-block" id="{block["id"]}">
            <span class=""><img class="author-icon" src="{block["author"]["avater"]}"></span>
            <div class="not-icon">
                <div class="author-details">
                    <span class="author-name" style="color: {int_to_rgb(block["author"]["role_color"])};">{_escapeHTML(block["author"]["name"])}</span>
                    {'<span class="author-tag">BOT</span>' if block["author"].get("bot", None) else "<span></span>"}
                    <span class="authed-datetime">{block.get("time", "Unknown")}</span>
                    <div class="chatlog--message">
                        <div class="markdown">
                            <span class="chatlog--message-content">
                                {_escapeHTML(block["details"]["content"])}
                            </span>
                        </div>{attr}
                    </div>
                </div>
            </div>
        </div>"""
            html += """
        <div class="scrollerSpacer"></div>
    </body>
</html>
"""
            for char in html:
                try:
                    char.encode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning):
                    html = html.replace(char, "")
            cache_file = f"{self.channel.guild.id}-{self.channel.category_id}-{self.channel.id}.html"

            ticketHTMLRequest = requests.post("https://kanokiw.com/tickets/by_coturnix/push", {
                "html": html,
                "json": json.dumps(data, indent=4, ensure_ascii=False),
                "filename_html": cache_file,
                "filename_json": f"{self.channel.id}_ticketmsgcache.json",
            })
            
            try:os.remove(f"./tickets/{self.channel.id}_ticketmsgcache.json")
            except PermissionError:...
            dm = await self.creator.create_dm()
            description = f"""**Creator:** {self.creator.mention}(`{self.creator.id}`)
**Created At:** <t:{data[0]["created_at"]}:F>
{f'**Participants:** {" ".join([f"<@{id}>" for id in participants])}' if len(participants) > 0 else '**Self-Solved:** `Yes...?`'}
**Transcript:** [Transcript](https://tickets.kanokiw.com/tickets/{cache_file[:-5]})"""
            embed = discord.Embed(title="Ticket Closed", description=description, color=0xffffff)
            await self.channel.delete()
            await dm.send(embed=embed)
            if self.cache is not None:
                await self.cache.send(embed=embed)
            print(f"{(datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y/%m/%d/%H:%M')}: {self.channel.name} \
channel(ticket) was closed by {interaction.user.display_name}(Owner: {self.creator.display_name})\n\
{Fore.GREEN}https://tickets.kanokiw.com/tickets/{cache_file[:-5]}{Fore.RESET}")
