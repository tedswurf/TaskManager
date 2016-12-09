'''
 Usage : python aservice.py install
 Usage : python aservice.py start
 Usage : python aservice.py stop
 Usage : python aservice.py remove
 
 C:\>python TaskManagementAsyncService.py  --username <username> --password <PASSWORD> --startup auto install
OR
Running as Administrator:
python TaskManagementAsyncService.py install

# TODO: 	
Basic constituent code blocks needed

The following are the required basic code blocks of your client application

Session request section: request a session with the provider
Session authentication section: provide credentials to the provider
Client section: create the Client
Security Header section: add the WS-Security Header to the Client
Consumption section: consume available operations (or methods) as needed

'''
from TaskManager import *
from Task import *
from Configure import *
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


class TaskManagementAsyncService (win32serviceutil.ServiceFramework):
    _svc_name_ = "TaskManagementOrchestrator"
    _svc_display_name_ = "Task Manager Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        #self.timeout = 640000    #640 seconds / 10 minutes (value is in milliseconds)
        self.timeout = 120000     #120 seconds / 2 minutes
        # This is how long the service will wait to run / refresh itself (see script below)
        print(VERSION_NUMBER_DATE)
        configuration = Configure()
        configuration.ReadTMConfiguration(TM_CONFIGURATION_FILE_NAME)

        taskManager = TaskManager()
        taskManager.PopulateTaskLibrary()

        here = os.path.dirname(os.path.realpath(__file__))
        subdir = "Tasks"
        filename = "TaskTestTarget.Task.xml"
        targetXmlFileName = os.path.join(here, subdir, filename)

        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("Stop Signal Encountered - STOPPED!")  #For Event Log
                break
            else:
                #[actual service code between rests]
                try:
                    # Need to activate Listener for a request
                    print("running")
                except:
                    pass
                #[actual service code between rests]

        #self.main()

    def main(self):
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(TaskManagementAsyncService)