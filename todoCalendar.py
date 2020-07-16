from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from os import path
import pprint 
import datetime

pp = pprint.PrettyPrinter(indent=4)
key = 'AIzaSyARG13WR-zhjWJ6cWsermUB6ojGobP_TIg'
now = datetime.datetime.utcnow().isoformat() + 'Z'
plusWeek = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file(str(os.getcwd())+'/client_secret.json',scopes=scopes)

creds = None
if os.path.exists('token.pkl'):
    
    with open('token.pkl', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scopes=scopes)
        creds = flow.run_console()
    # Save the credentials for the next run
    with open('token.pkl', 'wb') as token:
        pickle.dump(creds, token)



"""
if(not path.exists("token.pkl")):
    credentials = flow.run_console()
    pickle.dump(credentials,open("token.pkl","wb"))
else: 
    credentials = pickle.load(open("token.pkl","rb"))
    print(credentials)
"""
service = build("calendar","v3",credentials=creds)
result = service.calendarList().list().execute()
calendar_id = 'qsq85dgtp4d9ovvv46h5lh314g@group.calendar.google.com'



def createNewEvent(name,startDate,endDate):
    event = {
  'summary': name,
  'location': 'Richardson, Texas',
  'description': '',
    'start':{
        'date': startDate,
        'timeZone': 'America/Chicago',
    },
    'end': {
        'date': endDate,
        'timeZone': 'America/Chicago',
    },
    'recurrence': [],
    'attendees': [],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60}
             ],
        },
    }


    result = service.events().insert(calendarId=calendar_id, body=event).execute
    result()

def removeEvent(name):
    result = service.events().list(calendarId=calendar_id,timeMin=now,timeMax=plusWeek).execute()

    for i in range(100):
        try:
            eventName = result['items'][i]['summary']
            #print(eventName)
            if name == eventName: 
                result = service.events().delete(calendarId=calendar_id, eventId=result['items'][i]['id']).execute()      
                result()
        except Exception as e:
            print(end='')

def listEvents():
    result = service.events().list(calendarId=calendar_id,timeMin=now,timeMax=plusWeek).execute()
    for i in range(100):
        try:
            pprint.pprint((result['items'][i]['summary']).strip("'"))
        except Exception:
            print(end='')