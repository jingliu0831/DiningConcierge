from lf1 import utils
import re
import datetime


def validate_reservation(slots):
    city = utils.try_ex(lambda: slots['City'])
    cuisine = utils.try_ex(lambda: slots['Cuisine'])
    dinner_date = utils.try_ex(lambda: slots['Date'])
    dinner_time = utils.try_ex(lambda: slots['Time'])
    phone = utils.try_ex(lambda: slots['Phone'])

    if city and not isvalid_city(city):
        return utils.build_validation_result(
            False,
            'City',
            'We currently do not support {} as a valid city.  Can you try a different city?'.format(city)
        )

    if cuisine and not isvalid_cuisine(cuisine):
        return utils.build_validation_result(
            False,
            'Cuisine',
            'We currently do not support {} as a valid cuisine.  Can you try a different cuisine?'.format(cuisine)
        )

    if dinner_date:
        if not isvalid_date(dinner_date):
            return utils.build_validation_result(False, 'Date', 'That is an invalid date. '
                                                                'On what date would you like to have dinner?')
        if utils.get_date(dinner_date) < utils.get_today():
            return utils.build_validation_result(False, 'Date',
                                                 'Reservations must be scheduled at least one day in advance. '
                                                 'Can you try a different date?')

    if dinner_time:
        if utils.get_date(dinner_date) == utils.get_today() and not in_at_least_one_hour(dinner_time):
            return utils.build_validation_result(False, 'Time',
                                                 'Reservations must be scheduled at least one hour in advance. '
                                                 'Can you try a later hour?')

    if phone and not isvalid_phone(phone):
        return utils.build_validation_result(False, 'Phone', 'The number you provided is invalid for a US phone. '
                                                             'Could you say your phone number again?')

    return {'isValid': True}


def in_at_least_one_hour(dinner_time):
    hour, minute = dinner_time.split(":")
    dinner = utils.safe_int(hour) * 60 + utils.safe_int(minute)

    now = datetime.datetime.now()
    return dinner - (now.hour * 60 + now.minute) >= 60


def isvalid_city(city):
    valid_cities = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
                    'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
                    'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc',
                    'memphis', 'boston', 'nashville', 'baltimore', 'portland']
    return city.lower() in valid_cities


def isvalid_cuisine(cuisine):
    valid_cuisines = ['chinese', 'italian', 'korean', 'japanese', 'mediterranean', 'mexican']
    return cuisine.lower() in valid_cuisines


def isvalid_room_type(room_type):
    room_types = ['queen', 'king', 'deluxe']
    return room_type.lower() in room_types


def isvalid_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return True
    except ValueError:
        return False


def isvalid_phone(phone):
    phone = re.sub(r'(\W)+', '', phone)
    return len(phone) == 10
