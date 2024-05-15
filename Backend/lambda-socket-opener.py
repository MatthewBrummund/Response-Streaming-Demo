import json
import boto3

#We have to split the model call into two lambda's since the websocket connection isn't open for responses until the intial call has returned
#You can only send a response, once this lambda function has finished

lambda_connect = boto3.client('lambda')

#Lambda to create the websocket connection for two way communication
def lambda_handler(event, context):
    
    #gets the prompt from the user, and connectionId from the event
    if "body" in event:
        prompt = json.loads(event["body"])["prompt"]
    else:
        prompt = ""
    connectionId = event["requestContext"]["connectionId"]
    
    #format the prompt and Id to pass to the next lambda
    inputs = {
        "prompt": prompt,
        "connectionId": connectionId
    }
    
    #Call the main lambda function itself
    functionName = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"              #lambda function ARN
    lambda_connect.invoke(FunctionName=functionName, InvocationType="Event", Payload=json.dumps(inputs))
    
    return {
        'statusCode': 200
    }