import logging
# import datetime
from datetime import datetime, date
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
        return date.today().strftime('%Y年%m月%d日(%a)')


    def make_block(self, quote):

        count_down_msg = ""
        blocks = [
            self.make_greeting_block(),
            self.make_count_down_block(),
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

    def make_greeting_block(self):
        today = date.today().strftime('%Y年%m月%d日(%a)')
        greeting = f"おはようございます。今日は{today}です。"
        return {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": greeting
                    }
                }

    def make_count_down_block(self):
        now = datetime.now()
        gap = datetime(year=2023, month=7, day=5, hour=14) - now
        if gap.days == 0:
            # 大会当日（1日目の朝, 開会前）
            msg = f"JANOG52開会まで 残り{gap.seconds//3600}時間{gap.seconds%3600//60:02}分"

        elif gap.days == -1 or gap.days == -2:
            # 会期中（2日目,3日目の朝, 閉会前）
            gap = datetime(year=2023, month=7, day=7, hour=18) - now
            msg = f"JANOG52閉会まで 残り{gap.days*24 + gap.seconds//3600}時間{gap.seconds%3600//60:02}分"

        elif gap.days < -2:
            # 大会終了後
            return {"type":"section", "text": {"type":"mrkdwn", "text":" "}}
        else:
            msg =  f"JANOG52まで 残り{gap.days}日"

        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": msg
            }
        }



    def regist_msg(self):
        pass



if __name__ == "__main__":
    tmp = make_count_down_block()
    print(tmp)