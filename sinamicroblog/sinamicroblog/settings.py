# -*- coding: utf-8 -*-

# Scrapy settings for sinamicroblog project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/

from scrapy.exporters import JsonLinesItemExporter  
BOT_NAME = 'sinamicroblog'

SPIDER_MODULES = ['sinamicroblog.spiders']
NEWSPIDER_MODULE = 'sinamicroblog.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sinamicroblog (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.2  # 间隔时间
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sinamicroblog.middlewares.SinamicroblogSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'sinamicroblog.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'sinamicroblog.pipelines.SinamicroblogPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
COOKIE = {'SUHB': '0qj0GyBaa4oECt', 
    'SCF': 'AirodfBgSquakOha_rXoDhXFUYr21z_5Na6J8ZTii_BUan67TnoSu-j0YpUILr6f6FQL1d3oXihiDZAksnVcElw.',
    '_T_WM': '4e014bc25d77b3039d1aa50a3e5435f6', 
    'ALF': '1511441541', 'SSOLoginState': '1508851177', 
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5cK4i1qIRQd1Jw0mpUv85J5JpX5K-hUgL.Foe7S05Xe0epShM2dJLoIEBLxKMLB.BL1KMLxKqL1-zLB.eLxKnLB.qLB-2LxKBLB.2L1-2t',
    'SUB': '_2A2506025DeRhGeVO7FIV8y3NzzuIHXVUFFPxrDV6PUJbktAKLVXGkW2Sseyf62wo2H-LPBLYwQo-iKWI4A..'
    }

class CustomJsonLinesItemExporter(JsonLinesItemExporter):  
    def __init__(self, file, **kwargs):  
        super(CustomJsonLinesItemExporter, self).__init__(file, ensure_ascii=False, **kwargs)

#这里只需要将超类的ensure_ascii属性设置为False即可
#同时要在setting文件中启用新的Exporter类

FEED_EXPORTERS = {  
    'json': 'sinamicroblog.settings.CustomJsonLinesItemExporter',  
}  