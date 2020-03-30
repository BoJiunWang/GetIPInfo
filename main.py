# coding=utf-8

from urllib.request import urlopen
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import sys, smtplib, os, codecs

def GetIPWithBot():
    print('Try to get IP.')

    # Get ip via whatismyipaddress
    url = urlopen("https://bot.whatismyipaddress.com")
    ip = url.read().decode()

    print('Get IP: {0}.'.format(ip))
    return CheckWithFile(ip)

def CheckWithFile(ip):
    # Check file is exist, if not create it
    if os.path.isfile('./ip.txt') == False:
       codecs.open("./ip.txt", "x", "utf-8")

    # Open file
    file = codecs.open("./ip.txt", "r", "utf-8")

    # Check IP in file is change or not
    if file.read() != ip:
        file = codecs.open("./ip.txt", "w", "utf-8")
        file.write(ip)
        SendMail(sys.argv, ip)
    else:
        print("IP not change.")

    return ip

def SendMail(argv, ip):
    print('Try to send mail.')

    # Account setting
    user = 'userAccount'
    password = 'userPassword'

    # mail content
    content = '<html lang=\"zh-Hant-TW\"><head><meta charset=\"UTF-8\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=Noto+Sans+TC\"></head><style>body {vertical-align: center;font-family: \"Noto Sans TC\", \"Helvetica Neue\", Helvetica, Arial, sans-serif;font-size: 20px;}</style><body><span>&#10071;&#10071;&#10071; IP has been change to: {ip}</span></body></html>'.replace('{ip}', ip)
    
    # mail setting
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'IP has been modified!'
    msg['From'] = user
    msg.attach(MIMEText(content, 'html'))

    # Check has arg or not
    if len(argv) == 2:
        msg['To'] = argv[1]
    else:
        msg['To'] = 'defaultRecipient'

    # mail protocol
    try:
        mailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mailServer.ehlo()
        mailServer.login(user, password)
        mailServer.send_message(msg)
        print('Mail has been sent.')
    except (Exception) as error:
        print('Exception: {0}'.format (error.__class__.__name__))
    finally:
        mailServer.close()

if __name__ == '__main__':
    print('Run GetIPInfo.')
    GetIPWithBot()
    print('Close GetIPInfo.')
    sleep(3)
