# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# データ出力するフィールドを定義
class RecipeCollectorItem(scrapy.Item):
    hashed_url = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    steps = scrapy.Field()
    ingredients = scrapy.Field()
    category = scrapy.Field()
    random = scrapy.Field()
