##coding=utf-8
import sys,re,urllib2,os,socket
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.conf import settings
from scrapy.http import Request,HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from shopspider.diy.jeen import Jeen #载入自定义类方法
from shopspider.diy.configs import *
socket.setdefaulttimeout(conf_time_out)

class ProductSpider(CrawlSpider): #单独抓产品
    name = 'product'
    allowed_domains = ['toobm.com']
    start_urls = [
        'http://www.toobm.com', #入口
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=("http://www.toobm.com/product-1-1.html$"))),
        Rule(SgmlLinkExtractor(allow=("product-1-4.html$"))),
        Rule(SgmlLinkExtractor(allow=("/wp/1589268/pdetail0pd23317573.html$")),callback = "parse_product")
    )

    global p_count
    p_count = 0 #简略统计抓取商品数量
	#分析代码中请将页面中分析得到的图片路径赋值到新字段  logo_src  photo_src  image_src 中
#-- parse_product Start-----------------------------------------------
    def parse_product(self, response):
        #请参考 all.py 中的产品分析部分
        pass
#-- parse_product End  -----------------------------------------------
