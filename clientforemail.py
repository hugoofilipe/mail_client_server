import time
import socket
import os

debug=False

# create method or debug
def debug_print(mensagem):
    if debug:
        print(mensagem)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('127.0.0.1',10000)
sock.connect(server_address)

#method where receice the question, request input and return the input
def prompt_fields(question):
    while True:
        try:
            data = input(question)
            if len(data) > 0:
                return data
        except ValueError:
            print("Invalid input")

def attach_file_request(question):
    while True:
        try:
            data = input(question)
            if len(data) > 0:
                if data == "S":
                    filename, data = prompt_file("Nome do ficheiro:")
                    return filename, data
                elif data == "N":
                    return False
        except ValueError:
            print("Invalid input")

def prompt_file(question):
    while True:
        try:
            filename = input(question)
            if len(filename) > 0:
                if os.path.isfile(filename):
                    #save file data in variable
                    f = open(filename, "r")
                    data = f.read()
                    f.close()
                    return filename, data
                else:
                    print("File not found")
        except ValueError:
            print("Invalid input")

destinatario = prompt_fields("Definir o destinatário:")
remetente = prompt_fields("Definir o remetente:")
assunto = prompt_fields("Definir o assunto:")
corpo = prompt_fields("Definir o corpo:")
filename, data = attach_file_request("Anexar ficheiro? (S/N):")

print("filename: " + filename)
print("data: " + data)  
mens = destinatario+";"+remetente+";"+assunto+";"+corpo+";"
mens += filename+";" if filename else ""
mens += data if data else ""

# debug_print("Mensagem a enviar: " + mens)

sock.sendall(("Valida;"+mens+';EOF').encode())
data=sock.recv(1024)

debug_print(""+data.decode()+"")
