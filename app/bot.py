from flask import Flask, request, abort

import os

from janome.tokenizer import Tokenizer

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

# LineBotApiとWebhookへの接続
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    t = Tokenizer()

    textrep = ''
    for token in t.tokenize(event.message.text):
        textrep += token.base_form + "\t" + token.part_of_speech + "\n"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textrep))

if __name__ == "__main__":
    #port = int(os.getenv("PORT"))
    #app.run(host="0.0.0.0", port=port)
    app.run()
