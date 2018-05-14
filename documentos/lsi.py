import nltk
import codecs
import pytesseract
import zipfile

from bs4 import BeautifulSoup
from PIL import Image
from tika import parser

from abc import ABCMeta, abstractmethod


class DocumentAbstract(metaclass=ABCMeta):

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
        tokens = nltk.word_tokenize(self.soup.get_text())
        return list(map(lambda word: word, tokens))
        # return list(map(lambda word: Term(word=str(word), frequency=1), tokens))

    def get_title(self):
        return self.soup.title.string


class PDF(DocumentAbstract):
    raw = None

    def __init__(self, path):
        with codecs.open(path, 'r') as arq:
            self.raw = parser.from_file(arq)

    def get_words(self):
        tokens = nltk.word_tokenize(self.raw.get_text())
        return list(map(lambda word: word, tokens))
        # return list(map(lambda term: Term(word=str(term)), tokens))

    def get_title(self):
        return self.raw.title.string if self.raw.title is not None else 'sem titulo'


class OCR(DocumentAbstract):
    img=None

    def __init__(self, path):
        self.img = Image.open('download.jpg')

    def get_words(self):
        text = pytesseract.image_to_string(self.img, lang='por')
        tokens = nltk.word_tokenize(text)
        return list(map(lambda word: word, tokens))
        # return list(map(lambda word: Word(word=str(word)), texto))

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
        tokens = nltk.word_tokenize(self.soup.get_text())
        return list(map(lambda word: word, tokens))
        # return list(map(lambda word: Word(word=str(word)), tokens))

    def get_title(self):
        return self.soup.title.string if self.soup.title is not None else 'sem titulo'