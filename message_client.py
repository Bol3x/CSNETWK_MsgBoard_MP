import socket
import sys
import json

username = input("Enter username: ")
msg_message = "This is my message."

msg_register = {"command":"register","username":username}
msg_deregister = {"command":"deregister","username":username}
msg_send = {"command":"msg","username":username,"message":msg_message} #might move this

server_addr = input("Enter server address: ")
server_port = input("Port:")
server_port = int(server_port)

buffer_size = 1024

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    #register the user
    print("Registering as " + username)
    sock.sendto(json.dumps(msg_register), (server_addr, server_port))

    recv, address = sock.recvfrom(1024)
    #convert the received string into a json dict
    recv_json = json.loads(recv)
    recv_code = int(recv_json["ret_code"])

except:
    print("Error received, closing connection")
    sock.close()

if recv_code != 401:
    print("Server returned error code " + recv_code)
    print("Closing socket")
    sock.close()

print("Registration successful")

while True:
    msg_message = input("Enter message to send (type q to quit): ")

    #quit
    if msg_message = "q":
        break

    #send message
    sock.sendto(json.dumps(msg_send), (server_addr, server_port))
    recv, address = sock.recvfrom(1024)
    #convert the received string into a json dict
    recv_json = json.loads(recv)
    recv_code = int(recv_json["ret_code"])

    if recv_code != 401:
        print("Server returned error code "  + recv_code)
        break 


#send a dereg message and then close socket
sock.sendto(json.dumps(msg_deregister), (server_addr, server_port))
sock.close()
