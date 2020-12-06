import requests
from bs4 import BeautifulSoup
import time
from Model import *
from Handler import *


class GelbeseitenHandler:
    insertedIds = []

    def __init__(self, ort):
        self.crawl_all(ort)

    def crawl_all(self, ort):
        branchen = ["Informationssysteme", "EDV", "IT-Dienstleistungen", "IT-Beratung", "IT", "Softwareentwicklung",
                    "Softwareberatung", "Informationstechnik"]
        for branche in branchen:
            url = 'https://www.gelbeseiten.de/Suche/' + branche + '/' + ort
            self.crawl(url, ort)

    def crawl(self, url, ort):
        content = self.get_url_content(url)
        soup = BeautifulSoup(content, "html.parser")
        dataHandler = DataHandler()
        article_list = soup.findAll('article', {'class': 'mod mod-Treffer'})
        for article in article_list:
            company = Company()
            company.set_city(ort)
            company.set_id(article.attrs.get("data-teilnehmerid"))
            if company.id in self.insertedIds:
                continue
            for company_content_tmp in article.contents:
                if hasattr(company_content_tmp, 'attrs'):
                    company_content = company_content_tmp
                    break

            if company_content == None:
                continue

            for content_tmp in company_content.contents:
                if hasattr(content_tmp, 'attrs'):
                    if 'data-wipe-name' in content_tmp.attrs and content_tmp.attrs.get('data-wipe-name') == "Titel":
                        company.set_name(content_tmp.contents[0])
                    elif 'class' in content_tmp.attrs and len(content_tmp.attrs.get('class')) > 1 and content_tmp.attrs.get('class')[1] == 'mod-Treffer--besteBranche':
                        company.set_branche(self.delete_escape_char(content_tmp.contents[0]))
                    elif 'class' in content_tmp.attrs and len(content_tmp.attrs.get('class')) > 1 and content_tmp.attrs.get('class')[1] == 'mod-AdresseKompakt':
                        for address_content_tmp in content_tmp:
                            if hasattr(address_content_tmp, 'attrs') and 'data-wipe-name' in address_content_tmp.attrs and address_content_tmp.attrs.get('data-wipe-name') == "Adresse":
                                company.set_street(self.delete_escape_char(address_content_tmp.contents[0])[:-2])
                                company.set_plz(self.delete_escape_char(address_content_tmp.contents[1].contents[0])[0:5])
                            if hasattr(address_content_tmp, 'attrs') and 'data-wipe-name' in address_content_tmp.attrs and address_content_tmp.attrs.get('data-wipe-name') == "Kontaktdaten":
                                company.set_phone_number(address_content_tmp.contents[0])

            content = self.get_url_content(article.find('a').get('href'))
            soup = BeautifulSoup(content, "html.parser")
            company.set_website(self.get_website(soup))
            dataHandler.insert(company)
            self.insertedIds.append(company.id)
        dataHandler.close_connection()

    def delete_escape_char(self, string):
        filter = ''.join([chr(i) for i in range(1, 32)])
        return string.translate(str.maketrans('', '', filter))

    def get_website(self, soup):
        mail = soup.find('a', {'property': 'url'})
        if mail != None:
            return mail.contents[3].contents[0]
        return ""

    def get_url_content(self, url):
        time.sleep(1)
        return requests.get(url).text
