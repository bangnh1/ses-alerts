import os
import boto3
import logging
import json
from urllib.request import Request, urlopen, HTTPError
from urllib.error import URLError


SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_USER = os.environ['SLACK_USER']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
LOGGER_LEVEL = os.getenv('LOGGER_LEVEL')

log = logging.getLogger()
if LOGGER_LEVEL == None:
    log.setLevel(logging.INFO)
elif LOGGER_LEVEL.lower() == "debug":
    log.setLevel(logging.DEBUG)

ses_client = boto3.client('ses')


def main(event, context):
    record = event['Records'][0]
    subject = record['Sns']['Subject']
    message = json.loads(record['Sns']['Message'])
    body = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USER,
        'text': subject,
        'attachments': [{
            'text': message['NewStateReason'],
            'color': 'danger',
            'fields': [{
                'title': 'Time',
                'value': message['StateChangeTime'],
                'short': True,
            }, {
                'title': 'Alarm',
                'value': message['AlarmName'],
                'short': True,
            }, {
                'title': 'Account',
                'value': message['AWSAccountId'],
                'short': True,
            }, {
                'title': 'Region',
                'value': message['Region'],
                'short': True,
            }],
        }],
    }
    return send_message(body)


def update_account_seding(is_enabled):
    response = ses_client.update_account_sending_enabled(Enabled=is_enabled)


def send_message(msg):
    req = Request(SLACK_WEBHOOK_URL, json.dumps(msg).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        log.info("Message posted to %s", msg['channel'])
    except HTTPError as e:
        log.debug("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        log.debug("Server connection failed: %s", e.reason)
