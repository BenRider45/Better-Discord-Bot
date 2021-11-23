import random
import discord
from discord.channel import DMChannel
from discord.ext import commands
from discord import Intents


intents = discord.Intents.default()
intents.members = True
intents = Intents.all()
client = commands.Bot(command_prefix=";", intents=intents)
with open('Token.txt') as f:
    TOKEN = f.readline()
client.remove_command('help')


@client.event  
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_guild_join(Guild):  
    with open("helpMessage.txt","r") as file:
        fileCont= file.read()
    embed = discord.Embed(description = fileCont, color=0xE74C3C)
    
    await Guild.text_channels[0].send(embed=embed)
    

@client.event
async def on_member_join(member):
    Guild = member.guild
    embed = discord.Embed(description = f"Who let {member.mention} in?", color=0xE74C3C)
    await Guild.text_channels[0].send(embed=embed)


@client.event
async def on_member_remove(member,ctx):
    await ctx.send(f'{member} has left a server')



@client.command()
async def help(ctx):
    with open("helpMessage.txt","r") as file:
        fileCont= file.read()
    embed = discord.Embed(description = fileCont, color=0xE74C3C)
    await ctx.author.send(embed=embed)

@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def Luigi(ctx):
    while True:
        member=random.choice(ctx.guild.members)
        if member.bot==False:  
            break
    
    with open("luigi.txt","r") as file:
        msg1= file.read()
    msg2="You just got Luigied! Use the command, "";Luigi"" to totally Luigi someone random in your server! "
    embed = discord.Embed(description = msg2, color=0xE74C3C)    
    await member.send(msg1)
    await member.send(embed=embed)

@client.command()
async def join(ctx):   
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You have to be in a channel first silly!")

@client.command()
async def leave(ctx):   
    if(ctx.voice_client):
        
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected from voice")
    else:
        await ctx.send("I have to be in a channel first silly!")

client.run(TOKEN)