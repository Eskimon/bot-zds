import json
import urllib

from bs4 import BeautifulSoup
from urllib import request


API_ROOT_URL = 'https://zestedesavoir.com/api'
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


def get_members_count():
    req = request.Request(
        API_ROOT_URL + '/membres/',
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  # noqa
        }
    )
    try:
        data = request.urlopen(req).read().decode('utf-8')
        return json.loads(data)['count']
    except AttributeError:
        print('problem fetching data')
        return None
    except urllib.error.HTTPError as e:
        print('http error ({})'.format(e))
        return None
