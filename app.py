from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

# \u5f9e\u74b0\u5883\u8b8a\u6578\u8b80\u53d6 LINE channel secret & access token
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "<YOUR_CHANNEL_SECRET>")
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN", "<YOUR_CHANNEL_ACCESS_TOKEN>")

line_bot_api = LineBotApi(LINE_CHANNEL_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    # \u9019\u908a\u53ef\u4ee5\u52a0\u5165\u547c\u53eb Gemini API \u7684\u7a0b\u5f0f
    reply_text = f"\u4f60\u8aaa\uff1a{text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(port=3000)
