from django.db import models
from .lsi import Html
from functools import reduce


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
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    terms = models.ManyToManyField(Term, through='DocumentTerm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html = Html(self.file.url)

    @classmethod
    def make_corpus(cls, doc, terms):

        for term in terms:
            word = Term.objects.get_or_create(term=term)[0]
            word.frequency += 1
            word.save()
            doct = DocumentTerm.objects.filter(
                document=doc.id,
                term=word.id
            )
            if(len(doct) > 0):
                doct = doct[0]
            else:
                doct = DocumentTerm(document=doc, term=word)

            doct.frequency += 1
            doct.save()

    def get_terms(self):
        return self.html.get_words()

    def save(self, *args, **kwargs):
        self.title = self.html.get_title()
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title


class DocumentTerm(models.Model):
    document = models.ForeignKey(Document,  on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, blank=True, null=True)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return self.term
