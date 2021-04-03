from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruamerlen.spiders.merlen import MerlenSpider
from leruamerlen import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # input('')
    process.crawl(MerlenSpider, query='шурупы')

    process.start()