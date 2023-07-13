import locale
import base64
import sendgrid
from sendgrid.helpers.mail import (
    Mail, Content, To, Email, Attachment, FileContent, FileName,
    FileType, Disposition)
from io import BytesIO
from decouple import config

def send_email(df, res, product_type):
    
    contentsEmailBody = []
    
    for r in res:
        contentEmailBody = r["name"] + " , Preço com desc: " + locale.currency(r["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(r["old_price"], grouping=True, symbol=False)
        # contentEmailBody2 = res[1]["name"] + " , Preço com desc: " + locale.currency(res[1]["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(res[1]["old_price"], grouping=True, symbol=False)
        # contentEmailBody3 = res[2]["name"] + " , Preço com desc: " + locale.currency(res[2]["price"], grouping=True, symbol=False) + " , Preço normal: " + locale.currency(res[2]["old_price"], grouping=True, symbol=False)
        contentsEmailBody.append(contentEmailBody)
    buffer = BytesIO()
    df.to_csv(buffer);
    buffer.seek(0)
    data = buffer.read()
    encoded = base64.b64encode(data).decode()
    
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName('Descontos_' + product_type + '.csv')
    attachment.disposition = Disposition('attachment')
    
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    from_email = Email("brunoteixeiralc@gmail.com")  # Change to your verified sender
    to_email = To("brunoteixeiralc@gmail.com")
    subject = "Descontos " + product_type +  " - PDA"
    content = Content("text/plain", "Segue em anexo os itens com maior desconto no PDA\n\n" + "TOP 3 DE DESCONTO\n\n".join([item + '\n' for item in contentsEmailBody]) + "\n" )
    mail = Mail(from_email, to_email, subject, content)
    mail.attachment = attachment

    mail_json = mail.get()

    sg.client.mail.send.post(request_body=mail_json)
    
    print('Email enviado')
    
    return data