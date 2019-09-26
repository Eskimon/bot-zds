import discord
import random
import utils

from discord.ext import commands


ROOT_URL = 'https://zestedesavoir.com'
ZESTES = open('zestes.txt').readlines()

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def zeste(ctx):
    """Print a zeste"""
    zeste = random.choice(ZESTES)
    await ctx.send(zeste)


@bot.command()
async def cherche(ctx, *, args):
    results = utils.get_search_results(args)
    if results:
        result = results[0]
        embed = discord.Embed(
            type='rich',
            title=result['title'],
            description=result['description'],
            url=ROOT_URL + result['url'],
        )
        if result['thumbnail']:
            embed.set_thumbnail(url=ROOT_URL + result['thumbnail'])
        await ctx.send(content='Voici ce que j\'ai trouvé !', embed=embed)
    else:
        custom = discord.utils.get(ctx.bot.emojis, name='clemtriste')
        if custom:
            emoji = '<:{}:{}>'.format(custom.name, custom.id)
        else:
            emoji = '🙁'
        await ctx.send('{} Je n\'ai rien trouvé à ce sujet.'.format(emoji))


token = open('prod-token.txt', 'r').read().strip()
bot.run(token)
