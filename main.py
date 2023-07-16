import os
from dotenv import load_dotenv
from notion_client import Client
from time import sleep
from SlackWrapper import SlackWrapper
import json
from RoadMap import RoadMap
from Status import Status

TASK_DB = "88de9a3cf5554dd9a20476bc465cc68f"
PROJECT_DB = "adddfaea7fa7475eb04e4fc530af6932"
DRI_USER_GROUP = "S058TKUAX60"
PROJECT_DRI_USER_GROUP = "S05A84CKV09"
TASK_DRI_USER_GROUP = "S059NSGGY1L"
NOTIF_CHANNEL = "#log_notion_notifs"

load_dotenv()

notion = Client(auth=os.getenv('NOTION_AUTH_KEY'))
slack_app = SlackWrapper(os.getenv("SLACK_KEY"))

task_db_identifier = TASK_DB
project_db_identifier = PROJECT_DB

overrides = json.load(open("override.json"))

roadmap = RoadMap(project_db_identifier, task_db_identifier, notion)

project_dris = []
task_dris = []

for project in roadmap.projects:
    if project.status == Status.IN_PROGRESS:

        project_dri_mentions = []
        for user in project.dri_emails:
            email = user.email

            if email in overrides.keys():
                email = overrides[email]

            try:
                uid = slack_app.members[email]
                if uid not in project_dris:
                    project_dris.append(uid)
                project_dri_mentions.append(f"<@{uid}>")
            except KeyError:
                continue

        block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{project.project_url}|{project.project_name}>*",
                }
            },
        ]

        if (len(project_dri_mentions) >= 1):
            block.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f':office_worker:: {""" """.join(project_dri_mentions)}'
                    }
                },
            )

        project_info = "\n• ".join(project.info())
        project_warning = "\n• ".join(project.warnings())
        project_errors = "\n• ".join(project.errors())

        if len(project_info) >= 1:
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":information_source::\n• {project_info}"
                }
            }
            )

        if len(project_warning) >= 1:
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning::\n• {project_warning}"
                }
            })

        if len(project_errors) >= 1:
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":octagonal_sign::\n• {project_errors}"
                }
            })

        block += [
            {
                "type": "divider"
            }]

        if (project.has_issues() or project.has_sub_issues()):
            response = slack_app.client.chat_postMessage(
                channel=NOTIF_CHANNEL,
                link_names=True,
                blocks=block
            )
            sleep(1)  # Used to circumvent Slack rate limits

            project_thread = response.get("ts")

        for task in project.tasks:
            if task and task.status != Status.DONE:
                task_dri_mentions = []
                for user in task.dri_emails:
                    email = user.email

                    if email in overrides.keys():
                        email = overrides[email]

                    try:
                        uid = slack_app.members[email]
                        if uid not in task_dris:
                            task_dris.append(uid)
                        task_dri_mentions.append(f"<@{uid}>")
                    except KeyError:
                        continue

                block = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<{task.notion_url}|{task.task_name}>*",
                        }
                    },
                ]

                if (len(task_dri_mentions) >= 1):
                    block.append(
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f':office_worker:: {""" """.join(task_dri_mentions)}'
                            }
                        },
                    )

                task_info = "\n• ".join(task.info())
                task_warning = "\n• ".join(task.warnings())
                task_errors = "\n• ".join(task.errors())

                if len(task_info) >= 1:
                    block.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":information_source:\n• {task_info}"
                        }
                    }
                    )

                if len(task_warning) >= 1:
                    block.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":warning:\n• {task_warning}"
                        }
                    })

                if len(task_errors) >= 1:
                    block.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":octagonal_sign:\n• {task_errors}"
                        }
                    })

                block += [
                    {
                        "type": "divider"
                    }]

                if task.has_issues():
                    slack_app.client.chat_postMessage(
                        channel=NOTIF_CHANNEL,
                        link_names=True,
                        blocks=block,
                        thread_ts=project_thread
                    )
                    sleep(1)  # Used to circumvent Slack rate limits

slack_app.client.usergroups_users_update(usergroup=PROJECT_DRI_USER_GROUP, users=",".join(project_dris))

slack_app.client.usergroups_users_update(usergroup=TASK_DRI_USER_GROUP, users=",".join(task_dris))
