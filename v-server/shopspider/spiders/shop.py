##coding=utf-8
import sys,re,urllib2,os,socket
reload(sys)
sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(30)

from scrapy.conf import settings
from scrapy.http import Request,HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from shopspider.diy.funs import replace_item,init_item,handle_item #载入自定义方法
from shopspider.diy.configs import conf

class CompanySpider(CrawlSpider): #单独抓商家
    name = 'shop'
    allowed_domains = ['toobm.com']
    start_urls = [
        'http://www.toobm.com', #入口
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=("http://www.toobm.com/product-1-1.html$"))),
        Rule(SgmlLinkExtractor(allow=("product-1-4.html$"))),
        Rule(SgmlLinkExtractor(allow=("/wp/1589268/pdetail0pd23317573.html$"))),
        Rule(SgmlLinkExtractor(allow=("/wp/1589268/clist0cgp1.html#intro$")),callback = "parse_shop"),
    )
    global s_count
    s_count = 0  #简略统计抓取商家数量
	#分析代码中请将页面中分析得到的图片路径赋值到新字段  logo_src  photo_src  image_src 中
#-- parse_shop Start-----------------------------------------------
    def parse_shop(self, response):
        print '\r\n\t======== Page Crawl Start - Company -----------'
        hxs = HtmlXPathSelector(response)
        item = init_item('shop') #初始化 shop item
        try :
            if conf['show_messages'] : print '----Company Fetch Start----'
        #--分析代码开始#################################################################################################################
            item['url'] = response.url
        #--分析代码结束#################################################################################################################
            if conf['show_messages'] : print '---- Fetch Success ----'
        except EOFError,e :
            if conf['show_messages'] : print '----Company Fetch Error Start----'
            print e
            if conf['show_messages'] : print '----Company Fetch Error End----'
        if conf['show_messages'] : print '----Company Fetch End----'
        item = handle_item(item) #处理item 主要处理一些特殊字符  换行符  及多余空格
        global s_count ; s_count += 1;
        print str(s_count)+' Company\t======== Page Crawl Information End ========================='
        del hxs,response #销毁相关变量
        return item
#---Parse_shop End---------------------------------------------------------