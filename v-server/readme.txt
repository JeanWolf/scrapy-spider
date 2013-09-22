--------new
基于Scrapy-Spider重构
将相关数据库配置 整合到item中，已满足 不同spider 对应不同数据表的重构需求
更新同条数据需要分析多个页面的解决方案
统一开启代理IP，更新全局超时时间为30秒


进入项目目录后
执行 shopspider.sh shell脚本
# ./shopspider.sh start
然后ssh终端 就可以退出了

在其他支持curl命令的终端
# curl http://serverhost:6800/schedule.json -d project=shopspider -d spider=product
其中
serverhost为项目所在服务器的ip或域名
shopspider为本项目的名称  
product为蜘蛛的名称

如需结束对应项目  请先检索相关的pid  然后kill之
# ps -au |grep scrapy
# kill -2 thepid
建议在抓取之前 严格检查 测试，并移除不必要的调试信息，避免log文件过大

同台服务器中 只能开启一个 scrapy server
上传运行对应的抓取项目前 请先进行确认，避免冲突

--------old
命令行下 进入当前目录
$ scrapy crawl all   #整合抓取 测试用
$ scrapy crawl shop   #商家
$ scrapy crawl product   #产品

注意：
数据表结构，参见本目录下的 .sql文件
相关自定义配置，参见 diy/configs.py 中的配置及说明

添加了处理图片源路径的流程

暂未提供图片下载及图片本地路径处理

2013-7-31
添加 分析代码中 加载新页面的 代理使用  参见all.py中的  opener 
开启相关调试信息

