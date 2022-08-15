import scrapy
from scrapy_01_test.items import Scrapy01TestItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['bbs.mihoyo.com']
    start_urls = ['https://bbs.mihoyo.com/ys/obc/channel/map/189/25?bbs_presentation_style=no_header']

    def parse(self, response):
        ul = response.xpath('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a')
        for li in ul:
            href = li.xpath('@href').extract_first()
            name = li.xpath('.//div[2]/text()').extract_first()

            # 调用Scrapy01TestItem将数据存储中目标文件中
            # data = Scrapy01TestItem(href=href, name=name)

            # 第二页的地址
            url = 'https://bbs.mihoyo.com' + href

            yield scrapy.Request(url, callback=self.parse_second, meta={
                'href': href,
                'name': name
            })

            # 每次循环得到的结果交给管道，如果是多个管道链接调用泽在最后一个执行的管道中 yield 最终的数据
            # yield data

    def parse_second(self, response):
        src = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[3]/div[1]/div[1]/div/ul[2]/li/img/@src').extract_first()
        name = response.meta['name']
        href = response.meta['href']

        # 调用Scrapy01TestItem将数据存储中目标文件中
        data = Scrapy01TestItem(src=src, href=href, name=name)
        # 每次循环得到的结果交给管道，如果是多个管道链接调用泽在最后一个执行的管道中 yield 最终的数据
        yield data
