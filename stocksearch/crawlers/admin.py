from django.contrib import admin

# Register your models here.
from .models import Image, Tag, Crawler

class ImageInline(admin.TabularInline):
    model = Image.tags.through

class TagInline(admin.TabularInline):
    model = Image.tags.through

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['tags__name','page_url']
    list_display = ("page_url","clicks")
    readonly_fields=['tags']

    def tags(self, image):
        tags = []
        for tag in image.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

@admin.register(Crawler)
class CrawlerAdmin(admin.ModelAdmin):
    pass