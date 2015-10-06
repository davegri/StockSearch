from django.core.management.base import BaseCommand, CommandError
from crawlers.models import Image
from django.db.utils import IntegrityError

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fix',
            action='store_true',
            dest='fix',
            default=False,
            help='Delete duplicate images')
        
    def handle(self, *args, **options):
        images = Image.objects.all()
        if options['fix']:
            images = Image.objects.extra(where=['CHAR_LENGTH(hash)!=576'])
            print("There are {} broken hashes, fixing..".format(images.count()))
        length = len(images)
        for i,image in enumerate(images):
            image.create_hash()
            print("hashed {} of {}".format(i+1,length))