import discord

client: discord.Client = None

test_val = 0

def set_client(cli: discord.Client):
    global client
    client = cli


def set_test_val(v):
    global test_val
    test_val = v

