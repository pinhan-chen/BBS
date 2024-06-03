import socket
import argparse
import threading
import time
import datetime

today = datetime.datetime.now()

class chatroom():
    detach = False
    inchat = False
    exist = False
    state = False
    member = []
    message = []
    
_chat = chatroom()

HOST = '127.0.0.1'
PORT = 8000
parser = argparse.ArgumentParser()
parser.add_argument("host", nargs='?', default=HOST)
parser.add_argument("port", nargs='?', default=PORT)
args = parser.parse_args()
PORT = int(args.port)
HOST = args.host
check = True
addr = (HOST,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((HOST, PORT))
_client.connect((HOST, PORT))
c_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


method = "TCP"
rn = 0
_port = 1111

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
name = ""
run = False

def main():
    global rn, _port,name,_chat,run
    while True:
        # time.sleep(0.3)
        run = True
        message = str(input("% "))
        if message == "attach":
            if rn == str(0):
                print("Please login first")
                continue
            elif _chat.exist == False:
                print("Please create-chatroom first")
                continue
            elif _chat.state == False:
                print("Please restart-chatroom first")
                continue
            else:
                _chat.detach = False
                chat_server(_port,1)
                if _chat.inchat == False:
                    _chat.state = False
                continue
        elif message.split(' ')[0] == "register" or message == "whoami" or message == "list-chatroom":
            if message == "whoami" or message == "list-chatroom":
                message += " " + str(rn)
                _client.sendto(message.encode(),(HOST,PORT))
            else:
                _client.sendto(message.encode(),(HOST,PORT))
            method = "UDP"
        else:
            client.send(message.encode())
            method = "TCP"
        
        if method == "TCP":
            serverMessage = str(client.recv(1024), encoding='utf-8')
            if serverMessage.split(' ')[0] == "Welcome,":
                name = message.split(' ')[1]
                rn = str(client.recv(1024), encoding='utf-8')
            if serverMessage.split(' ')[0] == "start":
                _port = int(str(client.recv(1024), encoding='utf-8'))
                print(serverMessage)
                chat_server(_port,0)
                if _chat.inchat == False:
                    _chat.state = False
                continue
            if serverMessage.split(' ')[0] == "join":
                _port = int(serverMessage.split(' ')[-1])
                chat_client(_port)
                continue
        else:
            serverMessage,_addr = _client.recvfrom(1024)
            serverMessage = serverMessage.decode()
        
        if serverMessage.split(' ')[0] == "start" or serverMessage.split(' ')[0] == "join":
            continue
        elif serverMessage != "exit":
            if serverMessage.split(' ')[0] == "Bye, ":
                rn = 0
            print(serverMessage)
        
        else:
            break
    client.close()

def chat_server(port,num):
    global _port,_chat,run,HOST,c_server
    message = "Welcome to chatroom"
    if len(_chat.message) != 0:
        for item in _chat.message:
            message += "\n"
            message += str(item)
    print(message)
    _chat.detach = False
    
    if _chat.state == False:
        run = True
        _chat.exist = True
        _chat.state = True
        _chat.inchat = True
        try:
            c_server.bind((HOST,port))
            c_server.listen(10)
        except:
            c_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_send = threading.Thread(target=send_server,args=(), daemon=True) 
        TCP_send.start()
        TCP_server = threading.Thread(target=server,args=(), daemon=True) 
        TCP_server.start()
    else:
        TCP_send = threading.Thread(target=send_server,args=(), daemon=True) 
        TCP_send.start()
    while True:
        if _chat.detach == True:
            try:
                c_server.shutdown(2)
                c_server.close()
            except:
                pass
            break
    try:
        c_server.shutdown(2)
        c_server.close()
    except:
        pass
def server():
    global _chat,c_server
    while _chat.state:
        try:
            (connect, addr) = c_server.accept()
        except:
            break
        _name = str(connect.recv(1024), encoding='utf-8')
        message = "sys [" + str(today.hour) + ":" + str(today.minute) + "] : " + _name + " join us"
        if not _chat.detach:
            print(message)
        
        for item in _chat.member:
            item.send(message.encode())

        message = "Welcome to chatroom"
        if len(_chat.message) != 0:
            for item in _chat.message:
                message += "\n"
                message += str(item)
        connect.send(message.encode())

        _chat.member.append(connect)
        TCP_thread = threading.Thread(target=listen_server,args=(connect,), daemon=True)
        TCP_thread.start()
    # c_server.shutdown(2)
    # c_server.close()

def listen_server(connect):
    global run,_chat
    while run == True:
        try:
            cmsg = str(connect.recv(1024), encoding='utf-8')
        except:
            break
        if cmsg == "":
            continue
        if cmsg.split(' ')[-1] == "logout" or cmsg.split(' ')[-1] == "leave-chatroom":
            _chat.member.remove(connect)
            message = "sys [" + str(today.hour) + ":" + str(today.minute) + "] : " + cmsg.split('[')[0] + " leave us"
            for item in _chat.member:
                item.send(message.encode())
            print(message)
            break
        else:
            if len(_chat.message)<3:
                _chat.message.append(cmsg)
            else:
                del(_chat.message[0])
                _chat.message.append(cmsg)
        if len(_chat.member) != 0:
            for item in _chat.member:
                try:
                    item.send(cmsg.encode())
                except:
                    pass
        if _chat.detach:
            continue
        else:
            print(cmsg)
        if _chat.state == False:
            break

def send_server():
    global run,client,name,_chat,rn,c_server
    while run == True:
        message = name+"[" + str(today.hour) + ":" + str(today.minute) + "] : "
        message += str(input())
        if message.split(' ')[-1] == "detach":
            _chat.detach = True
            break
        if message.split('-')[-1] == "chatroom":
            message = "sys[" + str(today.hour) + ":" + str(today.minute) + "] : the chatroom is close"
            for item in _chat.member:
                item.send(message.encode())
            # time.sleep(0.1)
            client.send("leave-chatroom yes".encode())
            cmsg = str(client.recv(1024), encoding='utf-8')
            print(cmsg)
            _chat.inchat = False
            _chat.detach = True
            _chat.state = False
            try:
                c_server.shutdown(2)
                c_server.close()
            except:
                pass
            break
        if message.split(' ')[-1] != "logout":
            if len(_chat.message)<3:
                _chat.message.append(message)
            else:
                del(_chat.message[0])
                _chat.message.append(message)

        if message.split(' ')[-1] == "logout":
            client.send("logout".encode())
            cmsg = str(client.recv(1024), encoding='utf-8')
            print(cmsg)
            if cmsg.split(' ')[0] == "Bye,":
                rn = 0
                run = False
                break
        else:
            for item in _chat.member:
                item.send(message.encode())
def chat_client(_port):
    global run,name
    run = True
    c_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_client.connect((HOST, _port))
    c_client.send(name.encode())
    chat_tcp = threading.Thread(target=chat_TCP,args=(c_client,), daemon=True)
    chat_tcp.start()
    while True:
        if not run: 
            break
    c_client.shutdown(2)
    c_client.close()
def chat_TCP(c_client):
    TCP_listen = threading.Thread(target=listen,args=(c_client,), daemon=True)
    TCP_send = threading.Thread(target=send,args=(c_client,), daemon=True) 
    TCP_listen.start()
    TCP_send.start()
    while True:
        if run == False: 
            break
def listen(connect):
    global run,name,check
    while run == True:
        try:
            cmsg = str(connect.recv(1024), encoding='utf-8')
        except:
            break
        if cmsg.split('[')[0] == "sys" and cmsg.split(' ')[-1] == "close":
            print(cmsg)
            print("Welcome back to BBS\n% ",end='')
            check = False
            break
        if cmsg.split('[')[0] != name and cmsg.split(' ')[-1] != "logout" and cmsg.split(' ')[-1] != "leave-chatroom" and cmsg.split(' ')[-1] != "detach":
            print(cmsg)
        elif cmsg.split('[')[0] == name and cmsg.split(' ')[-1] == "logout" :
            break
        elif cmsg.split('[')[0] == name and cmsg.split(' ')[-1] == "leave-chatroom":
            check = False
            break
    run = False
def send(connect):
    global run,client,name,rn,method,_client
    while run == True:
        message = name+"[" + str(today.hour) + ":" + str(today.minute) + "] : "
        temp = str(input())
        message += temp
        # time.sleep(0.1)
        if not check:
            if temp == "register" or temp == "whoami" or temp == "list-chatroom":
                if temp == "whoami" or temp == "list-chatroom":
                    temp += " " + str(rn)
                    _client.sendto(temp.encode(),(HOST,PORT))
                else:
                    _client.sendto(temp.encode(),(HOST,PORT))
                method = "UDP"
            else:
                client.send(temp.encode())
                method = "TCP"
        
            if method == "TCP":
                serverMessage = str(client.recv(1024), encoding='utf-8')
                
            else:
                serverMessage,_addr = _client.recvfrom(1024)
                serverMessage = serverMessage.decode()
            print(serverMessage)
            break
        if message.split(' ')[-1] == "logout":
            connect.send(message.encode())
            client.send("logout".encode())
            cmsg = str(client.recv(1024), encoding='utf-8')
            print(cmsg)
            if cmsg.split(' ')[0] == "Bye,":
                rn = 0
                run = False
        elif message.split(' ')[-1] == "leave-chatroom":
            connect.send(message.encode())
            client.send("leave-chatroom".encode())
            cmsg = str(client.recv(1024), encoding='utf-8')
            print(cmsg)
            if cmsg.split(' ')[0] == "Welcome":
                run = False
        else:
            connect.send(message.encode())
        if not check:
            run = False
            break
if __name__ == "__main__":
    main()