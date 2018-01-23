# -*- coding: utf-8 -*-
import scrapy


class Ip3366Spider(scrapy.Spider):
    name = 'ip3366'
    allowed_domains = ['ip3366.net']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.6
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.ip3366.net',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cookies = {}

    def start_requests(self):
        start_urls = ['http://www.ip3366.net/free/?stype=1',
                      'http://www.ip3366.net/free/?stype=2',
                      'http://www.ip3366.net/free/?stype=3',
                      'http://www.ip3366.net/free/?stype=4']
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
            if dt and len(dt) >= 4:
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

        if '&page=' not in request_url:
            page_count = self.get_page_count(response)
            for ind in range(2, page_count):
                next_url = request_url + '&page=%s'%(ind)
                yield self.request(next_url, self.parse)

    def get_page_count(self, response):
        page_count = 1
        page_data = response.xpath('//div[@id="listnav"]/ul/a/text()').extract()
        for data in page_data:
            try:
                if page_count < int(data.strip()):
                    page_count = int(data.strip())
            except Exception as e:
                pass
        
        return page_count

