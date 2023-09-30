# Networking Programming Report A.Y. 2022
## Task #2
Development of a client-server application for file transfer using the connectionless network service (UDP).
**Software Objectives**:
- Client-server connection without authentication.
- Displaying available files on the server at the client.
- Downloading a file from the server.
- Uploading files to the server.

##### Communication Protocol Specifications
The protocol should include the exchange of two types of messages:
- **Command Messages**:
  - Sent from the client to the server
  - Request for executing various operations
- **Response Messages**:
  - Sent from the server to the client
  - Response to a command with the outcome of the operation

### Server Functionality
- Sending a response message to the **list** command to the requesting client (+ multiple clients simultaneously).
- Response message containing the *file list*.
- Sending a response message to the **get** command containing the requested file, if available, or an appropriate error message.
- Receiving a **put** message containing the file to be uploaded to the server and sending the corresponding response message (result).

### Client Functionality
- Sending the **list** message to request the list of available file names.
- Sending the **get** message to retrieve a file.
- Receiving a requested file through the get message or handling any errors.
- Sending the **put** message to perform the upload of a file to the server.
