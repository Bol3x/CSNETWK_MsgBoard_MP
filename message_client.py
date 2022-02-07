import socket
import sys
import json

username = input("Enter username: ")

msg_register = {"command":"register","username":username}
msg_deregister = {"command":"deregister","username":username}
msg_send = {"command":"msg","username":username,"message":"This is my message."}

server_addr = input("Enter server address: ")
server_port = input("Port:")
server_port = int(server_port)

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)