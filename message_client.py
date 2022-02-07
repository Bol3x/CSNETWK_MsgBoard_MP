import socket
import sys
import json

msg_register = {"command":"register","username":"user01"}
msg_deregister = {"command":"deregister","username":"user01"}
msg_send = {"command":"msg","username":"user01","message":"This is my message."}