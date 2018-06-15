import nltk
import codecs
import zipfile

import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
from tika import parser

from abc import ABCMeta, abstractmethod
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os


def remove_stopwords(list_terms):
    stopWords = set(stopwords.words('portuguese'))
    return list(filter(lambda w: w not in stopWords, list_terms))


def remove_adverb_verb(list_terms):
    with codecs.open('files/adverbs.txt') as arq:
        adverbs = nltk.word_tokenize(arq.read())
        return list(filter(lambda term: term not in adverbs, list_terms))


class DocumentAbstract(metaclass=ABCMeta):
    tokenizer = RegexpTokenizer(r'\w+')

    """recebe path, que é o caminha para o documento
    def __init__(self, path):
        pass"""

    """ deve retornar um lista com todas as palavras encontradas"""
    @abstractmethod
    def get_words(self):
        return []

    """deve retorna uma string com o titulo do documento caso exista"""
    @abstractmethod
    def get_title(self):
        return u''


class Html(DocumentAbstract):
    soup=None

    def __init__(self, path):
        with codecs.open(path, 'r') as arq:
            html = arq.read()
            self.soup = BeautifulSoup(html, 'lxml')

    def get_words(self):
        return list(self.tokenizer.tokenize(self.soup.get_text()))

    def get_title(self):
        return self.soup.title.string


class PDF(DocumentAbstract):
    raw = None

    def __init__(self, path):
        with codecs.open(path, 'r') as arq:
            self.raw = parser.from_file(arq)

    def get_words(self):
        return self.tokenizer.tokenize(self.raw.get_text())


    def get_title(self):
        return self.raw.title.string if self.raw.title is not None else 'sem titulo'


class OCR(DocumentAbstract):
    img=None

    def __init__(self, path):
        self.img = Image.open(path)

    def get_words(self):
        text = pytesseract.image_to_string(self.img)
        return self.tokenizer.tokenize(text)

    def get_title(self):
        return 'sem titulo'


class Docx(DocumentAbstract):
    soup=None

    def __init__(self, path):
        with codecs.open(path, 'r') as arq:
            with zipfile.ZipFile(arq.name, 'r') as zfp:
                doc=codecs.open('word/document.xml', 'r')
                self.soup= BeautifulSoup(doc.read(), 'xml')

    def get_words(self):
        return self.tokenizer.tokenize(self.soup.get_text())

    def get_title(self):
        return self.soup.title.string if self.soup.title is not None else 'sem titulo'


class DocumentFactory:
    @staticmethod
    def getFactory(file):
        name, extension = os.path.splitext(file.name)
        if extension == '.html':
            return Html(file.url)
        elif extension == '.pdf':
            return PDF(file.url)
        elif extension == '.docx':
            return Docx(file.url)
        elif extension in ['.png', '.jpeg']:
            return OCR(file.url)
        else:
            raise Exception(file)