# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    book_name = scrapy.Field()
    book_link = scrapy.Field()
    authors_name = scrapy.Field()
    currently_price = scrapy.Field()
    old_price = scrapy.Field()
    book_rating = scrapy.Field()
    _id = scrapy.Field()




