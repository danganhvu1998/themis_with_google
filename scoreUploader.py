from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configReader as Config
import supportFunction as SFunc
import time
import os
from pathlib import Path
import re

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# READ FROM FILE
DATA = Config.configReader()
CONFIG = DATA[ "config" ]

# WAITING TIME
RELOAD_AFTER_SEC = CONFIG[ "RELOAD_AFTER_SEC" ]

# The ID and range of a sample spreadsheet.
SHEET_OUTPUT_ID = CONFIG[ 'SHEET_OUTPUT_ID' ]

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    while(1):
        paths = sorted(Path("Logs").iterdir(), key=os.path.getmtime)
        for path in paths:
            fp = open(path, "r");
            firstLine = fp.readline().strip()
            fp.close()
            info = re.findall("[.a-zA-Z0-9]+", firstLine)
            studentName = info[0].strip().upper()
            problemCode = info[1].strip().upper()
            try:
                score = float(info[2])
            except:
                score = 0
            SFunc.updateScore(sheet, studentName, problemCode, score)
            time.sleep(3)
            os.remove(path)

if __name__ == '__main__':
    main()