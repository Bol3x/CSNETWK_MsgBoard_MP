import socket
import sys
import json

#buffer size of datagram
buffer_size = 1024

#server connection details
server_addr = input("Input the server address: ")
server_port = input("Input the server port: ")

#list of registered users
clients = []

#create socket to server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_addr, server_port)

print("Server is now waiting for requests.")
while True:
    #listen for data from clients
    data, address = server_socket.recvfrom(buffer_size)

    json_msg = json.load(data)      #convert json data into dictionary type
    command = json_msg['command']   #obtain command type of message
    
    #switch statement for server commands
    match command:
        case 'register':
            if len(json_msg) != 2:
                server_msg = {'command':'ret_code', 'code_no':201}
                
            elif json_msg['username'] in clients:
                server_msg = {'command':'ret_code', 'code_no':502}
            
            else:
                #add new user to list of clients registered
                clients.append(json_msg['username'])
                
                #return success message to client
                server_msg = {'command':'ret_code', 'code_no':401}
                
                #display list of users registered to server
                print("New user added: %s" %json_msg['username'])
                print("Current users in message board: ", clients)
                
            ret_msg = json.dumps(server_msg)
            server_socket.sendto(ret_msg, address)
            
                    
        case 'deregister':
            if len(json_msg) != 2:
                server_msg = {'command':'ret_code', 'code_no':201}
                
        case 'msg':
            if len(json_msg) != 3:
                server_msg = {'command':'ret_code', 'code_no':201}
            
                
    