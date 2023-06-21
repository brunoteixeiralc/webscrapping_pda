import requests
import pandas as pd
import locale
import ws_sendgrid
import ws_telegram_bot

locale.setlocale(locale.LC_ALL, '')

url = "https://api.linximpulse.com/engage/search/v3/hotsites"

querystring = {"apikey":"paodeacucar","origin":"https://www.paodeacucar.com","page":"1","resultsPerPage":"12","name":"semanacompleta_cervejasespeciais","salesChannel":["461","catalogmkp"],"sortBy":"descDiscount","filter":"d:3718:3719"}

payload = ""
headers = {
    "authority": "api.linximpulse.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "if-none-match": "W/16a87-CtUShW36pU8cJ5TRJn7iqnI6HsY",
    "origin": "https://www.paodeacucar.com",
    "referer": "https://www.paodeacucar.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

json_res = response.json()

res = []

for i in json_res["products"]:
    discount = "Same price" 
    if "desconto" in i["skus"][0]["specs"]:
        discount = i["skus"][0]["specs"]["desconto"][0]
        
    res.append({"name": i["name"],
                "discount": discount,
                "price": i["price"],
                "old_price": i["oldPrice"],
                "status": i["status"],
                "url_item": i["url"]})
    
df = pd.json_normalize(res)
df = pd.DataFrame(df) 
df.to_csv("desc_pda_cerva.csv", encoding="utf-8", index=False, sep=";")

data = ws_sendgrid.send_email(df, res)

ws_telegram_bot.send_to_telegram(res)

ws_telegram_bot.send_to_document_telegram(data)