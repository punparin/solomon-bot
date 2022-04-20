# yugioh-ocg-price-discord-bot

> Your friendly OCG cards' price bot standing by on discord. The price references are scraped from [bigweb](https://bigweb.co.jp/) and [YUYU-TEI](https://yuyu-tei.jp/).

## Showcase

![solomon-showcase](images/solomon-showcase.gif)

## For development

### Setup development environment

```sh
virtualenv venv
# For fish
source venv/bin/activate.fish
# For shell
source venv/bin/activate
pip install -r requirements.txt
```

### Environment variables

```
# .env
DISCORD_TOKEN=<TOKEN>
```
