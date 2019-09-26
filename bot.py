import discord
import random
import utils

from discord.ext import commands


ROOT_URL = 'https://zestedesavoir.com'

# Read all proverb
with (open("zestes.txt", "r") as f:
      ZESTES = f.readlines()

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(brief='Affiche un zeste proverbiale au hasard aide', usage='!zeste')
async def zeste(ctx):
    """Print a zeste"""
    zeste = random.choice(ZESTES)
    await ctx.send(zeste)


@bot.command(brief='Cherche un contenu sur ZdS', usage='!cherche <terme à rechercher>', aliases=['lycos', 'recherche])
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


@bot.command(brief='Affiche le nombre de membres sur ZdS', usage='!membres')
async def membres(ctx):
    count = utils.get_members_count()
    if not count:
        custom = discord.utils.get(ctx.bot.emojis, name='clemtriste')
        if custom:
            emoji = '<:{}:{}>'.format(custom.name, custom.id)
        else:
            emoji = '🙁'
        await ctx.send('{} Je n\'ai pas réussi à trouver l\'information.'.format(emoji))
    else:
        await ctx.send('Il y a actuellement **{} membres** d\'enregistré sur ZdS !'.format(count))


@bot.command(brief='Affiche cette aide', usage='!help', aliases=['aide'])
async def help(ctx):
    author = ctx.author
    message = 'Voici les commandes dont je dispose :\n\n'
    for command in ctx.bot.commands:
        message += '`{}`\t{}\t(ex: `{}`)\n'.format(command.name, command.brief, command.usage)
    await author.send(message)
    try:
        await ctx.message.delete()
    except discord.ext.commands.errors.CommandInvokeError:
        print('Missing permission to delete messages')

# Read the discord token
with open("prod-token.txt", "r") as f:
      token = f.read().strip()
      
bot.run(token)
