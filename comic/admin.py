from django.contrib import admin

# Register your models here.
from .models import Tag, Series, Episode

class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Series)
admin.site.register(Episode)
