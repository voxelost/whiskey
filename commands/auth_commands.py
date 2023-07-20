import discord

from class_definitions.bot import Bot


async def owner_only(message: discord.Message, bot: Bot, *args, **kwargs):
    """allow only owner"""
    if message.author.id != bot.owner_id:
        raise Exception('unauthorized')


async def anyone_anywhere(*args, **kwargs):
    """allow anyone"""
