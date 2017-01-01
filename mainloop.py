import sys
from subprocess import call
import os.path

cmd_list = ["up","down","headleft","headright", "headleftnudge", "headrightnudge","headcenter","left","nudgeleft","right","nudgeright","forward","back","stop","run"]

try:
    import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ## Create an abstract socket, by prefixing it with null. 
    s.bind( '\0mainloop_lock') 
      
except socket.error, e:
    error_code = e.args[0]
    error_string = e.args[1]
    print "Process already running (%d:%s ). Exiting" % ( error_code, error_string) 
    sys.exit (0)
    
else:
    try:
        while True:
            time.sleep(0.1)
            if os.path.isfile('/mnt/ramdisk/cmd-left.txt'):
                os.remove('/mnt/ramdisk/cmd-left.txt')
                call(["sudo python moveleft.py", ""])
            if os.path.isfile('/mnt/ramdisk/cmd-nudgeleft.txt'):
                os.remove('/mnt/ramdisk/cmd-nudgeleft.txt')
                call(["sudo python moveleft.py", ""])
        
    except:
        myfile.close()
        
