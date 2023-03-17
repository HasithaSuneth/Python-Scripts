import jwt  # [pip install PyJWT]
import requests  # [pip install requests]
import json
from time import time
# (optional) For environment variables [pip install python-decouple]
from decouple import config


# Enter your API key and your API secret.
# Replace config('') with your API informations "" or create a .env file.
API_KEY = config('API')
API_SEC = config('SEC')

# Create a function to generate a token using the pyjwt library


def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},

        # Secret used to generate token signature
        API_SEC,

        # Specify the hashing alg
        algorithm='HS256'
    )
    return token
    # return token.decode('utf-8')


# Link for the Official API Documentation
# https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#operation/meetingCreate

# Create json data for post requests

meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2023-03-17T14: 21: 57",
                  "duration": "45",
                  "timezone": "Asia/Colombo",
                  "agenda": "test",

                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "False",
                               "participant_video": "False",
                                "join_before_host": "False",
                                "mute_upon_entry": "True",
                                "watermark": "False",
                                "audio": "voip",
                                "auto_recording": "local"
                               }
                  }

# Send a request with headers including a token and meeting details


def createMeeting():
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))

    print("\n creating zoom meeting ... \n")
    # Converting the output into json and extracting the details
    y = json.loads(r.text)
    # print(y)	For refer all details
    join_URL = y["join_url"]
    meetingPassword = y["password"]

    print(
        f'\nHere is your zoom meeting link "{join_URL}" and your password: "{meetingPassword}"\n')


# Run the create meeting function
createMeeting()
