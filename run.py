from app import app
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    app.run(host=app.config["HOST"], port=5000)
