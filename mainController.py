import configReader as Config
from gsheets import Sheets
import time
import os

# READ FROM FILE
Data = Config.configReader()
students = Data[ "students" ]
config = Data[ "config" ]

# UPDATE SUBMISSION
currRow = 1
secretCodeCol = config[ "SECRET_CODE_COL" ]
problemCodeCol = config[ "PROBLEM_CODE_COL" ]
codeCol = config[ "CODE_COL" ]

while(1):
  print("Updating ...")
  # CONNECT WITH GOOGLE API
  sheets = Sheets.from_files('.client_secret.json', '.storage.json')
  sheet = sheets[ config["SHEET_ID"] ]
  while(1):
    isUpToDate = 0
    try:
      print( sheet.sheets[0].at(row=currRow, col=0) )
      isUpToDate = 0
    except:
      isUpToDate = 1
    if isUpToDate==1 : break
    # Taking Infomation
    studentSecretCode = sheet.sheets[0].at(row=currRow, col=secretCodeCol).strip().upper()
    studentName = students.get(studentSecretCode, studentSecretCode)
    problemName = sheet.sheets[0].at(row=currRow, col=problemCodeCol)
    code = sheet.sheets[0].at(row=currRow, col=codeCol)
    
    # Creating File
    folderUrl = config[ "FILE_OUT_AT" ] + studentName + "/" 
    if not os.path.exists(folderUrl):
      os.makedirs(folderUrl)
    fileUrl = folderUrl + problemName + "." + config[ "FILE_TYPE" ]
    # print( code) 
    # print( currRow, codeCol )
    # print( fileUrl )
    
    # Writing
    myfile = open( fileUrl, "w" )
    myfile.write(code)
    myfile.close()

    # Next Row
    currRow += 1
  print("Updated! Current at row", currRow)
  time.sleep( config[ "RELOAD_AFTER_SEC" ] )
