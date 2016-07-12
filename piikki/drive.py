"""
Created on Sun Jul  3 17:15:06 2016

@author: miika
"""

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

    from jnius import PythonJavaClass, autoclass, java_method, JavaException
    
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    activity = PythonActivity.mActivity
    
    Builder = autoclass("com.google.android.gms.common.api.GoogleApiClient$Builder")
    Drive = autoclass('com.google.android.gms.drive.Drive')
    ConnectionResult = autoclass('com.google.android.gms.common.ConnectionResult')
    GooglePlayServicesUtil = autoclass('com.google.android.gms.common.GooglePlayServicesUtil')
    GoogleApiClient = autoclass('com.google.android.gms.common.api.GoogleApiClient')
    
    
    class DriveAccessClient(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.common.api.GoogleApiClient$ConnectionCallbacks',
                              'com.google.android.gms.common.api.GoogleApiClient$OnConnectionFailedListener']
        __javacontext__ = 'app'
        
        def __init__(self):
            super(DriveAccessClient, self).__init__()
            self.on_connected_callback = None
            self.resolving_failure_callback = None
            self.in_resolving_connection = False
            self.mGoogleApiClient = None
            
        @java_method('(Landroid/os/Bundle;)V')
        def onConnected(self, connectionHint):
            Logger.info("Google: successfully logged in")
            #Drive.DriveApi.newDriveContents(getGoogleApiClient()).setResultCallback(driveContentsCallback);

            if self.on_connected_callback:
                self.on_connected_callback()
                

        @java_method('(V;)V')
        def onResume(self):
            super(DriveAccessClient,self).onResume()
            if self.mGoogleApiClient == None:
                try:
                     mGoogleApiClient = Builder(self.app). \
                        addConnectionCallbacks(self). \
                        addOnConnectionFailedListener(self). \
                        addApi(Drive.API).addScope(Drive.SCOPE_FILE).build()
                     self.mGoogleApiClient = mGoogleApiClient
                except JavaException:
                    Logger.info('failed building googleapiclient')
            self.mGoogleApiClient.connect()
              
        
         
        @java_method('(IILAndroid/content/Intent;)V')
        def on_activity_result(self, requestCode, resultCode, data):
            Logger.info("Google: back to activity result. %s, %s" % (requestCode, resultCode))
            super(DriveAccessClient, self).onActivityResult(requestCode, resultCode, data)

        
          /**
     * Handles resolution callbacks.
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode,
            Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_RESOLUTION && resultCode == RESULT_OK) {
            mGoogleApiClient.connect();
        }
    }   
    







