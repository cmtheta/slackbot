import logging
import datetime
from slack_sdk import WebClient

class DailyMessage:
    def __init__(self, client: WebClient, post_channel: str):
        self.post_channel = post_channel
        self.client = client


    def send(self):
        try:
            self.client.chat_postMessage(
                channel=self.post_channel,
                text="HELLO!",
                blocks=self.make_block(
                        quote=self.get_quote()
                       ,today = self.get_date()
                        )
            )
        except Exception as e:
            raise


    def get_quote(self):
        # TODO: DBからデータを取ってこれるようにしたい。
        return {
            "msg":"“If it's a good idea, go ahead and do it. It is much easier to apologize than it is to get permission.” \n 良いアイデアなら、どうぞやってください。許可を得るより、謝る方がずっと簡単です。",
            "person_name":"グレース・ホッパー"
        }


    def get_date(self) -> str:
        return datetime.date.today().strftime('%Y年%m月%d日(%a)')


    def make_block(self, quote, today):
        greeting = f"おはようございます。今日は{today}です。"
        # message: JANOG52まで残り〜日
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": greeting
                }
            },
            {
                "type": "divider"
            },
            # TODO:quoteブロックの数を残数に応じて変えられるようにしたい
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{quote['msg']}"
                }
            },
            {
			"type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f" by {quote['person_name']}",
                        "emoji": True
                    }
                ]
            }
        ]
        return blocks


    def regist_msg(self):
        pass

