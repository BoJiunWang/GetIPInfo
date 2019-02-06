# coding=utf-8

from urllib.request import urlopen
from email.mime.text import MIMEText
from time import sleep
import sys, smtplib, os, codecs

def GetIPWithBot():
    print('Try to get IP.')
    url = urlopen("https://bot.whatismyipaddress.com")
    ip = url.read().decode()
    print('Get IP: {0}.'.format(ip))
    return CheckWithFile(ip)

def CheckWithFile(ip):
    if os.path.isfile('./ip.txt') == False:
       codecs.open("./ip.txt", "x", "utf-8")
    file = codecs.open("./ip.txt", "r", "utf-8")
    if file.read() != ip:
        file = codecs.open("./ip.txt", "w", "utf-8")
        file.write(ip)
        SendMail(sys.argv, ip)
    else:
        print("IP not change.")
    return ip

def SendMail(argv, content):
    print('Try to send mail.')
    user = 'userName'
    password = 'userPassword'
    msg = MIMEText(content)
    msg['Subject'] = 'IP has been modified!'
    msg['From'] = user
    if len(argv) == 2:
        msg['To'] = argv[1]
    else:
        msg['To'] = 'default mail address'
    mailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mailServer.ehlo()
    mailServer.login(user, password)
    mailServer.send_message(msg)
    mailServer.quit()
    print('Mail has been sent.')

if __name__ == '__main__':
    print('Run GetIPInfo.')
    GetIPWithBot()
    print('Close GetIPInfo.')
    sleep(3)