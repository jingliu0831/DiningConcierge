import boto3
import handlers
import utils
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    sns = boto3.client('sns')
    sqs = boto3.client('sqs')
    dynamodb = boto3.client('dynamodb')
    table_name = 'yelp_restaurants'

    queue_url = 'https://sqs.us-east-1.amazonaws.com/267139716268/sqs_q1.fifo'
    es_host = 'https://search-dining-concierge-ddhbp6jsts77rmst425pma7yr4.us-east-1.es.amazonaws.com/'
    es_index = 'restaurants'

    num_of_suggestions = 3

    sqs_response = utils.poll_sqs(sqs, queue_url)
    messages = sqs_response['Messages'] if 'Messages' in sqs_response.keys() else []

    for message in messages:
        msg_attributes = message["MessageAttributes"]

        es_payload = handlers.compose_es_payload(utils.get_cuisine(msg_attributes), num_of_suggestions)
        es_response = utils.search_es(es_host + es_index, es_payload)
        ids = handlers.restaurant_ids_from_es(es_response)

        db_keys = handlers.db_keys_from_restaurant_ids(ids)
        suggested_restaurants = utils.dynamodb_batch_get(dynamodb, table_name, db_keys)
        logger.debug("Suggested restaurants: {}".format(suggested_restaurants))

        text = handlers.compose_text_message(msg_attributes, suggested_restaurants)
        phone = message["Body"]
        logger.info("Sending text message to: {}".format(phone))

        utils.publish_sns(sns, text, phone)
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
