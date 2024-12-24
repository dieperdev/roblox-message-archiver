import json

from sqlite3 import Cursor
from time_to_utc import convert_timestamp_to_utc

from requests import Session

def archive_archived(session: Session, archive_individual_messages: bool, cursor: Cursor) -> None:
    page_offset = 0

    messages = []
    messages_archived = 0

    while True:
        request = session.get(f'https://privatemessages.roblox.com/v1/messages?pageNumber={page_offset}&pageSize=20&messageTab=archive')
        response_json = json.loads(request.content)

        sent_messages = response_json['collection']
        current_page = response_json['pageNumber'] + 1 # ROBLOX uses zero-based indexing, smh
        total_messages = response_json['totalCollectionSize']
        total_pages = response_json['totalPages']

        if total_messages == 0:
            print('No messages were found in the ARCHIVE category.')

            break

        for message in sent_messages:
            message_id = message['id']

            message_data = {
                'id': message_id,
                'sender': {
                    'id': message['sender']['id'],
                    'verified': message['sender']['hasVerifiedBadge'],
                    'username': message['sender']['name'],
                    'display_name': message['sender']['displayName']
                },
                'recipient': {
                    'id': message['recipient']['id'],
                    'verified': message['recipient']['hasVerifiedBadge'],
                    'username': message['recipient']['name'],
                    'display_name': message['recipient']['displayName']
                },
                'read': message['isRead'],
                'system_message': message['isSystemMessage'],
                'isReportAbuseDisplayed': message['isReportAbuseDisplayed'],
                'created': convert_timestamp_to_utc(timestamp=message['created']),
                'updated': convert_timestamp_to_utc(timestamp=message['updated']),
                'subject': message['subject'],
                'body': message['body']
            }

            if archive_individual_messages:
                with open(f'archives/archive/{message_id}.json', 'w') as f:
                    f.write(json.dumps(message_data, indent=4))

            messages.append(message_data)
            cursor.execute('INSERT INTO archived (message_id, sender_id, sender_verified, sender_username, sender_display_name, recipient_id, recipient_verified, recipient_username, recipient_display_name, read, system_message, is_report_abuse_displayed, created, updated, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (message_id) DO NOTHING;', (message_id, message_data['sender']['id'], message_data['sender']['verified'], message_data['sender']['username'], message_data['sender']['display_name'], message_data['recipient']['id'], message_data['recipient']['verified'], message_data['recipient']['username'], message_data['recipient']['display_name'], message_data['read'], message_data['system_message'], message_data['isReportAbuseDisplayed'], message_data['created'], message_data['updated'], message_data['subject'], message_data['body']))

            messages_archived += 1

        print(f'Saved {messages_archived:,}/{total_messages:,} messages ({current_page} pages) from the ARCHIVE category so far. {(total_pages - current_page):,} pages ({(total_messages - messages_archived):,} messages) remain.')

        if current_page == total_pages:
            break

        page_offset += 1

    with open('archives/archive.json', 'w') as f:
        f.write(json.dumps(messages, indent=4))