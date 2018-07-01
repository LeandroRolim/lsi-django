from django.contrib import admin
from .ranking import *
from .models import *

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = ['title', 'stopwords', 'adverb_verb', 'count_terms']


@admin.register(DocumentTerm)
class DocumentTermAdmin(admin.ModelAdmin):
    list_display = [
        'term',
        'frequency',
        'TF',
        'IDF',
        'TFIDF',
    ]
    list_filter = ['document']

    def TF(self, term):
        return getTF(term)

    def IDF(self, term):
        return getIDF(term)

    def TFIDF(self, term):
        return getTFIDF(term)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        'term',
        'frequency',
    ]

