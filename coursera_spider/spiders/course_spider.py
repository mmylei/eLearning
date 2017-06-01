from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from coursera_spider.items import *


class CourseraCourseSpider(CrawlSpider):
    name = 'course'
    allowed_domains = ['www.coursera.org']
    start_urls = ['https://www.coursera.org/courses?_facet_changed_=true&domains=computer-science&languages=en&query=hkust']
    rules = (
        Rule(LinkExtractor(allow=(r'www\.coursera\.org/learn/',)), callback='parse_page'),
    )

    def __init__(self):
        CrawlSpider.__init__(self)

    def parse_page(self, response):
        self.logger.info('crawled page: %s', response.url)
        item = CourseraCourseItem()
        item['course_name'] = response.xpath('//div[@id="rendered-content"]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/h1/text()').extract()[0].strip()
        table_rows = response.xpath('//*[@id=" "]/div/div[4]/table/tbody//tr')
        for tr in table_rows:
            temp = tr.xpath('td[1]/span/text()').extract()
            self.logger.debug(str(temp))
            left = tr.xpath('td[1]/span/text()').extract()[0].strip()
            if left == 'Level':
                item['level'] = tr.xpath('td[2]/text()').extract()[0].strip()
            if left == 'User Ratings':
                item['rating'] = tr.xpath('td[2]/div/div[2]/text()').extract()[0].strip()
        item['instructor'] = response.xpath('//*[@id=" "]/div/div[3]/ul/li/div/div/div[2]/p/span/a/text()').extract()[0].strip()
        return item
