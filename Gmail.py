import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = "smtp.gmail.com"  # Gmail SMTP 서버 주소
port = 587  # STARTTLS를 위한 포트 번호

def sendMail(MailList):
    global host, port

    html = ""  # 이메일 본문 내용
    title = '시루 가맹점 리스트 정보 전송'
    senderAddr = "hyuli0604@tukorea.ac.kr"  # 보내는 사람 이메일 주소
    recipientAddr = "sungwon000604@gmail.com"  # 받는 사람 이메일 주소
    passwd = "xjgg dssm viwv essm"  # 실제 앱 비밀번호로 변경 필요

    for information in MailList:
        for text in information:
            html += text
        html += "<br>"

    print(html)  # 이메일 본문 내용 출력

    msg = MIMEMultipart("alternative")
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    htmlPart = MIMEText(html, 'html', _charset='UTF-8')
    msg.attach(htmlPart)

    print("connect smtp server ...")

    try:
        s = smtplib.SMTP(host, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, passwd)
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()
        print("Mail sending complete!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTPAuthenticationError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")