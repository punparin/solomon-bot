from PriceFinder import *

class YuyuteiPriceFinder(PriceFinder):
    def __init__(self):
        super().__init__()
        self.yuyutei_endpoint = "https://yuyu-tei.jp/game_ygo/sell/sell_price.php"
        self.source = "Yuyu-tei"
        self.yuyutei_icon = "https://yuyu-tei.jp/img/ogp.jpg"

    def __find_prices(self, en_name, jp_name):
        result = []
        url = self.yuyutei_endpoint + "?name=" + urllib.parse.quote(self.format_japanese_name(jp_name))

        jp_name = self.format_name_for_search_engine(jp_name)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        divs = soup.find_all("div", {"class": re.compile(r'^group_box.*$')})

        for div in divs:
            raw_rarity = div.find("em", {"class": "gr_color"})
            rarity = self.format_rarity(raw_rarity)
            cards = div.find_all("li", {"class": re.compile(r'^card_unit rarity_.*$')})

            for card in cards:
                raw_card_id = card.find("p", {"class": "id"})
                raw_price = card.find("p", {"class": "price"})
                card_id = raw_card_id.text.strip()
                price = self.format_price(raw_price)
                
                card = Card(card_id, en_name, jp_name, self.source, self.yuyutei_icon, url, rarity, "Play", price)
                result.append(card)

                print("[%s] - (%s) - Price: ¥%s" % (rarity, card_id, price))

        return result

    def find_prices(self, name):
        jp_name = self.find_japanese_name(name)
        if jp_name is not None:
            print("EN Name: %s" % (name))
            print("JP Name: %s" % (jp_name))
            return self.__find_prices(name, jp_name)

        en_name = self.find_fuzzy_name(name)
        if en_name is not None:
            print("Fuzzy EN Name: %s" % (en_name))
        else:
            print("Unable to retrieve EN name")
            return []

        jp_name = self.find_japanese_name(en_name)
        if jp_name is not None:
            print("JP Name: %s" % (jp_name))
            return self.__find_prices(en_name, jp_name)
        else:
            print("Unable to retrieve JP name")

        return []
