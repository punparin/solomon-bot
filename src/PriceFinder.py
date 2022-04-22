import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
from Card import *
from discord import Embed, Colour
from currency_converter import CurrencyConverter


class PriceFinder:
    def __init__(self):
        self.currency_converter = CurrencyConverter()
        self.ygoprodeck_card_set_info_endpoint= "https://db.ygoprodeck.com/api/v7/cardsetsinfo.php"
        self.ygoprodeck_card_info_endpoint = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        self.fandom_endpoint = "https://yugioh.fandom.com/wiki"
        self.bigweb_endpoint = "https://bigweb.co.jp/ver2/yugioh_index.php"
        self.yuyutei_endpoint = "https://yuyu-tei.jp/game_ygo/sell/sell_price.php"
        self.rarity_alias = {
            "ｼｰｸﾚｯﾄ": "SCR",
            "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ": "CR",
            "ｱﾙﾃｨﾒｯﾄ": "UTM",
            "SP": "SR",
            "SPPR": "SPR",
            "Mil-Super": "MSR",
            "KC-Ultra": "KCUR",
            "Ｇ": "GR",
            "P-N": "NP"
        }
    
    def find_name_by_set_code(self, set_code):
        set_code = set_code.lower()
        set_code = set_code.replace("jp", "en")
        url = self.ygoprodeck_card_set_info_endpoint + "?setcode=" + set_code

        r = requests.get(url)

        return r.json()["name"]

    def find_fuzzy_name(self, name):
        url = self.ygoprodeck_card_info_endpoint + "?fname=" + name

        r = requests.get(url)

        try:
            data = r.json()["data"]
            return data[0]["name"]
        except KeyError as err:
            return None

    def format_name(self, name):
        name = name.replace(" ", "_")

        return name

    def format_japanese_name(self, name):
        name = name.replace("－", " ")
        
        return name

    def find_japanese_name(self, en_name):
        formatted_name = self.format_name(en_name)
        url = self.fandom_endpoint + "/" + formatted_name

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        try:
            span = soup.find("table", {"class": "cardtable"})
            span = span.find("span", {"lang": "ja"})
            jp_name = span.text
            return jp_name
        except AttributeError as err:
            return None

    def format_price(self, price):
        return price.text.strip().replace("円", "")

    def format_rarity(self, rarity):
        rarity = rarity.text.strip()
        if rarity in self.rarity_alias:
            return self.rarity_alias[rarity]
        
        return rarity

    def format_name_for_search_engine(self, name):
        return name.replace("－", "−")

    def get_thb_price(self, yen_price):
        try:
            return int(self.currency_converter.convert(int(yen_price), "JPY", "THB"))
        except ValueError as err:
            return "-"

    def get_embed_from_cards(self, cards):
        try:
            embed = Embed(title="{0} ({1})".format(cards[0].en_name, cards[0].jp_name), color=Colour.orange())
            embed.set_author(name=cards[0].source,url=cards[0].url, icon_url=cards[0].source_icon)

            for card in cards:
                info = "ID: {0}\nRarity: {1}\nCondition: {2}\nPrice: ¥{3} (THB {4})".format(
                    card.card_id,
                    card.rarity,
                    card.condition,
                    card.jpy_price,
                    card.thb_price
                )
                embed.add_field(name="Information", value=info)

            return embed
        except IndexError as err:
            print(err)
            return Embed(title="Error retrieving data", description="Just try it later...", color=0xE4443A)
