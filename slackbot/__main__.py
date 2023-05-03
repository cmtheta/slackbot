import os
import logging
from slack_bolt import App
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

CHANNEL_ID = os.getenv("POST_CHANNEL_ID")

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

logging.basicConfig(
    filename="log/logging.log",
    level=logging.DEBUG,
    format="(%(asctime)s)[%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)

@app.event("channel_created")
def chennel_created(event):
    post_channel = CHANNEL_ID
    channel_name = event['channel']["name"]
    text = f"チャンネル #{channel_name} が作成されました。"
    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		}
	]
    try:
        client.chat_postMessage(
            channel=post_channel,
            text=text,
            blocks=blocks
        )
    except Exception as e:
        error_message()
        logging.exception('Raise Exception: %s', e)

def error_message():
    post_channel = CHANNEL_ID
    try:
        client.chat_postMessage(
            channel=post_channel,
            text="処理エラーが発生しました。",
        )
    except Exception as e:
        logging.exception('Raise Exception: %s', e)


handler = SocketModeHandler(app, SLACK_APP_TOKEN)
handler.start()


