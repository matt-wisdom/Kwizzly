import dotenv
import uvicorn
from core.config import config

dotenv.load_dotenv(dotenv.find_dotenv())

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )
