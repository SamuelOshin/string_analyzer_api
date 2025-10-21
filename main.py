from app.main import app
from app.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info",
        access_log=True
    )
