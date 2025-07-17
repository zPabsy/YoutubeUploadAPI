# -*- coding: utf-8 -*-

import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


MAX_UPLOADS = 10
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def load_metadata():
    with open("video_metadata.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def load_metadata():
    with open("video_metadata.json", "r", encoding="utf-8") as f:
        return json.load(f)

def upload_thumbnail(youtube, video_id, thumbnail_path):
    if not os.path.exists(thumbnail_path):
        print(f"⚠️ Thumbnail not found: {thumbnail_path}")
        return

    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    )
    response = request.execute()
    print(f"🖼️ Uploaded thumbnail: {os.path.basename(thumbnail_path)}")


def upload_video(youtube, video_path):
    file_name = os.path.basename(video_path)
    title = os.path.splitext(file_name)[0]
    metadata = load_metadata()

    request_body = {
        "snippet": {
            "title": title,
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": metadata["categoryId"],
            "defaultLanguage": metadata["defaultLanguage"],
            "defaultAudioLanguage": metadata["defaultAudioLanguage"]
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "embeddable": False
        }
    }


    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {file_name}... {int(status.progress() * 100)}%")

    print(f"? Upload complete: {file_name} (Video ID: {response['id']})")

    thumbnail_path = os.path.join(os.path.dirname(video_path), f"{title}.jpg")
    upload_thumbnail(youtube, response['id'], thumbnail_path)

    try:
        os.remove(video_path)
        print(f"🧹 Deleted local file: {file_name}\n")
    except Exception as e:
        print(f"⚠️ Failed to delete {file_name}: {e}")

def main():
    youtube = get_authenticated_service()
    video_folder = "video"
    uploaded_count = 0

    for file in os.listdir(video_folder):
        if file.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
            video_path = os.path.join(video_folder, file)
            try:
                upload_video(youtube, video_path)
                uploaded_count += 1
                if uploaded_count >= MAX_UPLOADS:
                    print("?? Reached max upload limit (4). Done.")
                    break
            except HttpError as e:
                print(f"? Failed to upload {file}: {e}")

if __name__ == "__main__":
    main()
