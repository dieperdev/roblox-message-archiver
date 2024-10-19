import json

from time_to_utc import convert_timestamp_to_utc

from requests import Session

def archive_sent(session: Session, archive_individual_messages: bool) -> None:
    page_offset = 0

    messages = []
    messages_archived = 0

    while True:
        request = session.get(f'https://privatemessages.roblox.com/v1/messages?pageNumber={page_offset}&pageSize=20&messageTab=sent')
        response_json = json.loads(request.content)

        sent_messages = response_json['collection']
        current_page = response_json['pageNumber'] + 1 # ROBLOX uses zero-based indexing, smh
        total_messages = response_json['totalCollectionSize']
        total_pages = response_json['totalPages']

        if total_messages == 0:
            print('No messages were found in the SENT category.')

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
                with open(f'archives/sent/{message_id}.json', 'w') as f:
                    f.write(json.dumps(message_data))

            messages.append(message_data)

            messages_archived += 1

        print(f'Archived {messages_archived:,}/{total_messages:,} messages from SENT ({current_page} pages) so far. {(total_pages - current_page):,} pages ({(total_messages - messages_archived):,} messages) remain.')

        if current_page == total_pages:
            break

        page_offset += 1

    with open('archives/sent.json', 'w') as f:
        f.write(json.dumps(messages))