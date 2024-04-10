from src.app import app

application = app

if __name__ == "__main__":
    application.run(port = 5000, debug = True)