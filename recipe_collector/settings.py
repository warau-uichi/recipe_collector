# -*- coding: utf-8 -*-

# Scrapy settings for recipe_collector project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# クロール秒数間隔
DOWNLOAD_DELAY = 3
# robots.txtに従うか否か
ROBOTSTXT_OBEY = True 


BOT_NAME = 'recipe_collector'

SPIDER_MODULES = ['recipe_collector.spiders']
NEWSPIDER_MODULE = 'recipe_collector.spiders'


# スクレイピング情報をcouchに格納するための情報
# pip install "ScrapyCouchDB"
ITEM_PIPELINES = [
  'scrapycouchdb.CouchDBPipeline',
]
COUCHDB_SERVER = 'http://localhost:5984/'
COUCHDB_DB = 'recipes'
COUCHDB_UNIQ_KEY = 'hashed_url'
COUCHDB_IGNORE_FIELDS = []


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recipe_collector (+http://www.yourdomain.com)'
