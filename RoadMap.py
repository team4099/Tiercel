from typing import List, Optional
from Project import Project, Status, DateRange
from User import User
from datetime import datetime
from Task import Task, Priority

class RoadMap:
    projects: List[Project]
    tasks: List[Task]
    
    def __init__(self, project_db_identifier: str, task_db_identifier: str, notion_client):
        project_dict = notion_client.databases.query(database_id = project_db_identifier).get("results")
        task_dict = notion_client.databases.query(database_id = task_db_identifier).get("results")

        self.projects = parse_project_dict(project_dict)
        self.tasks = parse_task_dict(task_dict)
        
        print(self.projects)

def parse_project_dict(project_dict: List[dict]) -> List[Project]:
    projects = []
    for project in project_dict:
        projects.append(
            Project(
                name = project["properties"]["Name"]["title"][0]["text"]["content"],
                status = Status.from_str(project["properties"]["Status"]["status"]["name"]),
                timeline = parse_timeline(project["properties"]["Timeline"]["date"]),
                dri_emails = parse_dri_emails(project["properties"]["DRI"]["people"]),
                task_ids = [task_reference["id"] for task_reference in project["properties"]["Tasks"]["relation"]],
                project_url = project["url"]
            )
        )
    return projects
    
def parse_timeline(date_dict: dict) -> Optional[DateRange]:
    try:
        start_date = datetime.strptime(date_dict['start'], "%Y-%m-%d")
        end_date = datetime.strptime(date_dict['end'], "%Y-%m-%d")

        return DateRange(end_date, start_date)
    except TypeError:
        return None
    
def parse_dri_emails(dri_dict: dict) -> List[User]:
    users = []
    for user in dri_dict:
        users.append(
            User(email = user["person"]["email"], notion_uid = user["id"])
        )
    return users

def parse_task_dict(task_dict: List[dict]) -> List[Task]:
    tasks = []
    for task in task_dict:
        if (len(task["properties"]["Name"]["title"]) >= 1):
            tasks.append(
                Task(
                    task_name = task["properties"]["Name"]["title"][0]["text"]["content"],
                    status = Status.from_str(task["properties"]["Status"]["status"]["name"]),
                    timeline = parse_due_date(task["properties"]["Due Date"]["date"]),
                    priority = parse_priority(task["properties"]["Priority"]),
                    dri_emails = parse_dri_emails(task["properties"]["Assigned to"]["people"]),
                    task_id = task["id"],
                    related_project_id = [prj_reference["id"] for prj_reference in task["properties"]["🌋 Project"]["relation"]],
                    notion_url = task["url"]
                )
            )
    return tasks

def parse_due_date(date_dict: dict) -> Optional[DateRange]:
    try:
        end_date = datetime.strptime(date_dict['start'], "%Y-%m-%d")

        return DateRange(end_date)
    except TypeError:
        return None

def parse_priority(priority_dict: dict) -> Priority:
    return Priority.from_str(priority_dict["select"]["name"])
    
def parse_dri_emails(dri_dict: dict) -> List[User]:
    users = []
    for user in dri_dict:
        users.append(
            User(email = user["person"]["email"], notion_uid = user["id"])
        )
    return users




