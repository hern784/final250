import argparse

import mailboxTools


valid_commands = ['quit', 'q', 'send_temp']

def command_is_valid(command):
    if command in valid_commands:
        return True

    else:
        print('Valid commands are {}'.format(valid_commands))
        return False

def main():
    mailbox_client = mailboxTools.mailboxClient(args.u, args.a, args.p)

    usr_input = ''
    command = ''

    while command != 'quit' and command != 'q':
        while not command_is_valid(usr_input):
            usr_input = input('Command: ')
            command = usr_input
        # if command is send temp and the address and temp are valid send request
        if command == 'send_temp':
            address = input('Destination address: ')
            address = address if address != '' else None

            temp = input('Desired Temp: ')

            if temp == '' or temp.isdigit() != True or int(temp)>100 or int(temp)<60:
                print("\nNot Valid!\n")
                continue
               
            print("Temp to be sent = " + str(temp))
            temp = int(temp) * int(temp)
            print("Encrypted temp to be sent = " + str(temp))
            try:
                mailbox_client.send_mail(address, temp)
            except Exception as e:
                print(e)

        print('')
        usr_input = ''

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mailClient',
            description='Script to send and read emails')

    parser.add_argument('-a', metavar='ip_addr:port_num', required=True,
            help="Address of the server in the format ip_addr:port_num")

    parser.add_argument('-p', metavar='password', required=True,
            help="Password to access server")

    parser.add_argument('-u', metavar='username', required=True,
            help="Username to go by when sending emails")

    args = parser.parse_args()

    main()


