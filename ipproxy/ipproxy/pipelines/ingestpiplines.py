#!/bin/python
#coding: utf-8

import pymysql
import os,sys

class IngestPipline(object):
    def __init__(self):
        self.db_conn = None
        self.db_cur = None

    def process_item(self, item, spider):
        if not item:
            return {}
        ip_list_info = item['ip_info']
        sql = "insert into proxy_info set ip_port = '%s', protocal = '%s';"
        for ip_info in ip_list_info:
            if not ip_info:
                continue
            ip = ip_info['ip_addr']
            port = ip_info['port']
            protocal = ip_info.get('protocal', 1)
            try:
                self.db_cur.execute(sql%(ip+':'+str(port), protocal))
            except Exception as e:
                pass
        return item

    def open_spider(self, spider):
        self.db_conn = pymysql.connect(host='localhost',
                                user='root',
                                passwd='reload123',
                                db='proxy',
                                charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        if self.db_cur:
            self.db_cur.close()
        if self.db_conn:
            self.db_conn.commit()
            self.db_conn.close()