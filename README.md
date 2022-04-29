# solomon-bot

Your friendly Yu-Gi-Oh! OCG bot running on discord to help you find cards' price in English. The price references are scraped from [bigweb](https://bigweb.co.jp/) and [YUYU-TEI](https://yuyu-tei.jp/).

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

```env
# .env
DISCORD_TOKEN=<TOKEN>
SOLOMON_API_ENDPOINT=https://solomon.pks.sh
ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT>
BIGWEB_ICON=https://bigweb.co.jp/inc/space2.gif
YUYUTEI_ICON=https://yuyu-tei.jp/img/ogp.jpg
```

### Running on local

```sh
# Run on machine
python src/main.py

# Run on docker
earthly +compose-up
earthly +compose-down
```

### Release

```sh
earthly --build-arg TAG=<TAG> --push +release
```
