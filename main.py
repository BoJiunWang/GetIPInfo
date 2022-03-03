# coding=utf-8

from urllib.request import urlopen
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import sys, smtplib, os, codecs

def GetIPWithBot():
    print('Try to get IP.')

    # Get ip via ipify
    try:
        ip = urlopen("https://api.ipify.org").read().decode()
    except (Exception) as error:
        logError(error)
        return;

    print('Get IP: {0}.'.format(ip))
    return CheckWithFile(ip)

def CheckWithFile(ip):
    fileName = "./ip.txt"
    
    try:
        # Check file is exist, if not create it
        if os.path.isfile(fileName) == False:
            codecs.open(fileName, "x", "utf-8")

        # Open file
        file = codecs.open(fileName, "r", "utf-8")

        # Check IP in file is change or not
        if file.read() != ip:
            # Send Mail first
            SendMail(sys.argv, ip)
            # Write IP to file
            file = codecs.open(fileName, "w", "utf-8")
            file.write(ip)
        else:
            print("IP not change.")
    except (Exception) as errorLog:
        print(errorLog)
    finally:
        file.close()
    
    if (ip):
        return ip

def logError(error):
    fileName = "./ip_Error.txt"

    # Log error
    try:
        # Check file is exist, if not create it
        if os.path.isfile(fileName) == False:
            codecs.open(fileName, "x", "utf-8")

        # Open file
        file = codecs.open(fileName, "w", "utf-8")
        file.write(str(error))
        print('{0} error, try to check file {1}'.format(error, fileName))
    except (Exception) as errorLog:
        print(errorLog)
    finally:
        file.close()

    return

def SendMail(argv, ip):
    print('Try to send mail.')

    # Account setting
    user = ''
    password = ''
    defaultMailAddress = ''

    # mail content
    content = '<html lang=\"zh-Hant-TW\"><head><meta charset=\"UTF-8\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+TC&display=swap\"></head><style>body {vertical-align: center;font-family: \"Noto Sans TC\", \"Helvetica Neue\", Helvetica, Arial, sans-serif;font-size: 20px;}</style><body><span>&#10071;&#10071;&#10071; IP has been change to: {ip}</span></body></html>'.replace('{ip}', ip)

    # mail setting
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'IP has been modified!'
    msg['From'] = user
    msg.attach(MIMEText(content, 'html'))

    # Check has arg or not
    if len(argv) == 2:
        msg['To'] = argv[1]
    else:
        msg['To'] = defaultMailAddress

    # mail protocol
    try:
        mailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mailServer.ehlo()
        mailServer.login(user, password)
        mailServer.send_message(msg)
        print('Mail has been sent.')
    except (Exception) as error:
        logError(error)
    finally:
        mailServer.close()

if __name__ == '__main__':
    print('Run GetIPInfo.')
    GetIPWithBot()
    print('Close GetIPInfo.')
    sleep(3)
