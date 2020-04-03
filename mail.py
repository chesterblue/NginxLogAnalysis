from smtplib import *
from email.mime.text import MIMEText
from email.header import Header
  
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
            self.smtpObj = SMTP_SSL(self._host)
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

