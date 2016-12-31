import sys
from subprocess import call

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
        myfile = open('/mnt/ramdisk/cmd1.txt', 'r')
        while True:
            time.sleep(0.1)
            cmd = myfile.readline()
            if cmd == 'left':
                call(["moveleft.py", ""])
        
    except:
        myfile.close()
    
