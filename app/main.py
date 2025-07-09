from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import vectorstore_operation
from app.api.v1.endpoints import chat
from app.core.config import Variable

app = FastAPI(
    title="Reassurance Bot API",
    version="v1.0",
)

app.include_router(
    vectorstore_operation.router,
    prefix="/vs",
    responses={"404": {"description":"Not Found"}}
)

app.include_router(
    chat.router,
    prefix="/chat",
    responses={"404": {"description":"Not Found"}}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Variable.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service Status</title>
        <style>
            body {
                background-color: #121212;
                color: #E0F7FA;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            .status-container {
                padding: 2rem;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.05);
            }
            h1 {
                color: #A5D6A7;
                margin-bottom: 0.5rem;
            }
            .status {
                font-size: 1.5rem;
                font-weight: bold;
                color: #CE93D8;
            }
        </style>
    </head>
    <body>
        <div class="status-container">
            <h1>Service Status</h1>
            <p class="status">All systems operational</p>
            <p>Last checked: <span id="timestamp"></span></p>
            <p><a href="/docs" style="color:#81D4FA;text-decoration:underline;">API Documentation</a></p>
        </div>

        <script>
            document.getElementById('timestamp').textContent = new Date().toLocaleString();
        </script>
    </body>
    </html>
    """