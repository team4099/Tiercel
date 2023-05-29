from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
from User import User
from Task import Task

class Status(Enum):
    NOT_STARTED = "Not started"
    ON_HOLD = "On Hold"
    IN_PROGRESS = "In progress"
    DONE = "Done"

    @staticmethod
    def from_str(label):
        if label in ("Not started"):
            return Status.NOT_STARTED
        elif label in ("On Hold"):
            return Status.ON_HOLD
        elif label in ("In progress"):
            return Status.IN_PROGRESS
        elif label in ("Done"):
            return Status.DONE
        else:
            raise NotImplementedError

@dataclass
class DateRange:
    end_date: datetime
    start_date: Optional[datetime]

    def __init__(self, end_date: datetime, start_date: Optional[datetime] = None):
        self.start_date = start_date
        self.end_date = end_date
    
    def is_overdue(self) -> bool:
        return datetime.now() > self.end_date
    
    def days_overdue(self) -> int:
        return (datetime.now() - self.end_date).days


class Project:
    project_name: str
    project_id: str
    status: Status
    timeline: DateRange
    dri_emails: List[str]
    task_ids: List[str]
    project_url: str
    tasks: List[Task]

    def __init__(self, name: str, prj_id: str, status: Status, dri_emails: List[User], task_ids: List[str], project_url: str, timeline: Optional[DateRange] = None):
        self.project_name = name
        self.project_id = prj_id
        self.status = status
        self.timeline = timeline
        self.dri_emails = dri_emails
        self.task_ids = task_ids
        self.project_url = project_url
        self.tasks = []
    
    def is_finished(self) -> bool:
        return self.status == Status.DONE

    def info(self) -> List[str]:
        ret_val = []

        return ret_val

    def warnings(self) -> List[str]:
        ret_val = []

        if self.timeline != None and self.timeline.is_overdue():
            ret_val.append(f"Project is {self.timeline.days_overdue()} day(s) overdue.")
        
        return ret_val
    
    def errors(self) -> List[str]:
        ret_val = []

        if len(self.dri_emails) == 0:
            ret_val.append("No Project DRI assigned.")

        if self.timeline == None:
            ret_val.append("No existing timeline for project.")
        
        return ret_val