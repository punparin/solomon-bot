import os
import json
import requests
import urllib.parse
from discord import Embed, Colour
from elasticsearch import Elasticsearch, helpers
from Card import Card
from CardInfo import CardInfo
from SolomonAPIError import SolomonAPIError
from currency_converter import CurrencyConverter

class Finder:
    def __init__(self, logger):
        self.logger = logger
        self.index = "yugioh_cards"
        self.solomon_api_endpoint = os.environ["SOLOMON_API_ENDPOINT"]
        self.es_endpoint = os.environ["ELASTICSEARCH_ENDPOINT"]
        self.currency_converter = CurrencyConverter()
        self.es = Elasticsearch(self.es_endpoint)

    def find_fuzzy_card_from_name(self, input_name):
        resp = self.es.search(
            index=self.index,
            query={
                    "match": {
                        "name": input_name
                    }
                }
            )

        cards = resp['hits']['hits']

        return None if len(cards) == 0 else cards[0]

    def get_cards(self, source, jp_name):
        url = "{0}/api/cards?source={1}&name={2}".format(self.solomon_api_endpoint, source.lower(), urllib.parse.quote(jp_name))

        try:
            r = requests.get(url)

            if r.status_code != 200:
                raise SolomonAPIError("Encountered invalid request from Solomon API")

            return r.json()
        except json.decoder.JSONDecodeError as err:
            self.logger.error("Finder.get_yuyutei_cards", err)
            raise SolomonAPIError("Encountered invalid response from Solomon API")

    def get_thb_price(self, yen_price):
        try:
            return int(self.currency_converter.convert(int(yen_price), "JPY", "THB"))
        except ValueError as err:
            return "-"

    def merge_solomon_response_to_card_info(self, card_info, solomon_response):
        card_info.url = solomon_response["url"]
        
        for card in solomon_response["cards"]:
            id = card["id"]
            rarity = card["rarity"]
            condition = card["condition"]
            jpy_price = card["price"]
            thb_price = self.get_thb_price(jpy_price)

            new_card = Card(id, rarity, condition, jpy_price, thb_price)
            card_info.add_card(new_card)

        return card_info

    def get_embed_from_card_info(self, card_info):
        embed = Embed(title="{0} ({1})".format(card_info.en_name, card_info.jp_name), color=Colour.orange())
        embed.set_author(name=card_info.source, url=card_info.url, icon_url=card_info.source_icon)
        embed.set_thumbnail(url=card_info.img_url)

        for card in card_info.cards:
            info = "ID: {0}\nRarity: {1}\nCondition: {2}\nPrice: ¥{3} (THB {4})".format(
                card.id,
                card.rarity,
                card.condition,
                card.jpy_price,
                card.thb_price
            )
            embed.add_field(name="Information", value=info)

        return embed

    def find_cards(self, input_name):
        es_card = self.find_fuzzy_card_from_name(input_name)

        if es_card is None:
            return Embed(
                title="Name not found",
                description="Unable to find {0}".format(input_name),
                color=0xE4443A
                )

        en_name = es_card["_source"]["name"]
        jp_name = es_card["_source"]["jp_name"]
        img_id = es_card["_source"]["id"]

        if jp_name == "":
            return Embed(
                title="Japanese name not found",
                description="Unable to find {0} in japanese".format(input_name),
                color=0xE4443A
                )

        bigweb_card_info = CardInfo("Bigweb", en_name, jp_name, img_id)
        yuyutei_card_info = CardInfo("YUYUTEI", en_name, jp_name, img_id)

        try:
            bigweb_solomon_response = self.get_cards("bigweb", jp_name)
        except SolomonAPIError as err:
            return Embed(
                title="Error from Solomon API",
                description=err,
                color=0xE4443A
                )
        
        try:
            yuyutei_solomon_response = self.get_cards("yuyutei", jp_name)
        except SolomonAPIError as err:
            return Embed(
                title="Error from Solomon API",
                description=err,
                color=0xE4443A
                )

        bigweb_card_info = self.merge_solomon_response_to_card_info(bigweb_card_info, bigweb_solomon_response)
        bigweb_embed = self.get_embed_from_card_info(bigweb_card_info)

        yuyutei_card_info = self.merge_solomon_response_to_card_info(yuyutei_card_info, yuyutei_solomon_response)
        yuyutei_embed = self.get_embed_from_card_info(yuyutei_card_info)

        return bigweb_embed, yuyutei_embed
