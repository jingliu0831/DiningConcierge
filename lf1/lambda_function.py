import time
import os
import logging
import handlers
import boto3


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GreetingIntent':
        return handlers.response_to_greeting(intent_request)
    elif intent_name == 'ThankYouIntent':
        return handlers.response_to_thank_you(intent_request)
    elif intent_name == 'DiningSuggestionsIntent':
        sqs = boto3.client("sqs")
        return handlers.gather_criteria(intent_request, sqs)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
