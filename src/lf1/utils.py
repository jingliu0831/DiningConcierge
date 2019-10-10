import datetime


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def get_date(dinner_date):
    return datetime.datetime.strptime(dinner_date, '%Y-%m-%d').date()


def get_hour(dinner_time):
    return datetime.datetime.strptime(dinner_time, '%H:%M').hour


def get_today():
    return datetime.date.today()


def get_hour_now():
    return datetime.datetime.now().hour
