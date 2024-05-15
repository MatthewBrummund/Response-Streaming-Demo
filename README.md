Welcome!

This demo is to show an example implementation of response streaming from anthropic models, (although it could be implmented here with others)

The demo consists of a streamlit frontend which makes calls to a lambda function through an API Gateway websocket
In order to open this websocket for responses, the initial call to it must be resolved
This adds the connectionId to the list of avalible ones to access in the API Gateway

This is why there are two lambda functions rather than one, the first (lambda-socket-opener) is only there to open the websocket connection for responses
The second (lambda-bedrock-caller) is what handles the actual model orchestraction (RAG, and response handling)

The demo also has code to implement RAG through knowlegde bases, but could be replaced with another embeddings model if needed

The only current issue is in the streamlit frontend, the display of the response isn't in a dynamic text box, but rather just prints the whole incomplete response for each new token recieved



SETUP GUIDE


FRONTEND
The frontend Streamlit app is set up like any other

Ensure that the virtual enviornment packages are installed, then create the venv
Next make sure that streamlit is installed in the venv, and the front end is ready to run

sudo apt install python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit
streamlit run streamlit-frontend.py


BACKEND

Create an API Gateway Websocket, the default route and stage work for the demo, just ensure that two way communication is enabled
Create two lambda functions, lambda-socket-opener, and lambda-bedrock-caller
For lambda-socket-opener, copy in the relevent code, and ensure it has permissions to invoke other lambda function
For lambda-bedrock-opener, copy the relevent code again, and ensure it has permissions to call API Gateways, as well as full bedrock access
Edit the permissions to match the use case, for the demo both had the following permissions (AmazonAPIGatewayInvokeFullAccess, AmazonBedrockFullAccess, AWSLambda_FullAccess) as well as logging
Don't forget to make sure that the AWS account has access to the bedrock model you want to call

Lastly, if you want, create an S3 bucket and link it to knowledge bases in order to use RAG (Although its not needed for the demo)



For any questions, reach out to mbrummun@asu.edu (Or realistically just slack me)


