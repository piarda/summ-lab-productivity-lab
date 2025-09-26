# Productivity Betting Tracker API

This API provides a backend for managing users and tracking their bets on various sports and events. Users can register, log in, create bets, view bets with pagination, update and delete them. Authentication is handled using JWT tokens, and all sensitive routes are protected. This API supports a clean and secure way to track betting productivity.

## Installation Instructions:
1. Upon cloning the repository, set up the Python environment via:
    pipenv
    pipenv install
    pipenv shell

2. Run database migrations via:
    flask db upgrade

3. Seed the database via:
    python seed.py

## Running the App:
Start the Flask development server via:
    flask run
The API will be accessible at http://localhost:5000/

## API Endpoints:
Authentication:

POST /auth/register
Registers a new user.
Request JSON: { "username": "user", "password": "pass" }
Response: Success message or error.

POST /auth/login
Logs in a user and returns a JWT token.
Request JSON: { "username": "user", "password": "pass" }
Response: JWT token and user info.

GET /auth/me
Returns the current logged-in user info.
Requires JWT token in Authorization header.

Bets:
All bet-related routes require JWT authentication.

POST /bets
Create a new bet.
Request JSON includes event, amount, odds, result, date, bet type, and sport.

GET /bets
Retrieve paginated list of bets for the current user.
Query parameters: page (default 1), per_page (default 5).

GET /bets/<id>
Get details for a single bet via ID.

PATCH /bets/<id>
Update an existing bet via ID.
Request JSON with any bet fields to update.

DELETE /bets/<id>
Delete a bet via ID.


Enjoy!
