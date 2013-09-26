命令行下 进入当前目录
$ scrapy crawl all   #整合抓取 #建议分开 分批次抓取
$ scrapy crawl shop   #商家
$ scrapy crawl product   #产品

注意：
数据表结构，参见本目录下的 .sql文件

相关自定义配置，参见 diy/configs.py 中的配置及说明

添加 分析代码中 加载新页面的 代理使用  参见all.py中的  opener 

开启相关调试信息

添加了处理图片源路径的流程

添加了图片下载及图片本地路径处理