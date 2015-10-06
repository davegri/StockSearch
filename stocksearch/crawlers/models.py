from django.db import models
from django.core.files import File
import tempfile

from PIL import Image as Imagelib, ImageOps
from .blockhash import blockhash, blockhash_even
import os
from io import BytesIO
import requests

from django.conf import settings as djangoSettings

import pdb
import time

from .origins import origins


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):

    source_url = models.URLField(max_length=400)
    page_url = models.URLField(unique=True, max_length=400)
    thumbnail = models.ImageField(upload_to='thumbs', null=True)
    origin = models.CharField(choices=origins, max_length=2)
    tags = models.ManyToManyField(Tag)
    hash = models.CharField(max_length=576, unique=True)

    def __str__(self):
        return self.page_url

    def create_hash(self):
        thumbnail = Imagelib.open(self.thumbnail.path)
        thumbnail = thumbnail.convert('RGB')
        hash = blockhash(thumbnail, 48)
        self.hash = hash
        self.save(update_fields=["hash"])
        return hash

    def create_thumbnail(self, image_url):
        if not self.thumbnail:
            if  not image_url:
                image_url = self.source_url
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            }
            for i in range(5):
                r = requests.get(image_url, stream=True, headers=headers)
                if r.status_code != 200 and r.status_code!= 304:
                    print("error loading image url status code: {}".format(r.status_code))
                    time.sleep(2)
                else:
                    break

            if r.status_code != 200 and r.status_code!= 304:
                    print("giving up on this image, final status code: {}".format(r.status_code))
                    return False

            # Create the thumbnail of dimension size
            size = 500, 500
            img = Imagelib.open(r.raw)
            thumb = ImageOps.fit(img, size, Imagelib.ANTIALIAS)

            # Get the image name from the url
            img_name = os.path.basename(image_url.split('?', 1)[0])


            file_path = os.path.join(djangoSettings.MEDIA_ROOT, "thumb" + img_name)
            thumb.save(file_path, 'JPEG')

            # Save the thumbnail in the media directory, prepend thumb
            self.thumbnail.save(
                img_name,
                File(open(file_path, 'rb')))

            os.remove(file_path)
            return True


class Crawler(models.Model):
    origin = models.CharField(choices=origins, max_length=2)
    current_page = models.IntegerField(default=1)
    images_scraped = models.IntegerField(default=0)

    def __str__(self):
        return self.get_origin_display()+" Crawler"


