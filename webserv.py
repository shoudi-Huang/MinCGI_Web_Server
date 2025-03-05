import socket, sys, os

# Function check configuration file and generate variable
def check_config():
    # Open Configuration file
    try:
        f = open(config_filename, "r")
    except Exception as e:
        print('Unable To Load Configuration File')
        exit()

    i = 0
    while True:
        l = f.readline()
        
        if l == "":
            break

        line = l.strip().split('=')
        key = line[0]
        # Check config syntax
        if len(line) != 2:
            return False
            
        if i == 0 and key == "staticfiles":
            static_file_path = line[1]
        elif i == 1 and key == "cgibin":
            cgibin_path = line[1]
        elif i == 2 and key == "port":
            if line[1].isdigit() == True:
                PORT = int(line[1])
            else:
                return False
        elif i == 3 and key == "exec":
            execute_path = line[1]
        else:
            return False

        i +=1

    # Check all variable appear
    if i!=4:
        return False
    
    config_variable_ls = [static_file_path, cgibin_path, PORT, execute_path]
    # Return generated variables
    return config_variable_ls

# Function generate file name and variable from request
def generate_variable_from_request(request_data):
    suitable_variable_ls = [
        "Host",
        "Accept",
        "User-Agent",
        "Accept-Encoding",
        "Content-Type",
        "Content-Length"]
    
    request_ls = request_data.strip().split("\n")

    i = 0
    postMethod_body = False
    while i<len(request_ls):
        if i == 0:
            # Generate file name, request method, URI and query string from first line
            request_method = request_ls[0].split(" ")[0]
            http_uri_path = request_ls[0].split(" ")[1]
            os.environ['REQUEST_METHOD'] = request_method + '\n'
            os.environ['REQUEST_URI'] = http_uri_path + '\n'

            filename_and_query_string = request_ls[0].split(" ")[1].split("?")
            filename = filename_and_query_string[0]

            if len(filename_and_query_string)>1:
                os.environ['QUERY_STRING'] = filename_and_query_string[1] + '\n'

        else:
            # Determination of post request body
            if os.getenv('REQUEST_METHOD') == "POST" and request_ls[i] == "":
                i += 1
                postMethod_body = True
                continue

            if postMethod_body:
                pass
            else:   # Generate environment variable
                variable = request_ls[i].split(': ')
                variable_name = variable[0]
                variable_value = variable[1]

                for suitable_variable in suitable_variable_ls:
                    if variable_name == suitable_variable:
                        if suitable_variable == "Content-Type" or suitable_variable == "Content-Length":
                            full_name = variable_name.upper()
                        else:
                            full_name = "HTTP_" + variable_name.upper()
                        
                        os.environ[full_name] = variable_value + '\n'
                        break
        
        i += 1
    
    return filename
            
# Function generate content type for static file
def generate_content_type(file_extension):
    file_extension_ls = ["txt", "html", "js", "css", "png", "jpg", "jpeg", "xml"]
    type_mapping_ls = [
        "text/plain",
        "text/html",
        "application/javascript",
        "text/css",
        "image/png",
        "image/jpeg",
        "image/jpeg",
        "text/xml"]

    unknown_file_extension = True
    i = 0
    while i<len(file_extension_ls):
        # Generate content type base on file extension
        if file_extension == file_extension_ls[i]:
            http_response = "Content-Type: " + type_mapping_ls[i] + "\n"*2
            unknown_file_extension = False
            break
        i += 1

    if unknown_file_extension:      # File with undefined extension
        return False
    else:
        return http_response


# ~ MAIN PROCESS ~
try:
    # Get Configuration File path
    config_filename = sys.argv[1]
except IndexError:
    print('Missing Configuration Argument')
    exit()

# Check Configuration File
check_config_result = check_config()
if check_config_result == False:
    print('Missing Field From Configuration File')
    exit()
else:
    # Generate variables from configuration file
    static_file_path = check_config_result[0]
    cgibin_path = check_config_result[1]
    PORT = check_config_result[2]
    execute_path = check_config_result[3]


# Socket set up
HOST = '127.0.0.1'
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

while True:
    # Wait for connection
    client_connection, client_address = listen_socket.accept()
    # Get client adr and port
    remote_addr = client_address[0]
    remote_port = client_address[1]
    os.environ['REMOTE_ADDRESS'] = str(remote_addr) + '\n'
    os.environ['REMOTE_PORT'] = str(remote_port) + '\n'

    # Get server adr and port
    server_addr = listen_socket.getsockname()[0]
    server_port = listen_socket.getsockname()[1]
    os.environ['SERVER_ADDR'] = str(server_addr) + '\n'
    os.environ['SERVER_PORT'] = str(server_port) + '\n'

    # Receive request
    request_data = client_connection.recv(4096).decode()

    # Generate file name and suitable environment variable
    filename = generate_variable_from_request(request_data)

    if filename == "/":     # Simulate index file
        filename = "/index.html"

    execute_file = False
    if len(filename.split("/")) > 2 and filename.split("/")[1] == "cgibin": # Determination of cgi file
        filename = "/" + filename.split("/")[2]
        execute_file = True

    file_not_found = False
    exec_error = False
    if execute_file:    # For cgi file

        read, write = os.pipe() 
        pid = os.fork()
        # In child process
        if pid == 0:
            os.close(read)
            # Execute cgi file and redirect stdout to variable 'response'
            if execute_path == '':
                response = os.popen('bash ' + cgibin_path + filename).read()
            else:
                response = os.popen(execute_path + ' '+ cgibin_path + filename).read()
            
            # Determination of cgi file execution though exit status of cgi file
            exit_status = os.wait()[1]
            if exit_status != 0:
                exit(1)

            # Write stdout to 'write' in pipe
            write = os.fdopen(write,'w') 
            write.write(response)
            write.close()
            exit(0) 
        
        # In parent process
        else: 
            # Determination of cgi file execution though exit status of child process.
            exit_status = os.wait()[1]
            
            if exit_status != 0:    # Error appear in cgi file execution.
                http_response = ('HTTP/1.1 500 Internal Server Error\n')
                exec_error = True

            else:
                os.close(write) 
                # Read stdout of cgi file in 'read' of pipe
                read = os.fdopen(read, 'r') 
                response = read.read()

                temp = ""
                for line in response.split("\n"): 
                    if "Content-Type" == line.split(':')[0]:    # Custom content type
                        os.environ["Content-Type"] = line + "\n"
                        
                    elif "Status-Code" == line.split(':')[0]:   # Custom status code
                        os.environ["Status-Code"] = line.split(':')[1] + "\n"
                    else:
                        if line != "":
                            temp += line + '\n'
                # Set stdout of cgi file as content of the http response
                content = temp.encode()
                read.close()
            

    else:   # For static file
        try:
            # Open static file and set the content of the file as 
            # the content of http response.
            f = open(static_file_path + filename, "rb")
            content = f.read()
            f.close()
        except FileNotFoundError:
            file_not_found = True


    if not execute_file:
        file_extension = filename.split(".")[-1]
        content_type = generate_content_type(file_extension)

    if file_not_found:  # For static file not found 
        # Simulate http response's header and content
        http_response = ('HTTP/1.1 404 File not found\n')
        http_response += ('Content-Type: text/html\n\n')

        content = b"""<html>
<head>
\t<title>404 Not Found</title>
</head>
<body bgcolor="white">
<center>
\t<h1>404 Not Found</h1>
</center>
</body>
</html>
"""

    else:   # For cgi or founded static file
        if exec_error == False: # No error during cgi file excution

            if os.getenv('Status-Code') != None:    # Custom status code
                status_code = os.getenv('Status-Code')
                http_response = 'HTTP/1.1' + status_code
            else:   # Default status code
                http_response = 'HTTP/1.1 200 OK\n'
            
            if os.getenv('Content-Type') != None:   # Custom content type
                http_response += os.getenv('Content-Type') + '\n'
            elif execute_file == False:
                if content_type != False:   # Simulate content type for static file
                    http_response += content_type
                else:
                    http_response += '\n'
            else:   # Content type not defined
                http_response += '\n'
    

    # Send http response
    http_response = http_response.encode()
    client_connection.send(http_response)
    if exec_error == False:
        client_connection.send(content)
    
    # Close connection
    client_connection.close()