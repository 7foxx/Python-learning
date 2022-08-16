# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from urllib.request import urlretrieve


class ScrapyYysPipeline:
    def process_item(self, item, spider):
        name = item.get("name")
        path = f'../img/{name}'
        # 判断目录是否存在
        if os.path.exists(path) is False:
            # 不存在泽创建目录
            os.makedirs(path)
        # 下载icon头像
        urlretrieve(item.get("iconUrl"), f'{path}/icon_{name}.png')
        # 下载例会
        urlretrieve(item.get("subjectImg"), f'{path}/{name}.png')
        return item
