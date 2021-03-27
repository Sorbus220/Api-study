import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F/?stype=0&page=1']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='cover']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()  #
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").extract_first()
        book_link = response.url
        authors_name = response.xpath("//div[@class='authors']/a/text()").extract()
        currently_price = response.xpath("//span[contains(@class,'buying-price-val-number')]/text() | //span[contains(@class,'buying-pricenew-val-number')]/text()").extract_first()
        old_price = response.xpath("//span[contains(@class,'buying-priceold-val-number')]/text()").extract_first()
        book_rating = response.xpath("//div[@id='rate']/text()").extract_first()
        yield JobparserItem(book_name=book_name,book_link=book_link,authors_name=authors_name,currently_price=currently_price,old_price=old_price,book_rating=book_rating)
        print()