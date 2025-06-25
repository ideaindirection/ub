"""Example usage of server_utils for different types of servers.

This demonstrates how to use the port conflict handling utilities
with various server frameworks.
"""


# Example 1: FastAPI/Uvicorn (like your PromptPulse)
def example_fastapi():
    from fastapi import FastAPI
    from seb_thor_priv.server_utils import start_uvicorn_with_port_handling

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    # This will handle port conflicts automatically
    start_uvicorn_with_port_handling(
        app, host="0.0.0.0", port=8000, reload=True  # For development
    )


# Example 2: Flask
def example_flask():
    from flask import Flask
    from seb_thor_priv.server_utils import start_flask_with_port_handling

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    # This will handle port conflicts automatically
    start_flask_with_port_handling(app, host="0.0.0.0", port=5000, debug=True)


# Example 3: Generic server with custom handler
def example_generic_server():
    from seb_thor_priv.server_utils import start_server_with_port_handling
    import http.server
    import socketserver

    def start_http_server(host="0.0.0.0", port=8080):
        """Simple HTTP server function."""
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((host, port), Handler) as httpd:
            print(f"Serving at http://{host}:{port}")
            httpd.serve_forever()

    # Use the generic handler
    start_server_with_port_handling(
        start_http_server, host="0.0.0.0", port=8080, service_name="Simple HTTP Server"
    )


# Example 4: Manual port conflict handling
def example_manual_handling():
    from seb_thor_priv.server_utils import handle_port_conflict
    import uvicorn

    # Your app setup code here
    from fastapi import FastAPI

    app = FastAPI()

    # Handle port conflicts manually
    desired_port = 8000
    final_port = handle_port_conflict("0.0.0.0", desired_port, "My Custom API")

    print(f"Starting server on port {final_port}")
    uvicorn.run(app, host="0.0.0.0", port=final_port)


# Example 5: Quick port availability check
def example_port_check():
    from seb_thor_priv.server_utils import (
        check_port_available,
        get_processes_using_port,
        find_available_port,
    )

    port = 8000

    if check_port_available("localhost", port):
        print(f"Port {port} is available!")
    else:
        print(f"Port {port} is in use.")
        processes = get_processes_using_port(port)
        for proc in processes:
            print(f"  Process: {proc['name']} (PID: {proc['pid']})")

        # Find an alternative
        alt_port = find_available_port(port + 1)
        print(f"Alternative port: {alt_port}")


if __name__ == "__main__":
    # Run one of the examples
    print("Running port availability check example...")
    example_port_check()
