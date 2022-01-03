#!/bin/sh
/usr/bin/audio_Reset_paths.sh
/usr/bin/audio_Record_from_lineIn_Micbias.sh
/usr/bin/audio_Playback_to_Lineout.sh
python /home/mbot/mbotProject/src/robot/MainController.py >>/var/log/m-bot.log
