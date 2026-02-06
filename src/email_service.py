import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = user_password

    @staticmethod
    def load_msg(from_: str, to: str, body: str, subject: str) -> str:
        msg = MIMEMultipart()
        msg["From"] = from_
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        return msg.as_string()

    def send_email(self, to: str, body: str, subject: str):
        service = smtplib.SMTP(EmailService.smtp_server, EmailService.smtp_port)
        try:
            service.starttls(context=ssl.create_default_context())  # Inicia a comunicação segura
            service.login(self.user_email, self.user_password)

            service.sendmail(self.user_email, to, EmailService.load_msg(self.user_email, to, body, subject))
        except Exception as e:
            with open("logs.txt", "a") as log_file:
                log_file.write(f"{e}\n")
        finally:
            service.quit()
