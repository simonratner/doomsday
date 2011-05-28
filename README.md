# Doomsday Device Monitor #
This is a Win32 service. To install, run the following from an `Administrator` account:

    python doomsday.py --username <user> --password <pass> install

To start the service and configure it to execute a command when triggered:

    sc start DoomsdayDevice <command>

User account used to run the service must have `SeServiceLogonRight` security access, see [KB325349](http://support.microsoft.com/kb/325349/en-us/ "How to grant users rights to manage services") for information on granting such access. Due to [Session 0 isolation](http://msdn.microsoft.com/en-us/library/bb756986.aspx "Session 0 Isolation"), any process started by `command` will never display any UI, even when running as the logged in user.

To configure the service to start on system boot (note the space after `=`):

    sc config DoomsdayDevice start= auto

To stop the service:

    sc stop DoomsdayDevice

To uninstall:

    sc stop DoomsdayDevice
    sc delete DoomsdayDevice
