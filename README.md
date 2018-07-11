Tyler Murray (811520280)

The goal of this project is to implement a simple HTTP server. The HTTP server parses through the GET line of the request sent
to it and returns the file specified by the client. If no argument is placed for a file in the GET request line or a '/' is
placed, it will default to the 'index.html' file. This server supports only html, text and png files. 


Instructions on how to start virtual environment:

	     Type: $ source bin/activate


Intructions on how to run the program:

	    Type: $python3 web_server.py [--root path]

	    [--root path] will change the root directory from 'www' to whatever is specified in the path argument

Other instructions:

            In a seperate terminal window, after running web_server.py, use the telnet, firefox or lynx to access the server.

	    Type: telnet [ip/cluster name] 47692

	    	  firefox & (in search bar: http://[ip/cluster]:47692/filename)

		  lynx http://[ip/cluster]:47692/filename




		