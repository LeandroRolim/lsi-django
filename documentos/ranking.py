from abc import ABCMeta, abstractmethod

from django.db.models import Count, Max

from documentos.models import *
from math import log


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
        return 1 + log(term.frequency)


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
        return log(getOrigIDF(term))
      

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
