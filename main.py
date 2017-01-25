import admin
# import user
import signal
import sys
if __name__ == "__main__":
    #Create session
    browser = admin.login('SECRETPW')
    #Do some magic to make sure we always log out, otherwise we might block the printer
    def signal_handler(signal, frame):
        admin.logout(browser)
        sys.exit(0)
    if admin.loggedIn:
        signal.signal(signal.SIGINT, signal_handler)
        try:
            #Let's create some test accounts
            admin._getUserByName('testUser', browser)
#             admin._getUserByName('131', browser)
#             admin.createUser('testUser', 'test123', browser)
#             admin.createUser('testUser2', 'test123', browser)
#             admin.createUser('testUser3', 'test123', browser)
#             admin.createUser('testUser3', 'test123', browser)
#             admin.setLimits('bla', bw = 100, color = 50, 'inc', browser)
        finally:
            admin.logout(browser)