from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_views', 'date_publication')
    search_fields = ('name', 'contents_article')
    list_filter = ('date_publication',)
