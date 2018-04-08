import json
import datetime
import time
import os
import dateutil.parser
import logging
import re
import boto3


# --- Helpers that build all of the responses ---


def elicit_slot(intent_name, slots, slot_to_elicit, message):
    result = {
        "sessionAttributes": {},
        "dialogAction": {
            "type": "ElicitSlot",
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
              "contentType": "PlainText",
              "content": message
            }
        }
    }
    return result
    

def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

#Helper functions

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


#validation functions, check if the user-provided slots are valid.

def is_valid_cuisine(c):
    c = c.lower()
    cuisine_list = ['chinese', 'french', 'american', 'japanese', 'korean', 'pizza', 'burger']
    for cuisine in cuisine_list:
        if c in cuisine or cuisine in c:
            return True
    return False




def is_valid_amount(c):
    amount = int(c)
    if amount < 8 and amount > 0:
        return True
    return False




def is_valid_phone(p):
    if re.match(r"\d{10}", p):
        return True
    return False




def validate_intent(slots):
    date = slots['Date']
    time = slots['Time']
    location = slots['Location']
    amount = slots['Amount']
    phone = slots['Phone']
    cuisine = slots['Cuisine']
    #if True:
    if cuisine and not is_valid_cuisine(cuisine):
        return build_validation_result(
            'False',
            'Cuisine',
            'Sorry, we only support pizzas, burgers, Chinese, French, American and Japanese cuisines right now.'
        )
    
    if phone and not is_valid_phone(phone):
        return build_validation_result(
            'False',
            'Phone',
            'Please type in a valid phone number in the format of (XXX)XXX-XXXX.'
        )
    
    if amount and not is_valid_amount(amount):
        return build_validation_result(
            'False',
            'Amount',
            'We do not support looking up for ' + str(amount) + ' people. If you are checking for a party over 8 people, please contact the restaurants directly.'
        )
    
    return {'isValid': True}




#fulfill order

def create_order(intent_request):
    date = intent_request['currentIntent']['slots']['Date']
    time = intent_request['currentIntent']['slots']['Time']
    location = intent_request['currentIntent']['slots']['Location']
    amount = intent_request['currentIntent']['slots']['Amount']
    phone = intent_request['currentIntent']['slots']['Phone']
    cuisine = intent_request['currentIntent']['slots']['Cuisine']
    validation_result = validate_intent(intent_request['currentIntent']['slots'])
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    
    if validation_result['isValid'] == 'False':
        slots = intent_request['currentIntent']['slots']
        slots[validation_result['violatedSlot']] = None
        return elicit_slot(
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                str(validation_result['message']['content'])
            )
    if cuisine is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Cuisine',
                'What cuisine?'
            )
    if date is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Date',
                'What date?'
            )
    if time is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Time',
                'What time?'
            )
    if location is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Location',
                'Location?'
            )
    if amount is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Amount',
                'How many people?'
            )
    if phone is None:
         return elicit_slot(
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'Phone',
                'Phone number ((XXX)XXX-XXXX)?'
            )

    sqs = boto3.resource('sqs')
    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='RestaurantRecom')
    
    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))
    print(intent_request)
    queue.send_message(MessageBody=json.dumps(intent_request))
    result = {
      "sessionAttributes": {},
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": "Thank you for using our service! You will receive a text message in a few minutes!"
        }
      }
    }
    return result



def lambda_handler(event, context):
    # TODO implement
    return create_order(event)
