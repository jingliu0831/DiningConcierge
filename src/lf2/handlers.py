import utils
import datetime


def compose_es_payload(cuisine, n):
    epoch = datetime.datetime.utcfromtimestamp(0)
    seed = (datetime.datetime.utcnow() - epoch).total_seconds() * 1000.0
    return {
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"cuisine": cuisine}}
                        ]
                    }
                },
                "random_score": {"seed": str(seed)},
                "score_mode": "sum"
            }
        },
        "from": 0,
        "size": n
    }


def compose_text_message(attributes, suggested_restaurants):
    suggested = ""
    index = 0
    for restaurant in suggested_restaurants:
        index += 1
        suggested += "{}. {}, located at {}".format(
            str(index),
            utils.get_restaurant_name(restaurant),
            utils.get_restaurant_address(restaurant)
        )
        if not index == len(suggested_restaurants):
            suggested += "; "

    return 'Hello! Here are my {} restaurant suggestions for {} people, ' \
           'for {} at {}: {}. ' \
           'Enjoy your meal!'.format(
                utils.get_cuisine(attributes),
                utils.get_people_count(attributes),
                utils.get_date(attributes),
                utils.get_time(attributes),
                suggested
            )


def restaurant_ids_from_es(es_result):
    hits = es_result['hits']['hits']

    ids = []
    for hit in hits:
        ids.append(str(hit['_source']['id']))
    return ids


def db_keys_from_restaurant_ids(business_ids):
    keys = []
    for business_id in business_ids:
        keys.append({
            'business_id': {
                'S': business_id
            }
        })
    return keys
