from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configReader as Config
import os
import time

def getRow(sheet, row):
  SHEET_INPUT_ID = Config.infomationTaker("SHEET_INPUT_ID")
  SHEET_INPUT_NAME = Config.infomationTaker("SHEET_INPUT_NAME")
  RANGE_NAME = SHEET_INPUT_NAME+"!"+str(row)+":"+str(row)
  result = sheet.values().get(spreadsheetId=SHEET_INPUT_ID, range=RANGE_NAME).execute()
  values = result.get('values', [])
  return values

def writeToFile(rowValue, dateAndTime):
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
  timestamp = time.mktime(time.strptime(dateAndTime, '%m/%d/%Y %H:%M:%S'))
  timestamp = int(timestamp)
  studentName = STUDENTS.get(rowValue[SECRET_CODE_COL], "__"+rowValue[SECRET_CODE_COL]+"__")
  problemName = rowValue[PROBLEM_CODE_COL]
  fileName = "{}{}[{}][{}].{}".format(FILE_OUT_AT, timestamp, studentName, problemName, FILE_TYPE)
  code = rowValue[ CODE_COL ]
  fp = open(fileName, "w")
  fp.write( code )
  fp.close()
  print("Write file id:", id)
  return timestamp

def markDone(sheet, dateAndTime, row):
  SHEET_INPUT_ID = Config.infomationTaker("SHEET_INPUT_ID")
  SHEET_INPUT_NAME = Config.infomationTaker("SHEET_INPUT_NAME")
  RANGE_NAME = SHEET_INPUT_NAME+"!A"+str(row)+":A"+str(row)
  print(RANGE_NAME)
  body = {
    'values': [[dateAndTime]]
  }
  result = sheet.values().update(
    spreadsheetId=SHEET_INPUT_ID,
    range=RANGE_NAME,
    valueInputOption="RAW", 
    body=body
  ).execute()
  print('{0} cells updated.'.format(result.get('updatedCells')))

def getRangeName(sheet, student, problem):
  SHEET_OUTPUT_ID = Config.infomationTaker("SHEET_OUTPUT_ID")
  SHEET_OUTPUT_NAME = Config.infomationTaker("SHEET_OUTPUT_NAME")

  # GET ROW
  FIRST_COL_RANGE_NAME = SHEET_OUTPUT_NAME+"!A:A"
  result = sheet.values().get(spreadsheetId=SHEET_OUTPUT_ID, range=FIRST_COL_RANGE_NAME).execute()
  values = result.get('values', [])
  found = 0
  writeRow = 1
  for value in values:
    if(value[0].strip().upper() == student): 
      found = 1
      break
    writeRow+=1
  if found == 0:
    writeRow = len(values) + 1
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
  writeCol = 1
  for value in values[0]:
    if(value.strip().upper() == problem): 
      found = 1
      break
    writeCol+=1
  if found==0:
    writeCol = len( values[0] ) + 1
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
  
  # Get RANGE_NAME
  RANGE_NAME = "{}!{}{}:{}{}".format(SHEET_OUTPUT_NAME, writeCol, writeRow, writeCol, writeRow)
  return RANGE_NAME

def updatePenalty(sheet, RANGE_NAME, score, submitTime):
  SHEET_OUTPUT_ID = Config.infomationTaker("SHEET_OUTPUT_ID")
  WRONG_SUBMISSION_PENALTY = Config.infomationTaker("WRONG_SUBMISSION_PENALTY")
  START_TIMESTAMP = Config.infomationTaker("START_TIMESTAMP")
  try:
    result = sheet.values().get(spreadsheetId=SHEET_OUTPUT_ID, range=RANGE_NAME).execute()
    currPenalty = float(result.get('values', [])[0][0])
  except:
    currPenalty = 0
  currPenalty += (score-1)*WRONG_SUBMISSION_PENALTY + int((submitTime-START_TIMESTAMP)/60)
  body = {
    'values': [[currPenalty]]
  }
  result = sheet.values().update(
    spreadsheetId=SHEET_OUTPUT_ID,
    range=RANGE_NAME,
    valueInputOption="RAW", 
    body=body
  ).execute()
  print("          RANGE_NAME: {} - Score: {} - Penalty: {}".format(RANGE_NAME, score, currPenalty))

def updateScore(sheet, student, problem, score, submitTime):
  SHEET_OUTPUT_ID = Config.infomationTaker("SHEET_OUTPUT_ID")
  CONTEST_MODE = Config.infomationTaker("CONTEST_MODE")
  RANGE_NAME = getRangeName(sheet, student, problem)
  isUpdatePenaltyNeeded = 0
  try:
    result = sheet.values().get(spreadsheetId=SHEET_OUTPUT_ID, range=RANGE_NAME).execute()
    currScore = float(result.get('values', [])[0][0])
  except:
    currScore = 0
  if CONTEST_MODE == "ACM":
    if currScore <= 0:
      currScore -= 1
      if score == 10: 
        score = -currScore
        isUpdatePenaltyNeeded = 1
      else: score = currScore
    else: score = currScore
  else:
    score = max(currScore, score)
  body = {
    'values': [[score]]
  }
  result = sheet.values().update(
    spreadsheetId=SHEET_OUTPUT_ID,
    range=RANGE_NAME,
    valueInputOption="RAW", 
    body=body
  ).execute()
  if isUpdatePenaltyNeeded:
    RANGE_NAME_PENALTY = getRangeName(sheet, student, "PENALTY")
    updatePenalty(sheet, RANGE_NAME_PENALTY, score, submitTime)
  print("          {} - {} - {}, score is {} at timestamp {}".format(student, problem, RANGE_NAME, score, submitTime))
