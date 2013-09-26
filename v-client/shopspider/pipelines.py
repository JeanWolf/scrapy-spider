##coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from hashlib import md5
from time import mktime,strptime,strftime,localtime
from datetime import date
from shopspider.diy.configs import *

class ShopspiderPipeline(object):
    def process_item(self, item, spider):
        try :
            #--读入相关配置 -------------
            show_message = conf_show_messages
            dbtype = conf_db_type  #数据库类型  oracle   mysql
            db_host = conf_db_host
            db_port = conf_db_port
            db_name = conf_db_name
            db_sid = conf_db_sid
            db_sname = conf_db_sname
            db_user = conf_db_user
            db_pass = conf_db_pass

            tb_prefix = conf_table_prefix #  表头 eg  TEST  -->   TEST_SHOP   TEST_PRODUCT   TEST_PRODUCT_IMAGE
            #处理抓取时间
            #item['fetch_date'] = date.today()
            if show_messages : print "--------Pipeline Start---------------"
            if dbtype == 'oracle' :
                import cx_Oracle
                import os
                os.environ['NLS_LANG']="AMERICAN_AMERICA.AL32UTF8"
            elif dbtype == 'mysql' :
                import MySQLdb
            else :
                print '------Database Type Undefined==========='
            if show_messages : print "--------Connect "+dbtype+" Database Start---------"   #数据库连接
            if dbtype == 'oracle' :
                # connect to Oracle
                #方法一 ： 使用 SID
                #db_dsn = cx_Oracle.makedsn(db_host,db_port,db_sid)
                #conn = cx_Oracle.connect(db_user,db_pass,db_dsn)
                #方法二： 使用服务名
                connstr = '%s/%s@%s:%s/%s' % (db_user,db_pass,db_host,db_port,db_sname)
                conn =cx_Oracle.connect(connstr)
                #conn =cx_Oracle.connect('phpzq/phptiger@172.16.4.223:18000/jlproject_primary')
            elif dbtype == 'mysql' :
                conn = MySQLdb.connect(host=db_host,user=db_user,passwd=db_pass,port=db_port,db=db_name,charset='utf8')
                #conn = MySQLdb.connect(host='192.168.0.43',user='spider',passwd='spider',port=3306,db='spider',charset='utf8')
            cur = conn.cursor()
            if show_messages : print "--------Connect Successful---------"
            sql = ''
            sql1 = ''
            sql2 = ''
            #处理抓取值
            if item['itemtype'] == 'shop' :
                value = [
                        #str(item['id']),     #唯一标识ID
                        #item['fetch_date'],     #抓取日期
                        str(item['com_id']),     # 1企业id
                        str(item['name']),     # 2公司名称
                        str(item['contactor']),     #3联系人
                        str(item['address']),     # 4公司地址
                        str(item['postcode']),     # 5邮编
                        str(item['area']),     # 6所在地区
                        str(item['country']),     #7所属国家
                        str(item['tel']),     # 8电话
                        str(item['phone']),     # 9手机
                        str(item['fax']),     # 10传真
                        str(item['email']),     #11邮箱
                        str(item['qq']),     # 12在线联系（qq）
                        str(item['other']),     #13其他联系方式
                        str(item['title']),     # 15职位
                        str(item['content']),     #16公司介绍
                        str(item['url']),     #17在被抓取网站的该店铺网址
                        str(item['website']),     # 18公司主页
                        str(item['logo']),     # 19标致（公司logo）
                        str(item['cet']),     #20荣誉证书
                        str(item['photo']),     #21营业执照图片
                        str(item['reg_address']),     #22注册地址
                        str(item['reg_money']),    #23注册资金
                        str(item['create_time']),     # 24成立时间
                        str(item['reg_number']),     # 25注册号
                        str(item['boss']),     #26法人代表
                        str(item['reg_com']),     # 27等级机关
                        str(item['type']),     # 28企业类型
                        str(item['valid']),     #29营业期限
                        str(item['custom']),     #30主要客户群
                        str(item['market']),     #31主要市场
                        str(item['market_address']),     #32主要经营地点
                        str(item['brand']),     # 33经营品牌
                        str(item['money']),     #34年营业额
                        str(item['employees']),     #35员工人数
                        str(item['industry']),     #36主营行业产品
                        str(item['range']),     # 37经营范围
                        str(item['modes']),     # 38经营模式
                        str(item['exports']),     # 39年出口额
                        str(item['imports']),     #40年进口额
                        str(item['bank']),     #41银行帐号
                        str(item['plant_area']),     #42厂房面积
                        str(item['iso']),     # 43管理体系认证
                        str(item['fetch_level']),     # 44 在被抓取网站的会员等级
                        str(item['fetch_reg_time']),     # 45在被抓取网站的注册时间
                        str(item['fetch_auth']),     #46在被抓取网站的认证情况
                        str(item['fetch_auth_time']),     # 47在被抓取网站的认证时间
                        str(item['fetch_evaluate']),     # 48在被抓取网站的客户评价
                        str(item['fetch_credit']),     # 49在被抓取网站的会员积分
                        str(item['fetch_sale_data']),     #50在被抓取网站的销售数据
                        str(item['fetch_other']),     # 51其它
                        str(item['logo_src']),      #logo源路径
                        str(item['photo_src'])      #photo源路径
                ]
                if dbtype == 'oracle' :
                    sql1 = 'INSERT INTO '+tb_prefix+'_SHOP (COM_ID, NAME, CONTACTOR, ADDRESS, POSTCODE, AREA, COUNTRY, TEL, PHONE, FAX, EMAIL, QQ, OTHER, TITLE, CONTENT, URL, WEBSITE, LOGO, CET, PHOTO, REG_ADDRESS, REG_MONEY, CREATE_TIME, REG_NUMBER, BOSS, REG_COM, TYPE, VALID, CUSTOM, MARKET, MARKET_ADDRESS, BRAND, MONEY, EMPLOYEES, INDUSTRY, RANGE, MODES, EXPORTS, IMPORTS, BANK, PLANT_AREA, ISO, FETCH_LEVEL, FETCH_REG_TIME, FETCH_AUTH, FETCH_AUTH_TIME, FETCH_EVALUATE, FETCH_CREDIT, FETCH_SALE_DATA, FETCH_OTHER, LOGO_SRC, PHOTO_SRC) VALUES  '
                    sql2 = ' (:com_id, :name, :contactor, :address, :postcode, :area, :country, :tel, :phone, :fax, :email, :qq, :other, :title, :content, :url, :website, :logo, :cet, :photo, :reg_address, :reg_money, :create_time, :reg_number, :boss, :reg_com, :type, :valid, :custom, :market, :market_address, :brand, :money, :employees, :industry, :range, :modes, :exports, :imports, :bank, :plant_area, :iso, :fetch_level, :fetch_reg_time, :fetch_auth, :fetch_auth_time, :fetch_evaluate, :fetch_credit, :fetch_sale_data, :fetch_other, :logo_src, :photo_src)'
                elif dbtype == 'mysql' :
                    sql1 = 'INSERT INTO `'+tb_prefix+'_SHOP` (`COM_ID`, `NAME`, `CONTACTOR`, `ADDRESS`, `POSTCODE`, `AREA`, `COUNTRY`, `TEL`, `PHONE`, `FAX`, `EMAIL`, `QQ`, `OTHER`, `TITLE`, `CONTENT`, `URL`, `WEBSITE`, `LOGO`, `CET`, `PHOTO`, `REG_ADDRESS`, `REG_MONEY`, `CREATE_TIME`, `REG_NUMBER`, `BOSS`, `REG_COM`, `TYPE`, `VALID`, `CUSTOM`, `MARKET`, `MARKET_ADDRESS`, `BRAND`, `MONEY`, `EMPLOYEES`, `INDUSTRY`, `RANGE`, `MODES`, `EXPORTS`, `IMPORTS`, `BANK`, `PLANT_AREA`, `ISO`, `FETCH_LEVEL`, `FETCH_REG_TIME`, `FETCH_AUTH`, `FETCH_AUTH_TIME`, `FETCH_EVALUATE`, `FETCH_CREDIT`, `FETCH_SALE_DATA`, `FETCH_OTHER`, `LOGO_SRC`, `PHOTO_SRC`) VALUES  '
                    sql2 = ' (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                else :
                    print '---SQL statement ERROR====='
                sql = "".join([sql1, sql2])
                if show_messages : print "--------Start to Insert Shop---------"
                cur.execute(sql, value)
                conn.commit()
                if show_messages : print "--------Shop Insert Successful--------"
            elif item['itemtype'] == 'product' :
                #处理抓取值 产品表
                value = [
                    #str(item['product_id']),    #唯一标识
                    #item['fetch_date'],    #抓取日期
                    str(item['p_id']),    #1产品id
                    str(item['com_id']),    #2相关企业会员关联id
                    str(item['name']),    #3产品名称
                    str(item['type']),    #4所属分类
                    str(item['photo']),    #5产品图片
                    str(item['price']),    #6产品价格（或价格区间）
                    str(item['area']),    #7产品所在地区
                    str(item['sale_area']),    #8目标销售地区
                    str(item['delivery_cycle']),    #9发货周期
                    str(item['moq']),    #10最小起订量
                    str(item['total']),    #11供应总量
                    str(item['expiry_date']),    #12信息到期时间
                    str(item['publish_date']),    #13发布时间
                    str(item['valid']),    #14有效期
                    str(item['brand']),    #15产品品牌
                    str(item['other']),    #16
                    str(item['detail']),    #17产品详细介绍
                    str(item['companyname']),    #公司名称
                    str(item['purl']),    #產品抓取葉URL
                    str(item['photo_src']) #产品图片源路径
                ]

                if dbtype == 'oracle' :
                    sql1 = 'INSERT INTO '+tb_prefix+'_PRODUCT (P_ID, COM_ID, NAME, TYPE, PHOTO, PRICE, AREA, SALE_AREA, DELIVERY_CYCLE, MOQ, TOTAL, EXPIRY_DATE, PUBLISH_DATE, VALID, BRAND, OTHER, DETAIL, COMPANYNAME, PURL,PHOTO_SRC) VALUES '
                    sql2 = '(:p_id, :com_id, :name, :type, :photo, :price, :area, :sale_area, :delivery_cycle, :moq, :total, :expiry_date, :publish_date, :valid, :brand, :other, :detail, :companyname, :purl, :photo_src)'
                elif dbtype == 'mysql' :
                    sql1 = 'INSERT INTO `'+tb_prefix+'_PRODUCT` (`P_ID`, `COM_ID`, `NAME`, `TYPE`, `PHOTO`, `PRICE`, `AREA`, `SALE_AREA`, `DELIVERY_CYCLE`, `MOQ`, `TOTAL`, `EXPIRY_DATE`, `PUBLISH_DATE`, `VALID`, `BRAND`, `OTHER`, `DETAIL`, `COMPANYNAME`, `PURL`, `PHOTO_SRC`) VALUES '
                    sql2 = '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                else :
                    print '---SQL statement ERROR====='
                sql = "".join([sql1, sql2])
                if show_messages : print "--------Start to Insert Product---------"
                cur.execute(sql, value)
                conn.commit()
                if show_messages : print "--------Product Insert Successful--------"
                #-另存一份产品主图
                if item['photo_src'] != '' :
                    value = [
                        #str(item['image_id']),    #唯一标识
                        #item['fetch_date'],    #抓取日期
                        str(item['p_id']),    #1产品id
                        str(item['photo']),    #图片相对路径
                        str(item['photo_src']) #图片源地址
                    ]
                    if dbtype == 'oracle' :
                        sql1 = 'INSERT INTO '+tb_prefix+'_PRODUCT_IMAGE (P_ID, IMAGE, IMAGE_SRC) VALUES '
                        sql2 = '(:p_id, :image, :image_src)'
                    elif dbtype == 'mysql' :
                        sql1 = 'INSERT INTO `'+tb_prefix+'_PRODUCT_IMAGE` (`P_ID`, `IMAGE`, `IMAGE_SRC`) VALUES '
                        sql2 = '(%s, %s, %s)'
                    else :
                        print '---SQL statement ERROR====='

                    sql = "".join([sql1, sql2])
                    if show_messages : print "--------Start to Insert Product Main Image---------"
                    cur.execute(sql, value)
                    conn.commit()
                    if show_messages : print "--------Product Main Image Insert Successful--------"

                #处理抓取值 多图字段
                if item['image_src'] != '' :
                    img_srcs = item['image_src'].split('|')
                    imgs = item['image'].split('|')
                    count = len(img_srcs)
                    i = 0
                    while i < count :
                        value = [
                            #str(item['image_id']),    #唯一标识
                            #item['fetch_date'],    #抓取日期
                            str(item['p_id']),    #1产品id
                            str(imgs[i]),    #图片
                            str(img_srcs[i]) #图片源地址
                        ]
                        if dbtype == 'oracle' :
                            sql1 = 'INSERT INTO '+tb_prefix+'_PRODUCT_IMAGE (P_ID, IMAGE, IMAGE_SRC) VALUES '
                            sql2 = '(:p_id, :image, :image_src)'
                        elif dbtype == 'mysql' :
                            sql1 = 'INSERT INTO `'+tb_prefix+'_PRODUCT_IMAGE` (`P_ID`, `IMAGE`, `IMAGE_SRC`) VALUES '
                            sql2 = '(%s, %s, %s)'
                        else :
                            print '---SQL statement ERROR====='

                        sql = "".join([sql1, sql2])
                        if show_messages : print "--------Start to Insert Product Multi Image---------"
                        cur.execute(sql, value)
                        conn.commit()
                        if show_messages : print "--------Product Multi Image Insert Successful--------"
                        i += 1
            else :
                print '---ItemType Undefined================='
            cur.close()
            conn.close()
            del sql,sql1,sql2,cur,conn,item,value,tb_prefix,dbtype #銷毀變量
        except Exception,e:
        	if show_messages : print '--------Pipeline Error Start---------------'
        	print e
        	if show_messages : print '--------Pipeline Error End---------------'
        if show_messages : print '--------Pipeline End---------------'
        if show_messages : print '\t==============Crawl Log Information============='
        return '----======== Page Crawl End=============\r\n\r\n'
        #return item
