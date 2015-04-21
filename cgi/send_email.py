import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender = 'xiao67@purdue.edu'
    receiver='xiao67@purdue.edu'
    msg = MIMEText("")
    msg['Subject'] = 'IUsucks'
    msg['From'] ="nobody@gmail.com"
    msg['To'] =receiver 
   
    smtpObj = smtplib.SMTP('localhost')
    
    smtpObj.sendmail(sender, receiver, msg.as_string())
send_email()
