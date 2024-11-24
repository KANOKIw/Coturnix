import json
import inspect
import asyncio
import discord
import discord.utils
import os
import time
import subprocess

from colorama import Fore
from nr_methods import *


PIPE = subprocess.PIPE
client: discord.Client = None

def set_client5(cli: discord.Client):
    global client
    client = cli
    

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


#サーバー停止確認ボタン
class stopconfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 7)

    @discord.ui.button(label = "はい、停止します", style = discord.ButtonStyle.red, custom_id = "stopconfirm")
    async def stopconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} stopped the evserver.")

        


#サーバー再起動確認ボタン
class restartconfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 7)

    @discord.ui.button(label = "はい、再起動します", style = discord.ButtonStyle.red, custom_id = "restartconfirm")
    async def restartconfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} restarted the evserver.")




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
            


class Disabled_eventservbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "サーバーを起動", style = discord.ButtonStyle.green, custom_id = "eventstarter", disabled=True)
    async def eventstarter(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "サーバーを停止", style = discord.ButtonStyle.red, custom_id = "eventstopper", disabled=True)
    async def eventstopper(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "再起動", style = discord.ButtonStyle.gray, custom_id = "eventrestarter", disabled=True)
    async def eventrestarter(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    @discord.ui.button(label = "プレイヤーリスト", style = discord.ButtonStyle.gray, custom_id = "eventplayerslist", disabled=True)
    async def eventplayerslist(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
