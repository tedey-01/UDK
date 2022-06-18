import os
import re
import ssl
import requests
import logging

from bs4 import BeautifulSoup
from collections import namedtuple


# logging.basicConfig(filename='parser.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(handlers=[logging.FileHandler(filename="./log_parser.txt", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}

URLS = {
    'start_url': 'http://ellib.gpntb.ru/subscribe/index_ntb.php',
    'base_url': 'http://ellib.gpntb.ru/subscribe', 
    'system_urls': ['https://doi.org/10.33186/1027-3689-2021-1-173-184', 
                    'https://doi.org/10.33186/1027-3689-2021-1-185-186',
                    ],
    'additional_url': '',
}
Doc = namedtuple('doc', ['age', 'topic', 'text'])


def extract_udk_value(topic_content, fantom_article_url):
    element = str(re.findall(r'{0}.*?КДУ'.format(fantom_article_url.text[::-1]), (topic_content.text.replace('\n', ' '))[::-1]))[::-1]
    udk = 'None'
    try:
        udk = re.findall(r'УДК[^A-Z|a-z|А-Я|а-я]+', element)[0].strip()
    except IndexError:
        logging.warning(f"UDK value extracting exception: {fantom_article_url}")
    return udk


def extract_article(article_url: str):
    try: 
        annot_of_the_article_resp = requests.get(article_url, headers = headers)
        annot_of_the_article_resp_soup = BeautifulSoup(annot_of_the_article_resp.content, 'lxml')

        article_href = annot_of_the_article_resp_soup.find(class_='fulltext').find('a').get('href')
        article_download_link = article_href.replace('view', 'download')
        logging.info(f"article href: {article_href}")
        logging.info(f"article download link: {article_download_link}")
        
        downloading_resp = requests.get(article_download_link, headers = headers)
        logging.info(f"downloading response: {downloading_resp}")
        return downloading_resp.content
    except AttributeError as ex:
        logging.warning(f"Extract article error on url: {article_url}")
        logging.warning(ex)


def load_article(article, base_path: str, file_name: str):
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(article)


def parse_topic(topic_href: str, topic_text: str, age: str):
    logging.info(f"\nParse topic {topic_text}")
    URLS['additional_url'] = topic_href
    topic_resp = requests.get(f"{URLS['base_url']}/{URLS['additional_url']}", verify=ssl.CERT_NONE)
    topic_content = BeautifulSoup(topic_resp.content.decode(), 'lxml')
    
    for fantom_article_url in topic_content.find_all('a'):
        if (
                fantom_article_url.get('target') and 
                fantom_article_url.text.startswith('https://doi.org') and 
                not fantom_article_url.text in URLS['system_urls']
        ):
            udk = extract_udk_value(topic_content, fantom_article_url)
            logging.info(f"\nFantom article url: {fantom_article_url.get('href')}\tudk value:{udk}")
            
            article = extract_article(fantom_article_url.get('href'))
            if not article:
                continue
            base_data_path = os.path.join('..', 'data_1')
            file_name = f"{age}_{topic_text}_{udk}_{fantom_article_url.get('href')}.pdf"
            file_name = file_name.replace('/', '-').replace(':', '-')
            load_article(article, base_data_path, file_name)


def parse_articles():
    response = requests.get(URLS['start_url'])
    soup = BeautifulSoup(response.content, 'lxml')

    years_table = soup.find_all('table')[1]
    ages = [str(i) for i in range(2013, 2023)]
    prev_cell = None 
    curr_age = None

    for row in years_table.find_all('tr'):
        for cell in row.find_all('td'):
            if cell.text in ages:
                curr_age = cell.text
                logging.info(f"Year: {cell.text}")
            elif prev_cell and prev_cell.text in ages:
                topics = list(map(lambda x: (x.get("href"), x.text), cell.find_all("a")))
                for topic_href, topic_text in topics:
                    # print(topic_href)
                    # print(topic_text)
                    parse_topic(topic_href, topic_text, curr_age)
            prev_cell = cell 


if __name__ == '__main__':
    parse_articles()

