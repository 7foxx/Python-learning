# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from urllib.request import urlretrieve


class ScrapyYysPipeline:
    def __init__(self):
        self.fb = None

    def open_spider(self,spider):
        # w 模式每次执行都会打开文件覆盖之前的内容
        self.fb = open('data.json', 'a', encoding='utf-8')
        self.fb.write("[")

    def process_item(self, item, spider):
        name = item.get("name")
        path = f'../img/{name}'
        # 判断目录是否存在
        if os.path.exists(path) is False:
            # 不存在泽创建目录
            os.makedirs(path)
        # 下载icon头像
        urlretrieve(item["imgUrl"]["icon_1"], f'{path}/icon_1_{name}.png')
        urlretrieve(item["imgUrl"]["icon_2"], f'{path}/icon_2_{name}.png')
        # 下载例会
        urlretrieve(item["imgUrl"]["subjectImg"], f'{path}/max_1_{name}.png')
        # 下载技能
        for v in item["imgUrl"]["skillIconArr"]: urlretrieve(v[1], f'{path}/{v[0]}.png')
        # 删除imgUrl
        del item["imgUrl"]
        # write 方法必须写一个字符串
        self.fb.write(','+str(item))
        return item

    def close_spider(self,spider):
        self.fb.write("]")
        # 关闭
        self.fb.close()