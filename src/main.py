import os
import sqlite3
import requests

from inbox_archiver import archive_inbox
from sent_archiver import archive_sent
from news_archiver import archive_news
from archived_archiver import archive_archived
from verify_roblosecurity import verify_cookie

from pathlib import Path
from sqlite3 import Cursor
from dotenv import load_dotenv

load_dotenv()

roblosecurity = os.environ.get('ROBLOSECURITY')
archive_individual_messages = os.environ.get('ARCHIVE_INDIVIDUAL')

def get_sqlite_cursor() -> Cursor:
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()

    return cursor

def main():
    Path('archives').mkdir(exist_ok=True)

    if archive_individual_messages:
        Path('archives/inbox').mkdir(exist_ok=True)
        Path('archives/sent').mkdir(exist_ok=True)
        Path('archives/news').mkdir(exist_ok=True)
        Path('archives/archive').mkdir(exist_ok=True)

    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = roblosecurity

    sqlite_cursor = get_sqlite_cursor()

    archive_inbox(session=session, archive_individual_messages=archive_individual_messages)
    archive_sent(session=session, archive_individual_messages=archive_individual_messages)
    archive_news(session=session, archive_individual_messages=archive_individual_messages)
    archive_archived(session=session, archive_individual_messages=archive_individual_messages)

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