from django.db import models
from .lsi import *
from django.db.models.signals import post_save
import os


# add document to corpus

def make_corpus(doc, terms_doc):
    terms = remove_adverb_verb(remove_stopwords(terms_doc))

    for term in terms:
        word = Term.objects.get_or_create(term=term)[0]
        word.frequency += 1
        word.save()
        doct = DocumentTerm.objects.filter(
            document=doc.id,
            term=word.id
        )
        if (len(doct) > 0):
            doct = doct[0]
        else:
            doct = DocumentTerm(document=doc, term=word)

        doct.frequency += 1
        doct.save()


def add_corpus(sender, **kwargs):
    if kwargs['created']:
        doc = kwargs['instance']
        make_corpus(doc, doc.get_terms())

# Create your models here.


class Term(models.Model):
    term = models.CharField(max_length=255, unique=True)
    frequency = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Term, self).save(*args, **kwargs)

    def __str__(self):
        return self.term


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField()
    stopwords = models.IntegerField(default=1)
    adverb_verb = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    terms = models.ManyToManyField(Term, through='DocumentTerm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docAbst = DocumentFactory.getFactory(self.file)

    def get_terms(self):
        terms = self.docAbst.get_words()
        return terms

    def count_terms(self):
        return len(self.get_terms())

    def save(self, *args, **kwargs):
        self.title = self.docAbst.get_title()
        self.stopwords = len(self.get_terms()) - len(remove_stopwords(self.get_terms()))
        self.adverb_verb = len(remove_stopwords(self.get_terms())) - len(remove_adverb_verb(remove_stopwords(self.get_terms())))
        print(self.stopwords)
        print(len(remove_stopwords(self.get_terms())))
        print(len(remove_adverb_verb(remove_stopwords(self.get_terms()))))
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title

# event called on post save


post_save.connect(add_corpus, sender=Document)


class DocumentTerm(models.Model):
    document = models.ForeignKey(Document,  on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True, null=True)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return self.term
