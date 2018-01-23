# -*- coding: utf-8 -*-
import scrapy


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    custom_settings = {
        'DONWLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.5
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.kuaidaili.com',
        'Referer': 'https://www.kuaidaili.com/free/intr/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cookies = {}
    
    def start_requests(self):
        start_urls = ['https://www.kuaidaili.com/free/inha/',
                  'https://www.kuaidaili.com/free/intr/']

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
        data_info = response.xpath('//div[@id="list"]/table/tbody/tr')
        
        for data in data_info:
            ip_info = {}
            dt = data.xpath('./td/text()').extract()
            if dt and len(dt) > 4:
                ip_info['ip_addr'] = dt[0]
                ip_info['port'] = dt[1]
                if 'http' == dt[3].lower():
                    ip_info['protocol'] = 1 
                elif 'https' == dt[3].lower():
                    ip_info['protocol'] = 2
                else:
                    continue
                ip_data['ip_info'].append(ip_info)
        yield ip_data
 
        if 'inha/' == request_url[-5:] or 'intr/' == request_url[-5:]:
            page_count = self.get_page_count(response)
            for ind in range(2, page_count):
                next_url = request_url + '%s/'%(ind)
                yield self.request(next_url, self.parse)

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
