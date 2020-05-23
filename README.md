# Telegram Bot

## Status : Code is broken.

## Creating a bot
Type `/newbot` at [https://telegram.me/botfather](https://telegram.me/botfather)

## API
[https://core.telegram.org/bots/api#making-requests](https://core.telegram.org/bots/api#making-requests)
All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: `https://api.telegram.org/bot<token>/<METHOD_NAME>`

Methods:
- `/getMe` [GET]
- `/getUpdates` [GET]
- `/sendmessage?chat_id=<CHAT_ID>&text=<MESSAGE>` [GET]

## Setup webhook
`/setWebhook?url=<your webhook>`
`/deleteWebhook`

## TODO
- Tunnelling (For local testing, use `ngrok`)
- API calls
- deployment
- uhhh get a life

## Heroku Deployment
List of files required
- `runtime.txt` to heroku python version
- `requirements.txt` for python libraries
- `Procfile` for deployment
