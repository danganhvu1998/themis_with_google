from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configReader as Config
import os

def getRow(sheet, row):
  SHEET_INPUT_ID = Config.infomationTaker("SHEET_INPUT_ID")
  SHEET_INPUT_NAME = Config.infomationTaker("SHEET_INPUT_NAME")
  RANGE_NAME = SHEET_INPUT_NAME+"!"+str(row)+":"+str(row)
  result = sheet.values().get(spreadsheetId=SHEET_INPUT_ID, range=RANGE_NAME).execute()
  values = result.get('values', [])
  return values

def writeToFile(rowValue, id):
  # DATA
  DATA = Config.configReader()
  STUDENTS = DATA[ "students" ]
  CONFIG = DATA[ "config" ]

  # UPDATE SUBMISSION
  SECRET_CODE_COL = CONFIG[ "SECRET_CODE_COL" ]
  PROBLEM_CODE_COL = CONFIG[ "PROBLEM_CODE_COL" ]
  CODE_COL = CONFIG[ "CODE_COL" ]
  FILE_TYPE = CONFIG[ "FILE_TYPE" ]

  # FOLDER URL
  FILE_OUT_AT = CONFIG[ "FILE_OUT_AT" ]
  if not os.path.exists(FILE_OUT_AT): os.makedirs(FILE_OUT_AT)

  # PRINT
  studentName = STUDENTS.get(rowValue[SECRET_CODE_COL], "__"+rowValue[SECRET_CODE_COL]+"__")
  problemName = rowValue[PROBLEM_CODE_COL]
  fileName = "{}{}[{}][{}].{}".format(FILE_OUT_AT, id, studentName, problemName, FILE_TYPE)
  code = rowValue[ CODE_COL ]
  fp = open(fileName, "w")
  fp.write( code )
  fp.close()
  print("Write file id:", id)
  return 1

def markDone(sheet, row):
  SHEET_INPUT_ID = Config.infomationTaker("SHEET_INPUT_ID")
  SHEET_INPUT_NAME = Config.infomationTaker("SHEET_INPUT_NAME")
  RANGE_NAME = SHEET_INPUT_NAME+"!A"+str(row)+":A"+str(row)
  print(RANGE_NAME)
  body = {
    'values': [["X"]]
  }
  result = sheet.values().update(
    spreadsheetId=SHEET_INPUT_ID,
    range=RANGE_NAME,
    valueInputOption="USER_ENTERED", 
    body=body
  ).execute()
  print('{0} cells updated.'.format(result.get('updatedCells')))