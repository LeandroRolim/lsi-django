from documentos.models import *
from math import log


# Log Normalization Algorithm
def getTF(term: Term):
    return 1 + log(term.frequency)


# Inverse Frequency Algorithm
def getIDF(term: Term):
    qtdDocs = Document.objects.count()
    qtdDocsTerm = Document.objects.filter(terms=term).count()
    return log(qtdDocsTerm / qtdDocs)


# TF * IDF
def getTFIDF(term: Term):
    return getTF(term) * getIDF(term)
