"""
Entry point — run with: python -m app.main
"""

import uvicorn
from app.config import HOST, PORT


def main():
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
