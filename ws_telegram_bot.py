import requests
import locale
import os
import hashlib
import tempfile
from decouple import config

def send_to_telegram(res):

    apiToken = config('API_TELEGRAM')
    chatID = config('CHAT_ID_TELEGRAM')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[0]["name"] + 
                                                "\n💰 "+ "Preço com desconto: " + "R$ " + locale.currency(res[0]["price"], grouping=True, symbol=False) +
                                                "\n💰 " + "Preço normal: " + "R$ " + locale.currency(res[0]["old_price"], grouping=True, symbol=False) + 
                                                "\n🔗 " + res[0]["url_item"]}
                                 )
        print(response.text)
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[1]["name"] + 
                                               "\n💰 "+ "Preço com desconto: " + "R$ " + locale.currency(res[1]["price"], grouping=True, symbol=False) + 
                                               "\n💰 " + "Preço normal: " + "R$ " + locale.currency(res[1]["old_price"], grouping=True, symbol=False) + 
                                               "\n🔗 " + res[1]["url_item"]}
                                 )
        print(response.text)
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': "🍺 " + res[2]["name"] + 
                                               "\n💰 "+ "Preço com desconto: " + "R$ " + locale.currency(res[2]["price"], grouping=True, symbol=False) + 
                                               "\n💰 " + "Preço normal: " + "R$ " + locale.currency(res[2]["old_price"], grouping=True, symbol=False) + 
                                               "\n🔗 " + res[2]["url_item"]}
                                 )
        print(response.text)
    except Exception as e:
        print(e)
        
    print('Mensagens enviadas')

def send_to_document_telegram(data):
    
    nome_arquivo = hashlib.md5(b"desc_pda_cerva").hexdigest()

    temp_dir = tempfile.gettempdir()
    temp_csv_path = os.path.join(temp_dir, nome_arquivo)

    with open(temp_csv_path, 'wb') as dst_file:
        dst_file.write(data)

    apiToken = config('API_TELEGRAM')
    chatID = config('CHAT_ID_TELEGRAM')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendDocument'
    
    params = {
    'chat_id': chatID
    }
    try:
        with open(temp_csv_path, 'rb') as csv_file:
            response = requests.post(apiURL, params=params, files={'document': ("desc_pda_cerva.csv", csv_file)})
            os.remove(temp_csv_path)
        print(response.text)
    except Exception as e:
        print(e)
        
    print('CSV enviado')