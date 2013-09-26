Scrapy 服务端代码 （上传运行自己的spider之前，请务必做好核查测试工作）
基于Scrapy-Spider重构
将相关数据库配置 整合到item中，已满足 不同spider 对应不同数据表的需求
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

建议在运行之前 先在服务器端查看 其他已运行的 蜘蛛对应的 进程pid
# ps -au |grep scrapy
避免在结束自己的抓取程序时  错误的结束了其他抓取程序

如需结束对应项目  请先检索相关的pid  然后kill之
# ps -au |grep scrapy
# kill -2 thepid
建议在抓取之前 严格检查 测试，并移除不必要的调试信息，避免log文件过大

同台服务器中 只能开启一个 scrapy server
上传运行对应的抓取项目前  请先进行确认，避免冲突
（注意spider的名称  及 class名称不要重复）



