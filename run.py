"""Run the server in development mode."""
from relately.server import app

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(
        host='0.0.0.0',
        port=8006,
        debug=True
    )
