import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "shyapp4@gmail.com"
EMAIL_PASSWORD = "vtbv mnpj jzgg ctqy"
SEND_TO = "cecilshy8@yahoo.com"

def send_email(subject, body):
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = EMAIL_ADDRESS
msg["To"] = SEND_TO

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
server.sendmail(EMAIL_ADDRESS, SEND_TO, msg.as_string())
server.quit()
