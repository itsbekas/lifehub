from pydantic.dataclasses import dataclass


@dataclass
class EmailRequest:
    From: str
    To: str
    Subject: str
    HtmlBody: str
    MessageStream: str
