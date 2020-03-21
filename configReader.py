import re
import json 

def configReader():
  result = {}
  configFile = open(".env.json").read()
  config = json.loads(configFile)
  studentsFile = open(config["STUDENT_LIST"]).read()
  students = json.loads(studentsFile)
  result[ "config" ] = config
  result[ "students" ] = students
  return result

def infomationTaker(key):
  configFile = open(".env.json").read()
  config = json.loads(configFile)
  return config[ key ]

##########################################
## DEBUG ##
##########################################

def __MAIN__():
  print( configReader() )

if __name__ == '__main__':
  __MAIN__()