import streamlit as st
import websocket
import json


#The wss socket URL from the stage of the api Gateway websocket connected to the first lambda function
end_URL = "#############################################" 


st.title("Response Streaming Demo")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What is up?"):


    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    #create the location for the response from the model to go, (create an empty element)
    with st.chat_message("assistant"):

        response = st.empty()
        st.session_state.current_text = ""


    ########## Definition for websocket handling below ##########

    #send the prompt once the socket is open
    def on_open(ws):
        print("###Opening###")

        prompt_to_send = {"prompt": prompt}
        ws.send(json.dumps(prompt_to_send))


    #Handle the incoming tokens from the websocket
    def on_message(ws, message):
        print("###Message###")

        message = json.loads(message)

        #if the message is the last token, close the socket
        if message['type'] == 'end':
            ws.close()

        #if it's not the last token, add the token to the full message (current_text), display it, and add it to the chat history
        else:
            st.session_state.current_text = st.session_state.current_text + message['text']
            response.markdown(st.session_state.current_text)

    ########## Definition for websocket handling above ##########
        

    #create the socket and run it 
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
    end_URL,
    on_open=on_open,
    on_message=on_message
    )
    ws.run_forever()

    #Add the user message and response to the chat history, as well as reset the current_text variable
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_text})
    st.session_state.current_text = ""



