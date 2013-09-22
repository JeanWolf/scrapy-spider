##coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field

class ShopItem(Item):
    # define the fields for your item here like:
    # name = Field()
    itemtype = Field() #用於判斷item的類型
    #企業表信息
    id = Field()     #唯一标识ID
    fetch_date = Field()     #抓取日期
    com_id = Field()     # 1企业id
    name = Field()     # 2公司名称
    contactor = Field()     #3联系人
    address = Field()     # 4公司地址
    postcode = Field()     # 5邮编
    area = Field()     # 6所在地区
    country = Field()     #7所属国家
    tel = Field()     # 8电话
    phone = Field()     # 9手机
    fax = Field()     # 10传真
    email = Field()     #11邮箱
    qq = Field()     # 12在线联系（qq）
    other = Field()     #13其他联系方式
    title = Field()     # 15职位
    content = Field()     #16公司介绍
    url = Field()     #17在被抓取网站的该店铺网址
    website = Field()     # 18公司主页
    logo = Field()     # 19标致（公司logo）
    logo_src = Field()      #logo源路径
    cet = Field()     #20荣誉证书
    photo = Field()     #21营业执照图片
    photo_src = Field()     #photo源路径
    reg_address = Field()     #22注册地址
    reg_money = Field()     # = Field()     #23注册资金
    create_time = Field()     # 24成立时间
    reg_number = Field()     # 25注册号
    boss = Field()     #26法人代表
    reg_com = Field()     # 27等级机关
    type = Field()     # 28企业类型
    valid = Field()     #29营业期限
    custom = Field()     #30主要客户群
    market = Field()     #31主要市场
    market_address = Field()     #32主要经营地点
    brand = Field()     # 33经营品牌
    money = Field()     #34年营业额
    employees = Field()     #35员工人数
    industry = Field()     #36主营行业产品
    range = Field()     # 37经营范围
    modes = Field()     # 38经营模式
    exports = Field()     # 39年出口额
    imports = Field()     #40年进口额
    bank = Field()     #41银行帐号
    plant_area = Field()     #42厂房面积
    iso = Field()     # 43管理体系认证
    fetch_level = Field()     # 44 在被抓取网站的会员等级
    fetch_reg_time = Field()     # 45在被抓取网站的注册时间
    fetch_auth = Field()     #46在被抓取网站的认证情况
    fetch_auth_time = Field()     # 47在被抓取网站的认证时间
    fetch_evaluate = Field()     # 48在被抓取网站的客户评价
    fetch_credit = Field()     # 49在被抓取网站的会员积分
    fetch_sale_data = Field()     #50在被抓取网站的销售数据
    fetch_other = Field()     # 51其它

class ProductItem(Item):
    # define the fields for your item here like:
    # name = Field()
    itemtype = Field() #用於判斷item的類型
    #产品表信息
    product_id = Field()    #唯一标识
    fetch_date = Field()    #抓取日期
    p_id = Field()    #1产品id
    com_id = Field()    #2相关企业会员关联id
    name = Field()    #3产品名称
    type = Field()    #4所属分类
    photo = Field()    #5产品图片
    photo_src = Field() #photo源路径
    price = Field()    #6产品价格（或价格区间）
    area = Field()    #7产品所在地区
    sale_area = Field()    #8目标销售地区
    delivery_cycle = Field()    #9发货周期
    moq = Field()    #10最小起订量
    total = Field()    #11供应总量
    expiry_date = Field()    #12信息到期时间
    publish_date = Field()    #13发布时间
    valid = Field()    #14有效期
    brand = Field()    #15产品品牌
    other = Field()    #16 其他信息
    detail = Field()    #17产品详细介绍
    companyname = Field()    #公司名称
    purl = Field()    #？？？
    #图片表信息
    image_id = Field()    #唯一标识
    #fetch_date = Field()    #抓取时间
    #p_id = Field()    #产品id
    image = Field()    #图片
    image_src = Field()    #图片源路径
