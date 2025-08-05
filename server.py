from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import sys
import os

# Add the hello-world package to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'hello-world'))

try:
    # Import from hello-world directory
    import main as hello_world_main
    has_hello_world = True
except ImportError:
    has_hello_world = False

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Hello from uv on DigitalOcean!",
                "uv_version": "0.7.10",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "hello_world_available": has_hello_world
            }
            
            if has_hello_world:
                try:
                    # Run the hello-world script and capture output
                    import subprocess
                    result = subprocess.run(['uv', 'run', 'hello-world/main.py'], 
                                          capture_output=True, text=True, cwd='.')
                    response["hello_world_message"] = result.stdout.strip()
                except Exception as e:
                    response["hello_world_error"] = str(e)
            
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"Server starting on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    main()
