#!/bin/python
#coding: utf-8

import pymysql
import os,sys
import time

class IngestPipline(object):
    def __init__(self):
        self.db_conn = None
        self.db_cur = None

    def process_item(self, item, spider):
        if not item:
            return {}
        if item.get('ip_info'):
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
        else:
            ip = item['ip_addr']
            response_time = item.get('response_time')
            alive = item.get('alive', False)
            if alive:
                sql = 'update proxy_info set alive = 1, response_time = "%.3f", check_time = "%s" where ip_port = "%s";'
            else:
                sql = 'update proxy_info set alive = alive + 1, response_time = "%.3f", check_time = "%s" where ip_port = "%s";'
            try:
                sql = sql%(response_time, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ip)
                self.db_cur.execute(sql)
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
        del_sql = 'delete from proxy_info where alive > 3;'
        try:
            self.db_cur.execute(del_sql)
        except Exception as e:
            pass
        if self.db_cur:
            self.db_cur.close()
        if self.db_conn:
            self.db_conn.commit()
            self.db_conn.close()