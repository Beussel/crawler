import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

class GelbeseitenHandler:

    def __init__(self, ort):
        self.crawl_all("Informationssysteme", ort)

    def crawl_all(self, branche, ort):
        url = 'https://www.gelbeseiten.de/Suche/' + branche + '/' + ort
        self.crawl(url)

    def crawl(self, url):
        content = self.get_url_content(url)
        soup = BeautifulSoup(content, "html.parser")

        article_list = soup.findAll('article', {'class': 'mod mod-Treffer'})
        for article in article_list:
            print("id: " + article.attrs.get("data-teilnehmerid"))

            for company_content_tmp in article.contents:
                if hasattr(company_content_tmp, 'attrs'):
                    company_content = company_content_tmp
                    break

            if company_content == None:
                continue

            for content_tmp in company_content.contents:
                if hasattr(content_tmp, 'attrs'):
                    if 'data-wipe-name' in content_tmp.attrs and content_tmp.attrs.get('data-wipe-name') == "Titel":
                        print("name: " + content_tmp.contents[0])
                    elif 'class' in content_tmp.attrs and len(content_tmp.attrs.get('class')) > 1 and content_tmp.attrs.get('class')[1] == 'mod-Treffer--besteBranche':
                        print("branche: " + self.delete_escape_char(content_tmp.contents[0]))
                    elif 'class' in content_tmp.attrs and len(content_tmp.attrs.get('class')) > 1 and content_tmp.attrs.get('class')[1] == 'mod-AdresseKompakt':
                        for address_content_tmp in content_tmp:
                            if hasattr(address_content_tmp, 'attrs') and 'data-wipe-name' in address_content_tmp.attrs and address_content_tmp.attrs.get('data-wipe-name') == "Adresse":
                                print("strasse: " + self.delete_escape_char(address_content_tmp.contents[0])[:-2])
                                print("plz: " + self.delete_escape_char(address_content_tmp.contents[1].contents[0])[0:5])
                            if hasattr(address_content_tmp, 'attrs') and 'data-wipe-name' in address_content_tmp.attrs and address_content_tmp.attrs.get('data-wipe-name') == "Kontaktdaten":
                                print("nummer: " + address_content_tmp.contents[0])

            content = self.get_url_content(article.find('a').get('href'))
            soup = BeautifulSoup(content, "html.parser")
            self.get_website(soup)
            print('_____________________________________________________')

    def delete_escape_char(self, string):
        filter = ''.join([chr(i) for i in range(1, 32)])
        return string.translate(str.maketrans('', '', filter))

    def get_website(self, soup):
        mail = soup.find('a', {'property': 'url'})
        if mail != None:
            print("website: " + mail.contents[3].contents[0])

    def get_url_content(self, url):
        time.sleep(1)
        return requests.get(url).text
