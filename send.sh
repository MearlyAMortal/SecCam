#!/bin/bash
source ./config.sh

#Takes a new photo and sends it to a telegram chat via bot

{
PHOTOS_DIR="$CONF_PHOTOS_DIR"

#Gets latest photo number
last=$(ls "$PHOTOS_DIR"/test*.jpg 2>/dev/null | sed 's/.*test\([0-9]*\)\.jpg/\1/' | sort -n | tail -1)
last=${last:-0}
next=$((last + 1))

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
CAPTION="Bozo spotted at $TIMESTAMP"

IMAGE="$PHOTOS_DIR/test$next.jpg"

BOT_TOKEN="$CONF_BOT_TOKEN"
CHAT_ID="$CONF_CHAT_ID"



#Takes photo in YOLO format
#ffmpeg -f v4l2 -input_format mjpeg -i /dev/video0 -frames:v 1 "$IMAGE"
ffmpeg -f v4l2 -input_format mjpeg -video_size 640x480 -i /dev/video0 -frames:v 1 "$IMAGE"


#Sends to telegram
curl -F chat_id="$CHAT_ID" -F photo="@$IMAGE" -F caption="$CAPTION" https://api.telegram.org/bot"$BOT_TOKEN"/sendPhoto

} > /dev/null 2>&1
