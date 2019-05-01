from pprint import pprint

import json
import requests

class mailboxClient():
    def __init__(self, username, serv_addr, serv_password):
        """
        Summary: Class that manages the HTTP interactions with a mailboxServer

        Args:
            username (string): Username that will identify the client for current session
            serv_addr (string): Target mailbox server to connect to in format ip_addr:port
            serv_password (string): Target mailbox server's password
        """
        self.serv_addr = serv_addr
        self.serv_pw = serv_password
        self.username = username

    def send_mail(self, address, temp):
        """
        Summary: Sends a POST message to the server to add mail

        Args:
            address (string): Target mailbox server to send mail to in format ip_addr:port
            subject (string): Message subject
            body (string): Message body
        """

        # This header sets the HTTP request's mimetype to `application/json`.
        # This means the payload of the HTTP message will be formatted as a
        # JSON object
        headers = {
            'Content-Type': 'application/json',
            'Authorization': None   # not using HTTP secure
        }

        # The payload of our message starts as a simple dictionary. Before sending
        # the HTTP message, we will format this into a JSON object
        payload = {
            'temp': temp,
            'sender': self.username
        }

        # Send an HTTP POST message and block until a response is given.
        # Note: requests is NOT the same thing as the request from the Flask
        # library.
        response = requests.get("http://{}/mailbox/search".format(address),
                                 headers=headers,
                                 data=json.dumps(payload))

        # Print the JSON object from the HTTP response in a pretty format
        pprint(response.json())

    