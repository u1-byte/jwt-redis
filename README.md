## Flask API with Redis and JWT

This project is a Flask-based API that demonstrates the use of Redis for token blocklisting and additionally also used for user data storage. JWT (JSON Web Token) is implemented for authentication, while Redis handles storing user-related data and managing a blocklist for invalidated JWT tokens.

### Key Points

-   **JWT Authentication**: Secure login/logout with JWT, supporting access and refresh tokens.
-   **Token Blocklisting**: Manage JWT tokens by blocking invalidated tokens (e.g., on logout).
-   **User Data Management**: Store user data such as username, password, city, and country in Redis.


### Getting Started

1. Clone the Repository
	```
	git clone <project repository>
	cd jwt-redis
	```
2. Install Docker and Docker Compose if not already installed.

### Running with Docker Compose
This project comes with a `docker-compose.yml` file that sets up the Flask API and Redis.
```
docker-compose up --build -d
```
### Running without Docker
1. Create a virtual environment and activate it:
	```
	python -m venv venv
	```
   - Windows:
		```
		venv\Scripts\activate
		```
   - Linux/macOS:
		```
		source venv/bin/activate
		```

2. Install dependencies:
	```
	pip install -r requirements.txt
	```
	
3. Run the application:
   ```
   python run.py
   ```

### API Endpoints
Base URL: `http://localhost:5000/`
API Docs: `http://localhost:5000/docs`
Token: `Bearer <apiKey>`

**Auth Endpoints `/auth`**
 - `POST /login` - Login and receive fresh access and refresh tokens
 - `POST /refresh` - Refresh access token and mark as not fresh
 - `DELETE /logout` - Logout user and revoke tokens

**User Endpoints `/users`**
 - `GET /free-access` - Get user data - Without JWT validation
 - `GET /protected` - Get user data - Required JWT token
 - `GET /admin-only` - Get user data - Required admin roles on token
 - `GET /whoami` - Get current login user info
