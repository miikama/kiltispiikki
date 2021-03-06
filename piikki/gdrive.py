from kivy.logger import Logger
from kivy.utils import platform


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


if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method, JavaException
    from android import activity

    Rstring = autoclass("android.R$string")
    Rid = autoclass("android.R$id")

    Drive = autoclass('com.google.android.gms.drive.Drive')
    Builder = autoclass("com.google.android.gms.common.api.GoogleApiClient$Builder")
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    Plus = autoclass("com.google.android.gms.plus.Plus")

    class GoogleApiClientConnectionCallback(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.common.api.GoogleApiClient$ConnectionCallbacks',
                              'com.google.android.gms.common.api.GoogleApiClient$OnConnectionFailedListener']
        __javacontext__ = 'app'
        RC_SIGN_IN = 9001
        RC_RESOLUTION = 1001
        RESULT_OK = -1
        RESULT_CANCELLED = 0
        REQUEST_ACHIEVEMENTS = 1
        REQUEST_LEADERBOARDS = 2

        def __init__(self):
            super(GoogleApiClientConnectionCallback, self).__init__()
            self.on_connected_callback = None
            self.resolving_failure_callback = None
            self.in_resolving_connection = False

        @java_method('(Landroid/os/Bundle;)V')
        def onConnected(self, connectionHint):
            Logger.info("Google: successfully logged in")
            
            if self.on_connected_callback:
                self.on_connected_callback()

        def on_activity_result(self, requestCode, resultCode, intent):
            Logger.info("Google: back to activity result. %s, %s" % (requestCode, resultCode))
            if requestCode == self.RC_RESOLUTION:
                self.in_resolving_connection = False
                if resultCode == self.RESULT_OK:
                    Logger.info("Google: resolving result okay")
                    self.client.connect()
                elif resultCode == self.RESULT_CANCELLED:
                    Logger.info("Google: resolving cancelled")
                else:
                    Logger.warning("Google: resolving failed. Error code: %s" % resultCode)
                    if self.resolving_failure_callback:
                        self.resolving_failure_callback(resultCode)

        @java_method('(Lcom/google/android/gms/common/ConnectionResult;)V')
        def onConnectionFailed(self, connectionResult):
            Logger.info(
                "Google: connection failed. Error code: %s. Trying to resolve..." % connectionResult.getErrorCode())

            if self.in_resolving_connection:
                Logger.info("Google: already in resolving, pass...")
                return

            self.in_resolving_connection = True

            if connectionResult.hasResolution():
                Logger.info("Google: starting resolution...")
                activity.bind(on_activity_result=self.on_activity_result)
                connectionResult.startResolutionForResult(PythonActivity.mActivity, self.RC_RESOLUTION)
            else:
                Logger.info("Google: connection issue has no resolution... "
                            "hasResolution says: %s" % connectionResult.hasResolution())

        @java_method('(I)V')
        def onConnectionSuspended(self, i):
            raise Exception("JAVA callback onConnectionSuspended wrap success")

        @java_method('()I')
        def hashCode(self):
            # hack because of the python and c long type error
            return (id(self) % 2147483647)

        @java_method('()Ljava/lang/String;', name='hashCode')
        def hashCode_(self):
            return '{}'.format(id(self))

        @java_method('(Ljava/lang/Object;)Z')
        def equals(self, obj):
            return obj.hashCode() == self.hashCode()

    class AndroidGoogleClient(AbstractGoogleClient):

        def __init__(self):
            self.app = PythonActivity.getApplication()
            super(AndroidGoogleClient, self).__init__()


        def _get_client(self):
            try:
                Logger.info("Google: building client...")
                self.connection_callback = GoogleApiClientConnectionCallback()
                mGoogleApiClient = Builder(self.app). \
                    addConnectionCallbacks(self.connection_callback). \
                    addOnConnectionFailedListener(self.connection_callback). \
                    addApi(Drive.API).addScope(Drive.SCOPE_FILE).build()
                self.connection_callback.client = mGoogleApiClient
            except JavaException:
                Logger.info('Google: retrieving client failed big time')
                return None
            return mGoogleApiClient

        def connect(self, success_callback=None, fail_callback=None):
            super(AndroidGoogleClient, self).connect()
            if self.client:
                self.connection_callback.on_connected_callback = success_callback
                self.connection_callback.resolving_failure_callback = fail_callback
                self.client.connect()

        def logout(self):
            super(AndroidGoogleClient, self).logout()
            if self.client and self.is_connected():
                try:
                    self.client.disconnect()
                except JavaException:
                    Logger.error("Google: error while logout")

        def is_connected(self):
            super(AndroidGoogleClient, self).is_connected()
            return self.client.isConnected()



    GoogleClient = AndroidGoogleClient
else:
    GoogleClient = DummyGoogleClient
