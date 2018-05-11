from django.db import models


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=200)
    url = models.FileField()

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        filename = self.url.url

    def __str__(self):
        return self.title


class DocumentTerm(models.Model):
    document = models.ForeignKey(Document,  on_delete=models.CASCADE,)
    term = models.CharField(max_length=255)
    frequency = models.IntegerField()

    def __str__(self):
        return self.term


class Term(models.Model):
    term = models.CharField(max_length=255)
    frequency = models.IntegerField()

    def __str__(self):
        return self.term