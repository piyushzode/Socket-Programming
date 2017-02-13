############################
# Author: Piyush Zode      #
# ID: ##########           #
############################

import socket
import sys
import time
import getopt

# Function for Defining the Usage of the program
def print_usage():
    print "\n-----------------------------"
    print "\tUsage"
    print "-----------------------------"
    print "client_code -i ip_address [-p port_number] [-f filename] [-m method]"
    print "-----------------------------\n"


# Function for send and receive the requests from the server
def make_client_request(ip_address,port_number,filename,method):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print "Host Name of Server : ",ip_address
    print "Socket Family is : AF_INET"
    print "Socket Type is : SOCK_STREAM"
    print "Protocol Used : IPPROTO_TCP"

    # Connect to server socket with the given IP address and Port Number
    # Connect takes only 1 parameter which is the combination of IP Address and Port number
    server_connection_address = (ip_address, int(port_number))
    sck.connect(server_connection_address)

    try:        
        # Make the request message headers
        headers = """HTTP/1.1\r
            Content-Type: {content_type}\r
            Content-Length: {content_length}\r
            Host: {host}\r
            Connection: close\r
            \r\n"""

        header_bytes = headers.format(
            content_type="application/x-www-form-urlencoded",
            content_length=len(filename),
            host=str(ip_address) + ":" + str(port_number)
            ).encode('iso-8859-1')


        main_message = " $:"+method+' /'+filename+' '+header_bytes
        print("Sending request to Server : ",main_message.split('$:')[1])

        # For RTT we need to calculate the time when we send the request and receive the response
        sending_time = time.time()

        sck.sendall(main_message)

        # Look for the response
        data = sck.recv(800)
        received_time = time.time()

        rtt_time = received_time - sending_time     # Calculate the RTT
        
        print >>sys.stderr, '\nReceived (From Server): "%s"' % data
        print "\n\nRTT[Round Trip Time] : "+str(rtt_time)+" seconds"

        response_code_from_server = data.split(' ')[1]
        if(response_code_from_server == '200'): # OK received from server
            # Code for downloading the file to the downloads folder
            downloaded_file_name = 'downloaded_'+filename.split('?')[0]
            fp = open(downloaded_file_name,"wb")
            fp.write(data.split('---------------------')[1])
            fp.close
            print "\n\nFile Downloaded successfully!"
        

    finally:
        sck.close()
        print "\n\nSocket Closed"


def main(argv):
    try:
        opts, arguments = getopt.getopt(argv[1:],"i:p:f:m:")
    except getopt.GetoptError:
        print_usage()
        sys.exit()
    
    # Giving default values to the parameters
    filename = "index.html"
    method="GET"
    ip_address = None
    port_number = 8080

    for opt, values in opts:
        if(opt == "-i"):
            ip_address = values
            print "IP Address is: ", ip_address
        elif(opt == "-p"):
            port_number = values
            print "Port Number is: ", port_number
        elif(opt == "-f"):
            filename = values
            print "File Name is: ", filename
        elif(opt == "-m"):
            method = values
            print "Method is: ", method
        
    if(ip_address):
        make_client_request(ip_address,int(port_number),filename,method)
    else:
        print_usage()
        sys.exit()


if __name__ == "__main__":
    main(sys.argv)