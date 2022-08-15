import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_02_crawlspider.items import Scrapy02CrawlspiderItem


class ReadSpider(CrawlSpider):
    name = 'read'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1188_1.html']

    rules = (
        # 注意这个 allow 会和 start_urls 进行匹配的所以 start_urls 一定要比对好
        Rule(LinkExtractor(allow=r'/book/1188_\d+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        list_li = response.xpath('/html/body/div[6]/div/div[2]/div[2]/ul/li')

        for li in list_li:
            src = li.xpath('.//div/div/a/img/@data-original').extract_first()
            if src is None:
                src = li.xpath('.//div/div/a/img/@src').extract_first()
            name = li.xpath('.//div/div/a/img/@alt').extract_first()

            data = Scrapy02CrawlspiderItem(src=src, name=name)
            yield data
