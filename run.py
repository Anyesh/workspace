import argh

from workspace import app

if __name__ == "__main__":
    try:
        argh.dispatch_command(app)
    except KeyboardInterrupt:
        print("See ya!")
