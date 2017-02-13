############################
# Author: Piyush Zode      #
# ID: XXXXXXXXXX           #
############################

import socket, errno
import sys
from thread import *

# Function for Defining the Usage of the program
def print_usage():
    print "\n-----------------------------"
    print "\tUsage"
    print "-----------------------------"
    print "server_code_name <port_number>"
    print "-----------------------------\n"

# Function for fulfilling the client request
def clientthread(connection,port_number):
    # Infinite loop so that function does not terminate and thread do not end.
    while True:
        try:
            # Receiving from client
            data = connection.recv(port_number)
            # Decode the data to String 
            decoded_data = bytes.decode(data)
            print("Request body: ",decoded_data)

            if(decoded_data.split(' ')[0] == 'GET'):    # Accept GET methods
                entire_link = decoded_data.split(' ')[1]
                filename = entire_link.split('?')[0]
                
                if(filename == '/'):
                    filename = '/index.html'    #default case if the filename is not listed properly

                print 'Web Page requested is: ',filename
                file_content=''
                try:
                    fp = open(filename[1:],'rb')    
                    file_content = fp.read()    # Read the file contents
                    fp.close()
                    response_header = '\HTTP/1.1 200 OK'
                except Exception as err_msg: # if error while opening the file
                    print("HTTP/1.1 404 Requested File Not Found.",err_msg)
                    response_header = '\HTTP/1.1 404 Not Found'
                    # convert to byte stream instead of string
                    file_content = b"<html><body><p><h1>Message from Server:</h1><br><br><p><h5>Error 404: File "+filename+" Not Found</p></h5>"
                    
                server_response_message = response_header.encode()
                server_response_message += '---------------------------'
                server_response_message += file_content

                print "\nSending data back to the client:",server_response_message
                # Send contents to the client
                for i in range(0, len(file_content)):
                    connection.send(file_content[i])

                connection.close() # As we need to close the connection after the request has been responded back
                print "Connection closed with client"
            else:   # If unknown method in HTTP request    
                print("HTTP/1.1 400 Bad Request : Unknown Method in HTTP Request : ",decoded_data.split(' ')[0])
                content = b"<html><body><p><h1>Message from Server:</h1><br><br><p><h5>HTTP/1.1 400 Bad Request: Unknown Method "+decoded_data.split(' ')[0]+" in HTTP Request</p></h5>"
                
                response_header = '\HTTP/1.1 400 Bad Request'
                server_response_message = response_header.encode()
                server_response_message += '\n---------------------'
                server_response_message += content
                print "\nSending data back to the client:",server_response_message

                for i in range(0, len(content)):
                    connection.send(content[i])
                connection.close() 
        except socket.timeout,err:  # If there is a timeout
            if(err.args[0] == "timed out"):
                print "Connection timed out! Retry"
                continue    # to continue the loop
        except socket.error,err_msg: # When the non blocking process tries to get the data immediately
            err=err_msg.args[0]
            pass                    
            if err == errno.EWOULDBLOCK or err == errno.EAGAIN:                       
                continue
            

def start_server(host,port_number):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # Reuse the same socket
    print 'Server Socket created'

    #Bind socket to localhost and port
    try:
        sck.bind(('',port_number))
    except sck.error as err_msg:
        print 'Bind failed. Error Code : ' + str(err_msg[0]) + ' Message ' + err_msg[1]
        sys.exit()
    print 'Bind Complete(Socket to localhost and port)'

    # Set the server Timeout(seconds) and the number should be in float
    sck.settimeout(15.0)
    print 'Server Port number is ',port_number

    while True:
        try:
            # Establish the connection
            print 'Ready to serve...'
            # Wait to accept a connection
            sck.listen(1) # Maximum number of queued connections 
            print 'Socket accepting new connections'
            connection, address = sck.accept()   # address -> Client's Address, Connection -> Socket connection to client

            print 'New Connection from ',address
            # Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread ,(connection,port_number))
        except socket.timeout,err:
            if(err.args[0] == "timed out"):
                print "Connection timed out! Retry"
                continue    # to continue the loop
        except socket.error,err_msg: # When the non blocking process tries to get the data immediately
            err=err_msg.args[0]
            pass                    
            if err == errno.EWOULDBLOCK or err == errno.EAGAIN:                       
                continue
    sck.close()


def main(argv):
    if(len(argv) == 2):
        host = ''   # Symbolic name meaning all available interfaces
        port_number = argv[1]
        #print socket.__file__
        start_server(host,int(port_number))
    else:
        print_usage()
        sys.exit()

# Run the main function when the code runs
if __name__ == "__main__":
    main(sys.argv)