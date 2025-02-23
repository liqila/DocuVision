import uvicorn
from api.app import app
from config.settings import API_HOST, API_PORT

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT) 