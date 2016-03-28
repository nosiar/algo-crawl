import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader
from algospot.items import User


class UserSpider(scrapy.Spider):

    def __init__(self, uid):
        self.uid = str(uid)
        self.start_urls = ['https://algospot.com/newsfeed/user/' + self.uid]

    name = 'user'
    allowed_domains = ['algospot.com']
    count = 0

    def parse(self, response):
        sel = Selector(response)
        last_page = sel.xpath('//span[@class="step-links"]/a/text()')[-1].extract()
        self.num_page = int(last_page)

        loader = ItemLoader(item=User(), response=response)
        loader.add_value('uid', self.uid)
        loader.add_xpath('name', '//a[@class="username"]/text()')

        for i in range(1, self.num_page + 1):
            url = self.start_urls[0] + '/' + str(i)
            yield Request(url,
                          callback=self.parse_list,
                          meta={'loader': loader})

    def parse_list(self, response):
        loader = response.meta['loader']
        sel = Selector(response)
        keywords = sel.xpath('//li[@class="judge"]/p/a/text()')
        keywords = [keyword.extract() for keyword in keywords]
        loader.add_value('problems', keywords)

        self.count += 1
        if self.count == self.num_page:
            yield loader.load_item()
