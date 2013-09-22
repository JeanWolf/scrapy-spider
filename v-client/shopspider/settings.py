##coding=utf-8
# Scrapy settings for shopspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'shopspider'

SPIDER_MODULES = ['shopspider.spiders']
NEWSPIDER_MODULE = 'shopspider.spiders'

ITEM_PIPELINES = ['shopspider.pipelines.ShopspiderPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

#SCHEDULER_MIDDLEWARES_BASE组件是用来过滤唯一地址的，防止spider进入trap。
SCHEDULER_MIDDLEWARES_BASE = {
    'scrapy.contrib.schedulermiddleware.duplicatesfilter.DuplicatesFilterMiddleware': 500,
}
#COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = False
DOWNLOAD_DELAY = 2
DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #'shopspider.diy.middlewares.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'shopspider.diy.rotate_useragent.RotateUserAgentMiddleware' :400,
}

PROXIES = [
    {'ip_port': '202.171.253.111:80', 'user_pass': ''},
    {'ip_port': '202.171.253.98:80', 'user_pass': ''},
    {'ip_port': '110.4.12.170:81', 'user_pass': ''},
    {'ip_port': '94.142.27.4:3128', 'user_pass': ''},
    {'ip_port': '68.180.195.138:80', 'user_pass': ''},
    {'ip_port': '124.225.52.14:8080', 'user_pass': ''},
    {'ip_port': '86.96.229.123:8088', 'user_pass': ''},
    {'ip_port': '86.96.229.68:8088', 'user_pass': ''},
    {'ip_port': '125.39.66.148:80', 'user_pass': ''},
    {'ip_port': '198.50.171.253:8089', 'user_pass': ''},
    {'ip_port': '218.201.21.179:80', 'user_pass': ''},
    {'ip_port': '211.119.134.132:8080', 'user_pass': ''},
    {'ip_port': '125.39.171.194:80', 'user_pass': ''},
    {'ip_port': '124.195.52.21:3128', 'user_pass': ''},
    {'ip_port': '119.18.151.121:80', 'user_pass': ''},
    {'ip_port': '125.39.171.194:82', 'user_pass': ''},
    {'ip_port': '187.51.57.210:3128', 'user_pass': ''},
    {'ip_port': '77.94.48.5:80', 'user_pass': ''},
    {'ip_port': '132.247.174.60:3128', 'user_pass': ''},
    {'ip_port': '86.96.229.68:80', 'user_pass': ''},
    {'ip_port': '111.13.87.150:80', 'user_pass': ''},
    {'ip_port': '202.58.96.56:80', 'user_pass': ''},
    {'ip_port': '62.122.101.26:80', 'user_pass': ''},
    {'ip_port': '203.172.161.211:3129', 'user_pass': ''},
    {'ip_port': '124.237.92.2:8080', 'user_pass': ''},
    {'ip_port': '37.28.165.107:3128', 'user_pass': ''},
    {'ip_port': '94.198.34.230:80', 'user_pass': ''},
    {'ip_port': '177.84.34.178:80', 'user_pass': ''},
    {'ip_port': '222.74.98.234:8080', 'user_pass': ''},
    {'ip_port': '59.172.208.189:8080', 'user_pass': ''},
    {'ip_port': '210.22.115.162:3128', 'user_pass': ''},
    {'ip_port': '111.95.243.37:80', 'user_pass': ''},
    {'ip_port': '124.207.15.50:80', 'user_pass': ''},
    {'ip_port': '113.53.254.124:8080', 'user_pass': ''},
    {'ip_port': '109.69.2.197:80', 'user_pass': ''},
    {'ip_port': '120.68.42.164:3128', 'user_pass': ''}
]
