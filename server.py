import socket
import threading
from datetime import datetime
from smtpmail import mail


def validamensagem(_v):   
   for tk in tokens:
      if _v==tk:
        return True      

   return False

def comrecebida(conn):
   try:
      print("Nova conexão:",conn)
      lermen=True
      while lermen:
          dados=b''
          while True:
             buff=conn.recv(64)         
             if len(buff)>0:
                 dados +=buff
                 if b';EOF' in dados:         
                   break
             else:
               lermen=False
               break
               
          data_decoded=dados.decode()
          groupofdata = data_decoded.replace(";EOF","")
          data = groupofdata.split(";")
          
          if data[0]=="Valida":  
            print("Valida")
            print(data[1])          
            dest = data[1]
            rem = data[2]
            ass = data[3]
            body = data[4]
            filename = data[5]
            filedata =data[6]
            response = mail.envio(rem,dest,ass, body, filename, filedata)
            if response==True:
              res="Enviado com Sucesso"
              conn.sendall(res.encode())
            else:
               res="Tenta noutra altura"
          else:
              res="Não permitido"
              conn.sendall(res.encode())
   except AssertionError as error:
     #print(error)
     print(":(  -- Com terminada remotamente.")
   finally:
     print(":(")

   # 6. close socket
   conn.close()      
   quit()

#inicio

tokens = []

# 1. create a socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address=('127.0.0.1',10000)
print('A reservar porta 10000')

# 2. bind the socket to a specific address and port
sock.bind(server_address)

# 3. listen for incoming connections
sock.listen(30)

while True:
   print("A espera de conexao:")
   # 4. accept connections
   connection, client = sock.accept()
   # 5. read / write
   th = threading.Thread(target=comrecebida, args=(connection,))
   th.start()
