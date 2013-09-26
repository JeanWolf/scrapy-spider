##coding=utf-8
# Define some diy functions here
import os,sys,re,platform,urllib2,random
reload(sys)
sys.setdefaultencoding('utf8')

from shopspider.items import ShopItem,ProductItem #两种ItemType
from shopspider.diy.configs import *

def get_type (tobj) : #返回数据类型
    t = str(type(tobj))
    t = t.replace("<type '","")
    t = t.replace("'>","")
    return t

def replace_item (somestr) : #字符串处理函数
    t = get_type(somestr)
    if t == 'str' :
        somestr = somestr.replace(u'\xa0',' ')
        somestr = somestr.replace('\t','')
        somestr = somestr.replace('\r','')
        somestr = somestr.replace('\n','')
        somestr = somestr.replace('   ','')
        return somestr
    elif t == 'list' or t == 'tuple' :
        somestr = ''.join(somestr)
        return replace_item(somestr)
    else :
        somestr = str(somestr).encode('utf8','ignore')
        return replace_item(somestr)

def init_item (itemtype) :
    if itemtype == 'shop' :
        item = ShopItem()
        item['itemtype'] = 'shop'   #企业表信息
        temps = ['id','fetch_date','com_id','name','contactor','address','postcode','area','country','tel','phone','fax','email','qq','other','title','content','url','website','logo','logo_src','cet','photo','photo_src','reg_address','reg_money','create_time','reg_number','boss','reg_com','type','valid','custom','market','market_address','brand','money','employees','industry','range','modes','exports','imports','bank','plant_area','iso','fetch_level','fetch_reg_time','fetch_auth','fetch_auth_time','fetch_evaluate','fetch_credit','fetch_sale_data','fetch_other']
    elif itemtype == 'product' :
        item = ProductItem()
        item['itemtype'] = 'product'    #产品及产品图片表信息
        temps = ['product_id','fetch_date','p_id','com_id','name','type','photo','photo_src','price','area','sale_area','delivery_cycle','moq','total','expiry_date','publish_date','valid','brand','other','detail','companyname','purl','image_id','image','image_src']
    else :
        print 'Item Type Undefined'
        return 'Item Type Undefined'
    for temp in temps :
        item[temp] = '' #相关变量赋初值
    return item

def handle_item (item) : #处理item中的分析采集值
    if item['itemtype'] == 'shop' :
        if conf['handle_image'] :
            temps = ['logo_src','photo_src']
            for temp in temps :
                item[temp] = handle_imgsrc(item['url'],item[temp])
        temps = ['id','fetch_date','com_id','name','contactor','address','postcode','area','country','tel','phone','fax','email','qq','other','title','content','url','website','logo','logo_src','cet','photo','photo_src','reg_address','reg_money','create_time','reg_number','boss','reg_com','type','valid','custom','market','market_address','brand','money','employees','industry','range','modes','exports','imports','bank','plant_area','iso','fetch_level','fetch_reg_time','fetch_auth','fetch_auth_time','fetch_evaluate','fetch_credit','fetch_sale_data','fetch_other']
    elif item['itemtype'] == 'product' :
        if conf['handle_image'] :
            item['photo_src'] = handle_imgsrc(item['purl'],item['photo_src'])
            if item['image_src'] != '' :
                temps = item['image_src'].split('|')
                t = ''
                for temp in temps :
                    if t == '' :
                        t = handle_imgsrc(item['purl'],temp)
                    else :
                        t += '|' + handle_imgsrc(item['purl'],temp)
                item['image_src'] = t
        temps = ['product_id','fetch_date','p_id','com_id','name','type','photo','photo_src','price','area','sale_area','delivery_cycle','moq','total','expiry_date','publish_date','valid','brand','other','detail','companyname','purl','image_id','image','image_src']
    for temp in temps :
        item[temp] = replace_item(item[temp]) #完善美化采集值
        if conf['show_messages'] :
            if item[temp] != '' :
                print temp+ ' == ' + item[temp].encode(get_codetype(),'ignore')
    return item

def get_systype () :  #判断系统类型
    t = platform.platform()
    if 'Windows' in t :
        return 'windows'
    elif 'Linux' in t :
        return 'linux'
    else :
        return t

def get_codetype () : #简单判断  命令行 输出使用的字符集类型
    if get_systype() == 'windows' :
        return 'gbk'
    else :
        return 'utf8'

def handle_imgsrc (murl,imgsrc) :
    if murl == '' or imgsrc == '':
        return imgsrc
    if re.compile('^http').match(imgsrc) == None :
        if re.compile('^/').match(imgsrc) != None :
            imgsrc = '/'.join(murl.split('/')[:3]) + imgsrc
        else :
            imgsrc = '/'.join(murl.split('/')[:-1]) + '/' +imgsrc
    return imgsrc


def get_proxy () :
	proxy_list = [
		{'ip_port': '202.171.253.111:80', 'user_pass': ''},
        {'ip_port': '202.171.253.98:80', 'user_pass': ''},
        {'ip_port': '58.20.61.88:9090', 'user_pass': ''},
        {'ip_port': '210.101.131.232:8080', 'user_pass': ''},
        {'ip_port': '86.96.229.68:8888', 'user_pass': ''},
        {'ip_port': '86.96.229.123:8088', 'user_pass': ''},
        {'ip_port': '211.119.134.132:8080', 'user_pass': ''},
        {'ip_port': '61.175.223.141:3128', 'user_pass': ''},
        {'ip_port': '218.201.21.179:80', 'user_pass': ''},
        {'ip_port': '163.23.70.129:3128', 'user_pass': ''},
        {'ip_port': '111.13.87.150:80', 'user_pass': ''},
        {'ip_port': '125.39.171.194:80', 'user_pass': ''},
        {'ip_port': '125.39.171.194:82', 'user_pass': ''},
        {'ip_port': '119.18.151.121:80', 'user_pass': ''},
        {'ip_port': '77.94.48.5:80', 'user_pass': ''},
        {'ip_port': '180.180.122.214:8080', 'user_pass': ''},
        {'ip_port': '112.2.25.40:3128', 'user_pass': ''},
        {'ip_port': '62.122.101.26:80', 'user_pass': ''},
        {'ip_port': '86.96.229.68:80', 'user_pass': ''},
        {'ip_port': '210.22.115.162:3128', 'user_pass': ''},
        {'ip_port': '212.119.105.65:3128', 'user_pass': ''},
        {'ip_port': '177.84.34.178:80', 'user_pass': ''},
        {'ip_port': '124.207.15.50:80', 'user_pass': ''},
        {'ip_port': '109.69.2.197:80', 'user_pass': ''}
	]
	proxy_item =  random.choice(proxy_list)
	proxy = ''
	if proxy_item['user_pass'] == '' :
		proxy = 'http://%s' % proxy_item['ip_port']
	else :
		proxy = 'http://%s@%s' % (proxy_item['user_pass'],proxy_item['ip_port'])
	return proxy



def download_image (item) :
    if os.path.exists(imgpath) == False :
        os.mkdir(imgpath) #确认图片目录是否存在
    temps = ['logo_src','photo_src']
    for temp in temps :
        if item[temp] != '' :
            if item[temp].count('http') == 0 :
                item[temp] = mainurl + item[temp] #处理图片源url为完整路径
            filename = item[temp].split('/')[-1]
            ttemp = temp.replace('_src','')
            item[ttemp] = '/'+sitename +'/'+item['com_id']+'/'+filename
            temppath = imgpath + item[ttemp]
            if systype == 'windows' :
                temppath = temppath.replace('/','\\') #for windows linux请注释
            tempdir = imgpath+'/'+sitename +'/'+item['com_id']
            if systype == 'windows' :
                tempdir = tempdir.replace('/','\\') #for windows linux请注释
            if os.path.exists(tempdir) == False :
                os.makedirs(tempdir) #创建目录
            print 'Download:'+item[temp]+'\r\nSave As:'+temppath
            if os.path.exists(temppath) == False :
                tre = urllib2.Request(item[temp]) #加载图片URL
                trs = urllib2.urlopen(tre).read() #读取图片
                open(temppath,'wb').write(trs) #保存图片
                del tre,trs #销毁变量
            else :
                print 'Image already exist~!'
