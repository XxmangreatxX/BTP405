from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mysql.connector

def create_db_connection():
    # Creates and returns a connection to the database.
    return mysql.connector.connect(
        host="localhost",  # Database host
        user="root",       # Database user
        password="password",  # Database password
        database="notes"   # Database name
    )

def execute_query(query, params=None, fetch=False):
    # Executes a given SQL query with optional parameters. Can fetch results.
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    if fetch:
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    else:
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        connection.close()
        return affected_rows

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def respond(self, status=200, content=None):
        # Sends a HTTP response with an optional JSON content.
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if content is not None:
            self.wfile.write(json.dumps(content).encode())

    def do_GET(self):
        # Handles GET requests: Fetches and returns all notes.
        notes = execute_query("SELECT * FROM notes", fetch=True)
        self.respond(200, notes)

    def do_POST(self):
        # Handles POST requests: Creates a new note with provided title and content.
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        query = "INSERT INTO notes (title, content) VALUES (%s, %s)"
        affected_rows = execute_query(query, (post_data['title'], post_data['content']))
        
        if affected_rows:
            self.respond(201, {"message": "Note created successfully."})
        else:
            self.respond(500, {"message": "Failed to create note."})

    def do_PUT(self):
        # Handles PUT requests: Updates an existing note by id.
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        note_id = self.path.strip("/").split("/")[-1]

        query = "UPDATE notes SET title = %s, content = %s WHERE id = %s"
        affected_rows = execute_query(query, (post_data['title'], post_data['content'], note_id))
        
        if affected_rows:
            self.respond(200, {"message": "Note updated successfully."})
        else:
            self.respond(404, {"message": "Note not found."})

    def do_DELETE(self):
        # Handles DELETE requests: Deletes an existing note by id.
        note_id = self.path.strip("/").split("/")[-1]

        query = "DELETE FROM notes WHERE id = %s"
        affected_rows = execute_query(query, (note_id,))
        
        if affected_rows:
            self.respond(200, {"message": "Note deleted successfully."})
        else:
            self.respond(404, {"message": "Note not found."})

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    # Runs the server.
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()