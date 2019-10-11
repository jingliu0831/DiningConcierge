import uuid
from botocore.vendored import requests


def poll_sqs(sqs, queue_url):
    return sqs.receive_message(
        QueueUrl=queue_url,
        MessageAttributeNames=[
            'City', 'Cuisine', 'Date', 'Time', 'PeopleCount'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=20,
        ReceiveRequestAttemptId=str(uuid.uuid1()).replace("-", "")
    )


def publish_sns(sns, text, phone):
    return sns.publish(
        PhoneNumber='+1' + phone,
        Message=text,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'YourDinner'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )


def search_es(es_url, payload):
    response = requests.get(es_url + "/_search", json=payload)
    return response.json()


def dynamodb_batch_get(dynamodb, table_name, keys):
    response = dynamodb.batch_get_item(
        RequestItems={
            table_name: {
                'ExpressionAttributeNames': {
                    '#name': 'name'
                },
                'ConsistentRead': True,
                'Keys': keys,
                'ProjectionExpression': '#name,address',
            }
        }
    )

    return response["Responses"][table_name]


def get_cuisine(attributes):
    return attributes['Cuisine']['StringValue'].lower()


def get_people_count(attributes):
    return attributes['PeopleCount']['StringValue']


def get_date(attributes):
    return attributes['Date']['StringValue']


def get_time(attributes):
    return attributes['Time']['StringValue']


def get_restaurant_address(restaurant):
    return restaurant["address"]["S"]


def get_restaurant_name(restaurant):
    return restaurant["name"]["S"]
