import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class mail():

  def envio(nome, email, assunto, corpo, filename="", filecontent=""):

      remetente = "dual@scorpionbonus.pt"
      destinatario = email

      corpo_html = "<html><head><title></title></head><body><h1>DUAL</h1><h2>Este email é apenas um teste.</h2><p>"+ corpo +"</p></body></html>"
      
      correio = MIMEMultipart()
      correio['Subject']= assunto
      correio['From']="DualChat, " + remetente
      correio['To']=nome +", " + destinatario
      correio.attach(MIMEText(corpo_html,"html"))

      if filename != "":
         # add filecontent into file
          f = open(filename + "_verified", "w") 
          f.write(filecontent)
          f.close()
          
      attach_file_name = filename
      attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
      payload = MIMEBase('application', 'octate-stream')
      payload.set_payload((attach_file).read())
      encoders.encode_base64(payload) #encode the attachment
      #add payload header with filename
      payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
      correio.attach(payload)

      try:
        smtpObj = smtplib.SMTP("mail.scorpionbonus.pt",587)
        smtpObj.starttls()
        smtpObj.login("dual@scorpionbonus.pt","Dual2023!")
        smtpObj.sendmail(remetente,destinatario,correio.as_string())
        smtpObj.close()
        print("Enviado com Sucesso!")
        return True
      except Exception as erro:
        print("Erro de envio:" + str(erro))
        return False
