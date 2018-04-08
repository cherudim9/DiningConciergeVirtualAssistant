from __future__ import print_function
import json
import boto3

def lambda_handler(event, context):
    data = json.loads(json.dumps(event))
    
    message = data["message"]
    userid = data["userId"]
    
    client = boto3.client('lex-runtime')
    
    response = client.post_content(
        botName='Testbot',
        botAlias = 'chatbot',
        userId = userid,
        contentType = 'text/plain; charset=utf-8',
        inputStream = message,
        accept = "text/plain; charset=utf-8"
    )
 
    return response['message']
