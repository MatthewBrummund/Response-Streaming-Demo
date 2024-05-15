import json
import boto3

def lambda_handler(event, context):
        
    #get the inputs from the previous lambda
    prompt = event["prompt"]
    connectionId = event["connectionId"]

    
    #create the model client to call, the RAG agent, and gateway connection for response
    apiGatewayURL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"      #https URL for the api gateway websocket
    gateway = boto3.client("apigatewaymanagementapi", endpoint_url=apiGatewayURL)
    bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")


    ########## Optional section to implement RAG (Example uses knowledge bases) below ##########


    # agent = boto3.client('bedrock-agent-runtime')
    
    
    # #inputs for the RAG from knowledge bases, the retrieve the RAG text (default is 5 sources)
    # Id = "XXXXXXXXXXXXXXXXXXXXXXXXXX"        #RAG agent Id
    # query = {
    #    'text': prompt
    # }
    # retrieve = agent.retrieve(knowledgeBaseId=Id, retrievalQuery=query)

    
    # #add the RAG info to the prompt, separated by a blank line for each source
    # RAGInfo = "INFORMATION\n\n"
    # for i in range(5):
    #    RAGInfo = RAGInfo + retrieve["retrievalResults"][i]["content"]["text"] + "\n\n"
    # prompt = RAGInfo + "USER INPUT\n\n" + prompt 


    ########## Optional section to implement RAG (Example uses knowledge bases) above ##########

    
    #Create the prompt API call to bedrock, includes: Model, content type, how the call is formatted, and the model specific info (tokens, prompt, etc)
    kwargs = {
        "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": prompt
                }
                ]
            }
            ]
        })
    }

    #Call the model with a response stream (creates an iterable object when converted)
    response = bedrock.invoke_model_with_response_stream(**kwargs)
    

    #Convert the model specific API response into general packet with start/stop info, here converts from Claude API response (Could be done for any model)
    stream = response.get('body')
    if stream:

        #for each returned token from the model:
        for token in stream:

            #The "chunk" contains the model-specific response
            chunk = token.get('chunk')
            if chunk:
                
                #Decode the LLm response body from bytes
                chunk_text = json.loads(chunk['bytes'].decode('utf-8'))
                
                #Construct the response body based on the LLM response, (Where the generated text starts/stops)
                if chunk_text['type'] == "content_block_start":
                    block_type = "start"
                    message_text = ""
                    
                elif chunk_text['type'] == "content_block_delta":
                    block_type = "delta"
                    message_text = chunk_text['delta']['text']
                    
                elif chunk_text['type'] == "content_block_stop":
                    block_type = "end"
                    message_text = ""

                else:
                    block_type = "blank"
                    message_text = ""
                    
                #Send the response body back through the gateway to the client    
                data = {
                    'statusCode': 200,
                    'type': block_type,
                    'text': message_text
                }
                gateway.post_to_connection(ConnectionId=connectionId, Data=json.dumps(data))
                

    return {
        'statusCode': 200
    }