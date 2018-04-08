def lambda_handler(event, context):
    # TODO implement
    result = {
      "sessionAttributes": {},
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": "Your are welcome. Hope to see you again!"
        }
      }
    }
    return result
