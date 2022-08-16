from urllib.parse import urlencode

import scrapy
from selenium import webdriver

from scrapy_yys.items import ScrapyYysItem


class YysSpider(scrapy.Spider):
    name = 'yys'
    allowed_domains = ['act.ds.163.com']
    start_urls = ['http://act.ds.163.com/41bab2a03a354547/']

    def parse(self, response):
        div_list = response.xpath('//*[@id="root"]/div/div')
        # 删除前两个元素
        div_list.pop(0)
        div_list.pop(0)
        for li in [div_list[3], div_list[4]]:
            # 名称
            name = li.xpath('.//div/div[2]/div/span[1]/text()').extract_first()
            CV = li.xpath('.//div/div[2]/div/span[2]/text()').extract_first()
            quality = li.xpath('.//div/div[2]/div/i[1]//@class').extract_first().split('___')[0].replace('quality', '')
            positioning = li.xpath('.//div/div[2]/p/text()').extract_first()
            iconUrl = li.xpath('.//div/div[1]/img//@src').extract_first()

            # 式神详细信息
            url = f'https://act.ds.163.com/41bab2a03a354547/item-detail?{urlencode({"id": name})}'

            yield scrapy.Request(url=url, callback=self.parse_item, meta={
                'name': name,
                'CV': CV,
                'quality': quality,
                'positioning': positioning,
                'iconUrl': iconUrl
            })

    def parse_item(self, response):
        print(response.meta)
        # 例会
        subjectImg = response.xpath('//*[@id="root"]/div/div[1]/div[1]/div[2]/img//@src').extract_first()

        # 属性
        AttributeData = []
        eleData = response.xpath('//*[@id="root"]/div/div[1]/div[1]/div[1]/ul/li')
        for li in eleData:
            key = li.xpath('.//*[@class="leftFeature___3fDr2"]/text()').extract_first()
            value1 = li.xpath('.//*[@class="rightFeature___1uJ5q"]/text()[1]').extract_first()
            value2 = li.xpath('.//*[@class="rightFeature___1uJ5q"]/text()[2]').extract_first()
            AttributeData.append({
                key: [value1, value2.strip()]
            })
        # 属性评级
        eleDataQua = response.xpath('//*[@id="root"]/div/div[1]/div[2]/div/div')
        for i, li in enumerate(eleDataQua):
            val1 = li.xpath('.//span[2]/@class').extract_first().split('___')[0].replace('level', '')
            val2 = li.xpath('.//span[4]/@class').extract_first().split('___')[0].replace('level', '')
            AttributeData[i]['quality'] = [val1, val2]



        yield ScrapyYysItem(
            name=response.meta['name'],
            CV=response.meta['CV'],
            quality=response.meta['quality'],
            positioning=response.meta['positioning'],
            iconUrl=response.meta['iconUrl'],
            subjectImg=subjectImg,
            AttributeData=AttributeData
        )

    def close(self, reason):
        pass
