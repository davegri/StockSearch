from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.db.utils import IntegrityError
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import re
import pdb
import os

from functools import wraps
import time

from crawlers.models import Image, Tag, Crawler as CrawlerDB

from crawlers.crawler import Crawler, RED, GREEN

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "stocksearch.settings.development")


class PexelCrawler(Crawler):
    origin = 'PX'
    base_url = 'https://www.pexels.com/?format=html&page={}'
    domain = 'www.pexels.com'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        article_tags = page_soup.select('article.photo-item')
        return [article.find('a') for article in article_tags]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='js-download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='photo__img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='list-padding')

class MagdeleineCrawler(Crawler):
    origin = 'MG'
    base_url = 'http://magdeleine.co/license/cc0/page/{}/'
    domain = 'www.magdeleine.co'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.select('a.photo-link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='download').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', id='main-img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='tags')

class FancycraveCrawler(Crawler):
    origin = 'FC'
    base_url = 'http://fancycrave.com/page/{}'
    domain = 'fancycrave.com'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='type-photo')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('aside', class_='metadata')['data-permalink']


class LittlevisualsCrawler(Crawler):
    origin = 'LV'
    base_url = 'http://littlevisuals.co/page/{}'
    domain = 'www.littlevisuals.co'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='photo')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['data-1280u']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

class StocksnapCrawler(Crawler):
    origin = 'SS'
    base_url = 'https://stocksnap.io/view-photos/sort/date/desc/page-{}'
    first_page_url = 'https://stocksnap.io/view-photos/sort/date/desc/'
    domain = 'www.stocksnap.io'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, first_page_url=self.first_page_url)

    def get_image_page_links(self, page_soup):
        return page_soup.select('a.photo-link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='img-photo')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='img-photo')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('table', class_='img-details')

class PixabayCrawler(Crawler):
    origin = 'PB'
    base_url = 'https://pixabay.com/en/editors_choice/?image_type=photo&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):

        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayunsplashCrawler(Crawler):
    origin = 'PBU'
    base_url = 'https://pixabay.com/en/users/Unsplash-242387/?tab=latest&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayfoundryCrawler(Crawler):
    origin = 'PBF'
    base_url = 'https://pixabay.com/en/photos/?q=user%3AFoundry+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabaymilivanilyCrawler(Crawler):
    origin = 'PBM'
    base_url = 'https://pixabay.com/en/photos/?q=user%3Amilivanily+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayolichelCrawler(Crawler):
    origin = 'PBO'
    base_url = 'https://pixabay.com/en/photos/?q=user%3Aolichel+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabaymarkusspiskeCrawler(Crawler):
    origin = 'PBMK'
    base_url = 'https://pixabay.com/en/photos/?q=user%3Amarkusspiske+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container
class PixabaytookapicCrawler(Crawler):
    origin = 'PBTP'
    base_url = 'https://pixabay.com/en/photos/?q=user%3Atookapic+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayjillCrawler(Crawler):
    origin = 'PBJ'
    base_url = 'https://pixabay.com/en/photos/?q=user%3Ajill111+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayryanCrawler(Crawler):
    origin = 'PBR'
    base_url = 'https://pixabay.com/en/photos/?q=user%3ARyanMcGuire+&image_type=photo&order=latest&cat=&pagi={}'
    domain = 'www.pixabay.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, "PB", self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', {'itemprop':'contentURL'})['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container
class SkitterphotoCrawler(Crawler):
    origin = 'SP'
    base_url = 'http://skitterphoto.com/?page_id=177132&paged={}'
    domain = 'www.skitterphoto.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', rel='bookmark')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', title='Download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='portfolio-image').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('footer', class_='entry-meta')

class TookapicCrawler(Crawler):
    origin = 'TP'
    base_url = 'https://stock.tookapic.com/photos?filter=free&list=curated&page={}'
    domain = 'www.stock.tookapic.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', class_='photo__link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find(lambda x: x.has_attr('download'))['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find(lambda x: x.has_attr('data-src'))['data-src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='mt- u-nano')

class KaboompicsCrawler(Crawler):
    origin = 'KP'
    base_url = 'http://kaboompics.com/s{}/recent'
    domain = 'www.kaboompics.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('div', class_='one')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='download')['link']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='img')['rel']

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('div', class_='title').find('a')['href']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

class PicjumboCrawler(Crawler):
    origin = 'PJ'
    base_url = 'https://picjumbo.com/latest-free-stock-photos/page/{}/'
    domain = 'www.picjumbo.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('div', class_='item_wrap')

    def get_image_source_url(self, image_page_soup):
        return "http://"+image_page_soup.find('img', class_='image')['src'][2:].split("?", 1)[0]

    def get_image_thumbnail_url(self, image_page_soup):
        return "http://"+image_page_soup.find('img', class_='image')['src'][2:].split("?", 1)[0]+"?&h=500"

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a', class_='button')['href']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

class LibreshotCrawler(Crawler):
    origin = 'LS'
    base_url = 'http://libreshot.com/page/{}/'
    domain = 'www.libreshot.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='post-thumbnail')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-inner').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-inner').find('img')['data-lazy-src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('p', class_='post-tags')

class JaymantriCrawler(Crawler):
    origin = 'JM'
    base_url = 'http://jaymantri.com/page/{}'
    domain = 'www.jaymantri.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='photo')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='caption').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='mobPhoto')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='tags')

class MmtCrawler(Crawler):
    origin = 'MT'
    base_url = 'http://mmtstock.com/page/{}/'
    domain = 'mmtstock.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='post')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='post-categories')

class FreenaturestockCrawler(Crawler):
    origin = 'FN'
    base_url = 'http://freenaturestock.com/page/{}'
    domain = 'freenaturestock.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='type-photo')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img')['data-highres']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('input', class_='short-url-field')['value']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

class BaraartCrawler(Crawler):
    origin = 'BA'
    base_url = 'http://www.bara-art.com/photos/page/{}/'
    domain = 'www.bara-art.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='blog-thumb')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('span', class_='tags')

class FreelyphotosCrawler(Crawler):
    origin = 'FP'
    base_url = 'http://freelyphotos.com/'
    domain = 'www.freelyphotos.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='post-container')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='post-content').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='wrapper').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('li', class_='post-tags')

class BarnimagesCrawler(Crawler):
    origin = 'BI'
    base_url = 'http://barnimages.com/images/page/{}/'
    domain = 'www.barnimages.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='format-image')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='download-button')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('img')['srcset'].split(',')[0]

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('meta', {'property':'article:tag'})
        return [tag['content'] for tag in tags]

class GoodstockphotosCrawler(Crawler):
    origin = 'GS'
    base_url = 'https://goodstock.photos/page/{}/'
    domain = 'www.goodstock.photos'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='entry-content')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='button')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return "http://"+image_page_soup.find('main', class_='content').find('img')['src'].replace("//","")

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('span', class_='entry-tags')


class FindaphotoCrawler(Crawler):
    origin = 'IP'
    base_url = 'http://finda.photo/search?q=&page={}'
    domain = 'www.finda.photo/'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_urls(self, page_soup):
        """
        returns a list of urls for each image on the page
        """
        image_page_links_containers = page_soup.find_all('div', class_="box")
        image_page_links = [link.find('a') for link in image_page_links_containers]
        if not image_page_links: raise ImageURLsNotFound
        image_page_urls = [ link['href'].replace('..', '') for link in image_page_links]
        # make sure urls are absolute
        image_page_urls = [self.make_absolute_url(url) for url in image_page_urls]
        return image_page_urls

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('a', class_='download-button')['href'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('div', class_='image-detail-image-container').find('img')['src'])

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='image-detail-tags')

class PicographyCrawler(Crawler):
    origin = 'PG'
    base_url = 'http://picography.co/page/{}/'
    domain = 'picography.co/'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', class_='hdt-pic-item')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', text='Download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('a', text='Download')['href']

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('meta', {'property':'article:tag'})
        tag_names = [tag['content'] for tag in tags if tag['content']!='download']
        return tag_names

class NegativespaceCrawler(Crawler):
    origin = 'NS'
    base_url = 'http://negativespace.co/photos/page/{}/'
    domain = 'negativespace.co'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('li', class_='product-small')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='button')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        try:
            return image_page_soup.find('div', class_='easyzoom').find('img')['srcset'].split(',',1)[0]
        except:
            return image_page_soup.find('div', class_='easyzoom').find('img')['src']
    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('span', class_='tagged_as')

class SplitshireCrawler(Crawler):
    origin = 'SH'
    base_url = 'http://www.splitshire.com/recent-photos/page/{}/'
    domain = 'www.splitshire.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='post-image')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('meta', {'property':'article:tag'})
        tag_names = [tag['content'] for tag in tags if tag['content']!='download']
        return tag_names

class RealisticshotsCrawler(Crawler):
    origin = 'RS'
    base_url = 'http://realisticshots.com/page/{}'
    domain = 'realisticshots.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='photo')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='photo').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='photo').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

class StreetwillCrawler(Crawler):
    origin = 'SW'
    base_url = 'http://streetwill.co/posts?_=1444819261026&page={}'
    domain = 'streetwill.co'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', class_='image')

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('div', class_='image-wrapper').find('img')['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('div', class_='image-wrapper').find('img')['src'])

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='info-grid')

    def make_absolute_url(self, url,):
        protocol = "http://"
        return urljoin(protocol + self.domain, url)

class BossfightCrawler(Crawler):
    origin = 'BF'
    base_url = 'http://bossfight.co/page/{}'
    domain = 'bossfight.co'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='post')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', text='Download Full Resolution Image Here')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('meta', {'property':'og:image'})['content']

    def get_tags(self, image_page_soup):
        tags_string = image_page_soup.find('h1', class_='entry-title').text
        tag_names = [tag for tag in tags_string.split(', ')]
        return tag_names

class LifeofpixCrawler(Crawler):
    origin = 'LP'
    base_url = 'http://www.lifeofpix.com/page/{}/'
    domain = 'www.lifeofpix.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('li', class_='time')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('ul', class_='slides').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('span', class_='post-thumb').find('img')['src']

    def get_tags(self, image_page_soup):
        tags_string = image_page_soup.find('div', class_='the-content').find('h1').string
        tag_names = [tag for tag in tags_string.split(', ')]
        return tag_names

class PublicdomainarchiveCrawler(Crawler):
    origin = 'PD'
    base_url = 'http://publicdomainarchive.com/public-domain-images/page/{}/'
    domain = 'publicdomainarchive.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', text='Download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('p').find('img')['src']

    def get_tags(self, image_page_soup):
        tags_string = image_page_soup.find('h1').string.replace('Public Domain Images – ','')
        tag_names = [tag for tag in tags_string.split(' ')]
        return tag_names

class BucketlistlyCrawler(Crawler):
    origin = 'BL'
    base_url = 'http://photos.bucketlistly.com/page/{}'
    domain = 'photos.bucketlistly.com'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('div', class_='photo')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find(lambda x: x.has_attr('download'))['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

class FreeimagebankCrawler(Crawler):
    origin = 'FB'
    base_url = 'http://www.freemagebank.com/page/{}/'
    domain = 'www.freemagebank.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', class_='dcs_view_details')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('span', text='#Tags').find_parent()

class CreativevixCrawler(Crawler):
    origin = 'CV'
    base_url = 'http://creativevix.com/stock{}'
    first_page_url = 'http://creativevix.com/stock'
    domain = 'creativevix.com'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False, first_page_url=self.first_page_url)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('li',class_="work-item")

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('a',text="Download")['href'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img')['src'])

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

    def get_tags(self, image_page_soup):
        tags_string = image_page_soup.find('img')['alt']
        tag_names = [tag for tag in tags_string.split(' ')]
        return tag_names

    def get_image_page_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('a',text="Download")['href'])

    def make_absolute_url(self, url,):
        protocol = "http://"
        return urljoin(protocol + self.domain, url)

class DesignerpicsCrawler(Crawler):
    origin = 'DP'
    base_url = 'http://www.designerspics.com/page/{}/'
    domain = 'www.designerspics.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='photos')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='wpdm_file').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='photo-tags')

class FreestocksCrawler(Crawler):
    origin = 'FS'
    base_url = 'http://freestocks.org/page/{}/'
    domain = 'freestocks.org'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='img-wrap')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='img-wrap').find('img')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='img-wrap').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('p', class_='tags')

class TravelcoffeebookCrawler(Crawler):
    origin = 'TC'
    base_url = 'http://travelcoffeebook.com/page/{}'
    domain = 'travelcoffeebook.com'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all(lambda tag: tag.name == 'div' and
                                   tag.get('class') == ['post'])

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='photoCaption').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='media').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find(class_='datenotes').find('a')['href']

class FoodiesfeedCrawler(Crawler):
    origin = 'FF'
    base_url = 'https://foodiesfeed.com/free-food-images/page/{}/'
    domain = 'foodiesfeed.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='post-thumbnail')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='wpdm-link-tpl')['data-durl']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_=re.compile(r'wp-image-'))['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('p', class_='post-tag')

class MystockphotosCrawler(Crawler):
    origin = 'MS'
    base_url = 'http://mystock.photos/page/{}/?s'
    domain = 'mystock.photos'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='post')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='download_link')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='wp-post-image')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('span', class_='tags-links')

class IsorepublicCrawler(Crawler):
    origin = 'IR'
    base_url = 'http://isorepublic.com/page/{}/'
    domain = 'isorepublic.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='image')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='dl')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='image').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='tags')

class JeshootsCrawler(Crawler):
    origin = 'JS'
    base_url = 'http://jeshoots.com/page/{}/'
    first_page_url = 'http://jeshoots.com'
    domain = 'jeshoots.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, first_page_url=self.first_page_url)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item-download')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        div = image_page_soup.find('div', class_='item-download')
        if not div:
            return image_page_soup.find('div', class_='entry-image').find('img')['src']
        elif '$' in div.text:
            print(div.text)
            raise TypeError
        else:
            return div.find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-image').find('img')['src']

    def get_tags(self, image_page_soup):
        return image_page_soup.find('h1', class_='entry-title').string,

class StokpicCrawler(Crawler):
    origin = 'SK'
    base_url = 'http://stokpic.com/page/{}/'
    domain = 'stokpic.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find('div',class_='et_pb_section_2').find_all('div', class_='has-post-thumbnail')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='et_pb_promo_button')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('a', class_='et_pb_promo_button')['href']

    def get_tags(self, image_page_soup):
        tag_list = image_page_soup.find('article', class_='has-post-thumbnail')['class']
        tags = [tag.replace('project_tag-','').replace('-',' ') for tag in tag_list if tag.startswith('project_tag-')]
        ignore_words = ['free','stokpic','stock photo','stock photography','stock images', 'commercial photography', 'free images', 'free photos', 'stock photos', 'free stock photos', 'image']
        return [tag for tag in tags if tag not in ignore_words]

class JoshuahibbertCrawler(Crawler):
    origin = 'JH'
    base_url = 'http://photos.joshnh.com/page/{}'
    domain = 'photos.joshnh.com'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='photo')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', text=re.compile('^Download$', re.IGNORECASE))['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='photo-wrapper').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('section', class_='has-tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find_all('a', class_='permalink')[1]['href']

    def get_tags(self, image_page_soup):
        tags_container = self.get_tags_container(image_page_soup)
        tag_links = tags_container.find_all('a')
        tag_names = [tag_link.text for tag_link in tag_links]
        return tag_names

class MinimographyCrawler(Crawler):
    origin = 'MI'
    base_url = 'http://minimography.com/page/{}/'
    domain = 'minimography.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='has-post-thumbnail')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('img')['src']

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('meta', {'property':'article:tag'})
        return [tag['content'] for tag in tags]

class PicklejarCrawler(Crawler):
    origin = 'IJ'
    base_url = 'http://picklejar.in/page/{}/'
    domain = 'picklejar.in'
    def __init__(self, db_record=None):
            Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='gallery-item')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img')['data-src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img')['data-src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

class AlanaioCrawler(Crawler):
    origin = 'AI'
    base_url = 'http://alana.io/downloads/page/{}/'
    domain = 'alana.io'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='type-download')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='attachment-product_page_image')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='attachment-product_page_image')['src']

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('a', {'rel':'tag'})
        return [tag.text for tag in tags]

class PicallsCrawler(Crawler):
    origin = 'PA'
    base_url = 'http://picalls.com/free-images/page/{}'
    domain = 'picalls.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='post')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='imagen-single')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        prefix = 'http://picalls.com/wp-content/themes/picalls/timthumb.php?src='
        suffix = '&h=500&zc=1'
        return prefix + image_page_soup.find('img', class_='imagen-single')['src'] + suffix

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags')

class StockifiedCrawler(Crawler):
    origin = 'SF'
    base_url = 'https://www.stockified.com/page/{}'
    domain = 'stockified.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='product-image')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='attachment-product-img')['data-lazy-src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='attachment-product-img')['data-lazy-src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='product-tags')

class LookingglassCrawler(Crawler):
    origin = 'LG'
    base_url = 'https://lookingglassfreephotos.tumblr.com/page/{}'
    domain = 'lookingglassfreephotos.tumblr.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='post')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='post--photo__img')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='post--photo__img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='post__actions-tags__items')

class NomadpicturesCrawler(Crawler):
    origin = 'NP'
    base_url = 'https://nomad.pictures/page/{}?s'
    domain = 'nomad.pictures'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('article', class_='type-post')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('img')['data-lazy-src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='entry-content').find('img')['data-lazy-src']

    def get_tags(self, image_page_soup):
        tags = image_page_soup.find_all('meta', {'property':'article:tag'})
        return [tag['content'] for tag in tags]

class AvopixCrawler(Crawler):
    origin = 'AP'
    base_url = 'https://avopix.com/search/photos/%20/{}'
    domain = 'avopix.com'
    def __init__(self, db_record=None):
        Crawler.__init__(self, db_record, self.origin, self.base_url, self.domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find('div', class_='grid').find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='detail').find('img')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='detail').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('p', class_='detail-sidebar-tags')

crawler_classes = [AvopixCrawler, NomadpicturesCrawler, LookingglassCrawler, StockifiedCrawler, PicallsCrawler, AlanaioCrawler, PicklejarCrawler, MinimographyCrawler, JoshuahibbertCrawler, JeshootsCrawler, IsorepublicCrawler, MystockphotosCrawler, FoodiesfeedCrawler, TravelcoffeebookCrawler, FreestocksCrawler, DesignerpicsCrawler, FreeimagebankCrawler, BucketlistlyCrawler, PublicdomainarchiveCrawler, LifeofpixCrawler,
                   StreetwillCrawler, RealisticshotsCrawler, SplitshireCrawler, PixabaymarkusspiskeCrawler,
                   NegativespaceCrawler, PicographyCrawler, BossfightCrawler,
                   BarnimagesCrawler, FreelyphotosCrawler, BaraartCrawler,
                   FreenaturestockCrawler, MmtCrawler, JaymantriCrawler,
                   PicjumboCrawler, KaboompicsCrawler, TookapicCrawler, SkitterphotoCrawler,
                   PixabayryanCrawler, PixabayunsplashCrawler, PixabayCrawler, PixabayolichelCrawler, PixabaymilivanilyCrawler, PixabaytookapicCrawler, PixabayjillCrawler, FancycraveCrawler, LittlevisualsCrawler, StocksnapCrawler, PexelCrawler, FindaphotoCrawler,]

def getClass(str):
    for crawler_class in crawler_classes:
        if str == crawler_class.origin:
            return crawler_class


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--full',
            action='store_true',
            dest='full_crawl',
            default=False,
            help='Trigger a full crawl that keeps going even if it finds existing images')
        parser.add_argument('origin', nargs='*')
        parser.add_argument('--page',default=1)
        parser.add_argument('--test',action='store_true',default=False)

    def handle(self, *args, **options):
        global crawler_classes
        if options['origin']:
            crawler_classes = [getClass(origin) for origin in options['origin']]
        crawlers = [crawler_class() for crawler_class in crawler_classes]
        full_crawl = options['full_crawl']
        test_mode = options['test']
        page = int(options['page'])
        for crawler in crawlers:
            crawler.crawl(full_crawl=full_crawl,start_page=page, test_mode = test_mode)
