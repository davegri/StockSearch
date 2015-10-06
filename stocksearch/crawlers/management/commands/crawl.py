from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.db.utils import IntegrityError

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
    def __init__(self, db_record=None):
        origin = 'PX'
        base_url = 'https://www.pexels.com/?format=html&page={}'
        domain = 'www.pexels.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        article_tags = page_soup.select('article.photos__photo')
        return [article.find('a') for article in article_tags]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='js-download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='photo__img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='list-padding')

class MagdeleineCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'MG'
        base_url = 'http://magdeleine.co/browse/page/{}/'
        domain = 'www.magdeleine.co'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        return page_soup.select('a.photo-link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('div', class_='download').find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', id='main-img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='tags')

class FancycraveCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'FC'
        base_url = 'http://fancycrave.com/page/{}'
        domain = 'www.fancycrave.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        return page_soup.select('a.timestamp')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', text='Download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='pxu-photo').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='tags') 

class LittlevisualsCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'LV'
        base_url = 'http://littlevisuals.co/page/{}'
        domain = 'www.littlevisuals.co'
        Crawler.__init__(self, db_record, origin, base_url, domain, nested_scrape=False)

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
    def __init__(self, db_record=None):
        origin = 'SS'
        base_url = 'https://stocksnap.io/view-photos/sort/date/desc/page-{}'
        first_page_url = 'https://stocksnap.io/view-photos/sort/date/desc/'
        domain = 'www.stocksnap.io'
        Crawler.__init__(self, db_record, origin, base_url, domain, first_page_url=first_page_url)

    def get_image_page_links(self, page_soup):
        return page_soup.select('a.photo-link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('img', class_='img-photo')['src']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='img-photo')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('table', class_='img-details') 

class PixabayCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'PB'
        base_url = 'https://pixabay.com/en/editors_choice/?image_type=photo&pagi={}'
        domain = 'www.pixabay.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='img_250')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', class_='pure-img')['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', class_='pure-img')['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class PixabayunsplashCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'PB'
        base_url = 'https://pixabay.com/en/users/Unsplash-242387/?tab=latest&pagi={}'
        domain = 'www.pixabay.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        containers = page_soup.find_all('div', class_='item')
        return [container.find('a') for container in containers]

    def get_image_source_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', class_='pure-img')['src'])

    def get_image_thumbnail_url(self, image_page_soup):
        return self.make_absolute_url(image_page_soup.find('img', class_='pure-img')['src'])

    def get_tags_container(self, image_page_soup):
        tag_container = image_page_soup.find('h1')
        [tag.extract() for tag in tag_container.find_all('a', class_='award')]
        return tag_container

class SkitterphotoCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'SP'
        base_url = 'http://skitterphoto.com/?page_id=13&paged={}'
        domain = 'www.skitterphoto.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', rel='bookmark')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', title='Download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('div', class_='portfolio-image').find('img')['src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('footer', class_='entry-meta')

class TookapicCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'TP'
        base_url = 'https://stock.tookapic.com/?filter=free&list=all&page={}'
        domain = 'www.stock.tookapic.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        return page_soup.find_all('a', class_='photo__link')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find(lambda x: x.has_attr('download'))['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find(lambda x: x.has_attr('data-src'))['data-src']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='c-list-tag')

class KaboompicsCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'KP'
        base_url = 'http://kaboompics.com/s{}/recent'
        domain = 'www.kaboompics.com'
        Crawler.__init__(self, db_record, origin, base_url, domain, nested_scrape=False)

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
    def __init__(self, db_record=None):
        origin = 'PJ'
        base_url = 'https://picjumbo.com/page/{}/'
        domain = 'www.picjumbo.com'
        Crawler.__init__(self, db_record, origin, base_url, domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('div', class_='item_wrap')

    def get_image_source_url(self, image_page_soup):
        return "http://"+image_page_soup.find('img', class_='image')['src'][2:].split("?", 1)[0]

    def get_image_thumbnail_url(self, image_page_soup):
        return "http://"+image_page_soup.find('img', class_='image')['src'][2:].split("?", 1)[0]+"?&h=500"

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a', class_='button')['href']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('div', class_='browse_more')

class LibreshotCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'LS'
        base_url = 'http://libreshot.com/page/{}/'
        domain = 'www.libreshot.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

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
    def __init__(self, db_record=None):
        origin = 'JM'
        base_url = 'http://jaymantri.com/page/{}'
        domain = 'www.jaymantri.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

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
    def __init__(self, db_record=None):
        origin = 'MT'
        base_url = 'http://mmt.li/page/{}/'
        domain = 'www.mmt.li'
        Crawler.__init__(self, db_record, origin, base_url, domain, nested_scrape=False)

    def get_image_containers(self, image_page_soup):
        return image_page_soup.find_all('article', class_='post')

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

    def get_image_page_url(self, image_page_soup):
        return image_page_soup.find('a')['href']

    def get_tags_container(self, image_page_soup):
        return image_page_soup.find('ul', class_='post-categories')

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--full',
            action='store_true',
            dest='full_crawl',
            default=False,
            help='Trigger a full crawl that keeps going even if it finds existing images')
        
    def handle(self, *args, **options):
        crawler_classes = [MmtCrawler, JaymantriCrawler, LibreshotCrawler, PicjumboCrawler, KaboompicsCrawler, TookapicCrawler, SkitterphotoCrawler,
                           PixabayunsplashCrawler, PixabayCrawler, PexelCrawler, MagdeleineCrawler, FancycraveCrawler,
                           LittlevisualsCrawler, StocksnapCrawler]
        crawlers = [crawler_class() for crawler_class in crawler_classes]
        full_crawl = options['full_crawl']
        for crawler in crawlers:
            crawler.crawl(full_crawl=full_crawl)



