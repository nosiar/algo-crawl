from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from algospot.items import AlgospotItem

class AlgospotSpider(Spider):
    name = 'algospot'
    allowed_domains = ['algospot.com']
    start_urls = ['https://algospot.com/judge/problem/list/']

    def parse(self, response):
        sel = Selector(response)
        last_page = sel.xpath('//span[@class="step-links"]/a/text()')[-1].extract()
        
        for i in range(1, int(last_page) + 1):
            url = 'https://algospot.com/judge/problem/list/' + str(i)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        sel = Selector(response)
        uids = sel.xpath('//table[@class="problem_list"]'
                          '/tbody/tr/td[2]/a/text()')

        for uid in uids:
            url = 'https://algospot.com/judge/problem/read/' + uid.extract()
            yield Request(url, callback=self.parse_problem)

    def parse_problem(self, response):
        sel = Selector(response)
        item = AlgospotItem()
        item['uid'] = sel.xpath('//li[@class="problem-id"]/a/text()').extract()
        item['name'] = sel.xpath('//header/h2/text()').extract()
        item['submitted'] = sel.xpath('//li[@class="submissions"]/a/b/text()').extract()
        item['accepted'] = sel.xpath('//li[@class="accepted"]/a/b/text()[1]').extract()
        item['source'] = sel.xpath('//li[@class="source"]/a/text()').extract()
        item['category'] = sel.xpath('//span[@id="problem_category"]/a/text()').extract()
        yield item

