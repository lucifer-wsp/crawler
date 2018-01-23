# -*- coding: utf-8 -*-
import scrapy


class GoubanjiaSpider(scrapy.Spider):
    name = 'goubanjia'
    allowed_domains = ['goubanjia.com']
    custom_settings = {
        'donwload_timeout': 30,
        'download_delay': 0.2,

    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.goubanjia.com',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cookies = {}

    def start_requests(self):
        start_urls = ['http://www.goubanjia.com/free/index.shtml']
        for url in start_urls:
            yield self.request(url, self.parse)

    def request(self, url, call_back, meta={}):
        meta['request_url'] = url
        return scrapy.Request(url=url,
                            callback=call_back,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta=meta)

    def parse(self, response):
        print(response.text)
        res_info = response.xpath('//div[@class="entry entry-content"]//tbody/tr/td[@class="ip"]/span/text()|//div[@class="entry entry-content"]//tbody/tr/td[@class="ip"]/div/text()').extract()
        for r in res_info:
            print(r)




