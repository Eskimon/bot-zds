import discord
import random
import urllib

from bs4 import BeautifulSoup
from urllib import request


ZESTES = open('zestes.txt').readlines()
ROOT_URL = 'https://zestedesavoir.com'
QUERY_SEARCH = 'https://zestedesavoir.com/rechercher/?q={query}'


def get_search_results(query):
    query = urllib.parse.quote_plus(query)
    print(QUERY_SEARCH.format(query=query))
    req = request.Request(
        QUERY_SEARCH.format(query=query),
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  # noqa
        }
    )
    try:
        page = request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
    except AttributeError:
        print('problem fetching data')
        return []
    except urllib.error.HTTPError as e:
        print('http error ({})'.format(e))
        return []

    results = soup.find_all("article", class_="content-item")
    if results:
        tag = results[0]
        info = tag.find_all("div", class_="content-info")[0]
        link = info.find_all("a")[0]
        desc = tag.find_all("p", class_="content-description")[0]
        try:
            thumbnail = tag.find_all('img')[0]['src']
        except IndexError:
            thumbnail = None
        return [{
            'thumbnail': thumbnail,
            'url': link['href'],
            'title': link.get_text().strip(),
            'description': desc.get_text().strip(),
        }]
    else:
        return []


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!zeste'):
            zeste = random.choice(ZESTES)
            await message.channel.send(zeste)

        elif message.content.startswith('!cherche'):
            query = message.content[len('!cherche '):]
            result = get_search_results(query)
            if result:
                result = result[0]
                embed = discord.Embed(
                    type='rich',
                    title=result['title'],
                    description=result['description'],
                    url=ROOT_URL + result['url'],
                )
                if result['thumbnail']:
                    embed.set_thumbnail(url=ROOT_URL + result['thumbnail'])
                await message.channel.send(content='Voici ce que j\'ai trouvé !', embed=embed)
            else:
                await message.channel.send(':clemtriste: Je n\'ai rien trouvé à ce sujet.')


token = open('prod-token.txt', 'r').read().strip()
client = MyClient()
client.run(token)
