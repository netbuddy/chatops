# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json

from .executor_ansible import AnsibleRunner
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionCopyFile(Action):

    def name(self) -> Text:
        return "action_copy_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        src_entity = {}
        src_entity['id'] = 1
        src_entity['path'] = tracker.get_slot('path')
        
        dst_entity = {}
        dst_entity['id'] = 2
        dst_entity['path'] = tracker.get_slot('dst_path')

        with open('/home/public/wp/chatops/tool/copy_file.json', 'r') as service_file:
            service = json.load(service_file)
            if service['executor'] == 'ansible':
                runner = AnsibleRunner('localhost', limit='')
                res = runner.run_module(service['ansible_module'], 'src=src_entity["path"] dest=dst_entity["path"]', extravars={})

        # print("tracker:")
        # print("slots:", tracker.slots, "events :", tracker.events)
        # print("domain:")
        # print(domain)
                dispatcher.utter_message(text=res)

        return []