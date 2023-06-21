import locale
import base64
import sendgrid
from sendgrid.helpers.mail import (
    Mail, Content, To, Email, Attachment, FileContent, FileName,
    FileType, Disposition)
from io import BytesIO
from decouple import config

def send_email(df, res):
    
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

    mail_json = mail.get()

    sg.client.mail.send.post(request_body=mail_json)
    
    print('Email enviado')
    
    return data