import discord
import random
import urllib

from bs4 import BeautifulSoup
from urllib import request


ZESTES = open('zestes.txt').readlines()
ROOT_URL = 'https://zestedesavoir.com'
QUERY_SEARCH = 'https://zestedesavoir.com/rechercher/?q={query}'


def get_search_results(query):
    req = request.Request(
        QUERY_SEARCH.format(query='Arduino'),
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
    tag = results[0]
    info = tag.find_all("div", class_="content-info")[0]
    link = info.find_all("a")[0]
    desc = tag.find_all("p", class_="content-description")[0]
    return [{
        'thumbnail': tag.find_all('img')[0]['src'],
        'url': link['href'],
        'title': link.get_text().strip(),
        'description': desc.get_text().strip(),
    }]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!zeste'):
            zeste = random.choice(ZESTES)
            await message.channel.send(zeste)

        if message.content.startswith('!cherche'):
            query = message.content[8:]
            result = get_search_results(' '.join(query))
            if result:
                result = result[0]
                embed = discord.Embed(
                    type='rich',
                    title=result['title'],
                    description=result['description'],
                    url=ROOT_URL + result['url'],
                )
                embed.set_thumbnail(url=ROOT_URL + result['thumbnail'])
                await message.channel.send(content='Voici ce que j\'ai trouvé !', embed=embed)
            else:
                await message.channel.send(':clemtriste: Je n\'ai rien trouvé à ce sujet.')


client = MyClient()
client.run('NTQ4NDE2NTEyOTE1MTQ0NzE2.XYn-qA.PAHGlnMblt-OJ9XtiB-djG5-aLk')
