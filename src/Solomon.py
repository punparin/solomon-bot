import re
import discord
from Finder import Finder
from Logger import Logger


logger = Logger()
finder = Finder(logger)

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

        embed = finder.find_cards(content)

        if len(embed) < 2:
            error_embed = embed[0]
            
            await message.channel.send(embed=error_embed)
        else:
            bigweb_embed, yuyutei_embed = embed[0], embed[1]

            await message.channel.send(embed=bigweb_embed)
            await message.channel.send(embed=yuyutei_embed)
