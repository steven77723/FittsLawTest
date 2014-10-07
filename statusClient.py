import socket
import sys

class Client:
    """ Echo client """
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.size = 1024
        self.open_socket()
        print "Enter a blank line to stop."
        sys.stdout.write('> ')

    def open_socket(self):
        """ Connect to the server """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((self.host,self.port))
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        """ Read from the keyboard and send this line to the server """
        self.server.send('mflt status')
        #print('received')
        data = self.server.recv(self.size)
        return data
    
    def click(self):
        self.server.send("click")

    def switch(self):
        self.server.send("switch")

    def close(self):
        self.server.close()
#         self.server.close()
        
        
        

        