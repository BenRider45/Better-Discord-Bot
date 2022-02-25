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
async def mock(ctx):
    
    SpaceLoc= ctx.message.content.find(" ")
    User= ctx.message.content[SpaceLoc+1:]
    
    async for message in ctx.channel.history(limit=1):
        fetchMessage=message
    i=0
    async for message in ctx.channel.history(before=fetchMessage): 
        i+=1
        fetchMessage = message
        if i ==100 and fetchMessage.author.display_name!=User:
            await ctx.send("Cannot find user message!")
            return
        
        if("https://" in fetchMessage.content or len(fetchMessage.content)==0) or fetchMessage.author.display_name!= User:
            continue
        else:
            break
    


    i=1
    output=""
    for char in fetchMessage.content:
        if(i>0):
            output+=char.upper()
        else:
            output+=char
        i*=-1

    await ctx.send(output,reference=fetchMessage)

@client.command()
async def luigi(ctx):
    while True:
        member=random.choice(ctx.guild.members)
        if member.bot==False:  
            break
    
    with open("luigi.txt","r") as file:
        msg1= file.read()
    msg2="Use the command, "";Luigi"" to totally Luigi someone random in your server! "
    embed = discord.Embed(description = msg2, color=0xE74C3C)    
    await member.send(msg1)
    await member.send(embed=embed)
    await ctx.send("Someone just got Luigied!")

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