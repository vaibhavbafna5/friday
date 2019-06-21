# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import os
import venmo

people = {
    'Ryan Ma': 6266230819,
    'Ryan Lieu': 2068835878,
}

def execute_venmo_request(phone_number, amount):
    request_body = 'venmo charge {} {} "you deserve it"'.format(phone_number, amount)
    os.system(request_body)

def execute_venmo_pay(phone_number, amount):
    payment_body = 'venmo pay {} {} "you deserve it"'.format(phone_number, amount)
    os.system(payment_body)

class ActionVenmoRequest(Action):
    
    def name(self) -> Text:
        return "action_venmo_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # gather data
            person_name = tracker.get_slot("person")
            dollar_amount = tracker.get_slot("dollar_amount")
            msg = "REQUEST PERSON: " + person_name + ", DOLLAR_AMOUNT: " + dollar_amount
            
            # check to see if person exists
            if person_name not in people:
                dispatcher.utter_message("Sorry, I'm not sure who this is :/")
        
            # execute request
            execute_venmo_request(people[person_name], dollar_amount)
            dispatcher.utter_message(msg)

class ActionVenmoPay(Action):

    def name(self) -> Text:
        return "action_venmo_pay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # gather data
            person_name = tracker.get_slot("person")
            dollar_amount = tracker.get_slot("dollar_amount")
            msg = "PAY PERSON: " + person_name + ", DOLLAR_AMOUNT: " + dollar_amount

            # check to see if person exists
            if person_name not in people:
                dispatcher.utter_message("Sorry, I'm not sure who this is :/")

            # execute payment
            execute_venmo_pay(people[person_name], dollar_amount)
            dispatcher.utter_message(msg)

