import os
from Solomon import *


if __name__ == "__main__":
    solomon = Solomon()
    discord_token = os.getenv('DISCORD_TOKEN')
    solomon.run(discord_token)
