# coding: utf-8
'''Items para matérias em tramitação na câmara'''
from calendar import timegm
from datetime import datetime
from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst


class TramitafloItem(Item):
    '''Matérias em tramitação'''
    proposicao = Field()
    tipo = Field()
    url = Field()
    entrada = Field()
    proponente = Field()
    autor = Field()
    ementa = Field()
    documento = Field()


class TramitaParseDate(object):
    def __call__(self, values):
        for datestamp in values:
            yield timegm(datetime.strptime(datestamp, '%d/%m/%Y').utctimetuple())


class TramitafloItemLoader(XPathItemLoader):
    '''Loader para matérias em transitação'''
    default_item_class = TramitafloItem
    default_output_processor = TakeFirst()
    entrada_in = TramitaParseDate()
