# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from time import sleep

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ScrapyYysSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyYysDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        # 在 DownloaderMiddleware 中更改 process_request 返回的 response 对象
        # 通过 webdriver 构建的 driver 对象去请求js渲染后的页面
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument("no-sandbox")  # 取消沙盒模式
        options.add_argument("disable-blink-features=AutomationControlled")  # 禁用启用Blink运行时的功能
        options.add_experimental_option('excludeSwitches', ['enable-automation'])    # 开发者模式

        # executable_path 是你的 selenium 调试工具的路径
        # win
        # executable_path = "D:\peak\Python\\xuexi\spider\scrapy_yys\chromedriver_win.exe"
        # M1
        executable_path = '/Users/mulin/Code/Python/learning/Python-learning/spider/scrapy_yys/chromedriver'
        driver = webdriver.Chrome(executable_path=executable_path, options=options)
        # 移除 `window.navigator.webdriver`. scrapy 默认为True
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #              Object.defineProperty(navigator, 'webdriver', {
        #                get: () =&gt; undefined
        #              })
        #            """
        # })

        driver.get(request.url)
        # driver.implicitly_wait(5)
        sleep(0.5)
        content = driver.page_source
        # 关闭 webdriver
        # driver.quit()
        # print('关闭 webdriver')
        request.meta["driver"] = driver

        # 引入 HtmlResponse 函数来重新返回 response 对象
        return HtmlResponse(url=request.url, body=content, request=request, encoding='utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
