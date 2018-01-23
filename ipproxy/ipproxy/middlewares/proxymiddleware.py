#!/bin/python
#coding: utf-8

import random
import scrapy
import pymysql

class ProxyMiddleWare(object):
    def __init__(self, settings, spider):
        print('proxy init...')
        self.proxy_ips = []
        self.settings = settings
        self.use_proxy = self.settings.get('use_proxy', False)
        
    @classmethod
    def from_crawler(cls, crawler):
       return cls(crawler.settings, crawler.spider)

    def process_request(self, request, spider):
        print('proxy request process...')
        print(request.meta)
        if self.use_proxy and request.meta.get('use_proxy'):
            if not self.proxy_ips:
                self.refresh_pool()
            if self.proxy_ips:
                ip = random.choice(self.proxy_ips)
                self.proxy_ips.remove(ip)
                print(ip)
                request.meta['proxy'] = ip
                request.meta['download_timeout'] = 10

    def process_response(self, response, request, spider):
        print('proxy response process...')
        return response

    def process_exception(self, request, exception, spider):
        print('proxy exception process...')
        raise None

    def refresh_pool(self):
        db_conn = pymysql.connect(host='localhost', user='root', \
                        passwd='reload123', db='proxy', charset='utf8')
        db_cur = db_conn.cursor()
        get = 'select ip_port, protocal from proxy_info where alive = 1 order by response_time limit 100;'
        row = db_cur.execute(get)
        rs = db_cur.fetchall()
        for dt in rs:
            if not dt or len(dt) < 2:
                continue
            ip_info = 'http://%s' if dt[1] == 1 else 'https://%s'
            self.proxy_ips.append(ip_info%(dt[0]))
        db_cur.close()
        db_conn.close()
