import sys
from subprocess import call
import os
import time

cmd_list = ["moveleft","nudgeleft","moveright","nudgeright","moveforward","moveback","stop","run", "faceup","facedown","faceleft","faceright", "faceleftnudge", "facerightnudge"]

os.nice(5)

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
                    print 'sudo python /var/www/html/' + c + '.py'
                    call(['sudo', 'python', '/var/www/html/' + c + '.py'])
                    os.remove('/mnt/ramdisk/cmd-' + c + '.txt')
                    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        exit()
