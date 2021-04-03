import scrapy
from scrapy.http import HtmlResponse
from leruamerlen.items import LeruamerlenItem
from scrapy.loader import ItemLoader


class MerlenSpider(scrapy.Spider):
    name = 'merlen'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D1%88%D1%83%D1%80%D1%83%D0%BF%D1%8B']

    def __init__(self, query):
        super(MerlenSpider, self).__init__()

        self.start_urls = [f'https://leroymerlin.ru/search/?sortby=3591&page=1&tab=products&q={query}']

    def parse(self, response: HtmlResponse):
        good_links = response.xpath("//a[@class='plp-item__info__title']")
        for link in good_links:
            yield response.follow(link, callback=self.parse_good)
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()  #
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruamerlenItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_xpath('features_names', "//div[@class='def-list__group']//dt/text()")
        loader.add_xpath('features', "//div[@class='def-list__group']//dd/text()")
        yield loader.load_item()
