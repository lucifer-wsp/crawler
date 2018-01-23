# -*- coding: utf-8 -*-
import scrapy


class A66ipSpider(scrapy.Spider):
    name = '66ip'
    allowed_domains = ['66ip.cn', 'chinaz.com']

    custom_settings = {
        'USE_PROXY': True,
        'DONT_RETRY': True,
        'MAX_RETRY_TIMES': 15,
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.5
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
        'Accept-Encoding': 'gzip, deflate', 
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive', 
        'Host': 'www.66ip.cn',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    cookies = {
    }
    
    def start_requests(self):
        start_urls = ['http://ip.filefab.com/index.php', 'http://ip.chinaz.com/getip.aspx']
        start_urls = ['http://www.66ip.cn/']
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
        try:
            ip_info_list = response.xpath('//table')
            request_url = response.meta.get('request_url')
            ip_list = []
            
            for ip_info in ip_info_list:
                ipinfo = ip_info.xpath('tr/td/text()').extract()
                for i in range(0, len(ipinfo), 5):
                    try:
                        ip = ipinfo[i:i+5][0].strip()
                        port = int(ipinfo[i:i+5][1].strip())
                        ip_list.append({'ip_addr': ip, 'port': port})
                    except Exception as e:
                        pass
            yield {'ip_info': ip_list}

            if '.html' not in request_url:
                page_count = self.get_page_count(response)
                for ind in range(page_count):
                    next_url = request_url + '%s.html'%(ind)
                    yield self.request(next_url, self.parse)
        except Exception as e:
            yield {}

    def get_page_count(self, response):
        page_info = response.xpath('//div[@class="mypage"]/div/div[@id="PageList"]/a/text()').extract()
        page_count = 1
        for page in page_info:
            try:
                if page_count < int(page):
                    page_count = int(page)
            except Exception as e:
                pass
        return page_count

        
