import asyncio
from interactions import Client, Intents, listen, slash_command, SlashContext
from discord.ext import tasks
from datetime import datetime, timedelta

bot = Client(intents=Intents.DEFAULT)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name='keepalive', description='Manually maintain all threads once')
async def maintain(ctx: SlashContext):
    await ctx.send("Thread maintenance sent 👌!")

    # Fetch all threads in the guild
    threads = ctx.guild.threads

    for thread in threads:
        # 'thread' is a TextChannel object representing the thread
        message = await thread.send("Maintenance Message! 👋")
        await asyncio.sleep(1)
        await message.delete()


@slash_command(name='auto', description='Automatically perform maintenance with a specified interval', options=[
    {
        'name': 'interval',
        'description': 'Interval in hours',
        'type': 4,  # type 4 represents integer
        'required': True
    }
])
async def auto(ctx: SlashContext, interval: int):
    await ctx.send(f"Auto maintenance started with an interval of {interval} hours! ⏰")
    auto_maintenance.change_interval(hours=interval)
    auto_maintenance.start(ctx)


@slash_command(name='stop', description='Stop the auto maintenance task')
async def stop(ctx: SlashContext):
    auto_maintenance.stop()
    await ctx.send("Auto maintenance stopped! 🛑")


# Default to hourly interval, will be changed dynamically by the 'auto' command
@tasks.loop(hours=1)
async def auto_maintenance(ctx: SlashContext):
    await ctx.send("Auto Thread maintenance started! ▶️")

    # Fetch all threads in the guild
    threads = ctx.guild.threads

    for thread in threads:
        # 'thread' is a TextChannel object representing the thread
        message = await thread.send("Maintenance Message! 👋")
        await asyncio.sleep(5)
        await message.delete()


@slash_command(name='status', description='Display the status of the auto update')
async def status(ctx: SlashContext):
    if auto_maintenance.is_running():
        await ctx.send(f"Auto maintenance is active. ✅")
    else:
        await ctx.send("Auto maintenance is not currently active. ❌")

bot.start("TOKEN")
