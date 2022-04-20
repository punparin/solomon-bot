import re
import discord
from BigWebPriceFinder import *
from YuyuteiPriceFinder import *


bigWebPriceFinder = BigWebPriceFinder()
yuyuteiPriceFinder = YuyuteiPriceFinder()

class Solomon(discord.Client):
    def format_content(self, content):
        return content.replace("(", "").replace(")", "")

    async def on_ready(self):
        print("{0} is now online!".format(self.user))

    async def on_message(self, message):
        isMatched = re.match("^\(.*\)$", message.content)
        content = self.format_content(message.content)

        if not isMatched:
            return

        bigweb_result = bigWebPriceFinder.find_prices(content)
        bigweb_embed = bigWebPriceFinder.get_embed_from_cards(bigweb_result)

        ryuyutei_result = yuyuteiPriceFinder.find_prices(content)
        yuyutei_embed = yuyuteiPriceFinder.get_embed_from_cards(ryuyutei_result)

        await message.channel.send(embed=bigweb_embed)
        await message.channel.send(embed=yuyutei_embed)
