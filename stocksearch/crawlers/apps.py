from django.apps import AppConfig
import watson

class CrawlersConfig(AppConfig):
    name = "crawlers"
    def ready(self):
        Image = self.get_model("Image")
        watson.register(Image,  fields=('tags__name',), store=('thumbnail__url', 'page_url', 'source_url', 'get_origin_display', 'tags__name'))
