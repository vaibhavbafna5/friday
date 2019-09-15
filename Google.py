import os
import click
import logging

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

import assistant_helpers
import browser_helpers

def start_google_assistant_client():
    
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


class GoogleAssistant:

    def __init__(self):
        self.client = start_google_assistant_client()
        print("Google Assistant booted successfully")

    def ask_assistant_query(query):
        with self.client:
            response_text, response_html = google_assistant.assist(text_query=query)
        
        if response_text:
            return response_text
        else: 
            return "Google is being a bitch"

