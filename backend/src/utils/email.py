from fastapi_mail import ConnectionConfig, MessageSchema, FastMail

from src.config import settings


class Email:
    def __init__(self):
        self.config_mail = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=587,
            MAIL_SERVER="in-v3.mailjet.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.mail = FastMail(
            config=self.config_mail
        )

    async def custom_email(
            self,
            recipients: list[str],
            subject: str,
            body: str
    ) -> None:
        schema = MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype='html'
        )
        await self.mail.send_message(schema)

    async def signup_mail(self, email, code):
        await self.custom_email([email], 'Exchange Sign up', signup_body(email, code))

    async def change_credentials_mail(self, email, code):
        await self.custom_email([email], 'Change credentials', credentials_body(email, code))


def signup_body(
        email: str,
        code: str,
):
    return f"""
<html>
    <body>
        <h1>Hello dear {email}</h1>
        <h5>You have been on our website and wanted to sign up your account</h5>
        <p>We are very happy about you, nice to meet you</p>
        <p>But first of all you must verify your email address</p>
        <h1>{code}</h1>
        <h3>So above you can see this code</h3>
        <h3>Please keep it safe and do not give it to third parties</h3>
    </body>
</html>
"""


def credentials_body(
        email: str,
        code: str
):
    return f"""
<html>
    <body>
        <h1>Hello dear {email}</h1>
        <h3>You want to change your credentials on our site</h3>
        <h1>{code}</h1>
        <h3>So here is your email verification code</h3>
    </body>
</html>
"""
