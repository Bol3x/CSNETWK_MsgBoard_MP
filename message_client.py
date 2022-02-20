import socket
import sys
import json

username = input("Enter username: ")
msg_message = "This is my message."

msg_register = {"command":"register","username":username}
msg_deregister = {"command":"deregister","username":username}

server_addr = input("Enter server address: ")
server_port = input("Port:")
server_port = int(server_port)

buffer_size = 1024

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    #register the user
    print("Registering as " + username)
    send_msg = json.dumps(msg_register).encode('utf-8')
    sock.sendto(send_msg, (server_addr, server_port))

    recv, address = sock.recvfrom(1024)
    #convert the received string into a json dict
    recv_json = json.loads(recv)
    recv_code = int(recv_json.get('code_no'))
    
    if recv_code == 502:
        print("Username is already taken.")
        print("Closing socket...")
        sock.close()
        
    else:
        print("Registration successful")
    
        while True:
            msg_message = input("Enter message to send (type q to quit): ")

            #quit
            if msg_message == "q":
                #send a dereg message and then close socket
                print("Leaving server...")
                dereg_msg = json.dumps(msg_deregister).encode('utf-8')
                sock.sendto(dereg_msg, (server_addr, server_port))
                
                recv, addr = sock.recvfrom(1024)
                recv_json = json.loads(recv)
                recv_code = int(recv_json.get('code_no'))
                if recv_code == 401:
                    print("Left the server.")
                    print("Closing socket.")
                    sock.close()
                    break
                else:
                    print("Server returned error code ", recv_code)

            else:
                msg_send = {"command":"msg","username":username,"message":msg_message}

                #send message
                send_msg = json.dumps(msg_send).encode('utf-8')
                sock.sendto(send_msg, (server_addr, server_port))
                recv, address = sock.recvfrom(1024)
                #convert the received string into a json dict
                recv_json = json.loads(recv)
                recv_code = int(recv_json.get('code_no'))

                if recv_code != 401:
                    print("Server returned error code ", recv_code)
                
                else:
                    print("Message sent.")

except Exception as e:
    print("Error received: ")
    print(e)
    print(e.__traceback__)
    print("closing socket.")
    sock.close()