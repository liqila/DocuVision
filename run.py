import uvicorn
from api.app import app
from config.settings import API_HOST, API_PORT, ENV

if __name__ == "__main__" and ENV == 'development':
    uvicorn.run(app, host=API_HOST, port=API_PORT) 