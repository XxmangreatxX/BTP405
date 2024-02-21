# **Activity 3** #

To try this note-taking application, You have to try all the given endpoints which are GET, POST, PUT, and DELETE requests:

1. First you have to clone my repository in VS code.
2. Then you have to have docker installed in your computer to build an image and use a container.
3. Now we have to open 2 git bash terminals.
4. Next you have to run this code to build the note-taking app:
   **docker run --name restfulapi -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=notes -d mysql:latest**
5. Now we have to run the server.py using **python server.py** in one of the git bash terminals. When it is running we can use the other terminal to try all the functions:
* To try GET: **curl -X GET http://localhost:8000/notes**

* To try POST:**curl -X POST http://localhost:8000/notes -H "Content-Type: application/json" -d "{\"title\": \"New Note\", \"content\": \"This is a new note.\"}"**

* To try PUT:**curl -X PUT http://localhost:8000/notes/1 -H "Content-Type: application/json" -d "{\"title\": \"Updated Note\", \"content\": \"This note has been updated.\"}"**

* To try DELETE:**curl -X DELETE http://localhost:8000/notes/1**

1 refers to the ID
