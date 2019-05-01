from flask import Flask
from flask import jsonify
from flask import request

import argparse
import json
import mailboxManager

app = Flask('RaspberryPi Mailbox Server')

@app.route('/send-mail', methods=['POST'])
def post_mail_callback():
    """
    Summary: A callback for when POST is called on [host]:[port]/mailbox/send-mail

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the sender, subject and body parameters
    payload = request.get_json()
    incomming_temp = payload["temp"]
    print(payload)
    print(incomming_temp)

    mailbox_manager.add_mail(payload)
    response = {'Response': 'Mail sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

if __name__ == '__main__':
    # Set up argparse, a Python module for handling command-line arguments
    parser = argparse.ArgumentParser(prog='mailServer',
            description='Script to start up mail server')

    parser.add_argument('-p', metavar='password', required=True,
            help='Required password to access server')

    args = parser.parse_args()

    mailbox_password = args.p   # password
    mailbox_manager = mailboxManager.mailboxManager()

    app.run(debug=False, host='0.0.0.0', port=5047)







