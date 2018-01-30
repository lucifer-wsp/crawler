#!/bin/python
#coding: utf-8
import scrapy

class RetryMiddleware(object):

    def __init__(self, settings, spider):
        self.settings = settings
        self.max_retry_times = self.settings.get('max_retry_times', 5)

    @classmethod
    def from_crawler(cls, crawer):
        return cls(crawer.settings, crawer.spider)

    def process_request(self, request, spider):
        return None

    def process_response(self, response, request, spider):
        retry_times = request.meta.get('retry_times', 0)
        if retry_times < self.max_retry_times and (response.status != 200 or not response.text):
            request.meta['use_proxy'] = True
            request.meta['retry_times'] = retry_times + 1
            request.dont_filter = True
            return request
        return response

    def process_exception(self, request, exception, spider):
        retry_times = request.meta.get('retry_times', 0)
        if retry_times < self.max_retry_times :
            request.meta['use_proxy'] = True
            request.meta['retry_times'] = retry_times + 1
            request.dont_filter = True
            return request
        else:
            return scrapy.http.TextResponse(url=request.url, status=200, body=None)
