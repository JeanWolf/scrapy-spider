##coding=utf-8
# Define some diy functions here
conf_table_prefix = 'P1_WJ_TEST_LANG'    #数据表前缀  #pipeline   eg  TEST  -->   TEST_SHOP   TEST_PRODUCT   TEST_PRODUCT_IMAGE
conf_show_messages = True   #是否打印相关调试信息  True  /  False
#-数据库配置---如需修改端口  请移步至 pipeline
conf_db_type = 'oracle'    #数据库类型 oracle  / mysql   #pipeline
conf_db_host = '172.16.4.211'  #数据库主机  #pipeline
conf_db_port = 1521
conf_db_user = 'spider' # 用户名
conf_db_pass = 'spider' # 密码
conf_db_name = 'spider' #mysql为数据库名
conf_db_sid =  'xe' # oracle sid
conf_db_sname = 'jlproject_primary' #oracle 服务名   jlproject_primary

conf_use_proxy = False  #是否使用代理
conf_handle_img = True  #是否处理图片 True / False #pipeline   一般无需修改   处理图片源路径为 http 绝对路径
conf_download_img = True   #是否下载图片 True / False #pipeline  一般无需修改
#conf_img_base_dir = '/picdir/php'    #图片存放根目录  linux    |  windows  'D:\\7788\\picdir\\php'   一般无需修改
conf_img_base_dir = 'D:\\7788\\temp' #本地测试
conf_img_save_dir = 'test_image_dir'  #该网站的图片存储目录名称
conf_retry_times = 3  #图片下载重试次数
conf_image_types = ['.png','.jpg','.gif','.jpeg']
conf_time_out = 30 #页面请求超时时间 N 秒