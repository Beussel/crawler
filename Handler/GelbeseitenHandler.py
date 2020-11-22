import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse


def crawl():
    url = 'https://www.gelbeseiten.de/Suche/Informationssysteme/Berlin'
    get_links(url)


def get_links(url):
    content = get_url_content(url)
    soup = BeautifulSoup(content, "html.parser")

    for article in soup.findAll('article', {'class': 'mod mod-Treffer'}):
        content = get_url_content(article.find('a').get('href'))
        soup = BeautifulSoup(content, "html.parser")
        get_address(soup)
        get_number(soup)
        get_mail(soup)


def get_address(soup):
    addressList = soup.findAll('address')
    print(addressList[1].text)


def get_number(soup):
    numberList = soup.findAll('span', {'data-role': 'telefonnummer'})
    print(numberList[0].get('data-suffix'))


def get_mail(soup):
    mail = soup.find('a', {'property': 'url'})
    if mail != None:
        print(mail.text)


def get_url_content(url):
    time.sleep(1)
    return requests.get(url).text


def get_domain(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)