a = 0

try:
    import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ## Create an abstract socket, by prefixing it with null. 
    s.bind( '\0postconnect_gateway_notify_lock') 
    print "done."
    while True:
      a = 0
      
except socket.error, e:
    error_code = e.args[0]
    error_string = e.args[1]
    print "Process already running (%d:%s ). Exiting" % ( error_code, error_string) 
    sys.exit (0)
