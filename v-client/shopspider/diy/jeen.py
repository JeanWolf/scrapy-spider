##coding=utf-8
import os,sys,re,platform,time,random,string,socket,urllib2
reload(sys)
sys.setdefaultencoding('utf8')
from shopspider.items import ShopItem,ProductItem
from shopspider.diy.configs import *
socket.setdefaulttimeout(conf_time_out)
class Jeen (object) :
    systype,codetype = 'linux','utf8' #默认
    #--读入相关配置 -------------
    show_messages = conf_show_messages
    handle_image = conf_handle_img
    download_image = conf_download_img
    image_types = conf_image_types
    img_base_dir = conf_img_base_dir
    img_save_dir = conf_img_save_dir
    retry_times = conf_retry_times
    use_proxy = conf_use_proxy
    start_time = time.time()
    def __init__(self) : #初始化
        self.systype = self.get_systype()
        self.codetype = self.get_codetype()

    def get_type (self,tobj=None) : #返回数据类型
        t = str(type(tobj))
        t = t.replace("<type '","")
        t = t.replace("'>","")
        return t

    def get_systype (self) :  #判断系统类型
        t = platform.platform()
        if 'Windows' in t :
            return 'windows'
        elif 'Linux' in t :
            return 'linux'
        else :
            return t

    def get_codetype (self) : #简单判断  命令行 输出使用的字符集类型
        if self.systype == 'windows' :
            return 'gbk'
        else :
            return 'utf8'

    def get_runtime (self) : #获取运行时间
        now_time = time.time()
        return now_time - self.start_time

    def strtrim(self,oldstr) : #去除字符串空格
        if oldstr == None :
            newstr = ''
        else :
            newstr = strip(oldstr)
        return newstr

    def show_msg (self,msg='') : #打印 提示信息
        msg = str(msg)
        if msg == '' :
            print '\t---\t---\t---\t---\t---'
            return 0
        else :
            #print msg.decode('utf8','ignore').encode(self.codetype,'ignore')
            print msg.encode(self.codetype,'ignore')
            return 1

    def list_unique(self,old_list): # 序列唯一化
        newList = []
        for x in old_list:
            if x not in newList :
                newList.append(x)
        return newList

    def handle_imgsrc (self,murl,imgsrc) : #处理图片源路径
        if murl == '' or imgsrc == '':
            return imgsrc
        if re.compile('^http').match(imgsrc) == None :
            if re.compile('^/').match(imgsrc) != None :
                imgsrc = '/'.join(murl.split('/')[:3]) + imgsrc
            else :
                imgsrc = '/'.join(murl.split('/')[:-1]) + '/' +imgsrc
        return imgsrc

    def handle_path (self,path) : # 处理文件名 并 检测文件后缀
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        title = os.path.splitext(file_name)[0]
        ext = string.lower(os.path.splitext(file_name)[1])
        if ext == '' or ext not in self.image_types :
            ext = '.jpg'
        title = self.validateTitle(title)
        return '%s/%s%s' % (dir_name,title,ext)

    def validateTitle(self,title): #处理Windows下文件名中的非法字符
    	rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    	new_title = re.sub(rstr, "", title)
    	return new_title


    def replace_item (self, somestr) : #字符串处理函数
        t = self.get_type(somestr)
        if t == 'str' :
            somestr = somestr.replace(u'\xa0',' ')
            somestr = somestr.replace('\t','')
            somestr = somestr.replace('\r','')
            somestr = somestr.replace('\n','')
            somestr = somestr.replace('   ','')
            return somestr
        elif t == 'list' or t == 'tuple' :
            somestr = ''.join(somestr)
            return self.replace_item(somestr)
        else :
            somestr = str(somestr).encode('utf8','ignore')
            return self.replace_item(somestr)

    def init_item (self, itemtype) :
        if itemtype == 'shop' :
            item = ShopItem()
            item['itemtype'] = 'shop'   #企业表信息
            temps = ['id','fetch_date','com_id','name','contactor','address','postcode','area','country','tel','phone','fax','email','qq','other','title','content','url','website','logo','logo_src','cet','photo','photo_src','reg_address','reg_money','create_time','reg_number','boss','reg_com','type','valid','custom','market','market_address','brand','money','employees','industry','range','modes','exports','imports','bank','plant_area','iso','fetch_level','fetch_reg_time','fetch_auth','fetch_auth_time','fetch_evaluate','fetch_credit','fetch_sale_data','fetch_other']
        elif itemtype == 'product' :
            item = ProductItem()
            item['itemtype'] = 'product'    #产品及产品图片表信息
            temps = ['product_id','fetch_date','p_id','com_id','name','type','photo','photo_src','price','area','sale_area','delivery_cycle','moq','total','expiry_date','publish_date','valid','brand','other','detail','companyname','purl','image_id','image','image_src']
        else :
            self.show_msg("Item Type Undefined,item['itemtype'] 未初始化")
            return 'Item Type Undefined'
        for temp in temps :
            item[temp] = '' #相关变量赋初值
        return item

    def handle_item (self, item) : #处理item中的分析采集值
        if item['itemtype'] == 'shop' :
            if self.handle_image :
                temps = ['logo_src','photo_src']
                for temp in temps :
                    if item[temp] != '' :
                        item[temp] = self.handle_imgsrc(item['url'],item[temp])
                        t_img_file = item[temp].split('/')[-1]
                        t_img = '/%s/%s/%s' % (self.img_save_dir,item['com_id'],t_img_file)
                        t_img = self.handle_path(t_img)
                        item[temp.replace('_src','')] = t_img
                        if self.download_image :
                            self.downloadImage(t_img,item[temp])
            temps = ['id','fetch_date','com_id','name','contactor','address','postcode','area','country','tel','phone','fax','email','qq','other','title','content','url','website','logo','logo_src','cet','photo','photo_src','reg_address','reg_money','create_time','reg_number','boss','reg_com','type','valid','custom','market','market_address','brand','money','employees','industry','range','modes','exports','imports','bank','plant_area','iso','fetch_level','fetch_reg_time','fetch_auth','fetch_auth_time','fetch_evaluate','fetch_credit','fetch_sale_data','fetch_other']
        elif item['itemtype'] == 'product' :
            if self.handle_image :
                if item['photo_src'] != '' :
                    item['photo_src'] = self.handle_imgsrc(item['purl'],item['photo_src'])
                    t_file = item['photo_src'].split('/')[-1] #文件名
                    t_photo = '/%s/%s/%s/%s' % (self.img_save_dir,item['com_id'],item['p_id'],t_file)
                    t_photo = self.handle_path(t_photo)
                    item['photo'] = t_photo
                    if self.download_image :
                        self.downloadImage(t_photo,item['photo_src'])
                if item['image_src'] != '' :
                    temps = item['image_src'].split('|')
                    t,t_src = '',''
                    for temp in temps :
                        image_src = self.handle_imgsrc(item['purl'],temp)
                        t_file = image_src.split('/')[-1] #文件名
                        t_image = '/%s/%s/%s/%s' % (self.img_save_dir,item['com_id'],item['p_id'],t_file)
                        t_image = self.handle_path(t_image)
                        if t == '' :
                            t_src = image_src
                            t = t_image
                        else :
                            t_src += '|' + image_src
                            t += '|' + t_image
                        if self.download_image :
                            self.downloadImage(t_image,image_src)
                    item['image_src'] = t_src
                    item['image'] = t
            temps = ['product_id','fetch_date','p_id','com_id','name','type','photo','photo_src','price','area','sale_area','delivery_cycle','moq','total','expiry_date','publish_date','valid','brand','other','detail','companyname','purl','image_id','image','image_src']
        for temp in temps :
            item[temp] = self.replace_item(item[temp]) #完善美化采集值
            if self.show_messages :
                if item[temp] != '' :
                    self.show_msg('%s == %s' % (temp, item[temp]))
        return item

    def get_user_agent (self) :
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
            'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.8pre) Gecko/20071001 Firefox/2.0.0.7 Navigator/9.0RC1',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.11pre) Gecko/20071206 Firefox/2.0.0.11 Navigator/9.0.0.5',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.11pre) Gecko/20071206 Firefox/2.0.0.11 Navigator/9.0.0.5',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20070321 Netscape/9.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
            'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
            'Mozilla/5.0 (X11; U; Linux amd64) Iron/21.0.1200.0 Chrome/21.0.1200.0 Safari/537.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.4a) Gecko/20030403 Phoenix/0.5',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.3a) Gecko/20030101 Phoenix/0.5',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.3a) Gecko/20021207 Phoenix/0.5',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2b) Gecko/20021029 Phoenix/0.4'
        ]
        return random.choice(user_agent_list)

    def get_proxy (self) :
        proxy_list = [
            {'ip_port': '192.227.139.227:7808', 'user_pass': ''},
            {'ip_port': '198.27.79.149:7808', 'user_pass': ''},
            {'ip_port': '208.110.83.204:8089', 'user_pass': ''},
            {'ip_port': '68.180.195.138:80', 'user_pass': ''},
            {'ip_port': '63.141.249.37:8089', 'user_pass': ''},
            {'ip_port': '172.245.9.56:7808', 'user_pass': ''},
            {'ip_port': '89.222.212.86:8080', 'user_pass': ''},
            {'ip_port': '198.50.171.253:8089', 'user_pass': ''},
            {'ip_port': '192.227.137.47:7808', 'user_pass': ''},
            {'ip_port': '208.110.83.205:8089', 'user_pass': ''},
            {'ip_port': '208.110.83.205:7808', 'user_pass': ''},
            {'ip_port': '31.131.30.161:3128', 'user_pass': ''},
            {'ip_port': '69.197.132.80:7808', 'user_pass': ''},
            {'ip_port': '204.84.216.200:8080', 'user_pass': ''},
            {'ip_port': '208.110.83.206:7808', 'user_pass': ''},
            {'ip_port': '147.31.182.137:80', 'user_pass': ''},
            {'ip_port': '208.110.83.204:7808', 'user_pass': ''},
            {'ip_port': '172.245.9.56:8089', 'user_pass': ''},
            {'ip_port': '199.115.231.51:3128', 'user_pass': ''},
            {'ip_port': '208.110.83.204:3128', 'user_pass': ''},
            {'ip_port': '212.156.86.242:8080', 'user_pass': ''},
            {'ip_port': '210.101.131.232:8080', 'user_pass': ''},
            {'ip_port': '211.119.134.132:8080', 'user_pass': ''},
            {'ip_port': '58.252.56.148:9000', 'user_pass': ''},
            {'ip_port': '198.50.241.160:8089', 'user_pass': ''},
            {'ip_port': '91.228.53.28:8089', 'user_pass': ''},
            {'ip_port': '208.110.83.203:8089', 'user_pass': ''},
            {'ip_port': '58.20.223.230:3128', 'user_pass': ''},
            {'ip_port': '59.65.233.132:80', 'user_pass': ''},
            {'ip_port': '5.199.166.250:7808', 'user_pass': ''},
            {'ip_port': '202.171.253.111:80', 'user_pass': ''},
            {'ip_port': '202.171.253.98:80', 'user_pass': ''},
            {'ip_port': '218.201.21.179:80', 'user_pass': ''},
            {'ip_port': '110.4.24.170:80', 'user_pass': ''},
            {'ip_port': '110.4.12.170:81', 'user_pass': ''},
            {'ip_port': '110.4.12.170:82', 'user_pass': ''},
            {'ip_port': '118.97.205.154:2020', 'user_pass': ''},
            {'ip_port': '111.13.87.150:80', 'user_pass': ''},
            {'ip_port': '218.197.148.4:21', 'user_pass': ''},
            {'ip_port': '124.195.52.21:3128', 'user_pass': ''},
            {'ip_port': '163.23.70.129:3128', 'user_pass': ''},
            {'ip_port': '119.167.231.73:8080', 'user_pass': ''},
            {'ip_port': '112.2.25.40:3128', 'user_pass': ''},
            {'ip_port': '119.18.151.121:80', 'user_pass': ''},
            {'ip_port': '218.108.85.59:80', 'user_pass': ''},
            {'ip_port': '202.58.96.56:80', 'user_pass': ''},
            {'ip_port': '62.122.101.26:80', 'user_pass': ''},
            {'ip_port': '121.14.9.76:110', 'user_pass': ''},
            {'ip_port': '119.254.90.18:8080', 'user_pass': ''},
            {'ip_port': '177.84.34.178:80', 'user_pass': ''},
            {'ip_port': '121.14.9.76:80', 'user_pass': ''},
            {'ip_port': '124.207.15.50:80', 'user_pass': ''}
        ]
        proxy_item =  random.choice(proxy_list)
        proxy = ''
        if proxy_item['user_pass'] == '' :
            proxy = 'http://%s' % proxy_item['ip_port']
        else :
            proxy = 'http://%s@%s' % (proxy_item['user_pass'],proxy_item['ip_port'])
        return proxy

    def getItemType(self,tablename) :
        tb = tablename.split('_')
        if tb[-1] == 'SHOP' :
            return 'shop'
        elif tb[-1] == 'PRODUCT' :
            return 'product'
        elif tb[-1] == 'IMAGE' :
            return 'productimage'
        else :
            return 'undefined'

    def downloadImage(self, path, src) : #存储相对路径， 图片源地址
        real_path = self.img_base_dir + path #绝对路径
        print real_path,'|',path,'|',src
        t_name = path.split('/')[-1]
        t_dir = real_path.split(t_name)[0]
        if os.path.exists(t_dir) == False :#判断目录是否存在
            os.makedirs(t_dir) #创建目录
        i = 0
        if os.path.exists(real_path) == False and i < self.retry_times :
            i = i + 1
            user_agent = { 'User-Agent' : self.get_user_agent() }  # 使用随机的 User-Agent
            if self.use_proxy :
                proxy_handle = urllib2.ProxyHandler({ 'http' : self.get_proxy() })
                opener = urllib2.build_opener(proxy_handle)
                try:
                    tre = urllib2.Request(src,headers = user_agent)
                    trs = opener.open(tre)
                except :
                    print 'some error with use proxy'
                    trs = 'some_error'
            else :
                try:
                    tre = urllib2.Request(src,headers = user_agent)
                    trs = urllib2.urlopen(tre)
                except :
                    print 'some error with no_use_proxy'
                    trs = 'some_error'
            try :
                if trs != 'some_error' :
                    trs = trs.read()
                    open(real_path,'wb').write(trs) #保存图片
                else :
                    self.show_msg('图片地址异常：%s' % src)
            except :
                pass
        if os.path.exists(real_path) == False : #下载 保存 失败
            self.show_msg('++++++++++++++++%s 下载失败 ~~~' % src)
            return 0
        else : #下载成功  返回 1
            return 1
        pass
