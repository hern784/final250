from flask import Flask
from flask import jsonify
from flask import request

import argparse
import json
import mailboxManager

app = Flask('RaspberryPi Mailbox Server')

@app.route('/mailbox/search', methods=['GET'])
def search_mailbox_callback():
    password = request.args.get('password')
    text = request.args.get('text')
    field = request.args.get('field')
    print(str(password) + str(text) + str(field))

    if password == mailbox_password:
        response = jsonify(mailbox_manager.get_mail(field, text))
        payload = request.get_json()
        in_temp = payload["temp"]
        print(in_temp)
        print(payload)

        mailbox_manager.add_mail(payload)
        response = {'Response': 'Mail sent'}

    # The object returned will be sent back as an HTTP message to the requester
        return json.dumps(response)
        
    else:
        if password == None:
            response = jsonify({'Response': 'Missing password'})

        else:
            response = jsonify({'Response': 'Password does not match'})

    return response  

@app.route('/send-mail', methods=['POST'])
def post_mail_callback():
    """
    Summary: A callback for when POST is called on [host]:[port]/mailbox/send-mail

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the sender, subject and body parameters
    payload = request.get_json()
    in_temp = payload["temp"]
    print(in_temp)
    print(payload)

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

    app.run(debug=False, host='0.0.0.0', port=5056)







