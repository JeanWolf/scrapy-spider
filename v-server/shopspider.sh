#端口号，根据此端口号确定PID  
PORT=6800  
#启动命令所在目录  
#HOME='/data/scrapy/shopspider'  
HOME='./'  
  
#查询出监听了PORT端口TCP协议的程序  
pid=`netstat -lnopt | grep :$PORT | awk '/python/{gsub(/\/python/,"",$7);print $7;}'`  
  
  
start(){  
   if [ -n "$pid" ]; then  
	  echo "server already start,pid:$pid"  
	  return 0  
   fi  
	 
   #进入命令所在目录  
   cd $HOME  
   nohup scrapy server > server.log &   #启动scrpayd服务器 把日志输出到HOME目录的nohup.out文件中   
   echo "start at port:$PORT" 
   scrapy deploy >> server.log & 
}  
  
stop(){  
   if [ -z "$pid" ]; then  
	  echo "not find program on port:$PORT"  
	  return 0  
   fi  
	 
   #结束程序，使用讯号2，如果不行可以尝试讯号9强制结束  
   kill -2 $pid     
   echo "kill program use signal 2,pid:$pid"  
}  
  
status(){  
   if [ -z "$pid" ]; then  
	  echo "not find program on port:$PORT"  
   else  
	  echo "program is running,pid:$pid"  
   fi  
}  
  
case $1 in  
   start)  
	  start  
   ;;  
   stop)  
	  stop  
   ;;  
   status)  
	  status  
   ;;  
   *)  
	  echo "Usage: {start|stop|status}"  
   ;;  
esac  
  
exit 0  
