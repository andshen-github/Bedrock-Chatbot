from flask import Flask, request, abort
import os
import http.client
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Set Bedrock API details
#bedrock_url = os.getenv("BEDROCK_API_BASE")

app = Flask(__name__)

# This function takes a chat message as input, appends it to the messages list, sends the recent messages to the Bedrock API, and returns the assistant's response.
def bedrock_chat_model(chat):
    # Append the user's message to the messages list
    messages = chat

    # Send the recent messages to the AWS API Gwateway of Bedrock and get the response
    conn = http.client.HTTPSConnection("012zvy7czl.execute-api.us-east-1.amazonaws.com")
    payload = json.dumps({
      "prompt_data": messages
    })
    headers = {
      'Content-Type': 'application/json',
      'X-Api-Key': 'OferNx35aB4X5Mi5VoAn6W61V1jFxlC6MGPyZNn7'
    }
    conn.request("POST", "/api/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return (data.decode("utf-8"))

# Initialize Line API with access token and channel secret
line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler1 = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# This route serves as a health check or landing page for the web app.
@app.route("/")
def mewobot():
    return 'Cat Time!!!'

# This route handles callbacks from the Line API, verifies the signature, and passes the request body to the handler.
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# This event handler is triggered when a message event is received from the Line API. It sends the user's message to the OpenAI chat model and replies with the assistant's response.
@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bedrock_chat_model(event.message.text))
    )

if __name__ == "__main__":
    app.run()
