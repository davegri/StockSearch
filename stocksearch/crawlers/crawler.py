from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from crawlers.models import Image, Tag, Url, Crawler as CrawlerModel
from requests.exceptions import HTTPError, ConnectionError
import pdb
import signal
import sys
import time

RED = "\033[01;31m{0}\033[00m"
GREEN = "\033[1;36m{0}\033[00m"
BLUE = "\033[1;34m{0}\033[00m"

def signal_handler(signal, frame):
        global interrupted
        interrupted = True

class ImageURLsNotFound(Exception):
    pass

class ImageContainersNotFound(Exception):
    pass

class ImageAlreadyExists(Exception):
    pass

class Crawler():
    def __init__(self, db_record, origin, base_url, domain, first_page_url=None, nested_scrape=True):
        """
        current_page is used to track what page the crawler is on

        db_record is an instance of the model class Crawler and represents the associated
        record in the table that keeps track of the crawler in the database

        base_url is the page that is used in order to scrape images from,
        must contain {} where the page number should be

        domain_name is the domain name of the website.
        used to transform relateive urls into absolute urls.

        nested_scrape is a boolean value wich specifies wether the images need to be scraped from an individual page (nested=True)
        or if they can be scraped with all the required metadata from the general page (nested=False)
        the default is nested=True
        note: if nested=True you must implement a get_image_links method

        first_page_base_url is an optional argument to specify a special url just for the first page
        """
        self.origin = origin
        if not db_record:
            db_record, created = CrawlerModel.objects.get_or_create(origin=self.origin)
        self.current_page = db_record.current_page
        self.db_record = db_record
        self.base_url = base_url
        self.domain = domain
        self.first_page_url = first_page_url

        self.images_added = 0
        self.images_failed = 0
        self.images_duplicate = 0

        self.nested_scrape = nested_scrape


    def make_absolute_url(self, url,):
        """
        returns an absolute url for a given url using the domain_name property
        example: '/photo/bloom-flower-colorful-colourful-9459/' returns 'https://www.pexels.com/photo/bloom-flower-colorful-colourful-9459/'
        where the domain_name is 'www.pexels.com'
        """
        protocol = "https://"
        return urljoin(protocol + self.domain, url)

    def strip_protocol(self, url):
        url = url.replace('https://www.', '')
        url = url.replace('http://www.', '')
        return url

    def request_url(self, page_url, attempts=5, delay=3):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        }
        for i in range(attempts):
            try:
                response = requests.get(page_url, headers=headers)
                response.raise_for_status()
            except HTTPError as e:
                print (RED.format("page responded with "+str(response.status_code)+". trying again"+str(page_url)))
                time.sleep(delay)
            else:
                return response
        else:
            # failed to get the page raise an exception
            response.raise_for_status()

    def get_page_soup(self, response):
        return BeautifulSoup(response.text)

    def get_image_page_urls(self, page_soup):
        """
        returns a list of urls for each image on the page
        """
        image_page_links = self.get_image_page_links(page_soup)
        if not image_page_links: raise ImageURLsNotFound
        image_page_urls = [ link['href'] for link in image_page_links if link]
        # make sure urls are absolute
        image_page_urls = [self.make_absolute_url(url) for url in image_page_urls]
        return image_page_urls


    def crawl(self, start_page=None, full_crawl=True, test_mode=False):
        print("Started Crawler for {}".format(self.domain))
        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)
        images_added = 0
        images_failed = 0
        visited_page_urls = []
        if start_page:
            self.current_page=start_page

        try:
            while True:
                print('crawling page {}'.format(self.current_page))
                current_page_url = self.base_url.format(self.current_page)
                if self.current_page == 1 and self.first_page_url:
                    current_page_url = self.first_page_url
                current_page_response = self.request_url(current_page_url)
                current_page_url = current_page_response.url
                current_page_soup = self.get_page_soup(current_page_response)
                if current_page_url in visited_page_urls:
                    raise HTTPError
                visited_page_urls.append(current_page_url)
                if self.nested_scrape:
                    image_page_urls = self.get_image_page_urls(current_page_soup)
                    for n,image_page_url in enumerate(image_page_urls):
                        if interrupted:
                            self.terminate_message()
                            return
                        print('crawling image at: {} (image {} of {})'.format(image_page_url, n+1, len(image_page_urls)))
                        if self.image_exists(image_page_url):
                            print("Image already exists in database, moving on")
                            if not full_crawl:
                                self.terminate_message()
                                return
                            continue
                        try:
                            image_page_soup = self.get_page_soup(self.request_url(image_page_url))
                        except HTTPError:
                            print(RED.format("Failed to reach image page url at: {} , moving on".format(image_page_url)))
                            self.images_failed+=1
                            continue
                        scraped = self.scrape_image(image_page_soup, image_page_url)
                        if scraped and test_mode:
                            self.terminate_message()
                            return
                else:
                    image_containers = self.get_image_containers(current_page_soup)
                    if not image_containers: raise ImageContainersNotFound
                    for n, container in enumerate(image_containers):
                        if interrupted:
                            self.terminate_message()
                            return
                        print('crawling images on page: {} (image {} of {})'.format(current_page_url, n+1, len(image_containers)))
                        try:
                            scraped = self.scrape_image(container, self.get_image_page_url(container))
                            if scraped and test_mode:
                                self.terminate_message()
                                return
                        except ImageAlreadyExists:
                            if not full_crawl:
                                self.terminate_message()
                                return

                self.current_page+=1
                if self.current_page == 500:
                    raise HTTPError


        # run out of pages
        except (ConnectionError, ImageContainersNotFound, ImageURLsNotFound, HTTPError) as e:
            print("exception: ", repr(e))
            print("no more pages! terminating crawler for {}".format(self.domain))
            self.terminate_message()
            return


    def terminate_message(self):
        print("Crawling halted.")
        print(GREEN.format("{} images added to database".format(self.images_added)))
        print(BLUE.format("{} images already existed from another website".format(self.images_failed)))
        print(RED.format("{} images failed to add".format(self.images_failed)))

    def image_exists(self, image_page_url):
        return Image.objects.filter(page_url__icontains=self.strip_protocol(image_page_url)).exists() or self.db_record.visited_urls.filter(url__icontains=self.strip_protocol(image_page_url)).exists()

    def scrape_image(self, image_container_soup, image_page_url=None):
        print('getting image source url')
        try:
            image_source_url = self.get_image_source_url(image_container_soup)
        except (AttributeError, TypeError):
                print(RED.format("There was a problem getting the image source url for this image, moving on"))
                self.images_failed+=1
                return      
        # if no page url is supplied use source url as page url
        if image_page_url is None:
            image_page_url = image_source_url    
        # check if image page url exists
        if self.image_exists(image_page_url):
            print("Image already exists in database, moving on")
            raise ImageAlreadyExists
        # save image page url as a visited url in the db_record for the crawler
        url = Url(url=image_page_url)
        url.save()
        self.db_record.visited_urls.add(url)

        print('getting image thumbnail url')
        try:
            image_thumbnail_url = self.get_image_thumbnail_url(image_container_soup)
        except AttributeError:
                print(RED.format("There was a problem getting the thumbnail url for this image, moving on"))
                self.images_failed+=1
                return
        print('getting tags')
        try:
            tags = self.get_tags(image_container_soup)
        except AttributeError:
            print(RED.format("There was a problem getting the tags for this image, moving on"))
            self.images_failed+=1
            return

        print('storing image in db')
        return self.store_image(image_source_url, image_page_url, image_thumbnail_url, tags)



    def get_image_page_links(self, page_soup):
        if self.nested_scrape:
            raise NotImplementedError("method get_image_page_links must be implemented if nested=True")

    def get_image_containers(self, page_soup):
        if not self.nested_scrape:
            raise NotImplementedError("method get_image_containers must be implemented if nested=False")

    def get_image_page_url(self, page_soup):
        if not self.nested_scrape:
            raise NotImplementedError("method get_image_page_url must be implemented if nested=False")

    def get_image_source_url(self, image_page_soup):
        raise NotImplementedError("method get_image_source_url must be implemented")

    def get_image_thumbnail_url(self, image_page_soup):
        raise NotImplementedError("method get_image_thumbnail_url must be implemented")

    def get_tags_container(self, image_page_soup):
        raise NotImplementedError("method get_tags_container must be implemented")




    def get_tags(self, image_page_soup):
        tags_container = self.get_tags_container(image_page_soup)
        tag_links = tags_container.find_all('a')
        tag_names = [tag_link.string.translate(str.maketrans(dict.fromkeys('#'))) for tag_link in tag_links if tag_link.string]
        return tag_names


    def store_image(self, image_source_url, image_page_url, image_thumbnail_url, tags):

        image = Image(source_url=image_source_url, page_url=image_page_url, origin=self.origin)

        print('creating thumbnail from url: '+image_thumbnail_url)
        if image.create_thumbnail(image_thumbnail_url):
            print(BLUE.format("thumbnail created"))
        else:
            print(RED.format("thumbnail creation failed, deleting image"))
            self.images_failed+=1
            return False

        hash = image.create_hash()
        print(BLUE.format('hash created: {}'.format(hash)))

        print('checking if duplicate of existing image')
        existing = Image.objects.exclude(pk=image.pk).exclude(hash__isnull=True).exclude(hash__exact='').extra(where=['hamming_text(hash,%s)>0.9'], params=[hash])
        if existing:
            print('image is a duplicate of {} added tags to existing image and moving on'.format(existing[0].page_url))
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                existing[0].tags.add(tag)
            print(BLUE.format('tags added'))
            self.images_duplicate+=1
            image.delete()
            return False

        image.save()
        print(GREEN.format("new image saved to database"))

        for tag in tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            image.tags.add(tag)
        print(BLUE.format('added tags to image'))
        self.images_added+=1
        return True
