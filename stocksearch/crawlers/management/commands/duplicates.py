from django.core.management.base import BaseCommand, CommandError
from crawlers.models import Image
from django.db.utils import IntegrityError
import pdb

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete duplicate images')
        
    def handle(self, *args, **options):
        images = Image.objects.distinct('hash')
        delete_images = 0
        for image in images:
            images2 = Image.objects.extra(where=['hamming_text(hash,%s)>=0.92'], params=[image.hash]).exclude(origin=image.origin)
            for image2 in images2:
                print("{} is a duplicate of {}".format(image.page_url,image2.page_url))
                if options['delete']:
                    try:
                        duplicate_tags = image2.tags.all()
                        image.tags.add(*duplicate_tags)
                        image2.delete()
                        delete_images+=1
                    except IntegrityError:
                        pass
        print("Deleted {} images".format(delete_images))





