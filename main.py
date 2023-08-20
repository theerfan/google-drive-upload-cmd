import sys
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def upload_to_drive(filename, folder_id=None):
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    # Call the Drive API
    service = build("drive", "v3", credentials=creds)

    # File metadata
    file_metadata = {"name": filename.split("/")[-1]}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    # Upload the file
    media = MediaFileUpload(filename, resumable=True)
    try:
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f"Uploaded {filename} to Google Drive with File ID: {file['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <filename> [<folder_id>]")
    else:
        filename = sys.argv[1]
        # folder_id = sys.argv[2] if len(sys.argv) > 2 else None
        folder_id = "17ImD62Tzpm1FWeASOeBelF5ApuMHxCW7"
        upload_to_drive(filename, folder_id)
