import discord
from discord.ext import commands
import disutils

bot = commands.AutoShardedBot(command_prefix=">")
music = disutils.Music()


@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()  # Joins author's voice channel


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, *, url):
    player = music.get_player(ctx)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued {song.name}")


@bot.command()
async def pause(ctx):
    player = music.get_player(ctx)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")


@bot.command()
async def resume(ctx):
    player = music.get_player(ctx)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")


@bot.command()
async def stop(ctx):
    player = music.get_player(ctx)
    await player.stop()
    await ctx.send("Stopped")


@bot.command()
async def loop(ctx):
    player = music.get_player(ctx)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")


@bot.command()
async def queue(ctx):
    player = music.get_player(ctx)
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")


@bot.command()
async def now(ctx):
    player = music.get_player(ctx)
    song = player.now_playing()
    await ctx.send(song.name)


@bot.command()
async def skip(ctx):
    player = music.get_player(ctx)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")


@bot.command()
async def volume(ctx, vol):
    player = music.get_player(ctx)
    # volume should be a float between 0 to 1
    song, volume = await player.change_volume(float(vol) / 100)
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")


@bot.command()
async def remove(ctx, index):
    player = music.get_player(ctx)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")
