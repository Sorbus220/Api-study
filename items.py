# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def fix_url(value):
    if value:
        value = value.replace('w_82,h_82', 'w_2000,h_2000')
    return value


def fix_features(value):
    if value:
        value = value.replace('\n', '').replace('  ', '')
    return value


class LeruamerlenItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(fix_url))
    features_names = scrapy.Field(input_processor=MapCompose(fix_features))
    features = scrapy.Field(input_processor=MapCompose(fix_features))
