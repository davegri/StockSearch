from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import SearchQuery


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    search_fields = ['text',]
    list_display = ("text","amount",)