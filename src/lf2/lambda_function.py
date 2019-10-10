import boto3
import uuid


def compose_text_message(attributes):
    cuisine = attributes['Cuisine']['StringValue']
    people_count = attributes['PeopleCount']['StringValue']
    date = attributes['Date']['StringValue']
    time = attributes['Time']['StringValue']

    return 'Hello! Here are my {} restaurant suggestions for {} people, for {} at {}: Always go to China Xiang. ' \
        'Enjoy your meal!'.format(cuisine, people_count, date, time)


def lambda_handler(event, context):
    sns = boto3.client('sns')
    sqs = boto3.client('sqs')

    queue_url = 'https://sqs.us-east-1.amazonaws.com/267139716268/sqs_q1.fifo'

    sqs_response = sqs.receive_message(
        QueueUrl=queue_url,
        MessageAttributeNames=[
            'City', 'Cuisine', 'Date', 'Time', 'PeopleCount'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=20,
        ReceiveRequestAttemptId=str(uuid.uuid1()).replace("-", "")
    )

    for message in sqs_response['Messages']:
        text = compose_text_message(message["MessageAttributes"])

        sns_response = sns.publish(
            PhoneNumber='+1' + message["Body"],
            Message=text,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'YourDinner'
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Promotional'
                }
            }
        )
        print("sns response: ")
        print(sns_response)

        # deleteResponse = sqs.delete_message(
        #     QueueUrl=queue_url,
        #     ReceiptHandle=message['ReceiptHandle']
        # )
