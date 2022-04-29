import os
import json

class CardInfo:
    def __init__(self, source, en_name, jp_name, img_id):
        self.cards = []
        self.en_name = en_name
        self.jp_name = jp_name
        self.source = source
        self.source_icon = self.get_source_icon(source)
        self.img_url = "https://storage.googleapis.com/ygoprodeck.com/pics_small/" + str(img_id) + ".jpg"
        self.url = None

    def get_source_icon(self, source):
        if source.lower() == "bigweb":
            return os.getenv('BIGWEB_ICON')
        elif source.lower() == "yuyutei":
            return os.getenv('YUYUTEI_ICON')
        else:
            return ""

    def add_card(self, card):
        self.cards.append(card)
