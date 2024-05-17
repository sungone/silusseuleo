import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"    #"465"

def sendMail(MailList):
    global host, port

    html = ""   # "| "
    title = 'Eat_Today 정보 전송'
    senderAddr = "sungwon000604@gmail.com"    # 보내는 사람 email 주소
    recipientAddr = "hyuli0604@tukorea.ac.kr"   # 받는 사람 email 주소
    passwd = "script11"

    for informaion in MailList:
        #html += "[ "
        for text in informaion:
            html += text
        html += "<br>"  # "\n" " / " " | " " ]"
    print(html)

    msg = MIMEBase("multipart", "alternative")
    #msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    htmlPart = MIMEText(html, 'html', _charset='UTF-8')
    msg.attach(htmlPart)
    print("connect smtp server ... ")

    s = smtplib.SMTP(host, port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()
    print("Mail sending complete!!!")