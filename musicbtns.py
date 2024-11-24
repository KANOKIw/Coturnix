import inspect
import discord
import discord.utils

from colorama import Fore
from nr_methods import *


client: discord.Client = None

def set_client4(cli: discord.Client):
    global client
    client = cli
    

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


    @discord.ui.button(label = "Stop", style = discord.ButtonStyle.red, custom_id = "Stop")
    async def Stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} stopped Coturnix")

        guild = interaction.user.guild
        count(interaction.user.name, "B.stop")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            await guild.voice_client.stop()
            await interaction.followup.send(inspect.cleandoc(f"""Stopped!!"""), ephemeral=True)

        except Exception:
            await interaction.followup.send(inspect.cleandoc(f"""Stopped maybe!!"""), ephemeral=True)

    
    @discord.ui.button(label = "Phoenix", style = discord.ButtonStyle.blurple, custom_id = "Phoenix")
    async def Phoenix(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Phoenix")

        guild = interaction.user.guild
        count(interaction.user.name, "B.phoenix")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Phoenix.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Minecraft**..."""), ephemeral=True)


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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/MiceOnVenus.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Mice On Venus**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Taswell", style = discord.ButtonStyle.green, custom_id = "Taswell")
    async def MiceOnVenus(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Taswell")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Taswell.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Taswell**..."""), ephemeral=True)


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
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Stal.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **Stal**..."""), ephemeral=True)

    
    @discord.ui.button(label = "Mall", style = discord.ButtonStyle.green, custom_id = "Mall")
    async def Mall(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"\n[{timestr()}] {Fore.GREEN}{interaction.user.name}{Fore.RESET} played Mall")

        guild = interaction.user.guild
        count(interaction.user.name, "B.minecraft")

        await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            vc = interaction.user.voice.channel
        except Exception:
            await interaction.followup.send("You must connect any vc to use this!!", ephemeral=True)
            return

        try:
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass
        
        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/Mall.mp3"))
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
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
            await vc.connect(self_mute=False, self_deaf=True)
        except Exception:
            pass

        guild.voice_client.stop()
        guild.voice_client.play(discord.FFmpegPCMAudio("musics/teionguys.mp3"))
        await interaction.followup.send(inspect.cleandoc(f"""Playing **低音ども**..."""), ephemeral=True)