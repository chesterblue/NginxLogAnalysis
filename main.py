import re
import json
from requests import *
from mail import *
from threading import Thread

logo=r'''
 _   _ _                   _                _           _     
| \ | | |    ___   __ _   / \   _ __   __ _| |_   _ ___(_)___ 
|  \| | |   / _ \ / _` | / _ \ | '_ \ / _` | | | | / __| / __|
| |\  | |__| (_) | (_| |/ ___ \| | | | (_| | | |_| \__ \ \__ \
|_| \_|_____\___/ \__, /_/   \_\_| |_|\__,_|_|\__, |___/_|___/
                  |___/                       |___/                 v0.1
'''

s=session()
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

'''
    读取日志文件
'''
def ReadIP():
    pat=re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

    logFile=open("G:\\安全学习资料\\python网络\\python\\流量分析\\access.log","r")
    info=logFile.read()
    #匹配日志中的IP
    IPS=pat.findall(info)
    return IPS

'''
    整理IP
'''
def OrginizeData(IPS):
    IPset={}
    for ip in IPS:
        if ip in IPset:
            IPset[ip]+=1
        else:
            IPset[ip]=1
    return IPset
'''
    查询IP信息
'''
def QueryIP(ip):
    url="http://ip-api.com/json/"+ip
    html=s.get(url)
    content=html.content
    stats=json.loads(content)
    return stats
'''
    添加IP对象到列表
'''
def addList(IPlst,ip,count,stats):
    ipinfo=IPinfo(ip,count)
    ipinfo.addInfo(stats)
    IPlst.append(ipinfo)

def HandleIP(IPset):
    IPlst=[]
    for ip in IPset.items():
        stats=QueryIP(ip[0])
        addList(IPlst,ip[0],ip[1],stats)
    return IPlst

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

# def modifyHTML():
#     goto
def sortByCount(IPlst):
    return sorted(IPlst, key=lambda ipinfo: ipinfo.count,reverse=True) 

def sendMail():
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="2958931649@qq.com"    #用户名
    mail_pass="yyrthptqjsuodgga"   #口令 
    sender = '2958931649@qq.com'    #发送方
    receivers = ['1191975374@qq.com']  # 接收邮件
    subject = 'Python SMTP HTML测试'
    fromHeader = "NginxLog"
    toHeader = "Admin"
    content = """<a href="https://www.relish.fun">博客网站</a>"""
    minorType = "html"  #发送html格式的邮件（默认为palin类型）
    newMail = mail(mail_host,mail_user,mail_pass)
    newMail.setPara(sender,receivers)
    newMail.initMess(subject,fromHeader,toHeader,content,minorType)
    newMail.sendMail()
def main():
    print(logo)
    IPS=ReadIP()
    IPset=OrginizeData(IPS)
    IPlst=HandleIP(IPset)
    IPlst=sortByCount(IPlst)
    for ipinfo in IPlst:
        PrintInfo(ipinfo)
    # sendMail()
    


if __name__=="__main__":
    main()
