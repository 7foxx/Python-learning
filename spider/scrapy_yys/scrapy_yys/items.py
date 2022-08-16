# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyYysItem(scrapy.Item):
    # define the fields for your item here like:
    # 名字
    name = scrapy.Field()
    # 声优
    CV = scrapy.Field()
    # 稀有度
    quality = scrapy.Field()
    # 定位
    positioning = scrapy.Field()
    # 头像
    iconUrl = scrapy.Field()
    # 觉醒前例会图
    subjectImg = scrapy.Field()
    # 属性述职
    AttributeData = scrapy.Field()
