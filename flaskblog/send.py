import qrcode 
import random
from random import randint
from flaskblog.models import Mail

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pyqrcode as qr
import png
import sys

def run_file():
    x = random.randint(1000, 9999)
    generate_image = qrcode.make(x)
    generate_image.save("QRCODE1.png")
    print(x)
    print(generate_image)
    return 1

def mail(email):
    from_email = 'deliveryditto@gmail.com'
    to_email = email

    msg = MIMEMultipart('alternative')
    msg['From'] =from_email
    msg['To'] = to_email
    msg['Subject'] = 'TEST TEST'
    html_file = "email.html"

    with open(html_file, 'r') as f:
        html_attachment = MIMEText(f.read(), 'html')
        msg.attach(html_attachment)

    qr_code_file='QRCODE1.png'

    with open(qr_code_file, 'rb') as f:
        qr_code_attachment = MIMEBase('application', 'octet-stream')
        qr_code_attachment.set_payload((f).read())
        encoders.encode_base64(qr_code_attachment)
        qr_code_attachment.add_header('Content-Disposition', "attachment; filename= %s" % qr_code_file)
        msg.attach(qr_code_attachment)

    msg_str = msg.as_string()

    email_session = smtplib.SMTP('smtp.gmail.com', 587)
    email_session.starttls()
    email_session.login(from_email, 'gkbltrhhngtfsxrm')

    email_session.sendmail(from_email, to_email, msg_str)
    email_session.quit()
    return 1

if __name__ == "__main__":
    email = sys.argv[1]
    run_file()
    mail(email)
