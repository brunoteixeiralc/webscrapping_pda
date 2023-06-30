import requests
import pandas as pd
import locale
import re
import ws_telegram_bot
import ws_product_enum
from decouple import config

locale.setlocale(locale.LC_ALL, '')

def callAllProductsAndSale(product_type):
    
    res = []
    res_alert = []
    res_top3 = []

    url = "https://api.linximpulse.com/engage/search/v3/hotsites"

    querystring = {"apikey":"paodeacucar","origin":"https://www.paodeacucar.com","page":"1","resultsPerPage":"24","name":product_type ,"salesChannel":["1344","catalogmkp"],"sortBy":"descDiscount","filter":"d:3718:3719"}

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
    
    print(json_res)

    if "products" in json_res:
        for i in json_res["products"]:
            
            discount = "Same price" 
            discount_int = 0
             
            if "desconto" in i["skus"][0]["specs"]:
                discount = i["skus"][0]["specs"]["desconto"][0]
                match = re.search(r'\b(\d+)\b', discount)
                if match:
                    discount_int = int(match.group(0))
            
            if i["status"] == "AVAILABLE" and discount_int != 0:    
                res.append({"id": i["id"],
                            "name": i["name"],
                            "discount": discount,
                            "discount_int": discount_int,
                            "price": i["price"],
                            "old_price": i["oldPrice"],
                            "status": i["status"],
                            "url_item": i["url"]})
                
                if discount_int >= int(config('DISCOUNT_VARIABLE')):
                    res_alert.append({"name": i["name"],
                        "discount": discount,
                        "discount_int": discount_int,
                        "price": i["price"],
                        "old_price": i["oldPrice"],
                        "status": i["status"],
                        "url_item": i["url"]})

        if len(res) != 0:
            ws_telegram_bot.send_to_telegram_day_time()
            ws_telegram_bot.send_to_telegram(res)

        if len(res_alert) != 0:
            ws_telegram_bot.send_to_telegram_alert(res_alert)
        
for enum_product in ws_product_enum.Product_BETA:
    callAllProductsAndSale(enum_product.value)
    callAllProductsAndSale(enum_product.value + "_ofertas")