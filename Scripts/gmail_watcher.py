from pathlib import Path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
INBOX = Path("../Inbox")
INBOX.mkdir(exist_ok=True)

def gmail_service():
    creds = None
    if Path("token.pickle").exists():
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as f:
            pickle.dump(creds, f)

    return build('gmail', 'v1', credentials=creds)

service = gmail_service()

results = service.users().messages().list(
    userId='me',
    maxResults=5
).execute()

messages = results.get('messages', [])

for msg in messages:
    msg_data = service.users().messages().get(
        userId='me',
        id=msg['id']
    ).execute()

    headers = msg_data['payload']['headers']
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')

    file = INBOX / f"{subject.replace(' ', '_')}.md"
    if not file.exists():
        file.write_text(
            f"# Gmail Task\nSubject: {subject}\n\n- Review email\n- Decide next action"
        )
        print("📧 Gmail task created:", file.name)
