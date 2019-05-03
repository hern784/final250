from pprint import pprint


import json
import requests

class mailboxClient():
    def __init__(self, username, serv_addr, serv_password):
      
        self.serv_addr = serv_addr
        self.serv_pw = serv_password
        self.username = username

    def send_mail(self, address, temp):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': None   # not using HTTP secure
        }

        payload = {
            'temp': temp,
            'sender': self.username
        }

        response = requests.post("http://{}/send-mail".format(address),
                                 headers=headers,
                                 data=json.dumps(payload))

        pprint(response.json())

    