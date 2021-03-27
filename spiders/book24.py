import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import time

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%9F%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[contains(@class,'book-preview__image-link')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        next_page = response.xpath("//div[@class='catalog-pagination__list']/a[last()]/@href").extract_first()  #
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").extract()
        book_link = response.url
        authors_name = response.xpath("//a[@itemprop='author']/text()").extract()
        currently_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        book_rating = response.xpath("//div[@class='rating__value-box']/div[1]/text()").extract_first()  # не работает
        #book_rating = response.css('div.live-lib__rate-value::text').extract_first()   не работает
        yield JobparserItem(book_name=book_name,book_link=book_link,authors_name=authors_name,currently_price=currently_price,old_price=old_price,book_rating=book_rating)

        print()