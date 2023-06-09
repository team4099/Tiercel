from dataclasses import dataclass
from typing import Optional, List
from User import User
from enum import Enum
from datetime import datetime, timedelta
from Status import Status

@dataclass
class DateRange:
    end_date: datetime
    start_date: Optional[datetime]

    def __init__(self, end_date: datetime, start_date: Optional[datetime] = None):
        self.start_date = start_date
        self.end_date = end_date
    
        def is_overdue(self) -> bool:
            return (datetime.now() - self.end_date).days > 0
    
        def days_overdue(self) -> int:
            return (datetime.now() - self.end_date).days

class Priority(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    null = "null"

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

    def info(self) -> List[str]:
        ret_val = []

        return ret_val

    def warnings(self) -> List[str]:
        ret_val = []

        if self.timeline != None and self.timeline.is_overdue() and self.status != Status.DONE:
            ret_val.append(f"Task is {self.timeline.days_overdue()} Day(s) Overdue.")

        return ret_val
    
    def errors(self) -> List[str]:
        ret_val = []

        if len(self.dri_emails) == 0:
            ret_val.append("No Task Lead(s) Assigned.")

        if self.timeline == None:
            ret_val.append("No Due Date for Task.")
        
        return ret_val
    
    def has_issues(self) -> bool:
        return (
            len(self.info()) != 0 
            or len(self.warnings()) != 0 
            or len(self.errors()) != 0 
        ) and self.status != Status.DONE

