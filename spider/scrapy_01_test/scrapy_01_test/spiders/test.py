import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['bbs.mihoyo.com/ys/obc/channel/map/189/25?bbs_presentation_style=no_header']
    start_urls = ['https://bbs.mihoyo.com/ys/obc/channel/map/189/25?bbs_presentation_style=no_header']

    def parse(self, response):
        ul = response.xpath('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a')
        for li in ul:
            href = li.xpath('@href').extract_first()
            src = li.xpath('.//div/@data-src').extract_first()
            print(src)