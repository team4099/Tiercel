import os
from dotenv import load_dotenv
from notion_client import Client
import re
import datetime
from SlackWrapper import SlackWrapper
import json
from RoadMap import RoadMap

load_dotenv()

notion = Client(auth=os.getenv('NOTION_AUTH_KEY'))
# slack_app = SlackWrapper(os.getenv("SLACK_KEY"))

task_db_identifier = os.getenv('TASK_DB')
project_db_identifier = os.getenv('PROJECT_DB')
task_url_prefix = os.getenv("TASK_URL_PREFIX")

# results = notion.databases.query( 
#     database_id=task_db_identifier
# ).get("results")

# project_results = notion.databases.query( 
#     database_id=project_db_identifier
# )

roadmap = RoadMap(project_db_identifier, task_db_identifier, notion)
print(roadmap.projects)
print(roadmap.tasks)


# for result in project_results:
#     print(result['properties'])

# alerts = []
# task_dris_slack_ids = []
# overrides = json.load(open("override.json"))

# for result in results:
#     alert = {"task_name": "", "task_url":"", "DRIs": [], "info": [], "warnings":[], "errors": []}
#     properties = result['properties']
#     alert["task_url"] = result["url"]

#     status = properties["Status"]['status']['name']

#     if status != "Done":
#         task_title_info = properties['Name']
#         if task_title_info["title"] != []:
#             task_name = task_title_info['title'][0]['text']['content']
#             alert["task_name"] = task_name
#             dris = []

#             assigned_people = properties['Assigned to']['people']
#             if len(assigned_people) >= 1:
#                 for people in assigned_people:
#                     func_id = people['id']
#                     dri = notion.users.retrieve(func_id)["person"]["email"]

#                     if dri in overrides.keys():
#                         dri = overrides[dri]

#                     try:
#                         uid = slack_app.members[dri]
#                         if uid not in task_dris_slack_ids:
#                             task_dris_slack_ids.append(uid)
#                         dris.append(f"<@{uid}>")
#                     except KeyError:
#                         continue
#             else:
#                 alert["errors"].append("No DRI has been assigned.")
            
#             alert["DRIs"] = dris

#             due_date_string = properties["Due Date"]['date']
#             if due_date_string != None:
#                 due_date = datetime.datetime.strptime(due_date_string['start'], "%Y-%m-%d")
#                 if datetime.datetime.now() > due_date:
#                     alert["warnings"].append(f"{task_name} is {(datetime.datetime.now() - due_date).days} day(s) overdue")
#             else:
#                 alert["errors"].append("No Due Date.")
        
#         if len(alert["info"]) == len(alert["warnings"]) == len(alert["errors"]) == 0:
#             continue
#         else:
#             alerts.append(alert)

# message = []

# for alert in alerts:
#     task_name = alert["task_name"]
#     task_url = alert["task_url"]
#     dri_string = " ".join(alert["DRIs"])
#     info = "\n• ".join(alert["info"])
#     warnings = "\n• ".join(alert["warnings"])
#     errors = "\n• ".join(alert["errors"])

#     message.append(
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": f"*<{task_url}|{task_name}>*",
# 			}
# 		}
#     )

#     message.append(
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": f"*DRIs*:office_worker:: {dri_string}"
# 			}
# 		}
#     )

#     if len(info) >= 1:
#         message.append({
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": f"*Info* :information_source::\n• {info}"
# 			}
# 		})
    
#     if len(warnings) >= 1:
#         message.append({
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": f"*Warnings* :warning::\n• {warnings}"
# 			}
# 		})
    
#     if len(errors) >= 1:
#         message.append({
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": f"*Errors* :octagonal_sign::\n• {errors}"
# 			}
# 		})

#     message += [
# 		{
# 			"type": "divider"
# 		}]
    
#     if len(message) >= 42:
#         response = slack_app.client.chat_postMessage(
#             channel='#log_notion_notifs',
#             link_names=True,
#             blocks=message)
#         message = []
#     else:
#         continue

# response = slack_app.client.chat_postMessage(
#             channel='#log_notion_notifs',
#             link_names=True,
#             blocks=message)

# slack_app.client.usergroups_users_update(usergroup=os.getenv('DRI_USER_GROUP'), users=",".join(task_dris_slack_ids))