from .reset_password import reset_password as reset_password_template
from .verify_email import verify_email as verify_email_template
from .welcome import welcome as welcome_template


def verify_email(name: str, verification_link: str) -> str:
    return verify_email_template.format(name=name, verification_link=verification_link)


def reset_password(name: str, reset_link: str) -> str:
    return reset_password_template.format(name=name, reset_link=reset_link)


def welcome(name: str) -> str:
    return welcome_template.format(name=name)


__all__ = [
    "verify_email",
    "reset_password",
    "welcome",
]
