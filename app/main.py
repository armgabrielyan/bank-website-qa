import uvicorn

from app.settings import HOST, LOG_LEVEL, PORT, RELOAD

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level=LOG_LEVEL,
        http="httptools",
    )
