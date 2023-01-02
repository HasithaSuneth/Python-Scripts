# import os
from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
 
# SLACK_TOKEN="xoxb-3875989314099-4598170463248-Tk2SrYxCty9Iu9J7Iho8wwou"
SLACK_TOKEN="xoxb-3875989314099-4598222582896-a6RAWuMLFbVn59RmXuPUi2Lz"

 
client = WebClient(token=SLACK_TOKEN)

# client.chat_postMessage(channel='#tech-team',text='Hello! Hasitha')

# response = client.chat_postMessage(
#         channel="#tech-team",
#         text="Hello from your app! :tada:"
#     )

# client.chat_postEphemeral(
#     channel="#tech-team",
#     text="Hello silently from your app! :tada:",
#     user="U03RKDFCJS2" #user-id
# )

# client.chat_postMessage(
#     channel="#tech-team",
#     blocks=[
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": "Danny Torrence left the following review for your property:"
#             }
#         },
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
#                     "237 was far too rowdy, whole place felt stuck in the 1920s."
#             },
#             "accessory": {
#                 "type": "image",
#                 "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
#                 "alt_text": "Haunted hotel image"
#             }
#         },
#         {
#             "type": "section",
#             "fields": [
#                 {
#                     "type": "mrkdwn",
#                     "text": "*Average Rating*\n1.0"
#                 }
#             ]
#         }
#     ]
# )

# response = client.reactions_add(
#     channel="#tech-team",
#     name="thumbsup",
#     timestamp="1234567890.123456"
# )

# response = client.files_upload(
#     channels="#tech-team",
#     file="image.png",
#     title="Image upload"
# )