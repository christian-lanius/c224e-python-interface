from admin import C224eAdmin
import user
import signal
import sys
if __name__ == "__main__":
    #Do some magic to make sure we always log out, otherwise we might block the printer
    def signal_handler(signal, frame):
        admin.logout()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    try:
        # Create administrator session
        admin = C224eAdmin()

        admin.login('password', 'printer.hostname')

        #Let's create some test accounts
        admin.createUser('testUser', 'test123')
        admin.getUserByName('testUser')
        admin.setLimits('testUser', 111, 222, 'abs')
        admin.getUserByName('testUser')
        admin.setLimits('testUser', 9, 8, 'inc')
        admin.getUserByName('testUser')

    finally:
        admin.logout()