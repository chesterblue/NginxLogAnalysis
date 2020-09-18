from smtplib import *
from email.mime.text import MIMEText
from email.header import Header
import datetime, configparser, os

class mail:
    def __init__(self,_host="localhost",_user="",_pass=""):
        self._host = _host
        self._user = _user
        self._pass = _pass
    def setPara(self,sender,receivers):
        self.sender = sender
        self.receivers = receivers
    def initMess(self,subject,fromHeader,toHeader,content,minorType="plain"):
        self.message = MIMEText(content, minorType, 'utf-8')      #内容
        self.message['Subject'] = Header(subject, 'utf-8')      #主题
        self.message['From'] = Header(fromHeader, 'utf-8')      #发送方名
        self.message['To'] = Header(toHeader, 'utf-8')          #接收方名
    def sendMail(self):
        try:
            # Linux
            self.smtpObj = SMTP(self._host,587)
            # Windows
            # self.smtpObj = SMTP()
            # self.smtpObj.connect(self._host, '25')
            self.smtpObj.login(self._user,self._pass)
            self.smtpObj.sendmail(self.sender, self.receivers, self.message.as_string())
            print ("邮件发送成功")
        except SMTPServerDisconnected:
            print("服务器连接错误")
        except SMTPSenderRefused:
            print ("发送者拒绝")
        except SMTPRecipientsRefused:
            print ("接收方拒绝")
        except SMTPDataError:
            print ("数据错误")
        except SMTPConnectError:
            print ("连接错误")
        except SMTPHeloError:
            print ("Hello拒收")
        except SMTPAuthenticationError:
            print ("认证失败")
        except SMTPException:
            print("Error")

def generateHTML(IPlst):
    html=r""
    for ipinfo in IPlst:
        stats=ipinfo.getInfo()
        if stats['status']=="success":
            html+=r"""<tr>"""
            html+=r"""<td bgcolor="#f2fbfe">"""
            html+=ipinfo.getIP()
            html+=r"</td>"
            html+=r"<td>"
            html+=stats['country']
            html+=r"</td>"
            html+=r"""<td bgcolor="#f2fbfe">"""
            html+=stats['countryCode']
            html+=r"</td>"
            html+=r"<td>"
            html+=stats['regionName']
            html+=r"</td>"
            html+=r"""<td bgcolor="#f2fbfe">"""
            html+=stats['city']
            html+=r"</td>"
            html+=r"<td>"
            html+=str(stats['lat'])
            html+=r"</td>"
            html+=r"""<td bgcolor="#f2fbfe">"""
            html+=str(stats['lon'])
            html+=r"</td>"
            html+=r"<td>"
            html+=stats['timezone']
            html+=r"</td>"
            html+=r"""<td bgcolor="#f2fbfe">"""
            html+=str(ipinfo.getCount())
            html+=r"</td>"
    return html

def sendMail(html):
    date=str(datetime.date.today())
    config = configparser.ConfigParser()
    dir = os.path.dirname(os.path.abspath(__file__))
    filepath = dir + "/config.ini"
    config .read(filepath,encoding='utf-8')
    mail_host = config.get('mail', 'host') #设置邮件服务器地址
    mail_user = config.get('mail', 'user') #用户名
    mail_pass = config.get('mail', 'pass') #口令 
    sender = config.get('mail', 'sender') #发送方
    receivers = [config.get('mail','receivers')] #接收邮件方
    subject = '%s Nginx 日志分析结果'%(date)
    fromHeader = "NginxLog"
    toHeader = "Admin"
    content=r"""<!DOCTYPE html>
<html lang="en">
  <meta name="viewport" content="width=device-width">
  <meta http-equiv="Content-Type" content="text/html; charset=US-ASCII">
  <title>Nginx's Logs</title>
  <body>
    <table border="0" bgcolor="#cccccc">
      <tr bgcolor="#e9faff">
        <th>IP</th>
        <th>Country</th>
        <th>CountryCode</th>
        <th>RegionName</th>
        <th>City</th>
        <th>Lat</th>
        <th>Lon</th>
        <th>Timezone</th>
        <th>Count</th>
      </tr>
      %s
    </table>
    </body>
</html>"""%(html)
    minorType = "html"  #发送html格式的邮件（默认为palin类型）
    newMail = mail(mail_host,mail_user,mail_pass)
    newMail.setPara(sender,receivers)
    newMail.initMess(subject,fromHeader,toHeader,content,minorType)
    newMail.sendMail()