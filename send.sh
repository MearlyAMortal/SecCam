#!/bin/bash
source ./config.sh

# AUTHOR: Logan Puntous
# DATE: 11/28/2025

# When executed will take a number of frames from a USB camera(NVG)
# Those frames are used to generate a GIF file with a timestamp
# The frames are sent to vision.sh which will return the number of humans detected
# The frames are then discarded
# If humans>=1 the GIF will be sent to a telegram chat via: telegramAPI
# STDERR and STDOUT are supressed
# Sensitive data is gathered from outside file

{
FILE_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DISPLAY_TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PHOTOS_DIR="$CONF_PHOTOS_DIR"
FRAMES_DIR="$PHOTOS_DIR/frames"
TODAY_DIR="$PHOTOS_DIR/gifs/$(date +%F)"

mkdir -p "$FRAMES_DIR"
mkdir -p "$TODAY_DIR"

#Camera settings
FRAMERATE=5
FRAMES=90
RESOLUTION="640x480"


#Takes multiple frames in YOLO format
ffmpeg -f v4l2 -input_format mjpeg -video_size "$RESOLUTION" -framerate "$FRAMERATE" -i /dev/video0 -frames:v "$FRAMES" "$FRAMES_DIR/frame_%03d.jpg"


#Generate GIF in telegram format
shopt -s nullglob
files=("$FRAMES_DIR"/frame_*.jpg)
FRAME_COUNT=${#files[@]}
if [ "$FRAME_COUNT" -eq 0 ]; then
    echo "ERROR: send.sh no frames found" >&2
    exit 1
fi
GIF_FILE="$TODAY_DIR/output_$FILE_TIMESTAMP.gif"
ffmpeg -pattern_type glob -i "$FRAMES_DIR/frame_*.jpg" -vf "fps=$FRAMERATE,scale=320:-1:flags=lanczos" "$GIF_FILE"


#Counts humans using vision script (Propogates STOUT two times: vision.py -> vision.sh -> here)
HUMAN_COUNT=$(./vision.sh | tail -n1 | grep -o '^[0-9]\+')


#Delete frames used for previous sections
#rm -f "$PHOTOS_DIR"/frames/frame_*.jpg


#Send GIF to telegram if humans are present
if [ "$HUMAN_COUNT" -gt 0 ]; then
    if [ "$HUMAN_COUNT" -eq 1 ]; then
        CAPTION="Human spotted at $DISPLAY_TIMESTAMP"
    else
        CAPTION="$HUMAN_COUNT Humans spotted at $DISPLAY_TIMESTAMP"
    fi

    BOT_TOKEN="$CONF_BOT_TOKEN"
    CHAT_ID="$CONF_CHAT_ID"

    #Sends GIF to telegram
    curl -s -X POST https://api.telegram.org/bot"$BOT_TOKEN"/sendAnimation -F chat_id="$CHAT_ID" -F animation="@$GIF_FILE" -F caption="$CAPTION" 
fi

} > /dev/null 2>&1
