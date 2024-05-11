# File Store

This project implements a simple file store service with HTTP server and a command-line client for storing, updating, deleting files, and performing operations on files stored in the server.

## Server

The server is implemented in Python using Flask framework. It handles HTTP requests from clients and performs operations on files stored in the server.

### Endpoints

- **/add:** POST request to add files to the store.
- **/ls:** GET request to list files in the store.
- **/rm/<filename>:** DELETE request to remove a file from the store.
- **/update/<filename>:** PUT request to update contents of a file in the store.
- **/wc:** GET request to get the word count of all files stored in the server.
- **/freq-words:** GET request to get the most frequent words in the files stored in the server.

## Client

The client is implemented in Python and provides a command-line interface for interacting with the server.

### Program Files

- **file_store/server/file_store_server.py:** Implements the Flask server and defines endpoints for handling client requests.
- **file_store/server/file_operations.py:** Contains functions for file operations such as adding, listing, removing, updating files, word count, and frequency analysis.
- **file_store/client/file_store_client.py:** Implements the command-line client for sending requests to the server.
- **file_store/README.md:** Documentation for the project.

## Sending Requests with Postman

You can use Postman, a popular API development tool, to send HTTP requests to the server endpoints.

1. Open Postman.
2. Set the request method (POST, GET, DELETE, PUT) and enter the URL for the desired endpoint.
3. For POST and PUT requests, make sure to include the file(s) in the request body if required.
4. Send the request and view the response from the server.

For example:

- To add files to the store, send a POST request to `http://localhost:5000/add` with files attached in the body.
- To list files in the store, send a GET request to `http://localhost:5000/ls`.
- To remove a file, send a DELETE request to `http://localhost:5000/rm/<filename>`.
- To update a file, send a PUT request to `http://localhost:5000/update/<filename>` with the updated file attached in the body.
- To get the word count of files, send a GET request to `http://localhost:5000/wc`.
- To get the most frequent words, send a GET request to `http://localhost:5000/freq-words`.

## Server Docker Image

A Docker image for the server has been created with the following details:

- Image name: `rajasur90/filestore-server:v1`
- Command to pull the image: `docker pull rajasur90/filestore-server:v1`

You can run the server locally using the following command:

```bash
docker run -d -p 5002:5002 rajasur90/filestore-server:v1
```
