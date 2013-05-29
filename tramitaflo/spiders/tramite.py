# coding: utf-8
'''Crawler e parser para matérias em tramitação'''
import re
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from tramitaflo.items import TramitafloItemLoader


class TramiteSpider(CrawlSpider):
    '''Crawler para matérias em tramitação'''
    name = 'tramite'
    allowed_domains = ['200.19.214.5']
    start_urls = ['http://200.19.214.5/tramitacao.php']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'individual.php'),
             callback='parse_item', follow=True),
    )

    field_xpath = u'//td[text()="%s"]/following-sibling::td[1]/text()'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.parse_starter)

    def parse_starter(self, response):
        hxs = HtmlXPathSelector(response)

        keys = ['Ano', 'Assunto', 'SiglaProp', 'Status01', 'Status02',
                'CodProced', 'DepartCod', 'PropNum', 'Autor',
                'PropTramitando', 'DataInicial', 'DataFinal',
                'TipoApresentacao']
        data = {key: '' for key in keys}

        pager = hxs.select(u'string(//td[@class="lbPequeno"]'
                           u'[contains(., "Página")])').extract()[0]

        try:
            page = re.compile(r'\d+\s+de\s+(\d+)').search(pager).groups()[0]
        except AttributeError:
            page = 0

        for i in range(1, int(page)):
            data['Pagina'] = str(i)
            yield FormRequest(response.url, formdata=data)

        for req in self.parse(response):
            yield req

    def parse_item(self, response):
        loader = TramitafloItemLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_xpath(
            'tipo',
            (self.field_xpath[:-7] % u'Proposição') + u'//td[1]/text()')
        loader.add_xpath('proposicao', self.field_xpath % u'Número')
        loader.add_xpath('proponente', self.field_xpath % u'Proponente')
        loader.add_xpath('autor', self.field_xpath % u'Autor')
        loader.add_xpath('entrada', self.field_xpath % u'DataEntrada')
        loader.add_xpath('ementa', self.field_xpath % u'Ementa')
        return loader.load_item()
