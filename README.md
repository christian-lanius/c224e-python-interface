# c224e-python-interface
Small python scripts to manage Bizhub C224e printer from Konica Minolta

#How To Use
RoboBrowser has to be set up correctly. This should be easy if an existing python 3.x environment exists: http://robobrowser.readthedocs.io/en/latest/
Use the respective login method to generate a browser session, this has to be supplied to each function call for this user.  The signal handler and case statement should be registered as shown in the main.py as to make sure the admin is logged off, otherwise the printer may be blocked.

#Not working
The admin can not login while a job is being processed, the login will fail. It is possible to instead login in as admin in usermode and delete the job stalling the printer. This is not implemented. The user functions have to error processing done and might result in an infinite loop. Some methods are lacking proper error handling.
