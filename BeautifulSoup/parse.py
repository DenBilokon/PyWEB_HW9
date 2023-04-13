import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

base_url = 'http://quotes.toscrape.com'


def get_author_urls():
    author_links = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    for q in quotes:
        author_links.append(q.find("a", href=True).get('href'))
    return author_links


def quote_spider():
    data = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select('div[class=col-md-8] div[class=quote]')
    for el in content:
        result = {}
        quote = el.find('span', attrs={'class': 'text'}).text
        author = el.find('small', attrs={'class': 'author'}).text
        tags = (list(filter(bool, [t.text.strip() for t in el.find('div')][1:])))
        result.update({'tags': tags, 'author': author, 'quote': quote})
        data.append(result)

    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(data, fd, ensure_ascii=False, indent=4)


def author_spider():
    data = []
    author_links = get_author_urls()
    for link in author_links:
        response = requests.get(base_url + link)
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.select('div[class=container] div[class=author-details]')
        for el in content:
            fullname = el.find('h3', attrs={'class': 'author-title'}).text.strip()
            date_born = el.find('span', attrs={'class': 'author-born-date'}).text.strip()
            born_location = el.find('span', attrs={'class': 'author-born-location'}).text.strip()
            bio = el.find('div', attrs={'class': 'author-description'}).text.strip()
            result = {'fullname': fullname, 'date_born': date_born, 'born_location': born_location, 'bio': bio}
            data.append(result)

    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(data, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    quote_spider()
    author_spider()
