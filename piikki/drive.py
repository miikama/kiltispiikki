"""
Created on Sun Jul  3 17:15:06 2016

@author: miika
"""

from kivy.logger import Logger
from jnius import autoclass

PythonActivity = autoclass('org.renpy.android.PythonActivity')
activity = PythonActivity.mActivity

Drive = autoclass('com.google.android.gms.drive.Drive')
ConnectionResult = autoclass('com.google.android.gms.common.ConnectionResult')

class AbstractGoogleClient(object):
    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        return None

    def connect(self, success_callback=None, fail_callback=None):
        Logger.info('Google: connecting...')

    def logout(self):
        Logger.info('Google: log out...')

    def is_connected(self):
        pass


class DummyGoogleClient(AbstractGoogleClient):
    def __init__(self):
        super(DummyGoogleClient, self).__init__()
        self.client = self._get_client()
        self.connected = False

    def connect(self, success_callback=None, fail_callback=None):
        super(DummyGoogleClient, self).connect(success_callback=None, fail_callback=None)
        if success_callback:
            success_callback()
        self.connected = True

    def is_connected(self):
        super(DummyGoogleClient, self).is_connected()
        return self.connected

    def logout(self):
        super(DummyGoogleClient, self).logout()
        self.connected = False


