# SecCam
## A modular day/night security camera system using radar-based motion detection (ESP32), UART communication with a Raspberry Pi, and a machine-vision (YOLO) human detection pipeline that generates animated GIF alerts and sends them to Telegram.

# 📸 Examples w/ telegram captions
### Left (day): "2 Humans spotted at 2025-11-28 16:25:52"
### Middle (night): "Human spotted at 2025-11-28 17:59:39"
### Right (low-light): "Human spotted at 2025-11-29 00:37:44"
![Alt text](examples/example_day.gif)
![Alt text](examples/example_night.gif)
![Alt text](examples/example_day2.gif)

YOLO was able to detect the correct amount of people reliably in ~5 seconds (tested up to four people)

# 📁 Overview
### SecCam is a hybrid hardware/software security system designed for reliable outdoor or indoor monitoring, even in low-light or no-light environments. 
Little to no downtime for camera (Sensor triggers -> ~10 seconds -> GIF appears in chat -> loop begin)

Pipeline:
1. Human radar sensor connected to an ESP32 via GPIO
2. Serial UART connection to RaspberryPi3b+
3. YOLO based machine-vision human detection
4. Frame capture -> GIF generation -> Telegram alerts

SecCam is optimized for low power, low false positives, and real-time responsiveness.

# 📡 Tech Stack
## Hardware / Communication
* HMMD-MMWave-Sensor [Buy](https://www.amazon.com/gp/product/B0DKFKZ867/ref=ox_sc_saved_title_3?smid=A3B0XDFTVR980O&psc=1)
* ESP32 Dev Board (handles radar data) [Buy](https://www.amazon.com/gp/product/B07WCG1PLV/ref=ox_sc_saved_title_2?smid=A2Z10KY0342329&th=1)
* UART Serial (Radar <-> ESP32)
* Raspberry-Pi3b+ (primary processing unit) [Buy](https://www.amazon.com/Raspberry-Pi-Model-Board-Plus/dp/B0BNJPL4MW/ref=sr_1_1_mod_primary_new?crid=18EG9YQ9KPA9O&dib=eyJ2IjoiMSJ9.23Sg4H89RDNyvDD-Kxi89E-T4MNtJ0tRRBnUOknhThV8oNn_kD6H1OGJ_F0kNLs0ZFqKcXpIRYoqSrvH8gdELvN2tqXQ7lj-ekrRTU9iccHL-2NPWEr4p5L1uOPqIHg1JkQhO5BLgNj1Fgt5LQrX5smOsIfGDyKOuN_VF4Dg82I9FFrTozQsaKu-he-6Lkgg_S8wPD-oAHLxUaSSG9YJHI-XM03HsSR2DkNWGDeVi45qByGK7cvDLCbqR_lQ5x1C0W1a-L2BkzpMEEA8bXtvRiQy7_XQk0AAoGu7fV5p7Mw.aH5JHlUT2_v2iEWm1g-Y9oTsLG3pMkCwTn0mVUtVIfs&dib_tag=se&keywords=raspberry+pi+3b%2B&qid=1764484282&s=electronics&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=raspberyr+pi+3b%2B%2Celectronics%2C204&sr=1-1)
* GPIO (power, triggers)
* Arducam 1080p night/day camera with automatic light detection [Buy](https://www.amazon.com/gp/product/B0829HZ3Q7/ref=ox_sc_saved_title_1?smid=A2IAB2RW3LLT8D&psc=1)
## Software
* Python
* Bash
* C++ (ESP32 firmware)
* Ultralytics YOLOv8n
* RPi.GPIO
* fmpeg (camera + GIF generation)
* curl (Telegram API sending)
* Telegram Bot API

# 🔌 System Architecture/Wiring
           ┌─────────────────────────┐
           │    HMMD Radar Module    │
           └─────────┬───────────────┘
                     │
                     │ Data: TX  ──► RX2 (ESP32)
                     │ Power: 3V3 ──► 3V3 (ESP32)
                     │ Ground: GND ──► GND (ESP32)
                     │
                ┌────┴───────┐
                │   ESP32    │
                └────┬───────┘
                     │
                     │ Data: GPIO23 ──► GPIO17 (Pi)
                     │ Power: VIN  ───► 5V (Pi)
                     │ Ground: GND ───► GND (Pi)
                     │
           ┌─────────┴──────────────┐
           │    Raspberry Pi 3B+    │
           │ - Frame Capture        │   USB   ┌───────────────┐
           │ - Human Detection      ├─────────┤ Camera module │
           │ - GIF Generation       │         └───────────────┘
           │ - Telegram API         │
           └─────────┬──────────────┘
                     │
                     ▼
             Smartphone Alerts


# 📦 Setup and Installation
### Clone the repo
```
git clone https://github.com/MearlyAMortal/SecCam.git
cd SecCam
```
### Setup Raspberry Pi
1. Create virtual environment:
   ```
   python3 -m venv ~/ml-env
   ```
2. Activate it:
   ```
   source ~/ml-env/bin/activate
   ```
3. Install dependencies (Depenting on pi OS):
   ```
   sudo apt install -y python3-pip ffmpeg curl
   pip install RPi.GPIO ultralytics 
   ```
4. Set up directory
   ```
   mkdir -p photos
   touch config.sh
   ```
5. Set up config.sh
   ```
   nano config.sh
   ```
   config.sh
   ```
   #!/bin/bash
   #Vision
   export CONF_FRAMES_DIR="your full frames directory path (should be in /home/.../SecCam/photos/frames)"
    
   #Send
   export CONF_PHOTOS_DIR="your full photos directory path (should be in /home/.../SecCam/photos)"
   export CONF_BOT_TOKEN="your telegram bot token"
   export CONF_CHAT_ID="your telegram chat id"
    
   #Listen
   export CONF_SEND_SCRIPT="your full send.sh directory path (should be in /home/.../SecCam/send.sh)"
   ```
   
### ESP32
Upload the firmware in SecCam/esp32_send.ino using Arduino IDE (ESP32 Dev Board, speed 115200).

### Telegram Bot setup
Full guide to setup bot [HERE](https://apidog.com/blog/beginners-guide-to-telegram-bot-api/)

# 💻 Usage
To start:
```
./listen.sh
```
To stop:

CTRL+c (SIGINT)

## © License and Contact
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Contact me: [GitHub profile](https://github.com/MearlyAMortal)

