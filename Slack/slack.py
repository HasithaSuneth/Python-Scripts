from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

SLACK_TOKEN = "xoxb-3875989314099-4598222582896-a6RAWuMLFbVn59RmXuPUi2Lz"

client = WebClient(token=SLACK_TOKEN)
channel = '#tech-team'


def single_msg(client, channel, text):
    client.chat_postMessage(channel=channel, text=text)


single_msg(client, channel, 'Hello! Hasitha :tada:')


def single_msg_to_user(client, channel, user_id, text):
    client.chat_postEphemeral(
        channel=channel,
        text=text,
        user=user_id
    )


single_msg_to_user(client, channel, "U03RKDFCJS2",
                   "Hello silently from your app! :tada:")


def block_msg(client, channel, msg):
    client.chat_postMessage(channel=channel, block=msg)


msg = [
    {
        "type": "section",
        "text": {
                "type": "mrkdwn",
                "text": "Danny Torrence left the following review for your property:"
        }
    },
    {
        "type": "section",
        "text": {
                "type": "mrkdwn",
                "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
                "237 was far too rowdy, whole place felt stuck in the 1920s."
        },
        "accessory": {
            "type": "image",
            "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
            "alt_text": "Haunted hotel image"
        }
    },
    {
        "type": "section",
        "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Average Rating*\n1.0"
                }
        ]
    }
]

block_msg(client, channel, msg)


def file_upload(client, channel, file, title):
    client.files_upload(
        channels=channel,
        file=file,
        title=title
    )


file_upload(client, channel, "image.png", "Title")
