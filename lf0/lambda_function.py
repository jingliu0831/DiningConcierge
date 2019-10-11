import datetime
import time
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Main handler ---

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='DiningConcierge',
        botAlias='$LATEST',
        userId=event['id'],
        sessionAttributes={},
        requestAttributes={},
        inputText=event["text"]
    )

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = {"id": event['id'], "text": response['message'], "timestamp": now}
    return message
