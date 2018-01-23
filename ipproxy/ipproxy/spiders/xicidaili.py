# -*- coding: utf-8 -*-
import scrapy


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'DOWNLOAD_TIMEOUT': 30
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.xicidaili.com',
        'Upgrade-Insecure-Requests': 1,
        'Cache-Control': 'max-age=0',
        'If-None-Match': 'W/"89d9a023dde43b372f411b0b8c5af520"',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cookies = {
    }

    def start_requests(self):
        start_urls = ['http://www.xicidaili.com/wn/', 
                      'http://www.xicidaili.com/wt/']
        for url in start_urls:
            yield self.request(url, self.parse)
            break

    def request(self, url, call_back, meta={}):
        meta['request_url'] = url
        return scrapy.Request(url=url,
                            callback=call_back,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta=meta)

    def parse(self, response):
        data = {'ip_info': []}
        request_url = response.meta.get('request_url')
        res_info = response.xpath('//table[@id="ip_list"]/tr')
        for r in res_info[1:]:
            if not r:
                continue
            data_info = r.xpath('.//td/text()').extract()
            ip_info = {}
            if len(data_info) > 5:
                ip_info['ip_addr'] = data_info[0]
                ip_info['port'] = data_info[1]
                ip_info['ip'] = 1 if data_info[4].lower() == 'http' else 2
                data['ip_info'].append(ip_info)
        yield data

        if False and request_url[-3] == 'w':
            page_count = self.get_page_count(response)
            for pind in range(2, page_count):
                next_url = request_url + str(pind)
                print(next_url)
                yield self.request(next_url, self.parse)

    def get_page_count(self, response):
        page_count = 1
        page_info = response.xpath('//div[@class="pagination"]/a/text()').extract()
        for page in page_info:
            try:
                if int(page.strip()) > page_count:
                    page_count = int(page.strip())
            except Exception as e:
                pass
        return page_count
