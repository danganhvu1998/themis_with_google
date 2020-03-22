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
    valueInputOption="RAW", 
    body=body
  ).execute()
  print('{0} cells updated.'.format(result.get('updatedCells')))

def updateScore(sheet, student, problem, score):
  SHEET_OUTPUT_ID = Config.infomationTaker("SHEET_OUTPUT_ID")
  SHEET_OUTPUT_NAME = Config.infomationTaker("SHEET_OUTPUT_NAME")

  # GET ROW
  FIRST_COL_RANGE_NAME = SHEET_OUTPUT_NAME+"!A:A"
  result = sheet.values().get(spreadsheetId=SHEET_OUTPUT_ID, range=FIRST_COL_RANGE_NAME).execute()
  values = result.get('values', [])
  found = 0
  if len(values)==0:
    writeRow = 2
  else:
    writeRow = 2
    for value in values:
      if len(value)==0: continue
      if(value[0].strip().upper() == student): 
        found = 1
        break
      writeRow+=1
  # REWRITE
  body = {
    'values': [[student]]
  }
  if found == 0:
    RANGE_NAME = "{}!A{}:A{}".format(SHEET_OUTPUT_NAME, writeRow, writeRow)
    result = sheet.values().update(
      spreadsheetId=SHEET_OUTPUT_ID,
      range=RANGE_NAME,
      valueInputOption="RAW", 
      body=body
    ).execute()

  # GET COL
  FIRST_ROW_RANGE_NAME = SHEET_OUTPUT_NAME+"!1:1"
  result = sheet.values().get(spreadsheetId=SHEET_OUTPUT_ID, range=FIRST_ROW_RANGE_NAME).execute()
  values = result.get('values', [])
  found = 0
  if len(values)==0:
    writeCol = 2
  else:
    writeCol = 2
    for value in values[0]:
      if len(value)==0: continue
      if(value.strip().upper() == problem): 
        found = 1
        break
      writeCol+=1
  writeCol = chr(writeCol-1+ord('A'))
  # REWRITE
  body = {
    'values': [[problem]]
  }
  if found == 0:
    RANGE_NAME = "{}!{}1:{}1".format(SHEET_OUTPUT_NAME, writeCol, writeCol)
    result = sheet.values().update(
      spreadsheetId=SHEET_OUTPUT_ID,
      range=RANGE_NAME,
      valueInputOption="RAW", 
      body=body
    ).execute()
  
  # WRITE SCORE
  body = {
    'values': [[score]]
  }
  RANGE_NAME = "{}!{}{}:{}{}".format(SHEET_OUTPUT_NAME, writeCol, writeRow, writeCol, writeRow)
  result = sheet.values().update(
    spreadsheetId=SHEET_OUTPUT_ID,
    range=RANGE_NAME,
    valueInputOption="RAW", 
    body=body
  ).execute()
  print("{} - {} - {}{}, score is {}".format(student, problem, writeCol, writeRow, score))
