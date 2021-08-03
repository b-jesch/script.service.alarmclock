[![Build Status](https://travis-ci.org/remigius42/script.service.alarmclock.svg?branch=master)](https://travis-ci.org/remigius42/script.service.alarmclock)

xbmc-alarm-clock
================

The add-on provides five individual alarms for XBMC playing either a file 
or an URL on repeat.

#Features
  - Up to five individual alarms
  - Scheduling for a week day, every day or Monday to Friday
  - Plays either a file or a custom path may be set which may point to any
      media type supported by XBMC including for example web radio URLs
  - Tries to activate the configured HDMI device over CEC

#Notes
  - If the duration is over, XBMC will stop playing regardless of what is
    being played at the moment. This means a) alarm 1 could disable
    alarm 2 if alarm 2 starts before alarm 1 start time plus duration 1
    is over and b) it may stop something you were playing intentionally
    in the meantime.
  - The overflow over to the next day is not considered. You should make
    sure the start time of any alarm plus its duration is before 0:00.

#Credits
  - Adapted and updated to Matrix from the original Addon "XBMC Alarm clock"
    by remigius: https://github.com/remigius42-old/script.service.alarmclock