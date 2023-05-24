from dataclasses import dataclass
from typing import Optional, List
from User import User
from Project import DateRange, Status
from enum import Enum

class Priority(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"

    @staticmethod
    def from_str(label):
        if label in ("P1"):
            return Priority.P1
        elif label in ("P2"):
            return Priority.P2
        elif label in ("P3"):
            return Priority.P3
        elif label in ("P4"):
            return Priority.P4
        elif label in ("P5"):
            return Priority.P5
        else:
            raise NotImplementedError

@dataclass
class Task:
    task_name: str
    status: Status
    timeline: DateRange
    priority: Priority
    dri_emails: List[User]
    task_id: str
    related_project_ids: List[str]
    notion_url: str

    def __init__(self, task_name: str, status: Status, timeline: DateRange, priority: Priority, dri_emails: List[User], task_id: str, related_project_id: List[str], notion_url: str):
        self.task_name = task_name
        self.status = status
        self.timeline = timeline
        self.priority = priority
        self.dri_emails = dri_emails
        self.task_id = task_id
        self.related_project_ids = related_project_id
        self.notion_url = notion_url


