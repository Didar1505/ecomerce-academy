import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server="smtp.mailersend.net", port=587):
        self.sender = "MS_UPUx9R@test-y7zpl98xdzp45vx6.mlsender.net"
        self.password = "mssp.HIleML3.jpzkmgqe27yg059v.v8M7FvA"
        self.smtp_server = smtp_server
        self.port = port
        self.context = ssl.create_default_context()

    def send(self, receiver_email, subject, body, html_body=None):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = receiver_email

        part1 = MIMEText(body, "plain")
        message.attach(part1)

        if html_body:
            part2 = MIMEText(html_body, "html")
            message.attach(part2)

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=self.context)
                server.login(self.sender, self.password)
                server.sendmail(self.sender, receiver_email, message.as_string())
            print(f"Email sent successfully to {receiver_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
