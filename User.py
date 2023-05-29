from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    notion_uid: Optional[str] = None

    def __init__(self, email: str, notion_uid: Optional[str] = None):
        self.email = email
        self.notion_uid = notion_uid

