from django.contrib import admin
from .ranking import *
from .models import *

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = [
        'title',
        'stopwords',
        'adverb_verb',
        'count_terms'
    ]


@admin.register(DocumentTerm)
class DocumentTermAdmin(admin.ModelAdmin):

    list_display = [
        'term',
        'frequency',
        'TF',
        'IDF',
        'TFIDF'
    ]
    list_filter = ['document']

    def TF(self, document):
        print(document)
        #tf = LogNormTF()
        return 'q'

    def IDF(self, term):
        return term.term

    def TFIDF(self, term):
        return term.term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        'term',
        'frequency',
    ]

