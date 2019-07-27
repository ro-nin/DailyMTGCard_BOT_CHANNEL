import requests
import telepot
import urllib3

proxy_url = "http://proxy.server:XXXX"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

try:
    req = requests.get('http://api.scryfall.com/cards/random')
    req.raise_for_status()
    respond = req.json()
    name= respond["name"]
    image_uris= respond["image_uris"]
    largeUrl=image_uris["large"]
    setName = respond["set_name"]

    f = open("/home/USERNAME/dailyCard.txt", "w")
    f.write(name+"\n")
    f.write(largeUrl+"\n")
    f.write(setName+"\n")

    bot = telepot.Bot('INSERT_BOT_KEY_HERE')
    bot.getMe()
    bot.sendPhoto(chat_id='INSERT_TARGET_HERE: @',photo=largeUrl,caption=name+", "+setName)

except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
