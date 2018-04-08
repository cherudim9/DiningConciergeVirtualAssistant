import boto3
import json

def lambda_handler(event, context):
    
    # Get the service resource
    sqs = boto3.resource('sqs')
    
    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='RestaurantRecom')
    
    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))
    
    print(event)
    
    queue.send_message(MessageBody=json.dumps(event))
    
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
