import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import threading

email_sender = '******'
email_receiver = '******'
email_password = '******'

def send_email(image_path):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = 'Human Detected'
    body = 'Human detected in the camera frame.'
    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_receiver, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def email_sender_thread(file_path):
    email_thread = threading.Thread(target=send_email, args=(file_path,))
    email_thread.start()
