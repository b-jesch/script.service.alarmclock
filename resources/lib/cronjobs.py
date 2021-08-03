"""
Cronjob like scheduling abstraction in Python.
"""

from datetime import datetime, timedelta
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()
addon_id = '[%s-%s]' % (addon.getAddonInfo('id'), addon.getAddonInfo('version'))


def log(message, level=xbmc.LOGDEBUG):
    xbmc.log('%s %s' % (addon_id, message), level)


class CronTab(object):

    """
    Simulates basic cron functionality by checking for firing jobs every minute.
    """

    def __init__(self):
        self.jobs = []
        self.__enabled = True

    def stop(self):
        """
        Stops the crontab.
        """
        self.__enabled = False

    def start(self):
        """
        Starts to check every minute, if the registered jobs should run.
        """
        cron_time_tuple = datetime(*datetime.now().timetuple()[:5])
        while self.__enabled and not xbmc.Monitor().abortRequested():
            for job in self.jobs:
                log("checking job #%s: (%02d:%02d [%s])" % (job.job_num, job.hours, job.mins, job.dow))
                job.check(cron_time_tuple)
            cron_time_tuple += timedelta(minutes=1)
            if datetime.now() < cron_time_tuple:
                xbmc.Monitor().waitForAbort((cron_time_tuple - datetime.now()).seconds)
                # xbmc.sleep((cron_time_tuple - datetime.now()).seconds * 1000)
        log('Cron finished')

class Job(object):
    """
    Cron job abstraction.
    """
    def __init__(self, number, action, minute=None, hour=None, dow=None, args=(), kwargs=None):
        self.job_num = int(number)
        self.mins = int(minute)
        self.hours = int(hour)
        self.dow = dow
        self.action = action
        self.args = args
        if kwargs is None: kwargs = {}
        self.kwargs = kwargs

    def is_matchtime(self, cron_time_tuple):
        """
        Is it the job's scheduled time
        """
        return ((cron_time_tuple.minute == self.mins) and
                (cron_time_tuple.hour == self.hours) and
                (cron_time_tuple.weekday() in self.dow))

    def check(self, cron_time_tuple):
        """
        Checks if it is the scheduled time and executes the job if so.
        """
        if self.is_matchtime(cron_time_tuple):
            self.action(*self.args, **self.kwargs)
