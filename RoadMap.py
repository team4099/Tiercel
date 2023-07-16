from typing import List, Optional
from Project import Project, DateRange
from User import User
from datetime import datetime
from Task import Task, Priority
from Status import Status


class RoadMap:
    projects: List[Project]
    tasks: List[Task]
    
    def __init__(self, project_db_identifier: str, task_db_identifier: str, notion_client):
        project_dict = notion_client.databases.query(database_id = project_db_identifier).get("results")
        project_results = project_dict.get("results")

        # Paginate through all the different projects if it ever overflows the Notion limit (precautionary measure).
        while project_dict.get("has_more"):
            project_dict = notion_client.databases.query(
                database_id=project_db_identifier,
                start_cursor=project_dict["next_cursor"]
            )
            print(project_dict)
            if project_dict.get("results"):
                project_results.append(project_dict.get("results"))

        task_dict = notion_client.databases.query(database_id = task_db_identifier)
        task_results = task_dict.get("results")

        # Paginate through all the different tasks
        while task_dict.get("has_more"):
            task_dict = notion_client.databases.query(
                database_id=task_db_identifier,
                start_cursor=task_dict["next_cursor"]
            )
            if task_dict.get("results"):
                task_results.append(task_dict.get("results"))

        self.tasks = parse_task_dict(self, task_dict)
        self.projects = parse_project_dict(self, project_dict)
        

def parse_project_dict(self, project_dict: List[dict]) -> List[Project]:
    projects = []
    for project in project_dict:
        if (len(project["properties"]["Name"]["title"]) >= 1):
            new_project = Project(
                    name = project["properties"]["Name"]["title"][0]["text"]["content"],
                    prj_id = project["id"],
                    status = Status.from_str(project["properties"]["Status"]["status"]["name"]),
                    timeline = parse_timeline(project["properties"]["Timeline"]["date"]),
                    dri_emails = parse_dri_emails(project["properties"]["DRI"]["people"]),
                    task_ids = [ task_reference["id"] for task_reference in project["properties"]["Tasks"]["relation"]],
                    project_url = project["url"]
                )

            projects.append(
                new_project
            )

            new_project.tasks = [find_task_by_id(self, task_id) for task_id in new_project.task_ids]

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

def parse_task_dict(self, task_dict: List[dict]) -> List[Task]:
    tasks = []
    for task in task_dict:
        if (len(task["properties"]["Name"]["title"]) >= 1):
            new_task = Task(
                    task_name = task["properties"]["Name"]["title"][0]["text"]["content"],
                    status = Status.from_str(task["properties"]["Status"]["status"]["name"]),
                    timeline = parse_due_date(task["properties"]["Due Date"]["date"]),
                    priority = parse_priority(task["properties"]["Priority"]),
                    dri_emails = parse_dri_emails(task["properties"]["Assigned to"]["people"]),
                    task_id = task["id"],
                    related_project_id = [prj_reference["id"] for prj_reference in task["properties"]["Project"]["relation"]],
                    notion_url = task["url"]
                )
            tasks.append(
                new_task
            )

    return tasks

def parse_due_date(date_dict: dict) -> Optional[DateRange]:
    try:
        end_date = datetime.strptime(date_dict['start'], "%Y-%m-%d")

        return DateRange(end_date)
    except TypeError:
        return None

def parse_priority(priority_dict: dict) -> Priority:
    try:
        return Priority.from_str(priority_dict["select"]["name"])
    except TypeError:
        return Priority.null
    
def parse_dri_emails(dri_dict: dict) -> List[User]:
    users = []
    for user in dri_dict:
        users.append(
            User(email = user["person"]["email"], notion_uid = user["id"])
        )
    return users

def find_task_by_id(self, task_id: str) -> Optional[Task]:
    for task in self.tasks:
        if task.task_id == task_id:
            return task
    return None

def find_project_by_name(self, project_name: str) -> Optional[Project]:
    for project in self.projects:
        if project.project_name == project_name:
            return project
    return None

def find_task_by_name(self, task_name: str) -> Optional[Task]:
    for task in self.tasks:
        if task.task_name == task_name:
            return task
    return None

def access_rollup_task_name(task_reference: dict) -> Optional[str]:
    try:
        return task_reference["title"][0]["plain_text"]
    except IndexError:
        return None
        


