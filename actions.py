# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from textinput import SampleTextAssistant

import os
import venmo
import click
import logging
import json

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

import assistant_helpers
import browser_helpers

# contact map
people = {
    'Ryan Ma': 6266230819,
    'Ryan Lieu': 2068835878,
}

# venmo helper functions
def execute_venmo_request(phone_number, amount):
    request_body = 'venmo charge {} {} "you deserve it"'.format(phone_number, amount)
    os.system(request_body)

def execute_venmo_pay(phone_number, amount):
    payment_body = 'venmo pay {} {} "you deserve it"'.format(phone_number, amount)
    os.system(payment_body)

# google assistant helpers
def start_google_assistant():
    
    api_endpoint = 'embeddedassistant.googleapis.com'
    credentials = os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json')
    device_model_id = 'thursday-6b92e-thursday-p1zrh6'
    device_id = 'thursday'
    lang = 'en-US'
    display = False
    verbose = False
    grpc_deadline = 60 * 3 + 5

    # Setup logging
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        return

       # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    return SampleTextAssistant(lang, device_model_id, device_id, display,
                        grpc_channel, grpc_deadline)

def ask_google_assistant(query):

    with google_assistant:
        response_text, response_html = google_assistant.assist(text_query=query)
        
        if response_text:
            return response_text
        else: 
            return "Google is being a bitch"

google_assistant = start_google_assistant()

# action classes 

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


class ActionOpenGoogleChannel(Action):

    def name(self) -> Text:
        return "action_ask_google"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.get_slot("query")
        response = ask_google_assistant(query)
        dispatcher.utter_message(response)

