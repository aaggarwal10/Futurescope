import imaplib
import email
from email.header import decode_header
import re
import os

# Login to your email account
def login(email_address, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    return mail

# Check for new messages and trigger an action
def check_inbox(mail):
    mail.select('inbox')
    result, data = mail.search(None, 'ALL from dan@tldrnewsletter.com')  # Search for unread messages
    if result == 'OK':
        count = 0
        for num in reversed(data[0].split()):
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                msg = email.message_from_bytes(data[0][1])
                subject = decode_header(msg['subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_address = msg['from']
                print(f'New message from {from_address} with subject "{subject}"')

                # Get the message body
                if msg.is_multipart():
                    count -=1 
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            # Extract reference numbers and URLs
                            refs, urls = extract_refs_and_urls(body)
                            print("URLs in Research & Innovation:", urls)
                else:
                    count += 1
                    body = msg.get_payload(decode=True).decode()
                    # Extract reference numbers and URLs
                    refs, urls = extract_refs_and_urls(body)
                    print("URLs in Research & Innovation:", urls)

                # Trigger your action here
                print(count)

def extract_refs_and_urls(body):
    # Extract reference numbers from the "Research & Innovation" section
    start = body.find("RESEARCH & INNOVATION")
    end = body.find("ENGINEERING & RESOURCES", start)
    section = body[start:end]
    refs = re.findall(r'\[(\d+)\]', section)
    # Extract URLs from the "Quick Links" section using the reference numbers
    urls = []
    for ref in refs:
        pattern = rf'\[{ref}\] (https?://[^\s]+)'
        match = re.search(pattern, body)
        if match:
            urls.append(match.group(1))
    return refs, urls



if __name__ == "__main__":
    email_address = os.environ['USER']
    password = os.environ['PASS']
    mail = login(email_address, password)
    check_inbox(mail)
    mail.logout()