FROM --platform=linux/arm64 python:3.9

ARG IMAGE=punparin/yugioh-ocg-price-discord-bot
ARG TAG=latest

WORKDIR /app

build:
    RUN pip install wheel
    COPY requirements.txt ./
    RUN pip wheel -r requirements.txt --wheel-dir=wheels
    COPY src src
    SAVE ARTIFACT src /src
    SAVE ARTIFACT wheels /wheels

release:
    COPY +build/src src
    COPY +build/wheels wheels
    COPY requirements.txt ./
    RUN pip install --no-index --find-links=wheels -r requirements.txt
    ENTRYPOINT ["python3", "-u", "./src/main.py"]
    SAVE IMAGE --push $IMAGE:$TAG

compose-up:
    LOCALLY
    WITH DOCKER --load=+release \
        --build-arg IMAGE=$IMAGE \
        --build-arg TAG=local
        RUN docker-compose -f docker-compose.yaml up -d
    END

compose-down:
    LOCALLY
    RUN  docker-compose -f docker-compose.yaml down
