import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    try:
        sender = "shyapp4@gmail.com"
        password = "vtbv mnpj jzgg ctqy"
        receiver = "cecilshy8@yahoo.com"
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        print("✅ Email Sent!")

    except Exception as e:
        print("Email Error:", e)
