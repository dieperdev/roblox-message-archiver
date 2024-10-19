import os
import requests

from inbox_archiver import archive_inbox
from verify_roblosecurity import verify_cookie

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

roblosecurity = os.environ.get('ROBLOSECURITY')
archive_individual_messages = os.environ.get('ARCHIVE_INDIVIDUAL')

def main():
    Path('archives').mkdir(exist_ok=True)
    Path('archives/inbox').mkdir(exist_ok=True)

    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = roblosecurity

    archive_inbox(session=session, archive_individual_messages=archive_individual_messages)

if __name__ == '__main__':
    if not roblosecurity:
        print('A ROBLOSECURITY cookie is required to continue.')

        exit(1)

    cookie_verified = verify_cookie(roblosecurity)

    if not cookie_verified:
        print('You need a valid ROBLOSECURITY cookie to continue.')

        exit(1)

    if not archive_individual_messages or archive_individual_messages not in ['0', '1']:
        print('You need to specify whether individual messages should be archived in their own files.')

        exit(1)

    archive_individual_messages = False if archive_individual_messages == '0' else True

    main()