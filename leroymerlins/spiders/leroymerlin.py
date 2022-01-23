import scrapy

from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlins.items import LeroymerlinsItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/tiski/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinsItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']//meta[@itemprop='price']/@content")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_value('url', response.url)
        yield loader.load_item()
