# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import HtmlResponse

class LeruamerlenPipeline:
    def process_item(self, item, spider):
        item['price'] = int(item['price'])
        item['features'] = dict(zip(item['features_names'], item['features']))
        del item['features_names']
        print()
        return item


class MNPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        file_dir = item['name']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{file_dir}]/{image_guid}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
