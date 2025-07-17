# YouTube Video Uploader GUI

A user-friendly GUI application for uploading videos to YouTube using the YouTube Data API v3.

## Features

- **Token Management**: Generate new OAuth tokens or refresh existing ones
- **File Browser Integration**: Easy file selection for videos, tokens, and client secrets
- **Custom Metadata**: Optional custom titles and tags for videos
- **Category Selection**: Choose from all YouTube video categories
- **Progress Tracking**: Real-time upload progress with clickable video URLs
- **Clean UI**: Modern, white-themed interface with organized sections

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```
Or Simply download [Youtube Uploader](https://github.com/zPabsy/YoutubeUploadAPI/releases/download/youtube/YouTube_Uploader.exe) executables on release.

## Setup

1. **Get Google API Credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials (Desktop Application)
   - Download the `client_secret.json` file

2. **Run the Application**:
   ```bash
   python youtube_uploader_gui.py
   ```

## Usage

### Authentication
1. **Client Secret**: Browse and select your `client_secret.json` file
2. **Save Token to**: Choose where to save the generated token file
3. **Token file**: Browse and select an existing token file (if you have one)
4. **Generate Token**: Click to start OAuth flow and generate new token
5. **Refresh Token**: Click to refresh an existing token

### Video Upload
1. **Video file**: Browse and select your video file (.mp4, .mov, .mkv, .webm, .avi)
2. **Category**: Select appropriate YouTube category from dropdown
3. **Enable custom title and tags**: Toggle to enable custom metadata
   - **Title**: Enter custom video title (optional)
   - **Tags**: Enter comma-separated tags (optional)
4. **Description**: Enter video description
5. **Generate Metadata**: Create metadata.json file with your settings
6. **Upload Video**: Start the upload process

### Features

- **Automatic Token Loading**: Generated tokens are automatically loaded for use
- **Clickable URLs**: Click on video URLs in the status log to open in browser
- **Progress Tracking**: Real-time upload progress percentage
- **Error Handling**: Clear error messages and status updates
- **File Auto-detection**: Automatically loads existing token.json and client_secret.json files

## File Structure

```
YTUpload/
├── youtube_uploader_gui.py    # Main GUI application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── client_secret.json        # Your Google API credentials (you provide)
├── token.json               # Generated OAuth token (auto-generated)
├── metadata.json            # Video metadata (auto-generated)
├── upload.py                # Original upload script (reference)
└── refresh.py               # Original refresh script (reference)
```

## Notes

- Videos are uploaded as **private** by default
- The application uses all YouTube API scopes for full functionality
- Token files are automatically refreshed when expired
- Generated metadata.json follows YouTube API format
- Status log shows clickable URLs for uploaded videos

## Troubleshooting

1. **"Client secret file not found"**: Make sure you've selected a valid client_secret.json file
2. **"Token file not found"**: Generate a new token or select an existing valid token file
3. **OAuth errors**: Try generating a new token if refresh fails
4. **Upload errors**: Check your internet connection and file format compatibility

## Original Scripts

The GUI integrates functionality from:
- `upload.py`: Original manual upload script
- `refresh.py`: Original token refresh script

These are kept for reference but the GUI provides all their functionality in a user-friendly interface.
