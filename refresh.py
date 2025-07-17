import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = 'C:/contoh/refresh.py'

def refresh_token():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes=['https://www.googleapis.com/auth/youtube.upload'])

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        print("Token refreshed.")
    else:
        print("Token is still valid.")

if __name__ == "__main__":
    refresh_token()
