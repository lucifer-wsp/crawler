# -*- coding: utf-8 -*-
import scrapy


class HttpsdailiSpider(scrapy.Spider):
    name = 'httpsdaili'
    allowed_domains = ['httpsdaili.com']

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.5,
    }
    headers = {}
    cookies = {}
        
    def start_requests(self):
        start_urls = ['http://httpsdaili.com/free.asp',
                      'http://httpsdaili.com/free.asp?stype=2',
                      'http://httpsdaili.com/free.asp?stype=3',
                      'http://httpsdaili.com/free.asp?stype=4']
        for url in start_urls:
            yield self.request(url, self.parse)

    def request(self, url, callback, meta={}):
        meta['request_url'] = url
        meta['dont_retry'] = True
        return scrapy.Request(url=url,
                            callback=callback,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta=meta)

    def parse(self, response):
        ip_data = {'ip_info': []}
        request_url = response.meta.get('request_url')
        res_info = response.xpath('//div[@id="list"]/table/tbody/tr')
        
        for res in res_info:
            ip_info = {}
            data = res.xpath('./td/text()').extract()
            if data and len(data) > 4:
                ip_info['ip_addr'] = data[0] 
                ip_info['port'] = data[1] 
                if data[3].lower() == 'http':
                    ip_info['protocol'] = 1
                elif data[3].lower() == 'https':
                    ip_info['protocol'] = 2
                else:
                    continue
                ip_data['ip_info'].append(ip_info)
        yield ip_data

        if 'page=' not in request_url:
            page_count = self.get_page_count(response)
            for ind in range(2, page_count):
                if request_url[-4:]  == '.asp':
                    next_url = request_url + '?page=%s'%(ind)
                else:
                    next_url = request_url + '&page=%s'%(ind)
                yield self.request(next_url, self.parse)

    def get_page_count(self, response):
        page_count = 1
        page_info = response.xpath('//div[@id="listnav"]//strong/text()').extract()
        for page in page_info:
            try:
                if page_count < int(page.strip()[1:]):
                    page_count = int(page.strip()[1:])
            except Exception as e:
                pass
        return page_count






