import os
import logging

from discord import Intents
from discord.ext import commands

from calc.calcs import calculate_chance_of_type_in_team

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"LOGGED IN AS {bot.user}")


@bot.command(name="ping")
async def cmd_ping(ctx):
    logger.info(f"PING RECEIVED!")
    await ctx.send("Pong!")


@bot.command(name="type")
async def cmd_type_on_team(ctx, pokemon_type, team_size=6, gen=3):
    logger.info(f"Calculating chance of {pokemon_type} on team of size {team_size}.")

    chance = calculate_chance_of_type_in_team(pokemon_type=pokemon_type, team_size=team_size, gen=gen)

    await ctx.send(f"There is a **{chance}%** chance of a **{pokemon_type} type** on a **team of {team_size}** in **Gen {gen}**!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    logger.info(f"MESSAGE RECEIVED: {message.content}")
    
    await bot.process_commands(message)


def run_bot():
    bot.run(os.environ["BOT_TOKEN"])
