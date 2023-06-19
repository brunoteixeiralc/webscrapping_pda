import requests
import base64
import pandas as pd
import locale
import sendgrid
from sendgrid.helpers.mail import (
    Mail, Content, To, Email, Attachment, FileContent, FileName,
    FileType, Disposition)
from io import BytesIO
from decouple import config

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

def send_email(res):
    
    contentEmailBody1 = res[0]["name"] + " , Preço com desc: " + locale.currency(res[0]["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(res[0]["old_price"], grouping=True, symbol=False)
    contentEmailBody2 = res[1]["name"] + " , Preço com desc: " + locale.currency(res[1]["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(res[1]["old_price"], grouping=True, symbol=False)
    contentEmailBody3 = res[2]["name"] + " , Preço com desc: " + locale.currency(res[2]["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(res[2]["old_price"], grouping=True, symbol=False)
    
    buffer = BytesIO()
    df.to_csv(buffer);
    buffer.seek(0)
    data = buffer.read()
    encoded = base64.b64encode(data).decode()
    
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName('desc_pda_cerva.csv')
    attachment.disposition = Disposition('attachment')
    
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    from_email = Email("brunoteixeiralc@gmail.com")  # Change to your verified sender
    to_email = To("brunoteixeiralc@gmail.com")
    subject = "Descontos Cervejas Artesanais - PDA"
    content = Content("text/plain", "Segue em anexo as 12 cervejas artesanais com maior desconto no PDA\n\n" + "TOP 3 DE DESCONTO\n\n" +
                      str(contentEmailBody1) + 
                      "\n" + str(contentEmailBody2) + 
                      "\n" + str(contentEmailBody3) + "\n"
                      ) 
    mail = Mail(from_email, to_email, subject, content)
    mail.attachment = attachment

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
   
    print('Email enviado')
    
send_email(res)

def send_to_telegram(message):

    apiToken = config('API_TELEGRAM')
    chatID = config('CHAT_ID_TELEGRAM')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[0]["name"] + 
                                               "\nPreço com desc: " + "💰 " + locale.currency(res[0]["price"], grouping=True, symbol=False) + 
                                               "\nPreço normal: " + "💰 " + locale.currency(res[0]["old_price"], grouping=True, symbol=False) + 
                                               "\nLink: " + res[0]["url_item"]}
                                 )
        print(response.text)
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[1]["name"] + 
                                               "\nPreço com desc: " + "💰 " + locale.currency(res[1]["price"], grouping=True, symbol=False) + 
                                               "\nPreço normal: " + "💰 " + locale.currency(res[1]["old_price"], grouping=True, symbol=False) + 
                                              "\nLink: " + res[1]["url_item"]}
                                 )
        print(response.text)
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[2]["name"] + 
                                               "\nPreço com desc: " + "💰 " + locale.currency(res[2]["price"], grouping=True, symbol=False) + 
                                               "\nPreço normal: " + "💰 " + locale.currency(res[2]["old_price"], grouping=True, symbol=False) + 
                                               "\nLink: " + res[2]["url_item"]}
                                 )
        print(response.text)
    except Exception as e:
        print(e)
        
    print('Mensagens enviadas')

send_to_telegram(res)