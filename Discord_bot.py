import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import youtube_dl
import logging

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
client = discord.Client()
bot = commands.Bot(command_prefix='-')
logging.basicConfig(filename='CetBot.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@bot.event
async def on_ready():
    print('#########')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('#########')
    
    logger.info("Logged in as " + str(bot.user.name) + " - " + str(bot.user.id))
    channel = client.get_channel(YOUR CHANNEL ID)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome {member.name}   :partying_face: :partying_face:'
    )
    logger.info("Logged in as " + str(member.name) + " - " + str(member.id))
    print(f"[!]New member joined to channel - {member.name}\n")


@bot.command(pass_context=True, aliases=['j', 'joi', 'jo', 'c', 'conn'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    user = ctx.message.author

    voice = get(bot.voice_clients, guild=ctx.guild)
    try:
        """
        if voice and voice.is_connected():
            await voice.move_to(channel)
            await ctx.send(f"Bot moved {channel}")
            logger.info("Bot moved to  " + str(channel))
        else:
            voice = await channel.connect()
            await ctx.send(f"Joined {channel}")
            logger.info("Bot joined to  " + str(channel))
        await voice.disconnect()
        """
        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()
            print(f"[!]Bot has connected to {channel}\n")
            logging.info(f'Bot has connected to {channel}  ')
    except Exception:
        print(f"[-]Too many join request {Exception}")
        logger.warning("Too many request from " + str(user) + str(channel))


@bot.command(pass_context=True, aliases=['d', 'dis', 'disconnect', 'l', 'leav'])
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    user = ctx.message.author
    try:
        if voice and voice.is_connected():

            await voice.disconnect()
            await ctx.send(f"Leaved {channel}\n GoodBy :wave: ")
            logging.info(f'Bot leaved {channel}  ')
            print(f"[!]Bot has disconnected {channel}")

        else:
            await ctx.send(f"Bot was never came  to  {channel} :thinking_face: ! ")
            await voice.disconnect()


    except Exception:
        print(f"[-]Too many leave request {Exception}")
        logging.info("Too many leave request   " + str(user))


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    logging.info(f"Play command  {ctx.message.author}  " + str(url))

    try:
        if song_there:
            os.remove("song.mp3")
            print("[!]Old file removeing")
    except PermissionError:
        print("[!]Couldn't delete : Permission denied")
        await ctx.send("ERROR: Music playing .")
        return

    await ctx.send("getting ready !")
    voice = get(bot.voice_clients, guild=ctx.guild)
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',

            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading file . , . , .\n")
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed file {file}\n")
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} Finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1.0
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing now {nname[0], nname[1]}")
        print("[+] Playing\n")
    except youtube_dl.utils.DownloadError:
        print("Url error")


@bot.command(pass_context=True, aliases=['s', 'sto', 'pause', 'pau'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music Stopped")
        await ctx.send("Music stopped")
        voice.pause()
    else:
        print("Music is not playing")


@bot.command(pass_context=True, aliases=['r', 'resu', 'continue', 'cont'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Music resumed")
        await ctx.send("Music resume")

        voice.resume()
    else:
        print("Music is not playing")



bot.run(TOKEN)
