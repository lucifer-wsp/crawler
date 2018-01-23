# -*- coding: utf-8 -*-
import scrapy


class NianshaoSpider(scrapy.Spider):
    name = 'nianshao'
    allowed_domains = ['nianshao.me']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'RETRY_ENABLED': False,
        'DOWNLOAD_DELAY': 0.3
    }
    
    headers = {}
    cookies = {}

    def start_requests(self):
        start_urls = ['http://www.nianshao.me/?stype=1',
                      'http://www.nianshao.me/?stype=2',
                      'http://www.nianshao.me/?stype=5']
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
        res_info = response.xpath('//table[@class="table"]/tbody/tr')
        for res in res_info:
            ip_info = {}
            data = res.xpath('./td/text()').extract()
            if data and len(data) > 5:
                ip_info['ip_addr'] = data[0]
                ip_info['port'] = data[1]
                if 'http' == data[4].lower():
                    ip_info['protocol'] = 1
                elif 'https' == data[4].lower():
                    ip_info['protocol'] = 2
                else:
                    continue
                ip_data['ip_info'].append(ip_info)
        yield ip_data

        if '&page=' not in request_url:
            page_count = self.get_page_count(response)
            for ind in range(2, page_count):
                next_url = request_url + '&page=%s'%(ind)
                yield self.request(next_url,  self.parse)

    def get_page_count(self, response):
        page_count = 1
        page_info = response.xpath('//div[@id="listnav"]//a/text()').extract()
        for page in page_info:
            try:
                if page_count < int(page.strip()):
                    page_count = int(page.strip())
            except Exception as e:
                pass
        return page_count
