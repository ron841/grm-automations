"""
google_drive_upload.py — Upload files to Google Drive (Get Rooted Media)
========================================================================
This script uploads a file to a shared Google Drive folder using a
Google Cloud Service Account. It's designed to be called from GitHub
Actions after other workflows generate output files.

NOT YET ACTIVE — This script is ready to deploy but requires Google
Cloud credentials to be set up first. See "Setup Instructions" below.

Usage:
    python scripts/google_drive_upload.py path/to/file.md

Requirements:
    pip install google-api-python-client google-auth

Setup Instructions (one-time, ~20-30 minutes):
    1. Go to console.cloud.google.com
    2. Create a project (or select an existing one)
    3. Enable the "Google Drive API":
       - Navigate to APIs & Services > Library
       - Search "Google Drive API" and click Enable
    4. Create a Service Account:
       - Go to APIs & Services > Credentials
       - Click "Create Credentials" > "Service Account"
       - Name it something like "grm-github-actions"
       - Skip the optional permissions steps, click Done
    5. Generate a JSON key:
       - Click on the new service account
       - Go to the "Keys" tab
       - Click "Add Key" > "Create new key" > JSON
       - Download the file (keep it safe — it's like a password)
    6. Share a Google Drive folder with the service account:
       - Create a folder in Google Drive (e.g., "GRM Automations Output")
       - Right-click > Share
       - Paste the service account email (looks like grm-bot@project.iam.gserviceaccount.com)
       - Give it "Editor" access
       - Copy the folder ID from the URL: drive.google.com/drive/folders/THIS_PART_IS_THE_ID
    7. Add secrets to GitHub:
       - Go to your repo > Settings > Secrets and variables > Actions
       - New secret: GOOGLE_SERVICE_ACCOUNT_KEY = entire contents of the JSON key file
       - New secret: GOOGLE_DRIVE_FOLDER_ID = the folder ID from step 6

Environment Variables (set in GitHub Actions workflow):
    GOOGLE_SERVICE_ACCOUNT_KEY  — The full JSON key file contents (from GitHub Secrets)
    GOOGLE_DRIVE_FOLDER_ID      — The ID of the shared Drive folder (from GitHub Secrets)
"""

# ── Imports ──────────────────────────────────────────────────────────────
import os       # For reading environment variables
import sys      # For command-line arguments and exit codes
import json     # For parsing the service account JSON key

# google-auth: Handles authentication with Google's APIs using the service account.
from google.oauth2 import service_account

# googleapiclient: The official Google API client library.
# "build" creates a connection to a specific Google API (in our case, Drive).
# MediaFileUpload handles streaming the file data to Google.
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# ── Configuration ────────────────────────────────────────────────────────

# The scope tells Google what permissions we need.
# This scope allows uploading and managing files in Drive.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


# ── Function: authenticate with Google ───────────────────────────────────
def get_drive_service():
    """
    Creates an authenticated Google Drive API client using a service account.

    The service account JSON key is read from the GOOGLE_SERVICE_ACCOUNT_KEY
    environment variable. We write it to a temporary file because the Google
    auth library expects a file path, not a raw string.

    Returns:
        A Google Drive API service object we can use to upload files.
    """
    # Read the JSON key from the environment variable.
    key_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    if not key_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_KEY environment variable is not set.")
        print("See the setup instructions at the top of this file.")
        sys.exit(1)

    # Parse the JSON string into a Python dictionary.
    # json.loads() turns a JSON string into a dict — the Google auth library
    # can accept this directly via from_service_account_info().
    key_data = json.loads(key_json)

    # Create credentials from the service account key.
    # "credentials" is like a login session — it proves we're authorized.
    credentials = service_account.Credentials.from_service_account_info(
        key_data,
        scopes=SCOPES
    )

    # Build the Drive API client.
    # "v3" is the current version of the Google Drive API.
    # cache_discovery=False avoids a warning about file caching.
    service = build("drive", "v3", credentials=credentials, cache_discovery=False)

    return service


# ── Function: upload a file to Google Drive ──────────────────────────────
def upload_file(file_path: str) -> str:
    """
    Uploads a single file to the shared Google Drive folder.

    Parameters:
        file_path (str): Path to the local file to upload.

    Returns:
        str: The Google Drive file ID of the uploaded file.
    """
    # Read the target folder ID from the environment.
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        print("ERROR: GOOGLE_DRIVE_FOLDER_ID environment variable is not set.")
        print("See the setup instructions at the top of this file.")
        sys.exit(1)

    # Make sure the file actually exists before trying to upload it.
    if not os.path.isfile(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    # Authenticate and get the Drive API client.
    service = get_drive_service()

    # Extract just the filename from the full path.
    # e.g., "output/edited_content_2026-03-21.md" → "edited_content_2026-03-21.md"
    file_name = os.path.basename(file_path)

    # "file_metadata" tells Google Drive what to name the file and which
    # folder to put it in. "parents" is a list of folder IDs — we use
    # just one (our shared GRM output folder).
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }

    # MediaFileUpload handles reading the file and streaming it to Google.
    # mimetype "text/markdown" tells Drive it's a markdown file.
    # resumable=True means if the upload is interrupted, it can resume
    # instead of starting over (useful for larger files).
    media = MediaFileUpload(
        file_path,
        mimetype="text/markdown",
        resumable=True
    )

    # Execute the upload.
    # service.files().create() is the Google Drive API call for uploading.
    # fields="id, name, webViewLink" tells the API what info to return.
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, webViewLink"
    ).execute()

    # Print confirmation with a direct link to the file in Drive.
    print(f"Uploaded: {uploaded_file['name']}")
    print(f"Drive ID: {uploaded_file['id']}")
    print(f"View at:  {uploaded_file['webViewLink']}")

    return uploaded_file["id"]


# ── Main ─────────────────────────────────────────────────────────────────
def main():
    """
    Main entry point. Reads a file path from the command line and uploads it.
    """
    # Check that the user provided a file path as an argument.
    if len(sys.argv) < 2:
        print("Usage: python scripts/google_drive_upload.py <file_path>")
        print()
        print("Example:")
        print("  python scripts/google_drive_upload.py output/edited_content_2026-03-21.md")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Uploading {file_path} to Google Drive...")
    upload_file(file_path)
    print("Done.")


# This runs only when you execute the script directly.
if __name__ == "__main__":
    main()
