# NginxLogAnalysis
Analyze  log of blogs built by nginx.  
Meanwhile send mail to address of email which you provide.  
Use mutithreading.  
Significantly reduced time-consuming.  

Usage:  
[log]  
#Enter your nginx log's diretory  
log = /var/log/nginx  

[mail]  
#Your mail host  
host = 127.0.0.1  
user = admin@test.com  
pass = bmosoqkybixddhcg  
sender = admin@test.com  
receivers = test1@test.com  