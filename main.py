import re, json, queue, log, os, datetime, configparser
from requests import *
from mail import *
from threading import Thread

''' global variates '''
logo=r'''
 _   _ _                   _                _           _     
| \ | | |    ___   __ _   / \   _ __   __ _| |_   _ ___(_)___ 
|  \| | |   / _ \ / _` | / _ \ | '_ \ / _` | | | | / __| / __|
| |\  | |__| (_) | (_| |/ ___ \| | | | (_| | | |_| \__ \ \__ \
|_| \_|_____\___/ \__, /_/   \_\_| |_|\__,_|_|\__, |___/_|___/
                  |___/                       |___/                 v0.1
'''

IPlst=[] #IP类列表
s=session()
config=configparser.ConfigParser()
dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = dir+"/config.ini"
config.read(config_file_path,encoding='utf-8')

class IPinfo:
    def __init__(self,ip,count):
        self.ip=ip
        self.count=count
    def addInfo(self,stats):
        self.stats=stats
    def getIP(self):
        return self.ip
    def getInfo(self):
        return self.stats
    def getCount(self):
        return self.count

# gunzip log file
def gunzip_log():
    today = datetime.date.today()
    today_string = str(today) #'2020-09-09'
    date_lst = today_string.split('-')
    today_date = ''.join(date_lst)
    log_root = config.get('log', 'log')
    from_file = log_root+"/access.log-"+today_date+".gz"
    to_file = dir+"/access.log"
    #gunzip -c $file > /root/NginxLogAnalysis/access.log
    shell = "gunzip -c %s > %s"%(from_file,to_file)
    os.system(shell)

# 读取日志文件
def ReadIP():
    pat = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    filepath = dir+"/access.log"
    logFile = open(filepath,"r")
    info = logFile.read()
    #匹配日志中的IP
    IPS=pat.findall(info)
    logFile.close()
    return IPS

# 整理IP
def OrginizeData(IPS):
    IPset={}
    for ip in IPS:
        if ip in IPset:
            IPset[ip]+=1
        else:
            IPset[ip]=1
    return IPset

# 查询IP信息
def QueryIP(ip):
    url="http://ip-api.com/json/"+ip
    html=s.get(url)
    content=html.content
    stats=json.loads(content)
    return stats

# 添加IP对象到列表
def addList(ip,count,stats):
    global IPlst
    ipinfo=IPinfo(ip,count)
    ipinfo.addInfo(stats)
    IPlst.append(ipinfo)

# 初始化队列
def InitQueue(query_queue,IPset):
    for IPTuple in IPset.items():
        query_queue.put(IPTuple)

# 多线程循环查询IP
def MultiThreadHandleIP(query_queue,IPset):
    while not query_queue.empty():
        IPTuple=query_queue.get(block = True,timeout = 1)
        stats=QueryIP(IPTuple[0])
        addList(IPTuple[0],IPTuple[1],stats)
        query_queue.task_done()

# 多线程
def MultiThread(ThreadNum,query_queue,IPset):
    for i in range(ThreadNum):
        t=Thread(target=MultiThreadHandleIP,args=(query_queue,IPset))
        t.start()

# 输出查询IP后的信息
def PrintInfo(ipinfo):
    ip=ipinfo.getIP()
    count=ipinfo.getCount()
    stats=ipinfo.getInfo()
    print("IP:",ip)
    print("Count: ",count)
    if stats['status']=="success":
        print("Country：",stats['country'])
        print("CountryCode：",stats['countryCode'])
        print("RegionName：",stats['regionName'])
        print("City：",stats['city'])
        print("Lat",stats['lat'])
        print("Lon",stats['lon'])
        print("Timezone",stats['timezone'])   
    else:
        print("非法IP")
    print("-------------------------------")

def sortByCount():
    global IPlst
    IPlst=sorted(IPlst, key=lambda ipinfo: ipinfo.count,reverse=True) 

def main():
    print(logo)
    gunzip_log()
    log.write("Gunzip nginx's logs to my space")
    IPS=ReadIP() #从文件中读取IP
    log.write("Read IP from log")
    IPset=OrginizeData(IPS) #处理重复IP
    log.write("Orginize Data")
    query_queue=queue.Queue(len(IPset))
    log.write("new queue")
    InitQueue(query_queue,IPset)
    log.write("Init Queue")
    MultiThread(10,query_queue,IPset)
    log.write("use MutilThread")
    query_queue.join()
    sortByCount()
    log.write("Sorted")
    # for ipinfo in IPlst:
    #     PrintInfo(ipinfo)
    log.write("Print Information")
    html=generateHTML(IPlst)
    sendMail(html)
    log.write("send mail")
    


if __name__=="__main__":
    main()
