"""
Startup script for the Kodi alarm clock add-on.
"""

import os
import xbmcvfs
from resources.lib.cronjobs import *

media = os.path.join(xbmcvfs.translatePath(addon.getAddonInfo('path')), 'resources', 'media', 'alert.mp3')


def _stop_playing():
    """
    Stops whatever is playing at the moment
    """
    xbmc.Player().stop()


def _start_playing(item, volume):
    """
    Starts playing the given item at the supplied volume.
    """
    xbmc.executebuiltin('CECActivateSource')
    xbmc.executebuiltin('SetVolume(%s)' % volume)
    xbmc.Player().play(item)


def get_jobs(number):
    """
    Initialize jobs(s) for alarm number.
    If the alarm has a duration enabled, both the start and the stop job
    are returned in the list.
    """
    days_of_week = int(addon.getSetting("day%d" % number))
    if days_of_week == 7:
        days_of_week = range(5)
    if days_of_week == 8:
        days_of_week = range(7)

    action = addon.getSetting("action%d" % number)
    if action == "0":
        file_name = media if addon.getSetting("file%d" % number) == 'alert.mp3' else addon.getSetting("file%d" % number)
    else:
        file_name = addon.getSetting("text%d" % number)

    jobs = [Job(number,
                _start_playing,
                int(addon.getSetting("minute%d" % number)),
                int(addon.getSetting("hour%d" % number)),
                dow=days_of_week,
                args=[file_name, addon.getSetting("volume%d" % number)])]

    if addon.getSetting("turnOff%d" % number) == "true":
        jobs.append(Job(number,
                        _stop_playing,
                        int(addon.getSetting("minute%d" % number)) +
                        (int(addon.getSetting("duration%d" % number)) % 60),
                        int(addon.getSetting("hour%d" % number)) +
                        (int(addon.getSetting("duration%d" % number)) / 60),
                        dow=days_of_week))
    return jobs


def get_alarms():
    """
    Get a list of the cron jobs for the enabled alarms.
    """
    jobs = []
    j = 0
    for i in range(1, 6):
        if addon.getSetting("alarm%d" % i) == "true":
            jobs.extend(get_jobs(i))
            j += 1
    log("%s active event(s) fetched" % j)
    return jobs


class AlarmClock(object):
    """
    Main alarm clock application class.
    """
    def __init__(self):
        self.crontab = CronTab()
        self.monitor = self.AddonMonitor(self.crontab)

    def apply_settings(self):
        """
        Gets the current configuration and updates the scheduler.
        """
        self.crontab.jobs = get_alarms()
        log('Settings loaded')

    def start(self):
        """
        Starts the alarm clock, ie. activates the defined alarms.
        """
        self.apply_settings()
        self.crontab.start()

    def stop(self):
        """
        Stops the alarm clock.
        """
        self.crontab.stop()

    class AddonMonitor(xbmc.Monitor):
        """
        Monitoring class
        """

        def __init__(self, crontab):
            xbmc.Monitor.__init__(self)
            self.crontab = crontab

        def onSettingsChanged(self):
            self.crontab.jobs = get_alarms()
            log('Settings applied')


if __name__ == '__main__':
    alarm_clock = AlarmClock()
    log("Starting alarm clock...")
    alarm_clock.start()
