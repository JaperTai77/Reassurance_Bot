# Reassurance Bot

Reassurance Bot is a web application designed to foster comfortable and encouraging conversations through a chatbot interface. In addition to the chatbot, the app provides a separate tab for users to view and search stored phrases, offering inspiration and support.

## Features

- **Chatbot Tab**: Engage in supportive, comforting conversations with an AI-powered chatbot.
- **Phrase Tab**: Search and browse stored encouraging phrases.
- **Separation of Backend and Frontend**: FastAPI backend (Python) and static frontend (HTML/JS/CSS).

## Demo Deployment

The app is deployed for demonstration at: [https://jasper177reassuranceweb-318ab640f7f9.herokuapp.com](https://jasper177reassuranceweb-318ab640f7f9.herokuapp.com)


## File Structure

```
.
├── app/                    # Backend (FastAPI)
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── chat.py
│   │           └── vectorstore_operation.py
│   │       └── repositories/
│   │           ├── chat.py
│   │           └── vectorstore_operation.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── models/
│       └── chat.py
├── static/                 # Frontend (Static Web)
│   ├── config.js           # Frontend config (set backend API URL here)
│   ├── index.html          # Main web page
│   ├── scripts.js          # Frontend logic
│   └── styles.css          # Styling
├── .env.sample             # Sample environment variables for backend
├── Dockerfile              # Dockerfile (API only)
├── docker-compose.yml      # Docker Compose (API only)
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .python-version
└── README.md
```

## Getting Started

### 1. Backend (API)

The backend is a FastAPI application located in the `app/` directory.

#### **Set up Openai api and MongoDB vector store**

1. Vector Store Setup in MongoDB

- For setting up the vector store in MongoDB, please refer to the official MongoDB Atlas Vector Search quick start guide:  
  https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/vector-search-quick-start/

2.  OpenAI API Key Setup

- To set up your OpenAI API key for the application, follow the OpenAI platform quickstart guide for chat API mode:  
https://platform.openai.com/docs/quickstart?api-mode=chat

#### **Run with Python (Option 1)**

1. Install dependencies (recommended: use a virtual environment):

    ```bash
    pip install -r requirements.txt
    # or if using poetry:
    poetry install
    # or if using uv
    uv sync
    ```

2. Copy the sample environment file and edit as needed:

    ```bash
    cp .env.sample .env
    # Edit .env with your preferred settings
    ```

3. Start the API server (default port: **8000**):

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

#### **Run with Docker (Option 2)**

1. Copy the sample environment file and edit as needed:

    ```bash
    cp .env.sample .env
    # Edit .env with your preferred settings

2. Launch with Docker.
    ```bash
    docker-compose up
    ```

The API will be available at: [http://localhost:8000](http://localhost:8000)

---

### 2. Frontend (Static Web)

The frontend is a static web app located in the `static/` directory.

#### **Configuring Backend API Endpoint**

Before deploying, **edit `static/config.js`** to set the correct backend API URL:

```js
window.BACKEND_ORIGIN = "http://localhost:8000";
```

Change the value as needed for your deployment environment.

#### **Development**

You can serve the frontend using any static file server. For example, using Python's built-in server:

```bash
cd static
python3 -m http.server 9000
```

The frontend will be available at: [http://localhost:9000](http://localhost:9000)

## API Endpoints

### Chat Endpoints (`/chat`)

- **GET `/chat/getratedresponse`**
  - **Query Parameter:** `text` (string) — Input text for which to get a rated reassurance response.
  - **Description:** Returns a rated reassurance response for the provided input.

- **GET `/chat/gettopresponse`**
  - **Query Parameter:** `text` (string) — Input text for which to get a revised response.
  - **Description:** Returns a random message and a revised response for the provided input.

### Phrase/Vectorstore Endpoints (`/vs`)

- **POST `/vs/createindex`**
  - **Description:** Creates an index in the vector store (database).

- **POST `/vs/adddocuments`**
  - **Query Parameters:** 
    - `text` (string) — The phrase or document to add.
    - `metadata` (string) — Metadata associated with the document.
  - **Description:** Adds a new document/phrase to the vector store.

- **GET `/vs/getalltexts`**
  - **Description:** Retrieves all stored phrases/documents.

- **GET `/vs/getsearchtexts`**
  - **Query Parameters:**
    - `text` (string) — Search query.
    - `k` (integer, default: 5) — Number of top results to return.
  - **Description:** Searches for phrases/documents similar to the input text.

## Notes

- **API Documentation**: Once the backend is running, interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend Deployment**: The frontend is static and can be hosted on any web server. Remember to update `config.js` for the correct backend API URL.
- **Docker**: The provided Docker setup only launches the backend API. You must serve the frontend separately.
