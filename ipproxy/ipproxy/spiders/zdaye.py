# -*- coding: utf-8 -*-
import scrapy


class ZdayeSpider(scrapy.Spider):
    name = 'zdaye'
    allowed_domains = ['ip.zdaye.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'DOWNLOAD_TIMEOUT': 30
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'ip.zdaye.com',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cookies = {
    }

    def start_requests(self):
        start_urls = ['http://ip.zdaye.com/dayProxy.html']
        for url in start_urls:
            yield self.request(url, self.parse_list)

    def request(self, url, call_back, meta={}):
        meta['request_url'] = url
        return scrapy.Request(url=url,
                            callback=call_back,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta=meta)

    def parse_list(self, response):
        proxy_list = response.xpath("//div[@class='table table-hover panel-default panel ips ']/div[@class=\"title\"]/a/@href").extract()
        print(proxy_list)
        for url in proxy_list:
            page_url = 'http://ip.zdaye.com' + url.strip()
            print(page_url)
            yield self.request(page_url, self.parse)
            break
        
    def parse(self, response):
        data_info = response.xpath("//div[@class='alert fade in alert-warning']/div/text()").extract()
        for data in data_info:
            print(data)


       
