# -*- coding: utf-8 -*-
import scrapy
import pymysql
import time

class CheckIpSpider(scrapy.Spider):
    name = 'check_ip'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'max_retry_times': 0
    }
    headers = {}
    cookies = {}

    allowed_domains = ['s.taobao.com', 'ip.filefab.com']

    def start_requests(self):
        start_urls = 'https://s.taobao.com/search?data-key=s&data-value=0&ajax=true&_ksTS=%s_1529&callback=jsonp1530'
        #start_urls = 'http://ip.filefab.com/index.php'
        db_conn = pymysql.connect(host='localhost',
                                user='root',
                                passwd='reload123',
                                db='proxy',
                                charset='utf8')
        db_cur = db_conn.cursor()
        if not db_cur:
            return None
        get_sql = 'select ip_port, protocal from proxy_info where alive < 4;'
        row = db_cur.execute(get_sql)
        rs = db_cur.fetchall()
        for data in rs:
            ip, protocal = data
            ip_port = 'http://%s'%(ip) if protocal == 1 else 'https://%s'%(ip)
            yield self.request(start_urls, self.parse, meta={'proxy': ip_port, 'ip_addr': ip})
                
        db_cur.close()
        db_conn.close()

    def request(self, url, callback, meta={}):
        meta['request_url'] = url
        meta['dont_obey_robotstxt'] = True
        meta['dont_retry'] = True
        return scrapy.Request(url, callback, dont_filter=True, meta=meta)

    def parse(self, response):
        ip_addr = response.meta.get('ip_addr')
        req_time = response.meta.get('req_time')
        res_time = response.meta.get('res_time')
        check_result = {'ip_addr': ip_addr, 'response_time': res_time - req_time}
        if response.status == 200 and response.text:
            check_result['alive'] = True
        else:
            check_result['alive'] = False

        yield check_result

        


