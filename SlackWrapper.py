import sys
from slack_sdk import WebClient
import json


class SlackWrapper:
    def __init__(self, api_key):
        self.client = WebClient(token=api_key)
        self.members = {}
        for member in self.client.users_list()["members"]:
            try:
                self.members[member["profile"]["email"]] = member["id"]
            except:
                pass

    def send_message(self, first_name, last_name, block):
        try:
            print("first name")
            self.client.chat_postMessage(
                channel=f"@{self.members[first_name+' '+last_name]}", blocks=block
            )
            return None
        except:
            print("firstinit_lastname")
            print(f"@{first_name[0]}{last_name}")
            self.client.chat_postMessage(
                channel=f"@{self.members[first_name[0]+last_name]}",
                blocks=block,
            )
            return None

    def send_verification_message(self, first_name, last_name, verification_number):
        verification_block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*FalconTrack Code*: {verification_number}"
                    ),
                },
            }
        ]
        print(first_name, last_name, verification_number)

        self.send_message(first_name, last_name, verification_block)

    def send_generic_message(self, first_name, last_name, message):
        generic_text_block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (message),
                },
            },
            {"type": "divider"},
        ]

        self.send_message(first_name, last_name, generic_text_block)