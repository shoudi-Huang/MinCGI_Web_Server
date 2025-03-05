# MinCGI Web Server

## Project Overview
**MinCGI Web Server** is a lightweight web server designed to handle multiple connections and execute applications compliant with a subset of the Common Gateway Interface (CGI) specification. The server processes HTTP requests, retrieves necessary headers, and passes data to CGI programs via environment variables and standard input. It supports serving static files and executing CGI scripts, with proper content-type mapping and HTTP response handling. The server reads configuration files to determine static file directories, CGI-bin paths, and listening ports. Key features include handling GET requests, returning appropriate status codes (200, 404, 500), and supporting asynchronous connections. The project includes extensions such as handling POST requests or implementing compression.
## Features
- **HTTP/1.1 Compliance**: The server adheres to the HTTP/1.1 protocol, handling GET requests and returning appropriate status codes.
- **Static File Serving**: The server can serve static files from a specified directory, with proper content-type mapping based on file extensions.
- **CGI Program Execution**: The server can execute CGI programs, passing request data via environment variables and standard input.
- **Configuration File Support**: The server reads a configuration file to determine static file directories, CGI-bin paths, and listening ports.
- **Error Handling**: The server returns appropriate error responses (404 for missing files, 500 for CGI program failures).
- **Asynchronous Connections**: The server supports asynchronous handling of connections by forking each accepted connection.

## Technical Details
- **Programming Language**: Python 3
- **File Structure**:
  - `webserv.py`: The main web server script.
  - `config.cfg`: Configuration file specifying static file directory, CGI-bin directory, port, and executable path.
  - `staticfiles/`: Directory containing static files (e.g., HTML, CSS, JS, images).
  - `cgibin/`: Directory containing CGI programs.

## How to Run
1. Start the Server:
   ```bash
   python3 webserv.py config.cfg
2. Access the Server:
   Open a web browser and navigate to http://localhost:8070/ to access the server.

## Acknowledgments
This project was developed as part of the INFO1112 course, focusing on building a minimal CGI-compliant web server.
