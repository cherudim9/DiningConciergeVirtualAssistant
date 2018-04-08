def lambda_handler(event, context):
    # TODO implement
    result = {
      "sessionAttributes": {},
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": "Hello! Thank you for using our service! You can start searching for nearby restaurants now!"
        }
      }
    }
    return result

