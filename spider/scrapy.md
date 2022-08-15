# rscrapy

## 安装

### Windows 安装方式

升级 pip 版本：

```sh
pip install --upgrade pip
```

通过 pip 安装 Scrapy 框架:

```sh
pip install Scrapy
```

### Ubuntu 安装方式

安装非 Python 的依赖:

```sh
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
```

通过 pip 安装 Scrapy 框架：

```sh
sudo pip install scrapy
```

### Mac OS 安装方式

pip版本必须转22+，升级pip版本

```
 pip3 install --upgrade pip
```

使用清华源下载

```sh
 pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scrapy 
```

> 注意：在mac中使用 scrapy 指令必须在前面加上 python3 -m

```
python3 -m scrapy
```

## 新建项目

在开始爬取之前，必须创建一个新的Scrapy项目。进入自定义的项目目录中，运行下列命令：

```sh
scrapy startproject mySpider
```

其中， mySpider 为项目名称，可以看到将会创建一个 mySpider 文件夹，目录结构大致如下：

下面来简单介绍一下各个主要文件的作用：

```py
mySpider/
    scrapy.cfg
    mySpider/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```

这些文件分别是:

- scrapy.cfg: 项目的配置文件。
- mySpider/: 项目的Python模块，将会从这里引用代码。
- mySpider/items.py: 项目的目标文件。
- mySpider/pipelines.py: 项目的管道文件。
- mySpider/settings.py: 项目的设置文件。
- mySpider/spiders/: 存储爬虫代码目录。

### 创建爬虫文件

1、cd 进入 `spiders` 文件夹中

```sh
cd mySpider\spiders\spiders
```

2、创建爬虫文件

```sh
# scrapy genspider 文件名  网页地址
scrapy genspider test www.baidu.com
```

3、`test.py`

```py
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        pass
```

### 运行爬虫代码

```sh
scrapy crawl 爬虫文件名
```

> 注意：有的网站会有 robots 协议，这是一个君子协议，scrapy 默认是启动遵守的，如果想要爬取需要关闭

在`settings.py`文件中

```
# Obey robots.txt rules
ROBOTSTXT_OBEY = True 注释该行
```

## 语法

### response对象

**解析数据返回的对象**

- `response.body` ：响应返回页面已二进制格式的内容
- `response.text` ：响应返回页面已字符串格式的内容
- `response.url` ：响应返回页面url
- `response.status` ：响应返回ajax请求状态码

- `response.xpath()`：（常用） 使用xpath路径查询特定元素，返回一个`selector`列表对象 
- `response.css()`：使用`css_selector`查询元素，返回一个`selector`列表对象 
  - 获取内容 ：`response.css('#su::text').extract_first()` 
  - 获取属性 ：`response.css('#su::attr(“value”)').extract_first()` 

### selector对象

> 通过`xpath`方法调用返回的是`seletor`列表

#### extract() 

- 提取`selector`对象的值 
- 如果提取不到值，那么会报错 
- 使用xpath请求到的对象是一个`selector`对象，需要进一步使用`extract()`方法拆 包，转换为`unicode`字符串 

#### extract_first() 

- 提取`seletor`列表中的第一个值 
- 如果提取不到值，会返回一个空值 
- 返回第一个解析到的值，如果列表为空，此种方法也不会报错，会返回一个空值 `xpath() css()`

> 注意：每一个`selector`对象可以再次的去使用`xpath`或者`css`方法

## 使用管道封装

1、items.py 在项目目标文件中定义

```py
class Scrapy01TestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # src = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
```

2、爬虫住文件

```py
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
```

3、在`settings.py`中开启管道

```py
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 管道可以有多个
   # scrapy_01_test.pipelines.Scrapy01TestPipeline 管道的类名路径
   # 300 是管道的优先级，范围1-1000，值越小优先级越高
   'scrapy_01_test.pipelines.Scrapy01TestPipeline': 300,
}
```

4、pipelines.py 管道文件

```py
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
```

5、items 目标文件

```py
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy01TestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    src = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
```

