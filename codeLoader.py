from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configReader as Config
import supportFunction as SFunc
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# READ FROM FILE
DATA = Config.configReader()
STUDENTS = DATA[ "students" ]
CONFIG = DATA[ "config" ]

# UPDATE SUBMISSION
start_row = CONFIG[ "SRAT_READING_ROW" ]
SECRET_CODE_COL = CONFIG[ "SECRET_CODE_COL" ]
PROBLEM_CODE_COL = CONFIG[ "PROBLEM_CODE_COL" ]
CODE_COL = CONFIG[ "CODE_COL" ]

# WAITING TIME
RELOAD_AFTER_SEC = CONFIG[ "RELOAD_AFTER_SEC" ]

# The ID and range of a sample spreadsheet.
SHEET_INPUT_ID = CONFIG[ 'SHEET_INPUT_ID' ]
SHEET_OUTPUT_ID = CONFIG[ 'SHEET_OUTPUT_ID' ]

def main(credentialsFile, tokenFile):
    global start_row
    print("Using", credentialsFile)
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenFile):
        with open(tokenFile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsFile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenFile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    

    currRow = start_row
    for i in range(10):
        print("     Cheking Row:", currRow)
        try:
            rowValues = SFunc.getRow(sheet, currRow)[0]
        except:
            print("     Found Nothing. Waiting for {} seconds".format(RELOAD_AFTER_SEC))
            time.sleep(RELOAD_AFTER_SEC)
            print("     Back to Updating ...")
            continue
        if not rowValues[0].isdigit():
            timestamp = SFunc.writeToFile(rowValues, rowValues[0])
            if timestamp: # Write Successful 
                print("         -> Writed to file", timestamp)
                SFunc.markDone(sheet, timestamp, currRow)
            else:
                print("         -> Not a valid contestants", timestamp)
        else:
            print("         -> Updated")
        currRow+=1
        start_row = currRow

if __name__ == '__main__':
    while(1):
        try: main('credentials2.json', "token2.pickle")
        except: time.sleep(5)
        try: main('credentials1.json', "token1.pickle")
        except: time.sleep(5)
        try: main('credentials.json', "token.pickle")
        except: time.sleep(5)
