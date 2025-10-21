# String Analysis API

A RESTful API service that analyzes strings and stores their computed properties including length, palindrome detection, character frequency, and more.

## Features

- ✅ Analyze strings and compute 6 different properties
- ✅ Store analyzed strings with SHA-256 hash as unique identifier
- ✅ Filter strings by multiple criteria
- ✅ Natural language query support
- ✅ Complete error handling with detailed responses
- ✅ In-memory storage (can be easily extended to PostgreSQL/SQLite)

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Python**: 3.8+
- **Server**: Uvicorn
- **Validation**: Pydantic

## Project Structure

```
project/
├── app/
│   ├── main.py                    # FastAPI app & configuration
│   ├── config.py                  # Settings & environment variables
│   ├── database.py                # In-memory database
│   ├── models/
│   │   └── string_model.py        # String entity model
│   ├── schemas/
│   │   ├── requests.py            # Request schemas
│   │   ├── responses.py           # Response schemas
│   ├── routers/
│   │   └── strings.py             # API endpoints
│   └── services/
│       ├── analyzer.py            # String analysis logic
│       ├── filters.py             # Filtering logic
│       └── nl_parser.py           # Natural language parsing
├── tests/                         # Test files
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/SamuelOshin
cd string-analysis-api
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (Optional)
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Create/Analyze String
```bash
POST /strings
Content-Type: application/json

{
  "value": "hello world"
}
```

**Response (201 Created)**:
```json
{
  "id": "b94d27b9934d3e08...",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08...",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1
    }
  },
  "created_at": "2025-10-20T10:00:00Z"
}
```

### 2. Get Specific String
```bash
GET /strings/hello%20world
```

### 3. Get All Strings with Filtering
```bash
GET /strings?is_palindrome=true&min_length=5&word_count=1
```

**Query Parameters**:
- `is_palindrome`: boolean (true/false)
- `min