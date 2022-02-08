import socket
import sys
import json

#server return messages
incomplete_param_msg = server_msg = {'command':'ret_code', 'code_no':201}   #incomplete command parameters
unknown_command_msg = {"command":"ret_code", "code_no":301}                 #unknown command
success_command_msg = {"command":"ret_code", "code_no":401}                 #successful command
unknown_user_msg = {"command":"ret_code", "code_no":501}                    #unknown user referenced
existing_user_msg = {"command":"ret_code", "code_no":502}                   #existing user registered


#buffer size of datagram
buffer_size = 1024

#server connection details
server_addr = input("Input the server address: ")
server_port = input("Input the server port: ")
server_port = int(server_port)

#list of registered users
clients = []

#create socket to server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_addr, server_port))

print("Server is now waiting for requests.")
while True:
    #listen for data from clients
    data, address = server_socket.recvfrom(buffer_size)

    json_msg = json.loads(data)                 #convert json data into dictionary type
    command = str(json_msg.get('command'))      #obtain command type of message
        
    #register command
    if command == 'register':
        if len(json_msg) != 2:
            server_msg = incomplete_param_msg
            
        elif json_msg.get('username') in clients:
            server_msg = existing_user_msg
        
        else:
            #add new user to list of registered clients
            clients.append(json_msg.get('username'))
            
            #return success message to client
            server_msg = success_command_msg
            
            #display list of users registered to server
            print("New user added: {user}".format(user=json_msg.get('username')))
            print("Current users in message board: ", clients)
            
        
    #deregister command     
    elif command == 'deregister':
        if len(json_msg) != 2:
            server_msg = incomplete_param_msg
            
        elif json_msg.get('username') not in clients:
            server_msg = unknown_user_msg
            
        else:
            #remove user from list of registered clients
            clients.remove(json_msg.get('username'))
            
            #return success message to client
            server_msg = success_command_msg
            
            print("{user} left the message board.".format(user=json_msg.get('username')))
            print("Current users in message board: ", clients)
            
            
    #message command
    elif command == 'msg':
        if len(json_msg) != 3:
            server_msg = incomplete_param_msg
        
        else:
            #display message to server
            fwd_msg = "From {username}: {msg}".format(username = json_msg.get('username'), msg = json_msg.get('message'))
            print(fwd_msg)
            server_msg = success_command_msg    #return success message to sender
            
        
    #unknown command case
    else:
        server_msg = unknown_command_msg
    
    ret_msg = json.dumps(server_msg).encode('utf-8')
    server_socket.sendto(ret_msg, address)