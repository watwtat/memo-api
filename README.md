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

### GET /memo/{id}
Retrieve a specific memo by its ID.

**Response:**
```json
{
  "id": 1,
  "content": "Sample memo content",
  "created_at": "2025-06-20T16:59:24.111248"
}
```

Returns 404 if memo with the specified ID doesn't exist.

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

### PUT /memo/{id}
Update an existing memo by its ID.

**Request Body:**
```json
{
  "content": "Updated memo content"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Updated memo content",
  "created_at": "2025-06-20T16:59:24.111248"
}
```

Returns 404 if memo with the specified ID doesn't exist.

### DELETE /memo/{id}
Delete a memo by its ID.

**Response:**
```json
{
  "message": "Memo 1 deleted successfully"
}
```

Returns 404 if memo with the specified ID doesn't exist.

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

### Build and run with persistent storage
```bash
docker build -t memo-api .
docker run -p 8000:8000 -v memo-data:/app/data memo-api
```

The API will be available at `http://localhost:8000`

**Note:** Using the `-v memo-data:/app/data` volume mount ensures that your memo data persists even when the container is deleted or restarted. The database file will be stored in the named Docker volume `memo-data`.

### Alternative: Using a host directory
```bash
mkdir -p ./data
docker run -p 8000:8000 -v $(pwd)/data:/app/data memo-api
```

This mounts a local `./data` directory to store the database file on your host system.

## Example Usage

```bash
# Get all memos
curl http://localhost:8000/memo

# Get a specific memo by ID
curl http://localhost:8000/memo/1

# Create a new memo
curl -X POST http://localhost:8000/memo \
  -H "Content-Type: application/json" \
  -d '{"content": "Remember to buy groceries"}'

# Update a memo by ID
curl -X PUT http://localhost:8000/memo/1 \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated memo content"}'

# Delete a memo by ID
curl -X DELETE http://localhost:8000/memo/1
```