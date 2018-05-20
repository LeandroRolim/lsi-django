from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']


@admin.register(DocumentTerm)
class DocumentTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'frequency']
    list_filter = ['document']
# admin.site.register(DocumentTerm)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        'term',
        'frequency',
    ]

#admin.site.register(Term)
