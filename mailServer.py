from flask import Flask
from flask import jsonify
from flask import request

import argparse
import json
import mailboxManager
import math

app = Flask('RaspberryPi Mailbox Server')

in_temp2 = 2


@app.route('/send-mail', methods=['POST'])
def post_mail_callback():

    global in_temp2

    payload = request.get_json()
    in_temp = int(payload["temp"])

    # Print incomming temp
    print("Incomming encrypted temp = " + str(in_temp))
    in_temp2 = math.sqrt(in_temp)
    print("Incomming decrypted temp = " + str(in_temp2))
    print(payload)

    if (in_temp2>60) and (in_temp2 <100):
        mailbox_manager.add_mail(payload)
        response = {'Response': 'Mail sent', 'Recieved': in_temp2}
    else:
        response = {'Response': 'Invalid temp sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return in_temp2

if __name__ == '__main__':

    in_temp2 = 0

    # Set up argparse, a Python module for handling command-line arguments
    parser = argparse.ArgumentParser(prog='mailServer',
            description='Script to start up mail server')

    parser.add_argument('-p', metavar='password', required=True,
            help='Required password to access server')

    args = parser.parse_args()

    mailbox_password = args.p   # password
    mailbox_manager = mailboxManager.mailboxManager()

    app.run(debug=False, host='rpi-jaeishin', port=5596)







