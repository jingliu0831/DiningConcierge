import json
from lf1 import validations, utils, execution
import logging
import boto3
import uuid


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Functions that control the bot's behavior --- """


def send_to_sqs(sqs, criteria):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/267139716268/sqs_q1.fifo'
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=criteria['Phone'],
        MessageAttributes={
            'City': {
                'StringValue': criteria['City'],
                'DataType': 'String'
            },
            'Cuisine': {
                'StringValue': criteria['Cuisine'],
                'DataType': 'String'
            },
            'Date': {
                'StringValue': criteria['Date'],
                'DataType': 'String'
            },
            'Time': {
                'StringValue': criteria['Time'],
                'DataType': 'String'
            },
            'PeopleCount': {
                'StringValue': str(criteria['PeopleCount']),
                'DataType': 'Number'
            }
        },
        MessageDeduplicationId=str(uuid.uuid1()).replace("-", ""),
        MessageGroupId='dininglf1'
    )
    return response


def suggest_restaurant(intent_request):
    """
    Performs dialog management and fulfillment for booking a hotel.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    city = utils.try_ex(lambda: intent_request['currentIntent']['slots']['City'])
    cuisine = utils.try_ex(lambda: intent_request['currentIntent']['slots']['Cuisine'])
    dinner_date = utils.try_ex(lambda: intent_request['currentIntent']['slots']['Date'])
    dinner_time = utils.try_ex(lambda: intent_request['currentIntent']['slots']['Time'])
    people_count = utils.try_ex(lambda: intent_request['currentIntent']['slots']['PeopleCount'])
    phone = utils.try_ex(lambda: intent_request['currentIntent']['slots']['Phone'])

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    criteria = {
        'City': city,
        'Cuisine': cuisine,
        'Date': dinner_date,
        'Time': dinner_time,
        'PeopleCount': people_count,
        'Phone': phone
    }
    criteria_json = json.dumps(criteria)

    session_attributes['currentCriteria'] = criteria_json

    if intent_request['invocationSource'] == 'DialogCodeHook':
        validation_result = validations.validate_reservation(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return execution.elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        session_attributes['currentCriteria'] = criteria_json
        return execution.delegate(session_attributes, intent_request['currentIntent']['slots'])

    # Sending the search criteria to SQS
    logger.debug('Searching for {} restaurants in city {}...'.format(cuisine, city))
    sqs = boto3.client("sqs")
    send_to_sqs(sqs, criteria) # TODO: may need to add re-try logic

    utils.try_ex(lambda: session_attributes.pop('currentCriteria'))

    return execution.close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'You are all set. Expect a suggestion from me shortly!'
        }
    )


def response_to_greeting(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    return execution.close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hi there, how can I help you?'
        }
    )


def response_to_thank_you(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    return execution.close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'You are very welcome!'
        }
    )
