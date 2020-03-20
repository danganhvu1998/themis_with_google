# Connet Google Drive with Themis

## Setting

+ Python3
  + ```pip install gsheets```
+ Google API:
  + Log into the Google Developers Console with the Google account whose spreadsheets you want to access. Create (or select) a project and enable the Drive API and Sheets API (under Google Apps APIs). More info about setting Google API: [here](https://gsheets.readthedocs.io/en/stable/)
  + Copy list of your OAuth 2.0 client IDs to ```.client_secret.json```. Something like: 
    + ```{"installed":{"client_id":"sth_sth.apps.googleusercontent.com","project_id":"sth_sth","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"sth_sth","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}```

+ Setting ```.env.json```
  + ```SHEET_ID```: if link is ```docs.google.com/spreadsheets/d/1byw0Qh_3IWUlcMYOzFlR3T0SyMH_AAW9Cj2XkNug5Ck``` then id is ```1byw0Qh_3IWUlcMYOzFlR3T0SyMH_AAW9Cj2XkNug5Ck```
  + ```SECRET_CODE_COL```, ```PROBLEM_CODE_COL```, ```CODE_COL```: index starts from 0.
+ Setting ```students.json```
  + Using json. Key is secret code, value is student name

## Running

+ ```python mainController.py```
+ Output files are at ```.env.json -> FILE_OUT_AT```
