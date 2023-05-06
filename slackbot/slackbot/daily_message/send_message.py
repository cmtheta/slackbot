import os
import json
import random
import logging
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
                blocks=self.make_block()
            )
        except Exception as e:
            raise


    def get_date(self) -> str:
        return date.today().strftime('%Y年%m月%d日(%a)')


    def make_block(self):
        blocks = []
        blocks.append(self.make_greeting_block())
        blocks.append(self.make_count_down_block())
        blocks.extend(self.make_quote_blocks())
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

    def make_quote_blocks(self):
        blocks = []
        blocks.append({"type": "divider"})
        template_quote_block = lambda quote: [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': f"{quote['text']}"}},
                    {'type': 'context', 'elements': [{'type': 'plain_text', 'text': f" by {quote['person_name']}", 'emoji': True}]}]
        blocks.extend(sum([template_quote_block(quote) for quote in self.get_quotes()], []))
        return blocks

    def get_quotes(self):
        cwdpath = os.path.dirname(__file__)
        with open(cwdpath + "/quote.json", 'r') as f:
            quotes_all = json.load(f)

        random.shuffle(quotes_all)
        quotes_all.sort( key=lambda x: x['selected_count'])
        select_num = max(len(quotes_all)//20, 1)
        selected_quotes = quotes_all[:select_num]
        for quote in quotes_all[:select_num]:
            quote['selected_count'] = quote['selected_count'] + 1

        with open(cwdpath + "/quote.json", 'w',  encoding="utf-8") as f:
            json.dump(quotes_all, f, indent=4, ensure_ascii=False)

        return selected_quotes

    def regist_msg(self):
        pass
