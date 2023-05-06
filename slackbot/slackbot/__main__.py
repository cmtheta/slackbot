import os
import logging
import schedule
import threading
from time import sleep
from slack_bolt import App
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .channel_created import ChannelCreated
from .daily_message import DailyMessage

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

POST_CHANNEL_ID = os.getenv("POST_CHANNEL_ID")

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

logging.basicConfig(
    filename="log/logging.log",
    level=logging.DEBUG,
    format="(%(asctime)s)[%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)

# >>> channel created
channel_created = ChannelCreated(client=client, post_channel=POST_CHANNEL_ID)
@app.event("channel_created")
def chennel_created(event):
    try:
        channel_created.exec(event)
    except Exception as e:
        logging.exception('Raise Exception: %s', e)
        error_message()
# <<< channel created

# >>> daily massage
daily_message = DailyMessage(client=client, post_channel=POST_CHANNEL_ID)
schedule.every(10).seconds.do(daily_message.send)
# <<< daily massage

def error_message():
    post_channel = POST_CHANNEL_ID
    try:
        client.chat_postMessage(
            channel=post_channel,
            text="処理中にエラーが発生しました。",
        )
    except Exception as e:
        logging.exception('Raise Exception: %s', e)

def schedule_run():
    while True:
        schedule.run_pending()
        sleep(5)

thread = threading.Thread(target=schedule_run)
thread.start()

handler = SocketModeHandler(app, SLACK_APP_TOKEN)
handler.start()


