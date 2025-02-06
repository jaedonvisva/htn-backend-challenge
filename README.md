# Hackathon Backend API

This is a Flask-based backend API for managing attendee data and badge scans for a hackathon event. The API supports endpoints for retrieving user information, adding scans, and handling check-ins and check-outs.

## Getting Started

To run this project on your own machine, follow these steps:

### Prerequisites

- Python 3.6 or higher
- SQLite3 (this is included with Python)
- Flask (you can install it using `pip install flask`)

### Steps to Start the Project

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Install dependencies**:
    Make sure to install Flask and any other dependencies:
    ```bash
    pip install flask
    ```

3. **Set up the database**:
    Before running the Flask application, you need to initialize the database. To do so, run the `init_db.py` script:
    ```bash
    python init_db.py
    ```
    This will create the `hackathon.db` SQLite database and set up the necessary tables.

4. **Run the Flask app**:
    After initializing the database, you can start the Flask server:
    ```bash
    python main.py
    ```
    The server will start running at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. **Get All Users**

- **Endpoint**: `GET /users`
- **Description**: Retrieve information about all users, including their scan activities.
- **Response**: A list of user objects with their details and associated scan activities.

**Example response**:
```json
[
  {
    "badge_code": "abc123",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "scans": [
      {
        "activity_name": "Registration",
        "scanned_at": "2025-02-06T15:30:00+00:00",
        "activity_category": "Onboarding"
      },
      {
        "activity_name": "Workshop 1",
        "scanned_at": "2025-02-06T16:00:00+00:00",
        "activity_category": "Workshops"
      }
    ]
  },
  {
    "badge_code": "def456",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "2345678901",
    "scans": [
      {
        "activity_name": "Breakfast",
        "scanned_at": "2025-02-06T15:50:00+00:00",
        "activity_category": "meal"
      },
      {
        "activity_name": "Workshop 1",
        "scanned_at": "2025-02-06T16:30:00+00:00",
        "activity_category": "Workshops"
      }
    ]
  }
]
```
### 2. **Get User Information by Badge Code**

- **Endpoint**: `GET /users/<string:badge_code>`
- **Description**: Retrieve information about one user, including their scan activities, by their badge code.
- **Parameters** `badge_code`(string): The badge code of the user.
- **Response**: A user object with their details and associated scan activities.

**Example response**:
```json
  {
    "badge_code": "abc123",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "scans": [
      {
        "activity_name": "Registration",
        "scanned_at": "2025-02-06T15:30:00+00:00",
        "activity_category": "Onboarding"
      },
      {
        "activity_name": "Workshop 1",
        "scanned_at": "2025-02-06T16:00:00+00:00",
        "activity_category": "Workshops"
      }
    ]
  }
```

### 3. **Update User Information**

- **Endpoint**: `PUT /users/<badge_code>`
- **Description**: Update user information such as name, email, and phone number.
- **Parameters**:
  - `badge_code` (string): The badge code of the user to update.
  - Request body (JSON):
    ```json
    {
      "name": "Updated Name",
      "email": "updated@example.com",
      "phone": "0987654321"
    }
    ```
- **Response**: The updated user information.

**Example response**:
```json
{
  "badge_code": "abc123",
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "0987654321",
  "updated_at": "2025-02-06T17:00:00+00:00"
}
```