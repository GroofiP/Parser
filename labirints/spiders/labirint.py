import scrapy
from scrapy.http import HtmlResponse

from labirints.items import LabirintsItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Python/?stype=0']
    main_urls = "https://www.labirint.ru"

    def parse(self, response):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(f"{self.main_urls}{link}", callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        authors = response.xpath("//a[@data-event-label='author']/text()").getall()
        name = response.xpath("//div[@id='product-title']/h1/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        sale = response.xpath("//div[@id='product-left-column']//span[@class='action-label__text']/text()").get()
        url = response.url

        yield LabirintsItem(name=name, price=price, url=url, authors=authors, sale=sale, rating=rating)
