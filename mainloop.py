import sys
from subprocess import call
import os.path

cmd_list = ["moveleft","nudgeleft","moveright","nudgeright","moveforward","moveback","stop","run", "faceup","facedown","faceleft","faceright", "faceleftnudge", "facerightnudge"]

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
            for c in cmd_list:
                if os.path.isfile('/mnt/ramdisk/cmd-' + c + '.txt'):
                    os.remove('/mnt/ramdisk/cmd-' + c + '.txt')
                    call(["sudo python " + c + ".py &", ""])
        
