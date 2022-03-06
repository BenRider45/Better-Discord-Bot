import random
from unittest.mock import Mock
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

def BlackList(ID):
    with open('BlackList.txt') as f:
        lines= f.readlines()
    for line in lines:
        line= int(line)

        if line=="": 
            continue
        else:
            if int(line)==ID :
                return True

            
    return False


@client.event  
async def on_ready():
    activity = discord.Game(name="Just Swaggin || (;help for more!)", type=2)
    await client.change_presence(status=discord.Status.online, activity=activity)
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
async def on_member_remove(ctx,member):
    await ctx.send(f'{member} has left a server')



@client.command()
async def help(ctx):
    with open("README.md","r") as file:
        fileCont= file.read()
    embed = discord.Embed(description = fileCont, color=0xE74C3C)
    await ctx.author.send(embed=embed)

@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def blacklist(ctx):
    if BlackList(ctx.message.author.id):
        await ctx.send("Nah")
        return
    with open("AdminPass.txt","r") as f:
        PASS=f.read()
    SpaceLoc= ctx.message.content.find(" ")
    User= ctx.message.content[SpaceLoc+1:]
    embed = discord.Embed(description = "Enter super secret password:", color=0xE74C3C)
    await ctx.author.send(embed=embed)
    
    def check(m):
        print(m.channel.type)

        return m.content == PASS and str(m.channel.type) == "private"

    msg = await client.wait_for("message", check=check)
    USR = discord.utils.get(ctx.guild.members, display_name=User)
    with open("BlackList.txt",'w') as f:
        f.writeline(str(USR.id))
    await ctx.send(f"User <@%s> has been blacklisted from using the BDB!"%(USR.id))

@client.command()
async def mock(ctx):
    if BlackList(ctx.message.author.id):
        await ctx.send("Nah")
        return ctx.message.author.id
    
    origUser=ctx.message.author.display_name 
    SpaceLoc= ctx.message.content.find(" ")
    User= ctx.message.content[SpaceLoc+1:]
    if User.upper()=="BDB":
        MockBot=True
        await ctx.send("Nice one chuckle nuts")
        User = ctx.message.author.display_name
        
    User=User.lower()
    
    async for message in ctx.channel.history(limit=1):
        fetchMessage=message
    i=0
    async for message in ctx.channel.history(before=fetchMessage): 
        i+=1
        fetchMessage = message
        if i ==100 and fetchMessage.author.display_name!=User:
            await ctx.send("Cannot find user message!")
            return
        
        if("https://" in fetchMessage.content or len(fetchMessage.content)==0) or fetchMessage.author.display_name.lower()!= User:
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
    if MockBot:
        await ctx.send("==insult "+User)

@client.command()
async def luigi(ctx):
    if BlackList(ctx.message.author.id):
        await ctx.send("Nah")
        return
    SpaceLoc= ctx.message.content.find(" ")
    User= ctx.message.content[SpaceLoc+1:]

    if User==';luigi':
        while True:
            member=random.choice(ctx.guild.members)
            if member.bot==False:  
                break
    else:
        member = discord.utils.get(ctx.guild.members, display_name=User)

    

    with open("luigi.txt","r") as file:
        msg1= file.read()
    msg2="Get Luigied!"
    embed = discord.Embed(description = msg2, color=0xE74C3C)    
    try:
        await member.send(msg1)
        await member.send(embed=embed)
        await ctx.send("<@%s> just got Luigied!"%(member.id))
    except discord.errors.Forbidden:
        embed = discord.Embed(description = "ERROR: User does not except dms :(", color=0xE74C3C)    
        await ctx.send(embed=embed)

@client.command()
async def join(ctx):   
    
    if(ctx.author.voice):
        channel = ctx.medssage.author.voice.channel
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
