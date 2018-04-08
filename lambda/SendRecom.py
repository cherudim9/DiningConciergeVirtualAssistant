from __future__ import print_function

import json
import boto3
import datetime
from botocore.vendored import requests

print('Loading function')

def get_address(list1):
    result = ""
    for i in range(0, len(list1)):
        if i > 0:
            result = result + ", "
        result = result + list1[i]
    return str(result)

def lambda_handler(event, context):
    sqs = boto3.resource('sqs')

    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='RestaurantRecom')
    
    # You can now access identifiers and attributes
    print(queue.url)
    
    for message in queue.receive_messages():
        # Get the custom author message attribute if it was set
        slots=(json.loads(message.body))['currentIntent']['slots']
        #print(message.body)
        Cuisine=str(slots['Cuisine'])
        Phone=str(slots['Phone'])
        Amount=str(slots['Amount'])
        Location=str(slots['Location'])
        Time=str(slots['Time'])
        Date=str(slots['Date'])
        Phone='+1' + Phone
        #print(Cuisine,Phone,Amount,Location,Time,Date)
        timestamp = datetime.datetime(int(Date.split('-')[0]), int(Date.split('-')[1]), int(Date.split('-')[2])\
                    , int(Time.split(':')[0]), int(Time.split(':')[1])).strftime("%s")
        sns = boto3.client('sns')
        
        url = "https://api.yelp.com/v3/businesses/search?term=food&limit=5&location=" + Location +"&open_at=" + timestamp +\
                "&categories=" + Cuisine
        headers = {"Authorization":"Bearer l_uOn3P1tESZYoOia4Emb56jWp1nurCy0hT0T4UNyJ388b69iPJaLHAVnHiB8vlI2kLPc12YUE6D8YmJe0XpjnrugrfnIfKi1zr192QOfPHSTKhORHe85FKPQZa-WnYx"}
        print(url)
        request = requests.get(url, headers = headers)
        response = json.loads(request.text)
        print(str(response))
        if 'businesses' not in response:
            response_msg = "Location not found, please try again!"
            result=sns.publish(PhoneNumber = Phone, Message=response_msg)
            message.delete()
            print(Phone, response_msg)
            return ''

        businesses = response['businesses']
        response_msg = "Hello! Here are my " + Cuisine.lower() + " restaurant suggestions for " + Amount + " people, for " +\
                        Date + " at " + Time + ":\n"
        if len(businesses) == 0:
            response_msg = response_msg + "No businesses found.\n"
        else:
            for i in range(0, len(businesses)):
                cuisine_msg = "cuisine(s): "
                cuisine_data = businesses[i]['categories']
                for j in range(0, len(cuisine_data)):
                    cuisine_msg = cuisine_msg + str(cuisine_data[j]['alias']) + ", "
                    
                response_msg = response_msg + str(i + 1) + ". " + str(businesses[i]['name']) + ", " + cuisine_msg + "located at " + get_address(businesses[i]['location']['display_address']) + "\n"
        response_msg = response_msg + "Thank you for using our service! Enjoy your meal!"
        
        result=sns.publish(PhoneNumber = Phone, Message=response_msg)
        
        print(response_msg)
        
        
    
        # Let the queue know that the message is processed
        message.delete()
    
    return ''
