import logging
from slack_sdk import WebClient

class ChannelCreated:
    def __init__(self, client: WebClient, post_channel: str):
        self.post_channel = post_channel
        self.client = client


    def exec(self, event):
        channel_name = event['channel']["name"]
        text = self.make_text(channel_name)
        try:
            self.client.chat_postMessage(
                channel=self.post_channel,
                text=text,
                blocks=self.make_block(text)
            )
        except Exception as e:
            raise

    def make_text(self, channel_name):
        return f"チャンネル #{channel_name} が作成されました。"

    def make_block(self, text):
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
        return blocks


