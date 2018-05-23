# from scrapy import CrawlSpider
# from selenium import webdriver
# import time
#
# class FooSpider(CrawlSpider):
#     name = 'foo'
#     allow_domains = 'foo.com'
#     start_urls = ['foo.com']
#
#     def __init__(self, *args, **kwargs):
#         super(FooSpider, self).__init__(*args, **kwargs)
#         self.download_delay = 0.25
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(60)
#
#     def parse_foo(self.response):
#         self.browser.get(response.url)  # load response to the browser
#         button = self.browser.find_element_by_xpath("path") # find
#         # the element to click to
#         button.click() # click
#         time.sleep(1) # wait until the page is fully loaded
#         source = self.browser.page_source # get source of the loaded page
#         sel = Selector(text=source) # create a Selector object
#         data = sel.xpath('path/to/the/data') # select data
#         ...

import scrapy
from selenium import webdriver

class product_spiderItem(scrapy.Item):
    title = scrapy.Field()
    price=scrapy.Field()
    pass

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_odkw=books&_osacat=0&_trksid=p2045573.m570.l1313.TR0.TRC0.Xpython&_nkw=python&_sacat=0&_from=R40']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)

        while True:

            sel = scrapy.Selector(text=self.driver.page_source)

            for prod in sel.xpath('//ul[@id="GalleryViewInner"]/li/div/div'):
                item = product_spiderItem()
                item['title'] = prod.xpath('.//div[@class="gvtitle"]/h3/a/text()').extract()
                item['price'] = prod.xpath('.//div[@class="prices"]//span[@class=" bold"]/text()').extract()
                yield item

            next = self.driver.find_element_by_xpath('//td[@class="pagn-next"]/a')

            try:
                next.click()

            except:
                break

    def closed(self, reason):
        self.driver.close()