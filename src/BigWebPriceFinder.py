from PriceFinder import *

class BigWebPriceFinder(PriceFinder):
    def __init__(self):
        super().__init__()
        self.bigweb_endpoint = "https://bigweb.co.jp/ver2/yugioh_index.php"
        self.source = "bigweb"
        self.bigweb_icon = "https://bigweb.co.jp/inc/space2.gif"
    
    def __find_prices(self, en_name, jp_name):
        result = []
        url = self.bigweb_endpoint \
            + "?search=yes&type_id=9&action=search&shape=1&seriesselect=&tyselect=&colourselect=&langselect=&condiselect=&selecttext=" \
            +  urllib.parse.quote(self.format_japanese_name(jp_name))
        
        jp_name = self.format_name_for_search_engine(jp_name)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            divs = soup.find_all("div", {"class": "watermat abcd"})
        except AttributeError as err:
            print(err)
            return result

        for div in divs:
            try:
                raw_name = div.find("a", {"href": "javascript:;"})
                scratch = div.find("abbr", {"title": "=キズ"})
                raw_price = div.find("span", {"class": "yendtr"})
                raw_rarity = div.find("abbr", {"title": re.compile(r'.*レア$|.*レル|.*ーマル|^=20SC$|^=PG$|^=Mil-Super$|^=KC-Ultra$')})
                price = self.format_price(raw_price)
                rarity = self.format_rarity(raw_rarity)
                name = re.search("\"《.+》\"", str(raw_name)).group().replace("《", "").replace("》", "").replace("\"", "")

                if jp_name != name:
                    continue

                if scratch is not None:
                    card = Card("-", en_name, jp_name, self.source, self.bigweb_icon, url, rarity, "Scratch", price)
                    print("[%s] - (Scratch) - Price: ¥%s" % (rarity, price))
                else:
                    card = Card("-", en_name, jp_name, self.source, self.bigweb_icon, url, rarity, "Play", price)
                    print("[%s] - (Play) - Price: ¥%s" % (rarity, price))
                
                result.append(card)
            except AttributeError as err:
                print(err)

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
