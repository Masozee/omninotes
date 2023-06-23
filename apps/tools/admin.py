from django.contrib import admin
from .models import Visitor

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visited_url', 'visited_at', 'browser', 'country', 'city')
    list_filter = ('browser', 'country', 'city')
    search_fields = ('visited_url', 'browser', 'country', 'city')
    date_hierarchy = 'visited_at'

admin.site.register(Visitor, VisitorAdmin)
