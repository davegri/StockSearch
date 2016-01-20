from django.apps import AppConfig
from watson import search as watson

class CrawlersConfig(AppConfig):
    name = "crawlers"
    def ready(self):
        Image = self.get_model("Image")
        watson.register(Image,  fields=('tags__name',), store=('thumbnail__url', 'page_url', 'source_url', 'get_origin_display', 'tags__name'))
