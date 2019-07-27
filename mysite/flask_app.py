from flask import Flask, request
import telepot
import urllib3
import requests

proxy_url = "http://proxy.server:XXXX"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "INSERT_SECRET_KEY"
bot = telepot.Bot('INSERT_BOT_KEY_HERE')
bot.setWebhook("INSERT_WEBHOOK_ULR_HERE/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]

        if text == "/random" :
            req = requests.get('http://api.scryfall.com/cards/random')
            respond = req.json()
            name= respond["name"]
            image_uris= respond["image_uris"]
            largeUrl=image_uris["large"]
            setName = respond["set_name"]
            bot.sendPhoto(chat_id,largeUrl,name+", "+setName)
        elif text == "/daily":
            f = open("/home/ronin17/dailyCard.txt", "r")
            msg=f.readline()
            url=f.readline()
            setName=f.readline()
            bot.sendPhoto(chat_id,url,msg+", "+setName)

    return "OK"