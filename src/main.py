import requests
import re
from bs4 import BeautifulSoup


YGOPRODECK_ENDPOINT = "https://db.ygoprodeck.com/api/v7/cardsetsinfo.php"
FANDOM_ENDPOINT = "https://yugioh.fandom.com/wiki"
BIGWEB_ENDPOINT = "https://bigweb.co.jp/ver2/yugioh_index.php"

RARITY_MAP = {
    "ｼｰｸﾚｯﾄ": "SCR",
    "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ": "CR",
    "ｱﾙﾃｨﾒｯﾄ": "UTM",
    "SP": "SR",
    "SPPR": "SPR",
    "Mil-Super": "MSR",
    "KC-Ultra": "KCUR",
    "Ｇ": "GR"
}

def find_name_by_set_code(set_code):
    set_code = set_code.lower()
    set_code = set_code.replace("jp", "en")
    url = YGOPRODECK_ENDPOINT + "?setcode=" + set_code

    r = requests.get(url)

    return r.json()["name"]

def format_name(name):
    name = name.replace(" ", "_")

    return name

def format_japanese_name(name):
    name = name.replace("－", " ")
    
    return name

def find_japanese_name(en_name):
    formatted_name = format_name(en_name)
    url = FANDOM_ENDPOINT + "/" + formatted_name

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    span = soup.find("table", {"class": "cardtable"})
    span = span.find("span", {"lang": "ja"})

    try:
        jp_name = span.text
        return jp_name
    except AttributeError as err:
        return None

def format_price(price):
    return price.text.replace("円", "")

def format_rarity(rarity):
    if rarity in RARITY_MAP:
        return RARITY_MAP[rarity]
    
    return rarity

def find_prices(jp_name):
    url = BIGWEB_ENDPOINT \
        + "?search=yes&type_id=9&action=search&shape=1&seriesselect=&tyselect=&colourselect=&langselect=&condiselect=&selecttext=" \
        + format_japanese_name(jp_name)
    
    jp_name = jp_name.replace("－", "−")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all("div", {"class": "watermat abcd"})

    for div in divs:
        raw_name = div.find("a", {"href": "javascript:;"})
        scratch = div.find("abbr", {"title": "=キズ"})
        raw_price = div.find("span", {"class": "yendtr"})
        raw_rarity = div.find("abbr", {"title": re.compile(r'.*レア$|.*レル|.*ーマル|^=20SC$|^=PG$|^=Mil-Super$|^=KC-Ultra$')})
        price = format_price(raw_price)
        rarity = format_rarity(raw_rarity.text.strip())
        name = re.search("《.+》", str(raw_name)).group().replace("《", "").replace("》", "")

        if jp_name != name:
            continue

        if scratch is not None:
            print("[%s] - (Scratch) - Price: ¥%s" % (rarity, price))
        else:
            print("[%s] - (Play) - Price: ¥%s" % (rarity, price))


if __name__ == "__main__":
    while True:
        en_name = input("Input name: ").strip()
        # en_name = find_name_by_set_code(name)
        print("\nEN Name: %s" % (en_name))
        jp_name = find_japanese_name(en_name)
        if jp_name is not None:
            print("JP Name: %s" % (jp_name))
            find_prices(jp_name)
        else:
            print("Unable to retrieve JP name")
        print()
