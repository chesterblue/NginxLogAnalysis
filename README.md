# NginxLogAnalysis
## Based on Python3
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
pass = xxxxxxxxxxxxxxxx  
sender = admin@test.com  
receivers = test1@test.com  

How to make this procedure work:  
You need to write fllowing to /etc/cron.d  
### First: 
cd /etc/cron.d  
vim newcronfile
### Second:  
SHELL=/bin/bash  
PATH=/sbin:/bin:/usr/sbin:/usr/bin  
MAILTO=root  
HOME=/root/test/NginxLogAnalysis #The directory where your procedure is located  
27 22 * * * root python /root/test/NginxLogAnalysis/main.py  
  
### You can restart the service if necessary
