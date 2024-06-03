import socket
import argparse
import random
import threading
import time
import datetime

HOST = '127.0.0.1'
PORT = 8000
parser = argparse.ArgumentParser()
parser.add_argument("port", nargs='?', default=PORT)
args = parser.parse_args()
PORT = int(args.port)
clients = []
post_number = 1
today = datetime.datetime.now()

class client():
    def __init__(self, name, password, email, login = False, now = False):
        self.name = name
        self.password = password
        self.login = login
        self.email = email
        self.number = []

class comment():
    def __init__(self,name,words):
        self.name = name
        self.words = words

class post():
    def __init__(self,author,title):
        self.author = author
        self.title = title
        self.content = None
        self.date = str(today.month)+"/"+str(today.day)
        self.comments = []
        self.number = None

class board():
    def __init__(self,name,mod):
        self.name = name
        self.mod = mod
        self.posts = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_server.bind((HOST, PORT))
server.listen(10)

def generate():
    global clients
    a = client("andy","123","andy@aaa.com")
    b = client("ben","123","ben@aaa.com")
    c = client("cena","123","cena@aaa.com")
    d = client("deny","123","deny@aaa.com")
    e = client("eve","123","eve@aaa.com")
    f = client("froggy","123","froggy@aaa.com")
    g = client("gina","123","gina@aaa.com")
    h = client("horn","123","horn@aaa.com")
    i = client("ian","123","ian@aaa.com")
    j = client("john","123","john@aaa.com")
    clients = [a,b,c,d,e,f,g,h,i,j]

now = []
boards = []
posts = []
b_name = []
chats = []
ports = {}
state = {}
def TCP_react(cmsg,login,number):
    global now,clients,post_number,b_name,boards,chats
    smsg = ""
    #login reaction
    if cmsg[0] == "login" and len(cmsg) == 3:
        if login == False:
            if len(clients) == 0:
                smsg = "Login failed."
            else:
                for item in clients:
                    if cmsg[1] == item.name:
                        if cmsg[2] == item.password:
                            #item.login = True
                            #login = True
                            now[number] = item
                            smsg = "Welcome, " + item.name+"."
                        else:
                            smsg = "Login failed."
                        break
                    elif cmsg[1] == item.name and item.login == True:
                        smsg = "Please logout first"
                        break
                    else:
                        smsg = "Login failed."
        elif login == True:
            smsg = "Please logout first"
        else:
            smsg = "Login failed."
    elif cmsg[0] == "login" and len(cmsg) < 3:
        smsg = "Usage: login <username> <password>"
    #logout
    elif cmsg[0] == "logout":
        if now[number] != None and now[number].name in list(state.keys()):
            if login == True and state[now[number].name] == "close":
                smsg = "Bye, " + now[number].name +"."
                now[number]  = None
                login = False
            elif state[now[number].name] == "open":
                smsg = "Please do “attach” and “leave-chatroom” first."
        else:
            if login == True:
                smsg = "Bye, " + now[number].name +"."
                now[number]  = None
                login = False
            else:
                smsg = "Please login first."
    #list
    elif cmsg[0] == "list-user":
        smsg = "Name            Email"
        for item in clients:
            smsg += "\n"+item.name+"     "+item.email
    #exit 
    elif cmsg[0] == "exit":
        smsg = "exit"
        try:
            state[now[number].name] = "close"
        except:
            pass
    #creat-board
    elif cmsg[0] == "create-board":
        if login == False:
            smsg = "Please login first"
        else:
            if  cmsg[1] in b_name:
                smsg = "Board already exists"
            else:
                smsg = "Create board successfully"
                boards.append(board(cmsg[1],now[number].name))
                b_name.append(cmsg[1])
    #creat-post
    elif cmsg[0] == "create-post":
        if login == False:
            smsg = "Please login first"
        else:
            if  cmsg[1] not in b_name:
                smsg = "Board does not exists"
            else:
                for item in boards:
                    if cmsg[1] == item.name:
                        num = 0
                        _title = cmsg[3]
                        for i in range(4,len(cmsg)):
                            if cmsg[i] == "--content":
                                num = i+1
                                break
                            _title += " "
                            _title += cmsg[i]
                        temp = post(now[number].name,_title)

                        temp.content = cmsg[num].split("<br>")[0]
                        try:
                            temp += "\n" + cmsg[num].split("<br>")[1]
                        except:
                            pass
                        for i in range(num+1,len(cmsg)):
                            temp.content += " " + cmsg[i].split("<br>")[0]
                            try:
                                temp.content += "\n" + cmsg[i].split("<br>")[1]
                            except:
                                pass
                        temp.number = post_number
                        posts.append(temp)

                        item.posts.append(post_number)
                        post_number += 1
                        smsg = "Create post successfully"
                        break
    #list-board
    elif cmsg[0] == "list-board":
        index = 1
        smsg = "Index".ljust(5) + "Name".center(8) + "Moderator".rjust(5)
        for i in range(len(boards)):
            smsg += "\n"
            smsg += str(i+1).ljust(5) + boards[i].name.center(8) + boards[i].mod.rjust(5)
    #list-post
    elif cmsg[0] == "list-post":
        if cmsg[1] not in b_name:
            smsg = "Board does not exists"
        else:
            smsg = "S/N".ljust(5) + "Title".center(8) + "Author".center(5) + "Date".rjust(5)
            for item in boards:
                if item.name == cmsg[1]:
                    for i in range(len(posts)):
                        if i+1 in item.posts and posts[i] != None:
                            smsg += "\n"
                            smsg += str(posts[i].number).ljust(5) + posts[i].title.center(8) + posts[i].author.center(8) + posts[i].date.rjust(5)
    #read
    elif cmsg[0] == "read":
        if int(cmsg[1]) not in range(len(posts)+1) or  posts[int(cmsg[1])-1]==None:
            smsg = "Post not exist"
        else:
            i =  int(cmsg[1])-1
            smsg = "Author:" + posts[i].author + "\n"
            smsg += "Title:" + posts[i].title + "\n"
            smsg += "Date:" + posts[i].date + "\n--\n"
            smsg += posts[i].content + "\n"
            smsg += "--"
            for item in posts[i].comments:
                smsg += "\n"
                smsg += item.name + ": " + item.words
    #delete
    elif cmsg[0] == "delete-post":
        i =  int(cmsg[1])-1
        if login == False:
            smsg = "Please login first"
        elif i+1 not in range(len(posts)+1) or posts[i] == None:
            smsg = "Post not exist"
        elif now[number].name != posts[i].author:
            smsg = "Not the post owner"
        else:
            posts[i] = None
            smsg = "Delete successfully"
    #update-post
    elif cmsg[0] == "update-post":
        i =  int(cmsg[1])-1
        if login == False:
            smsg = "Please login first"
        elif i+1 not in range(len(posts)+1) or posts[i] == None:
            smsg = "Post not exist"
        elif now[number].name != posts[i].author:
            smsg = "Not the post owner"
        else:
            if cmsg[2] == "--title":
                posts[i].title = cmsg[3]
                for j in range(4,len(cmsg)):
                    posts[i].title += " " + cmsg[j]
            else:
                posts[i].content = cmsg[3].split("<br>")[0]
                try:
                    posts[i] += "\n" + cmsg[3].split("<br>")[1]
                except:
                    pass
                for j in range(4,len(cmsg)):
                    posts[i].content += " " + cmsg[j].split("<br>")[0]
                    try:
                        posts[i].content += "\n" + cmsg[j].split("<br>")[1]
                    except:
                        pass
            smsg = "Update successfully"
    #comment
    elif cmsg[0] == "comment":
        i =  int(cmsg[1])-1
        if login == False:
            smsg = "Please login first"
        elif i+1 not in range(len(posts)+1) or posts[i] == None:
            smsg = "Post not exist"
        else:
            temp = comment(now[number].name,cmsg[-1])
            posts[i].comments.append(temp)
            smsg = "Comment successfully"
    #create-chatroom
    elif cmsg[0] == "create-chatroom":
        if login == False:
            smsg = "Please login first"
        elif now[number].name in chats:
            smsg = "User has already created the chatroom"
        else:
            smsg = "start to create chatroom..."
            chats.append(now[number].name)
            ports[now[number].name] = cmsg[-1]
            state[now[number].name] = "open"
    #join-chatroom
    elif cmsg[0] == "join-chatroom":
        if login == False:
            smsg = "Please login first"
        elif cmsg[-1] not in chats or state[cmsg[-1]] == "close":
            smsg = "The chatroom does not exist or the chatroom is close"
        else:
            smsg = "join "
            smsg += ports[cmsg[-1]]
    #restart-chatroom
    elif cmsg[0] == "restart-chatroom":
        if login == False:
            smsg = "Please login first"
        elif now[number].name not in chats:
            smsg = "Please create-chatroom first"
        elif state[now[number].name] == "open":
            smsg = "Your chat room is still running"
        else:
            state[now[number].name] = "open"
            smsg = "start to create chatroom..."
    #leave-chatroom
    elif cmsg[0] == "leave-chatroom":
        if cmsg[-1] == "yes":
            state[now[number].name] = "close"
        smsg = "Welcome back to BBS"
    else:
        smsg = 'wrong method'
    return smsg

def UDP_react(cmsg,number):
    smsg = ""
    #rigister
    if cmsg[0] == "register" and len(cmsg) ==4:
        exist = False
        for item in clients:
            if cmsg[1] == item.name:
                smsg = "Username already used."
                exist = True
                break
        if exist == False:
            temp = client(cmsg[1],cmsg[3],cmsg[2])
            clients.append(temp)
            smsg = "Register successfully."
    elif cmsg[0] == "register" and len(cmsg) < 4:
        smsg = "Usage: register <username> <email> <password>"
    #whoami
    elif cmsg[0] == "whoami" :
        if cmsg[-1] == str(0):
            smsg = "Please login first."
        else:
            for item in clients:
                for i in range(len(item.number)):
                    if str(item.number[i]) == cmsg[-1]:
                        smsg = item .name
                        break
    #list-chatroom
    elif cmsg[0] == "list-chatroom":
        if int(cmsg[-1]) == 0:
            smsg = "Please login first"
        else:
            smsg = "Chatroom_name".ljust(8) + "Status".rjust(8)
            for item in chats:
                smsg += "\n"
                smsg += item.ljust(8) + state[item].rjust(8)
    return smsg

def TCP(connect,number):
    rn = 0
    login = False
    while True:
        cmsg = str(connect.recv(1024), encoding='utf-8').split(' ')
        print('Client message is:', cmsg)
        smsg = TCP_react(cmsg,login,number)
        
        if smsg.split(' ')[0] == "Welcome,":
            login = True
            rn = random.randrange(1,1000)
            now[number].number.append(rn)
            connect.send(smsg.encode())
            time.sleep(0.1)
            connect.send(str(rn).encode())
        elif smsg.split(' ')[0] == "start":
            connect.send(smsg.encode())
            time.sleep(0.1)
            connect.send(str(ports[now[number].name]).encode())
        elif smsg.split(' ')[0] == "Bye,":
            login = False
            connect.send(smsg.encode())
        elif smsg == "exit":
            connect.send(smsg.encode())
            break
        else:
            connect.send(smsg.encode())
def UDP(number):
    while True:
        cmsg,addr = _server.recvfrom(1024)
        cmsg = cmsg.decode().split(' ')
        print('Client message is:', cmsg)
        smsg = UDP_react(cmsg,number)
        _server.sendto(smsg.encode(),addr)
def listen(connect,number):
    TCP_thread = threading.Thread(target=TCP,args=(connect,number,))
    TCP_thread.start()
def main():
    global now
    number = 0
    UDP_thread = threading.Thread(target=UDP,args=(number,))
    UDP_thread.start()
    while True:
        (connect, addr) = server.accept()
        print("Nem connection")
        _thread = threading.Thread(target=listen,args=(connect,number,))
        number +=1
        now.append(None)
        _thread.start()
    connect.close()

if __name__ == "__main__":
    #generate()
    main()