##coding=utf-8
import sys,re,urllib2,os
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.conf import settings
from scrapy.http import Request,HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from shopspider.diy.funs import replace_item,init_item,handle_item,get_proxy #载入自定义方法
from shopspider.diy.configs import conf

class AllSpider(CrawlSpider):  #同时抓取
    name = 'all'
    allowed_domains = ['toobm.com']
    start_urls = [
        'http://www.toobm.com', #入口
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=("http://www.toobm.com/product-1-1.html$"))),
        Rule(SgmlLinkExtractor(allow=("product-1-4.html$"))),
        Rule(SgmlLinkExtractor(allow=("/wp/2419405/pdetail0pd26427581.html$")),callback = "parse_product",follow=True),
        Rule(SgmlLinkExtractor(allow=("/wp/2419405/clist0cgp1.html#intro$")),callback = "parse_shop"),

        #Rule(SgmlLinkExtractor(allow=("/wp/([0-9]+)/pdetail0pd([0-9]+).html$")),callback = "parse_product",follow=True),
        #Rule(SgmlLinkExtractor(allow=("/wp/([0-9]+)/clist0cgp1.html#intro$")),callback = "parse_shop"),
    )
    global s_count,p_count
    s_count = 0
    p_count = 0
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
            item['logo_src'] = 'http://baidu.com/abc/ddd.jpg'
            item['photo_src'] = '/image/abcd.jpg'
            newurl = 'http://cn.china.cn' #构造企业介绍页Url
            try : #尝试加载新页面，使用代理IP
                proxy_handle = urllib2.ProxyHandler({ 'http' : get_proxy() })
                opener = urllib2.build_opener(proxy_handle)
                temp = opener.open(newurl,timeout=30) #请求
            except : #重试一次，如果仍无法打开.. 然后..就没有然后了
                proxy_handle = urllib2.ProxyHandler({ 'http' : get_proxy() })
                opener = urllib2.build_opener(proxy_handle)
                temp = opener.open(newurl,timeout=30) #请求
            temp = temp.read() #读数据
            newresponse = HtmlResponse(newurl)
            newresponse._set_body(temp)
            hxs = HtmlXPathSelector(newresponse) #构建新的xpath选择器
            #print temp
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
        #return item
#---Parse_shop End---------------------------------------------------------
#-############
#-- parse_product Start-----------------------------------------------
    def parse_product(self, response):
        print '\r\n\t======== Page Crawl Start - Product -----------'
        hxs = HtmlXPathSelector(response)
        item = init_item('product') #初始化 shop item
        try :
            if conf['show_messages'] : print '----Product Fetch Start----'
        #--分析代码开始#################################################################################################################
            item['purl'] = response.url
            item['photo_src'] = '/abcd.jpg'
            item['image_src'] = 'http://123.com/abcd.jpg|/abc/ddd.jpg|./dew.jpg|.././ccc.jpg'
        #--分析代码结束#################################################################################################################
            if conf['show_messages'] : print '---- Fetch Success ----'
        except EOFError,e :
            if conf['show_messages'] : print '----Product Fetch Error Start----'
            print e
            if conf['show_messages'] : print '----Product Fetch Error End----'
        if conf['show_messages'] : print '----Product Fetch End----'
        item = handle_item(item) #处理item 主要处理一些特殊字符  换行符  及多余空格
        global p_count; p_count += 1;
        print str(p_count)+' Product\t======== Page Crawl Information End ========================='
        del hxs,response #销毁相关变量
        #return item
#---Parse_product End---------------------------------------------------------
