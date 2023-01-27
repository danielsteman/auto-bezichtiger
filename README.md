## Description
Scrape data from housing websites and store listings in a database. Whenever a listing has been found that wasn't present in the database, notify users with a Telegram message. The application is configurable by the means of `settings.yaml`. The Dockerfile can be used to build an image, which can be deployed anywhere (e.g. Heroku).

Supported housing providers:
- Pararius

## Run locally
`python src/main.py`

