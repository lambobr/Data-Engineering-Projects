from slack_sdk import WebClient
from datetime import datetime

SLACK_CHANNEL_ID = "C04EPNAC31U"

client = WebClient(token="INSERT TOKEN HERE")
client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=f"Run successfully: {datetime.now()}")
