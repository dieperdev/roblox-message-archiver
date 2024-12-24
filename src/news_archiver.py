import json

from sqlite3 import Cursor
from time_to_utc import convert_timestamp_to_utc

from requests import Session

def archive_news(session: Session, archive_individual_messages: bool, cursor: Cursor) -> None:
    messages = []
    messages_archived = 0

    request = session.get(f'https://privatemessages.roblox.com/v1/announcements')
    response_json = json.loads(request.content)

    news_messages = response_json['collection']
    total_messages = response_json['totalCollectionSize']

    if total_messages == 0:
        print('No messages were found in the NEWS category.')

    for message in news_messages:
        message_id = message['id']

        message_data = {
            'id': message_id,
            'sender': {
                'id': message['sender']['id'],
                'verified': message['sender']['hasVerifiedBadge'],
                'username': message['sender']['name'],
                'display_name': message['sender']['displayName']
            },
            'created': convert_timestamp_to_utc(timestamp=message['created']),
            'updated': convert_timestamp_to_utc(timestamp=message['updated']),
            'subject': message['subject'],
            'body': message['body']
        }

        if archive_individual_messages:
            with open(f'archives/news/{message_id}.json', 'w') as f:
                f.write(json.dumps(message_data, indent=4))

        messages.append(message_data)
        cursor.execute('INSERT INTO news (message_id, sender_id, sender_verified, sender_username, sender_display_name, created, updated, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (message_id) DO NOTHING;', (message_id, message_data['sender']['id'], message_data['sender']['verified'], message_data['sender']['username'], message_data['sender']['display_name'], message_data['created'], message_data['updated'], message_data['subject'], message_data['body']))

        messages_archived += 1

    print(f'Saved {messages_archived} messages from the NEWS category.')

    with open('archives/news.json', 'w') as f:
        f.write(json.dumps(messages, indent=4))