# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseraCourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    course_id = scrapy.Field()
    course_name = scrapy.Field()
    rating = scrapy.Field()
    level = scrapy.Field()
    instructor = scrapy.Field()
