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
    msg_send = json.dumps(msg_register).encode('utf-8')
    sock.sendto(msg_send, (server_addr, server_port))

    recv, address = sock.recvfrom(1024)
    #convert the received string into a json dict
    recv_json = json.loads(recv)
    recv_code = int(recv_json.get('code_no'))
    
    if recv_code != 401:
        print("Server returned error code " + recv_code)
        print("Closing socket")
        sock.close()

    print("Registration successful")

except Exception as e:
    print("Error received: ")
    print(e)
    print("closing connection")
    sock.close()


while True:
    msg_message = input("Enter message to send (type q to quit): ")

    #quit
    if msg_message == "q":
        break

    #send message
    send_msg = json.dumps(msg_send).encode('utf-8')
    sock.sendto(send_msg, (server_addr, server_port))
    recv, address = sock.recvfrom(1024)
    #convert the received string into a json dict
    recv_json = json.loads(recv)
    recv_code = int(recv_json.get('code_no'))

    if recv_code != 401:
        print("Server returned error code "  + recv_code)
        break 


#send a dereg message and then close socket
print("Closing connection")
send_msg = json.dumps(msg_deregister).encode('utf-8')
sock.sendto(send_msg, (server_addr, server_port))
sock.close()
