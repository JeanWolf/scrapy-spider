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

class AllSpider(CrawlSpider):  #同时抓取
    name = 'all'
    allowed_domains = ['toobm.com']
    start_urls = [
        'http://www.toobm.com', #入口
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=("http://www.toobm.com/product-1-1.html$"))),
        Rule(SgmlLinkExtractor(allow=("product-1-4.html$"))),
        Rule(SgmlLinkExtractor(allow=("/wp/2419405/pdetail0pd26427768.html$")),callback = "parse_product",follow=True),
        Rule(SgmlLinkExtractor(allow=("/wp/2419405/clist0cgp1.html#intro$")),callback = "parse_shop"),

        #Rule(SgmlLinkExtractor(allow=("/wp/([0-9]+)/pdetail0pd([0-9]+).html$")),callback = "parse_product",follow=True),
        #Rule(SgmlLinkExtractor(allow=("/wp/([0-9]+)/clist0cgp1.html#intro$")),callback = "parse_shop"),
    )
    global s_count,p_count # 用于 shop   product  抓取数量统计
    s_count = 0
    p_count = 0
#分析代码中请将页面中分析得到的图片路径赋值到新字段  logo_src  photo_src  image_src 中
#-- parse_shop Start-----------------------------------------------
    def parse_shop(self, response):
        jeen = Jeen()
        if conf_show_messages : print '\r\n\t======== Page Crawl Start - Company -----------'
        hxs = HtmlXPathSelector(response)
        item = jeen.init_item('shop') #初始化 shop item
        try :
            if conf_show_messages : print '----Company Fetch Start----'
        #--分析代码开始#################################################################################################################
            item['url'] = response.url
            item['logo_src'] = 'http://china.toocle.com/images/comp/11/s19.gif'
            item['photo_src'] = 'http://img1.toocle.com/bin/img/?x=217&y=156&t=company_cn&m=1&s=/2013/09/05/05/2519405_1.jpg'
            newurl = 'http://cn.china.cn' #构造企业介绍页Url
            if conf_use_proxy :
                try : #尝试加载新页面，使用代理IP
                    proxy_handle = urllib2.ProxyHandler({ 'http' : jeen.get_proxy() })
                    opener = urllib2.build_opener(proxy_handle)
                    temp = opener.open(newurl,timeout=30) #请求
                except : #重试一次，如果仍无法打开.. 然后..就没有然后了
                    proxy_handle = urllib2.ProxyHandler({ 'http' : jeen.get_proxy() })
                    opener = urllib2.build_opener(proxy_handle)
                    temp = opener.open(newurl,timeout=30) #请求
            else :
                try :
                    temp = urllib2.urlopen(newurl,timeout=30)
                except :
                    temp = urllib2.urlopen(newurl,timeout=30)
            temp = temp.read() #读数据
            newresponse = HtmlResponse(newurl)
            newresponse._set_body(temp)
            hxs = HtmlXPathSelector(newresponse) #构建新的xpath选择器
            #print temp
        #--分析代码结束#################################################################################################################
            if conf_show_messages : print '---- Fetch Success ----'
        except EOFError,e :
            if conf_show_messages : print '----Company Fetch Error Start----'
            print e
            if conf_show_messages : print '----Company Fetch Error End----'
        if conf_show_messages : print '----Company Fetch End----'
        item = jeen.handle_item(item) #处理item 主要处理一些特殊字符  换行符  及多余空格
        global s_count ; s_count += 1;
        jeen.show_msg('%s Company\t======== Page Crawl Information End =========================' % s_count)
        del hxs,response #销毁相关变量
        #return item
#---Parse_shop End---------------------------------------------------------
#-############
#-- parse_product Start-----------------------------------------------
    def parse_product(self, response): #分析产品时，主图 请勿重复添加 到多图字段中
        jeen = Jeen()
        if conf_show_messages : print '\r\n\t======== Page Crawl Start - Product -----------'
        hxs = HtmlXPathSelector(response)
        item = jeen.init_item('product') #初始化 shop item
        try :
            if conf_show_messages : print '----Product Fetch Start----'
        #--分析代码开始#################################################################################################################
            item['purl'] = response.url
            item['photo_src'] = 'http://img1.toocle.com/bin/img/?x=160&y=160&t=product_cn&m=1&s=/2012/11/11/08/26527608_1.jpg'
            item['image_src'] = 'http://img1.toocle.com/bin/img/?x=160&y=160&t=product_cn&m=1&s=/2012/11/11/08/26527608_1.jpg'
        #--分析代码结束#################################################################################################################
            if conf_show_messages : print '---- Fetch Success ----'
        except EOFError,e :
            if conf_show_messages : print '----Product Fetch Error Start----'
            print e
            if conf_show_messages : print '----Product Fetch Error End----'
        if conf_show_messages : print '----Product Fetch End----'
        item = jeen.handle_item(item) #处理item 主要处理一些特殊字符  换行符  及多余空格
        global p_count; p_count += 1;
        jeen.show_msg('%s Product\t======== Page Crawl Information End =========================' % p_count)
        del hxs,response #销毁相关变量
        #return item
#---Parse_product End---------------------------------------------------------
