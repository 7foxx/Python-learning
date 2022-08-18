import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_02_crawlspider.items import Scrapy02CrawlspiderItem


class ReadSpider(CrawlSpider):
    name = 'read'
    allowed_domains = ['webstatic.mihoyo.com']
    start_urls = ['https://webstatic.mihoyo.com/upload/static-resource/2022/08/18/0e826fac53a9b4dab066d52796708cd7_5722391385935730073.mp4']

    rules = (
        # 注意这个 allow 会和 start_urls 进行匹配的所以 start_urls 一定要比对好
        Rule(LinkExtractor(allow=r'/book/1188_\d+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        pass

