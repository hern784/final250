from datetime import datetime
from threading import Lock

import pickle

MAIL_REQ_FIELDS = ['subject', 'body', 'sender']
MAIL_DB_FILE = 'mail.pickle'

class mailboxManager(object):
    def __init__(self):

        print('starting mailbox manager')

        self.mailbox = []   # list for in-memory mail storage

        try:
            with open(MAIL_DB_FILE, 'rb') as f:
                print('Loading {}'.format(MAIL_DB_FILE))
                # TODO: load the pickle data into self.mailbox
                while 1:
                    self.mailbox = pickle.load(f)
                    #f.close()
        except EOFError:
            pass

        except FileNotFoundError:
            with open(MAIL_DB_FILE, "wb+") as f:
                f.close()

    def _mail_format_valid(self, mail_entry):

        if isinstance(mail_entry, dict):
            mail_fields = mail_entry.keys()
            if len(mail_fields) == len(MAIL_REQ_FIELDS):
                for field in MAIL_REQ_FIELDS:
                    if not field in mail_fields or mail_entry[field] == '':
                        return False

                return True

            else:
                return False

        else:
            return False

    def _update_DB(self):

        with open(MAIL_DB_FILE, 'wb') as f:
            print('updating database')
            # TODO: save the mailbox data as a pickle file
            pickle.dump(self.mailbox, f)
            f.close()

    def add_mail(self, mail_entry):

        print('adding mail')
        if self._mail_format_valid(mail_entry):
    
            if len(self.mailbox) == 0:
                proposed_id = 0

            else:
                proposed_id = self.mailbox[-1]['id'] + 1

            # Assign an ID to the mail and give it a timestamp
            mail_entry['id'] = proposed_id
            mail_entry['time'] = str(datetime.now())
            self.mailbox.append(mail_entry)
            self._update_DB()

        else:
            print('mail entry {} not in valid format'.format(mail_entry))


