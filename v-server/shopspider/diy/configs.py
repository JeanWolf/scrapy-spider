##coding=utf-8
# Define some diy functions here
table_prefix = 'P1_WJ_TEST_LANG'    #数据表前缀  #pipeline   eg  TEST  -->   TEST_SHOP   TEST_PRODUCT   TEST_PRODUCT_IMAGE
show_messages = True   #是否打印相关调试信息  True  /  False
#-数据库配置---如需修改端口  请移步至 pipeline
db_type = 'oracle'    #数据库类型 oracle  / mysql   #pipeline
db_host = '172.16.4.211'  #数据库主机  #pipeline
db_user = 'spider' # 用户名
db_pass = 'spider' # 密码
db_name = 'spider' #mysql为数据库名
db_sid =  'xe' # oracle为服务名   jlproject_primary
handle_image = True  #是否处理图片 True / False #pipeline   一般无需修改   处理图片源路径为 http 绝对路径
download_image = False   #是否下载图片 True / False #pipeline  一般无需修改
image_dir = '/picdir/php'    #图片存放根目录  linux    | windows  'D:\\7788\\picdir\\php'   一般无需修改

global conf
conf = {
    'table_prefix' : table_prefix,
    'show_messages' : show_messages,
    'db_type' : db_type,
    'db_host' : db_host,
    'db_user' : db_user,
    'db_pass' : db_pass,
    'db_name' : db_name,
    'db_sid' : db_sid,
    'handle_image' : handle_image,
    'download_image' : download_image,
    'image_dir' : image_dir
}

#if conf['show_messages'] :