import socket
import sys
import threading
import os
import argparse

"""
Class: HandlerThread
Param: threading.Thread
Def: This class creates an object for threading
"""
class HandlerThread(threading.Thread):
    
    """
    Function: Constructor
    Param: self. Client is the variable for the current client being passed in. Address is the address of the device hosting the client
    Def: The constructor sets up the attributes for the thread object
    """
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
    
    """
    Function: run
    Param: takes in the self parameter
    Def: This is the client code for each individual thread that is generated
    """
    def run(self):
        #args is a byte string
        args = ''.encode('UTF-8')

        #argsSep will store the original byte string from client.read
        argsSep = b''
        
        #Boolean flags that depics which error to set
        flag200 = False
        flag404 = False
        flag400 = False
        flag403 = False
        
        #sets the parsing variable to allow for a command line root change#
        parser = argparse.ArgumentParser(description='Setting a new path for web files')
        parser.add_argument('-r', '--root', action="store", default='www')
        p = parser.parse_args()
        fileDirectory = p.root + '/'
        
        #starts the loop that reads in the client header HTTP request#
        while True:
            #take in the first byte string from the HTTP request
            argsSep += self.client.recv(4096)

            #splits the HTTP request into tokens for easier reading
            args = argsSep.split()

            #This if statement makes sure that the first word is GET and that HTTP/1.(1/0) is the protocol used
            if args[0] == b'GET' and (b'HTTP/1.1' in args or b'HTTP/1.0' in args):

                #This statement runs if no file is specified or / is typed into for the filename
                if args[1][:-1] == b'HTTP/1.' or args[1] == b'/':

                    #if the index.html is there, open it
                    if os.path.exists(fileDirectory + 'index.html'):
                        fileRead = open(fileDirectory + 'index.html', "rb")
                        flag200 = True

                    #if index.html doesn't exist, try to open index.txt
                    elif os.path.exists(fileDirectory + 'index.txt'):
                        fileRead = open(fileDirectory + 'index.html', "rb")
                        flag200 = True

                    #if both index files don't exist, send a 404 error
                    else:
                        flag404 = True
                
                #if a file is specified, run this code
                elif args[2][:-1] == b'HTTP/1.':

                    #check if the file exists
                    if os.path.exists(fileDirectory + args[1].decode()):

                        #Check of the file extension is supported
                        if args[1].decode().endswith('.html') or args[1].decode().endswith('.png') or args[1].decode().endswith('.txt'): 
                            
                            #if the file extension is supported, check if the user has permissions
                            if os.access(fileDirectory + args[1].decode(), os.R_OK):
                                
                                #if the user has permissions, open the file
                                fileRead = open(fileDirectory + args[1].decode(), "rb")
                                flag200 = True
                            else:
                                flag403 = True
                        else:
                            flag400 = True
                    else:
                        flag404 = True
                else:
                    flag400 = True                
            else:
                flag400 = True
            
            #if the carriage return is read, break out of the loop to and send a response
            if "\r\n\r\n".encode('UTF-8') in argsSep:
                break        
        
        #if the 200 flag was set
        if flag200:
            
            #if the file is HTML or .txt, send respone + content type
            if fileRead.name.endswith('.html') or fileRead.name.endswith('.txt'):
                self.client.send(b'HTTP/1.1 200 OK \r\nContent-Type: text/html \r\n\r\n')
                self.client.sendall(fileRead.read())
                
            #if the file is png, send respone + content type
            elif fileRead.name.endswith('.png'):
                self.client.send(b'HTTP/1.1 200 OK \r\nContent-Type: png \r\n\r\n')
                self.client.sendall(fileRead.read())

        #if the 404 flag was set, send the 404 html response
        elif flag404:
            self.client.send(b'HTTP/1.1 404 Not Found \r\nContent-Type: text/html \r\n\r\n')
            self.client.sendall(open('www/errors/404.html', "rb").read())

        #if the 400 flag was set, send the 400 html response
        elif flag400:
            self.client.send(b'HTTP/1.1 400 Bad Request \r\nContent-Type: text/html \r\n\r\n')
            self.client.sendall(open('www/errors/400.html', "rb").read())

        #if the 403 flag was set, send the 403 html response 
        elif flag403:
            self.client.send(b'HTTP/1.1 403 Forbidden \r\nContent-Type: text/html \r\n\r\n')
            self.client.sendall(open('www/errors/403.html', "rb").read())
            
        #when the HTTP request/response is over, close the connection
        self.client.close()


"""initializes the connection variable to a socket"""
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""sets the socket options for the connection variable"""
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""binds the connection socket to any IP address and port 47692"""
connection.bind(('0.0.0.0', 47692))

"""allows the connection to accept 10 users"""
connection.listen(10)
    


"""infinite while loop"""
while True:

    """stores two peices of data, the address of the devices in address and the socket info in client"""
    client, address = connection.accept()

    """thread handler object"""
    th = HandlerThread(client, address)
    th.start()
        
    

    
