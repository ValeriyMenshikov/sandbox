import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from application.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    async def send_email(self, subject: str, text: str, to: str):
        msg = self._build_message(subject, text, to)
        self._send_email_mailhog(msg)

    def _build_message(self, subject: str, text: str, to: str) -> MIMEMultipart:
        msg = MIMEMultipart()

        msg["From"] = self.settings.MAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain"))
        return msg

    def _send_email_mailhog(self, msg: MIMEMultipart) -> None:
        with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
            server.send_message(msg)
