#!/bin/bash
source ./config.sh

#Takes a new photo and sends it to a telegram chat via bot

{
FILE_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DISPLAY_TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PHOTOS_DIR="$CONF_PHOTOS_DIR"

#Gets latest photo number
last=$(ls "$PHOTOS_DIR"/test*.jpg 2>/dev/null | sed 's/.*test\([0-9]*\)\.jpg/\1/' | sort -n | tail -1)
last=${last:-0}
next=$((last + 1))

IMAGE="$PHOTOS_DIR/test$next.jpg"
#------------------------------------

FRAMES_DIR="$PHOTOS_DIR/frames"
TODAY_DIR="$PHOTOS_DIR/gifs/$(date +%F)"
mkdir -p "$TODAY_DIR"

FRAMERATE=5
FRAMES=90
RESOLUTION="640x480"

#Takes photo in YOLO format
#ffmpeg -f v4l2 -input_format mjpeg -video_size 640x480 -i /dev/video0 -frames:v 1 "$IMAGE"
#------------------------------------
#Takes multiple frames in YOLO format
ffmpeg -f v4l2 -input_format mjpeg -video_size "$RESOLUTION" -framerate "$FRAMERATE" -i /dev/video0 -frames:v "$FRAMES" "$FRAMES_DIR/frame_%03d.jpg"

#Combine into a GIF in telegram format
FRAME_COUNT=$(ls "$FRAMES_DIR"/frame_*.jpg 2>/dev/null | wc -l)
if [ "$FRAME_COUNT" -eq 0 ]; then
    echo "No frames captured, skipping GIF creation."
    exit 1
fi
GIF_FILE="$TODAY_DIR/output_$FILE_TIMESTAMP.gif"
ffmpeg -pattern_type glob -i "$FRAMES_DIR/frame_*.jpg" -vf "fps=$FRAMERATE,scale=320:-1:flags=lanczos" "$GIF_FILE"

#Counts humans using vision script (Propogates STOUT two times: vision.py -> vision.sh -> here)
#HUMAN_COUNT=$(./vision.sh | tr -dc '0-9')
HUMAN_COUNT=$(./vision.sh | tail -n1 | grep -o '^[0-9]\+')
#HUMAN_COUNT=1



#Remove frames used for YOLO and GIF generation
#rm -f "$PHOTOS_DIR"/frames/frame_*.jpg



#Send GIF to telegram if humans are present
if [ "$HUMAN_COUNT" -gt 0 ]; then
    if [ "$HUMAN_COUNT" -eq 1 ]; then
        CAPTION="Bozo spotted at $DISPLAY_TIMESTAMP"
    else
        CAPTION="$HUMAN_COUNT Bozos spotted at $DISPLAY_TIMESTAMP"
    fi

    BOT_TOKEN="$CONF_BOT_TOKEN"
    CHAT_ID="$CONF_CHAT_ID"

    #Sends to telegram
    #curl -F chat_id="$CHAT_ID" -F photo="@$IMAGE" -F caption="$CAPTION" https://api.telegram.org/bot"$BOT_TOKEN"/sendPhoto
    curl -s -X POST https://api.telegram.org/bot"$BOT_TOKEN"/sendAnimation -F chat_id="$CHAT_ID" -F animation="@$GIF_FILE" -F caption="$CAPTION" 
else
    echo "No humans detected."
fi

} > /dev/null 2>&1
