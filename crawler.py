import requests
from bs4 import BeautifulSoup
import os
import re



class Image:

    def __init__(self, filename, tags,):
        self.filename = filename
        self.tags = tags


class PexelCrawler:

    def __init__(self):
        self.start_page = 0
        self.IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'Images')

    @staticmethod
    def _getPage(page_number=1):
        """ Gets page from pexels website and returns a BeautifulSoup object of the page """

        response = requests.get(
            'https://www.pexels.com/?format=js&page={}'.format(page_number))
        return BeautifulSoup(response.text)

    @staticmethod
    def _makeAbsoluteUrl(url):
        return 'https://www.pexels.com/' + url[2:-2]

    @staticmethod
    def _makeFileNameFromUrl(url):
        p = re.compile(r'(?=[^\/]*$).+')
        return re.search(p, url).group()


    def crawl(self):
        current_page = self.start_page
        while True:
            current_page+=1
            soup = PexelCrawler._getPage(current_page)
            image_links = [PexelCrawler._makeAbsoluteUrl(
                link["href"]) for link in soup.find_all('a') if link.has_attr('title')]

            for image_link in image_links:
                response = requests.get(image_link)
                soup = BeautifulSoup(response.text)
                image_source_link = soup.find('a', {'class': 'js-download'})["href"]

                print("requesting image at: "+ image_source_link)

                image_response = requests.get(image_source_link, stream=True)

                print("saving image")
                filename = PexelCrawler._makeFileNameFromUrl(image_response.url)
                if image_response.status_code == 200:
                    with open(os.path.join(self.IMAGE_DIR, filename), 'wb') as f:
                        for chunk in image_response:
                            f.write(chunk)


PexelCrawler = PexelCrawler()
PexelCrawler.crawl()
