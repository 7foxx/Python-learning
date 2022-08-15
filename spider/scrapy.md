# scrapy

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

### Mac OS 安装方式**

对于Mac OS系统来说，由于系统本身会引用自带的python2.x的库，因此默认安装的包是不能被删除的，但是你用python2.x来安装Scrapy会报错，用python3.x来安装也是报错，我最终没有找到直接安装Scrapy的方法，所以我用另一种安装方式来说一下安装步骤，解决的方式是就是使用virtualenv来安装。

```sh
$ sudo pip install virtualenv
$ virtualenv scrapyenv
$ cd scrapyenv
$ source bin/activate
$ pip install Scrapy
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



