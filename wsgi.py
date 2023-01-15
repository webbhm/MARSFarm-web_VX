# Entry point for gunicorn to run Flask

from app import app

if __name__ == "__main__":
    app.run()