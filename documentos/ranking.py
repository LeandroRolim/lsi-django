from django.db.models import Count, Max
from documentos.models import *
from math import log
from abc import ABCMeta, abstractmethod


class TFAbstract(metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, term: Term, document: Document):
        return 0


class IDFAbstract(metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, term: Term, document: Document):
        return 0

    """# TF * IDF
    def getTFIDF(term: Term):
        return getTF(term) * getIDF(term)"""


# ---------------------------------------  TF Algorithms --------------------------------------------
class LogNormTF(TFAbstract):
    # Log Normalization Algorithm
    def calculate(self, term: Term, document: Document):
        return 1 + log(DocumentTerm.objects.filter(term=term, document=document).first().frequency, 2)


class DoubleNormTF(TFAbstract):
    # Double Normalization Algorithm
    def calculate(self, term: Term, document: Document):
        max_freq_in_doc = getMaxFreqInDoc(document)
        return 0.5 + 0.5 * (term.frequency / max_freq_in_doc)


class DoubleKNormTF(TFAbstract):
    K = None

    # Double K Normalization Algorithm
    def __init__(self, k):
        self.K = k

    def calculate(self, term: Term, document: Document):
        max_freq_in_doc = getMaxFreqInDoc(document)
        return self.K + (1 - self.K) * (term.frequency / max_freq_in_doc)


# ---------------------------------------  IDF Algorithms --------------------------------------------
class OriginalIDF(IDFAbstract):
    # Original Algorithm
    def calculate(self, term: Term, document: Document):
        return getOrigIDF(term)


class DefaultIDF(IDFAbstract):
    # Default Algorithm
    def calculate(self, term: Term, document: Document):
        return log(getOrigIDF(term), 2)


class SmoothIDF(IDFAbstract):
    # Smooth Algorithm
    def calculate(self, term: Term, document: Document):
        return log(1 + getOrigIDF(term), 2)


class MaxFrequenceIDF(IDFAbstract):
    # Max Frenquence Algorithm
    def calculate(self, term: Term, document: Document):
        max_freq_in_doc = getMaxFreqInDoc(document)
        qtd_docs_term = DocumentTerm.objects.filter(term=term)
        return log(1 + max_freq_in_doc / qtd_docs_term, 2)


class ProbabilisticIDF(IDFAbstract):
    # Probabilistic Algorithm
    def calculate(self, term: Term, document: Document):
        qtd_docs = Document.objects.count()
        qtd_docs_term = DocumentTerm.objects.filter(term=term)
        return (qtd_docs - qtd_docs_term) / qtd_docs_term


def getOrigIDF(term: Term):
    # Algoritmo original de IDF
    qtd_docs = Document.objects.count()
    qtd_docs_term = DocumentTerm.objects.filter(term=term)
    return qtd_docs / qtd_docs_term


def getMaxFreqInDoc(document: Document):
    # Retorna a maior frequência dos termos em um documento
    return DocumentTerm.objects.filter(document=document).annotate(num_terms=Count('term')) \
        .aggregate(max=Max('num_terms'))