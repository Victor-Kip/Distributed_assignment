from flask import Flask, jsonify
import os

# --- Configuration Constants ---
# Environment variable name for the server ID
SERVER_ID_ENV_VAR = "SERVER_ID"
# Default value for the server ID if the environment variable is not set
DEFAULT_SERVER_ID = "unknown"
# Default port for the Flask application
DEFAULT_PORT = 5000
# Default host for the Flask application (0.0.0.0 makes it accessible externally)
DEFAULT_HOST = "0.0.0.0"

def create_app():
    """
    Creates and configures the Flask application instance.

    This function encapsulates the app initialization and route registration,
    making the application more modular and easier to test or extend.
    """
    app = Flask(__name__)

    # Retrieve the server ID from environment variables, using a default if not found.
    server_id = os.getenv(SERVER_ID_ENV_VAR, DEFAULT_SERVER_ID)

    @app.route('/home', methods=["GET"])
    def home():
        """
        Handles GET requests to the /home endpoint.
        Returns a JSON response with a welcome message and server status.
        """
        return jsonify({
            "message": f"hello from server {server_id}",
            "status": "successful"
        }), 200

    @app.route("/heartbeat", methods=["GET"])
    def heartbeat():
        """
        Handles GET requests to the /heartbeat endpoint.
        Used for health checks to confirm the server is operational.
        Returns an empty response with a 200 OK status.
        """
        return "", 200

    return app

if __name__ == "__main__":
    # Create the Flask application instance
    app = create_app()
    # Run the application, making it accessible on the specified host and port.
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
