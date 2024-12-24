import os
import sqlite3
import requests

from inbox_archiver import archive_inbox
from sent_archiver import archive_sent
from news_archiver import archive_news
from archived_archiver import archive_archived
from verify_roblosecurity import verify_cookie

from pathlib import Path
from sqlite3 import Connection, Cursor
from dotenv import load_dotenv

load_dotenv()

roblosecurity = os.environ.get('ROBLOSECURITY')
archive_individual_messages = os.environ.get('ARCHIVE_INDIVIDUAL')

def get_sqlite_connection() -> tuple[Connection, Cursor]:
    conn = sqlite3.connect('archive.db')
    cursor = conn.cursor()

    return (conn, cursor)

def create_sqlite_tables(cursor: Cursor):
    # Table for inbox messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id LONG INTEGER UNIQUE NOT NULL,
            sender_id INTEGER NOT NULL,
            sender_verified BOOLEAN NOT NULL,
            sender_username VARCHAR(64) NOT NULL,
            sender_display_name VARCHAR(64) NOT NULL,
            recipient_id INTEGER NOT NULL,
            recipient_verified BOOLEAN NOT NULL,
            recipient_username VARCHAR(64) NOT NULL,
            recipient_display_name VARCHAR(64) NOT NULL,
            read BOOLEAN NOT NULL,
            system_message BOOLEAN NOT NULL,
            is_report_abuse_displayed BOOLEAN NOT NULL,
            created REAL NOT NULL,
            updated REAL NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        );
    ''')

    # Table for sent messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id LONG INTEGER UNIQUE NOT NULL,
            sender_id INTEGER NOT NULL,
            sender_verified BOOLEAN NOT NULL,
            sender_username VARCHAR(64) NOT NULL,
            sender_display_name VARCHAR(64) NOT NULL,
            recipient_id INTEGER NOT NULL,
            recipient_verified BOOLEAN NOT NULL,
            recipient_username VARCHAR(64) NOT NULL,
            recipient_display_name VARCHAR(64) NOT NULL,
            read BOOLEAN NOT NULL,
            system_message BOOLEAN NOT NULL,
            is_report_abuse_displayed BOOLEAN NOT NULL,
            created REAL NOT NULL,
            updated REAL NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        );
    ''')

    # Table for news messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id LONG INTEGER UNIQUE NOT NULL,
            sender_id INTEGER NOT NULL,
            sender_verified BOOLEAN NOT NULL,
            sender_username VARCHAR(64) NOT NULL,
            sender_display_name VARCHAR(64) NOT NULL,
            created REAL NOT NULL,
            updated REAL NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        );
    ''')

    # Table for archived messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archived (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id LONG INTEGER UNIQUE NOT NULL,
            sender_id INTEGER NOT NULL,
            sender_verified BOOLEAN NOT NULL,
            sender_username VARCHAR(64) NOT NULL,
            sender_display_name VARCHAR(64) NOT NULL,
            recipient_id INTEGER NOT NULL,
            recipient_verified BOOLEAN NOT NULL,
            recipient_username VARCHAR(64) NOT NULL,
            recipient_display_name VARCHAR(64) NOT NULL,
            read BOOLEAN NOT NULL,
            system_message BOOLEAN NOT NULL,
            is_report_abuse_displayed BOOLEAN NOT NULL,
            created REAL NOT NULL,
            updated REAL NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        );
    ''')

def main():
    Path('archives').mkdir(exist_ok=True)

    if archive_individual_messages:
        Path('archives/inbox').mkdir(exist_ok=True)
        Path('archives/sent').mkdir(exist_ok=True)
        Path('archives/news').mkdir(exist_ok=True)
        Path('archives/archive').mkdir(exist_ok=True)

    session = requests.Session()
    session.cookies['.ROBLOSECURITY'] = roblosecurity

    sqlite_conn, sqlite_cursor = get_sqlite_connection()

    create_sqlite_tables(sqlite_cursor)

    archive_inbox(session=session, archive_individual_messages=archive_individual_messages, cursor=sqlite_cursor)
    archive_sent(session=session, archive_individual_messages=archive_individual_messages, cursor=sqlite_cursor)
    archive_news(session=session, archive_individual_messages=archive_individual_messages, cursor=sqlite_cursor)
    archive_archived(session=session, archive_individual_messages=archive_individual_messages, cursor=sqlite_cursor)

    sqlite_conn.commit()

    sqlite_cursor.close()
    sqlite_conn.close()

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