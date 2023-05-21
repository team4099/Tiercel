import os
from dotenv import load_dotenv
from notion_client import Client
import re
import datetime
from SlackWrapper import SlackWrapper
import json

load_dotenv()

notion = Client(auth=os.getenv('NOTION_AUTH_KEY'))
slack_app = SlackWrapper(os.getenv("SLACK_KEY"))

db_identifier = os.getenv('TASK_DB')
task_url_prefix = os.getenv("TASK_URL_PREFIX")

results = notion.databases.query( 
    **{
        "database_id": db_identifier,
    }
).get("results")

alerts = []
task_dris_slack_ids = []
overrides = json.load(open("override.json"))

for result in results:
    alert = {"task_name": "", "task_url":"", "DRIs": [], "info": [], "warnings":[], "errors": []}
    properties = result['properties']
    alert["task_url"] = result["url"]

    status = properties["Status"]['status']['name']

    if status != "Done":
        task_title_info = properties['Name']
        if task_title_info["title"] != []:
            task_name = task_title_info['title'][0]['text']['content']
            alert["task_name"] = task_name
            dris = []

            assigned_people = properties['Assigned to']['people']
            if len(assigned_people) >= 1:
                for people in assigned_people:
                    func_id = people['id']
                    dri = notion.users.retrieve(func_id)["person"]["email"]

                    if dri in overrides.keys():
                        dri = overrides[dri]

                    dris.append(dri)
                    try:
                        uid = slack_app.members[dri]
                        if uid not in task_dris_slack_ids:
                            task_dris_slack_ids.append(uid)
                    except KeyError:
                        continue
            else:
                alert["errors"].append("No DRI has been assigned.")
            
            alert["DRIs"] = dris

            due_date_string = properties["Due Date"]['date']
            if due_date_string != None:
                due_date = datetime.datetime.strptime(due_date_string['start'], "%Y-%m-%d")
                if datetime.datetime.now() > due_date:
                    alert["warnings"].append(f"{task_name} is {(datetime.datetime.now() - due_date).days} day(s) overdue")
            else:
                alert["errors"].append("No Due Date.")
        
        if len(alert["info"]) == len(alert["warnings"]) == len(alert["errors"]) == 0:
            continue
        else:
            alerts.append(alert)

slack_app.client.usergroups_users_update(usergroup=os.getenv('DRI_USER_GROUP'), users=",".join(task_dris_slack_ids))