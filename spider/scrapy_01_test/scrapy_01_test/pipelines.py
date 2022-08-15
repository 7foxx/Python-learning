# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import urllib.request

from itemadapter import ItemAdapter


# 必须在setings中开启管道才能使用
class Scrapy01TestPipeline:
    # 在爬虫文件执行之前调用一次
    def __init__(self):
        self.fb = None
        self.initdata = []

    def open_spider(self, spider):
        pass

    # itme 就是在yield后面的对象
    def process_item(self, item, spider):
        self.initdata.append(item)
        return item

    # 在爬虫文件执行之后调用一次
    def close_spider(self, spider):
        # w 模式每次执行都会打开文件覆盖之前的内容
        self.fb = open('data.json', 'a', encoding='utf-8')
        # write 方法必须写一个字符串
        self.fb.write(str(self.initdata))
        # 关闭
        self.fb.close()


# 多管道开始
#    在 settings 中开启管道
#    'scrapy_01_test.pipelines.DownLoadYS': 301,
class DownLoadYS:
    # itme 就是在yield后面的对象
    def process_item(self, item, spider):
        url = item.get('src')
        filename = f'./img/{item.get("name")}.jpg'

        urllib.request.urlretrieve(url=url, filename=filename)

        return item
