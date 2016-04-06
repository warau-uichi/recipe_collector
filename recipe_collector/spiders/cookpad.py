# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from recipe_collector.items import RecipeCollectorItem
import hashlib
import re
import random
import requests
import base64

class Cookpad(CrawlSpider):
    name = 'cookpad'
    allowed_domains = ['cookpad.com']


    def __init__(self, category=None, *args, **kwargs):
        # カテゴリオプション
        self.category = unicode(category, "utf-8")
        """
        http://cookpad.com/search/パスタ 時短?purpose=時短
        のようなURLからクローリングを開始 
        """
        self.start_urls = [
            'http://cookpad.com/search/{0}%E3%80%80%E6%99%82%E7%9F%AD?purpose=%E6%99%82%E7%9F%AD'
                .format(requests.utils.quote(self.category.encode("utf-8")))
        ]
        self.rules = [
            #正規表現にマッチするリンクをparse_recipeメソッドでスクレイピング
            Rule(SgmlLinkExtractor(allow=(r'/recipe/[\d]+$')), callback='parse_recipe')
        ]
        super(Cookpad, self).__init__(*args, **kwargs)


    def url_to_b64(self, url):
        return self.bytes_to_b64(self.url_to_bytes(url))


    def url_to_bytes(self, url):
        return requests.get(url).content


    def bytes_to_b64(self, bytes):
        if bytes[0] == "\xff" and bytes[1] == "\xd8" and bytes[-2] == "\xff" and bytes[-1] == "\xd9":
            imgsrc = "data:image/jpeg;base64,"
        elif bytes[0] == "\x89" and bytes[1] == "\x50" and bytes[2] == "\x4e" and bytes[3] == "\x47":
            imgsrc = "data:image/png;base64,"
        elif bytes[0] == "\x47" and bytes[1] == "\x49" and bytes[2] == "\x46" and bytes[3] == "\x38":
            imgsrc = "data:image/git;base64,"
        elif bytes[0] == "\x42" and bytes[1] == "\x4d":
            imgsrc = "data:image/bmp;base64,"
        else:
            imgsrc = "data:image/unknown;base64,"
        return imgsrc + base64.b64encode(bytes)

    
    def parse_recipe(self, response):
        item = RecipeCollectorItem()
        sel = Selector(response)
        strip_regexp = re.compile(r"<[^>]*?>")
        strip_regexp2 = re.compile(r"<[^>]*?>|\n")

        item['url'] = "http://cookpad.com/recipe/{0}"\
            .format(sel.xpath('//*[@id="recipe"]/@data-recipe-id').extract()[0])
        item['hashed_url'] = hashlib.sha1(item['url']).hexdigest()
        item['title'] = strip_regexp2.sub("", sel.xpath('//h1/text()').extract()[0])
        item['image'] = self.url_to_b64\
            (sel.xpath('//*[@id="main-photo"]/img/@src').extract()[0].split('?')[0])
        steps = []
        step_elms = sel.xpath('//*[@class="step_text"]/text()').extract()
        for step in step_elms:
            steps.append(strip_regexp.sub("", step))
        item['steps'] = steps
        ingredients = []
        ing_elms = sel.xpath('//*[@class="ingredient_name"]/span').extract()
        for ing in ing_elms:
            ingredients.append(strip_regexp.sub("", ing))
        item['ingredients'] = ingredients
        item['category'] = self.category
        item['random'] = random.uniform(0, 1)

        yield item
