# Memo API

A simple Flask-based REST API for managing memos.

## Features

- Create new memos with content
- Retrieve all memos
- Persistent SQLite database storage
- Automatic database initialization

## API Endpoints

### GET /memo
Retrieve all memos.

**Response:**
```json
[
  {
    "id": 1,
    "content": "Sample memo content",
    "created_at": "2025-06-20T16:59:24.111248"
  }
]
```

### POST /memo
Create a new memo.

**Request Body:**
```json
{
  "content": "Your memo content here"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Your memo content here",
  "created_at": "2025-06-20T16:59:24.111248"
}
```

## Running Locally

### Prerequisites
- Python 3.12+
- pip
- SQLite (included with Python)

### Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

**Note:** The SQLite database file (`memos.db`) will be automatically created in the project directory on first run.

## Running with Docker

### Build and run
```bash
docker build -t memo-api .
docker run -p 8000:8000 memo-api
```

The API will be available at `http://localhost:8000`

**Note:** The database file will be created inside the Docker container and data will persist only while the container exists.

## Example Usage

```bash
# Get all memos
curl http://localhost:8000/memo

# Create a new memo
curl -X POST http://localhost:8000/memo \
  -H "Content-Type: application/json" \
  -d '{"content": "Remember to buy groceries"}'
```