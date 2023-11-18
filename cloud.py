import aiohttp
import discord
import json
import os
import platform
import random
import sys
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio
import io
import datetime, time
if not os.path.isfile("config.json"):
    sys.exit("'config.json' file not found")
else:
    with open("config.json") as fp:
        config = json.load(fp)
# Intents
intents = discord.Intents.default()
intents.members = True

# Setup The Bot Prefix
bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
bot.remove_command('help')


# ----------------------EVENTS--------------------------- #

@bot.event
async def on_ready():
    print(f"=======================")
    print(f"{bot.user.name} is online.")
    print(f"Python Version: {platform.python_version()}")
    print(f"Run on: {platform.system()} {platform.release()} ({os.name})")
    print(f"Developer: Snoozy")
    print(f"=======================")
    status_task.start()
    global startTime
    startTime = time.time()

@tasks.loop(seconds=15)
async def status_task():
    statuses = ["with terminal", "with clouds"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Ai gresit comanda bos')

# Notify command used
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"[+] Comanda executata {executedCommand} in {ctx.guild.name} de {ctx.message.author} (ID: {ctx.message.author.id})")
@bot.event
async def on_member_join(member):
    guild = bot.get_guild(member.guild.id)
    channel1 = discord.utils.get(member.guild.text_channels, name="🔒・verify")
    channel2 = discord.utils.get(member.guild.text_channels, name="💬・hangout")
    await channel1.send(f"{member.mention}. \n `You will be verified as soon as possible please wait here.`")
    
    
   #----------------COMMANDS---------------#



@bot.command()
async def uptime(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    await ctx.reply(f"**Uptime Cloud:** `{uptime}`")

@bot.command()
async def prost(ctx, member: discord.Member, intensity: int = 5):
         avatar = member.avatar_url_as(size=1024, format=None, static_format='png')
         emoji = ":penguin:"

         message = await ctx.send(f"{emoji} — **Processing the image please wait!**")
         await message.delete(delay=3)

         async with aiohttp.ClientSession() as cs:
             async with cs.get(f"https://nekobot.xyz/api/imagegen?type=magik&image={avatar}&intensity={intensity}") as r:
                 res = await r.json()
                 embed = discord.Embed(
                     color=0x101412,
                 )
                 embed.set_image(url=res["message"])
                 embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                 embed.timestamp = datetime.datetime.utcnow()
                 await ctx.reply(embed=embed)
                 
@bot.command()
async def help(ctx):
         embed=discord.Embed(title="!cat", color=0x101412)
         embed.add_field(name="**Fun Commands**", value="<:4478reply:881998789806805042> `.cat` **-** (returns one cat photo) \n <:4478reply:881998789806805042> `.dog` **-** (returns one dog photo)", inline=False)
         embed.add_field(name="**Fun Commands**", value="<:4478reply:881998789806805042> ` .meme` **-** ****(meme gen)****\n<:4478reply:881998789806805042> `.cat` **-** ****(returns one cat photo)**** \n <:4478reply:881998789806805042> `.dog` **- ** ****(returns one dog photo)****\n<:4478reply:881998789806805042> `.coffee` **-** ****(coffee photo)****\n<:4478reply:881998789806805042> `.mind <text>` **-** ****(change my mind meme)****\n<:4478reply:881998789806805042> `.triggered` **-** ****(trigger your profile pic)****\n<:4478reply:881998789806805042> `. vs <@user1> <@user2>` **-** ****(vs two members)****\n<:4478reply:881998789806805042> `.youtube <text>` **-** ****(youtube comment pic)****\n<:4478reply:881998789806805042> `.ph` **-** ****(phub your profile pic)****\n<:4478reply:881998789806805042> `.prost <@user>` **-** ****(prost user photo)****", inline=False)
         embed.add_field(name="**Other**", value="<:4478reply:881998789806805042> `.ping` **-** ****(bot ping)****\n<:4478reply:881998789806805042> `.uptime` **-** ****(bot uptime)****", inline=False) 
         embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
         embed.timestamp = datetime.datetime.utcnow()
         await ctx.reply(embed=embed)

@bot.command
@commands.has_permissions(administrator = True)
async def ban(ctx, member, user: discord.Member):
        await ctx.guild.ban(user) 
        await user.send(f"You have been banned.")
        await ctx.reply(f"{user} has been successfully banned.")


@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f'{user.mention} **unbanned successfully!**')
                return


@bot.command()
async def meme(ctx):
        embed = discord.Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)


@bot.command()
async def ping(ctx):
        before = time.monotonic()
        pong = int(round(bot.latency * 1000, 1))

        message = await ctx.send("• **Pong** — :ping_pong:")

        ping = (time.monotonic() - before) * 1000
        await message.delete(delay=1)
        await asyncio.sleep(1)

        embed = discord.Embed(
            color=0x4ca1bd,
            title="Cloud's Ping ",
        )
        embed.add_field(name="• WS:", value=f"{pong}ms")
        embed.add_field(name="• REST:", value=f"{int(ping)}ms")
        await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/cat') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=0x101412,
                )
                embed.set_image(url=res['link'])
                embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)
    
@bot.command()
async def dog(ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=0x101412,
                )
                embed.set_image(url=res['message'])
                embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)
    
@bot.command()
async def coffee(ctx):
         async with aiohttp.ClientSession() as cs:
             async with cs.get("https://coffee.alexflipnote.dev/random.json") as r:
                    res = await r.json()
                    embed = discord.Embed(
                     color=0x101412,
                    )
                    embed.set_image(url=res["file"])
                    embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.reply(embed=embed)
    
@bot.command()
async def triggered(ctx):
    picture = ctx.author.avatar_url_as(size=1024, format=None, static_format='png')
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://some-random-api.ml/canvas/triggered?avatar={picture}") as r:
            res = io.BytesIO(await r.read())
            triggered_file = discord.File(res, filename=f"triggered.gif")
            embed = discord.Embed(
                    color=0x101412,
                )
            embed.set_image(url="attachment://triggered.gif")
            embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed, file=triggered_file)
           
        @bot.command()
        async def ph(ctx):
            picture = ctx.author.avatar_url_as(size=1024, format=None, static_format='png')
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={picture}&text=Ador acest filmulet forta!&username={ctx.author}") as r:
                    res = await r.json()
                    embed = discord.Embed( color=0x101412,
                                         )
                    embed.set_image(url=res["message"])
                    embed.set_footer(text=f"CLOUD by JustinNotBieber- beta")
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.reply(embed=embed)

@bot.command()
async def belgia(ctx):
    embed=discord.Embed(title="Belgia", description="Plec pe Belgia bos!", color=0xfb0404)
    embed.set_author(name="CLOUD")
    embed.set_footer(text="CLOUD by JustinNotBieber- beta")
    embed.set_image(url="https://cdn.discordapp.com/attachments/517056018534891523/995684613068431380/belgia.jpg")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

    # -------------- COMMANDS--INJURA ------------------- #
@bot.command()
async def injura(ctx, random):
    responses = ['Bgamas gura ta',
                'sa te fut in gura',
                'Te rup pe genunchi bos',]
    await ctx.reply(random.choice_responses)

    # --------------- CUSTOM--COMMANDS------------------ #
@bot.command()
async def zoran1(ctx):
    embed=discord.Embed(title="Zoran", description="TEST TEST", color=0xfb0404)
    embed.set_author(name="CLOUD")
    embed.set_footer(text="CLOUD by JustinNotBieber- beta")
    embed.set_image(url="https://cdn.discordapp.com/attachments/899222297045520384/1014850769134034984/Screenshot_1.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@bot.command()
async def zoran2(ctx):
     embed=discord.Embed(title="Zoran", description="TEST TEST", color=0xfb0404)
     embed.set_author(name="CLOUD")
     embed.set_footer(text="CLOUD by JustinNotBieber- beta")
     embed.set_image(url="https://cdn.discordapp.com/attachments/899222297045520384/1014850769134034984/Screenshot_1.png")
     embed.timestamp = datetime.datetime.utcnow()
     await ctx.send(embed=embed)

    



#############-RUN-################
bot.run(config["token"])
