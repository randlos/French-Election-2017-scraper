# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class stimmenPipeline(object):
    def process_item(self, item, spider):
        if item['stimmen']:
            str = item['stimmen']
            item['stimmen'] = str.replace(" ","")
        return item
