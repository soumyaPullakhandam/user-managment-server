# Application Overview

## How the Application Works

1. The user provides their full name and a valid email ID.
2. A verification email is sent to the provided email ID.
3. The verification link in the email navigates the user to the password setup page.
4. The user sets a password.
5. Once done, the user can access the application.

**Key Point:**
- Only verified users can log in to the application.

## Design Flow

### Backend Architecture

- Choosing of application type
- Database design
- Choosing of libraries
- Application flow
- ORM design
- Schema design
- API design

### Frontend Architecture

- Choosing of application type
- Choosing of state management
- Choosing of libraries
- Choosing of web components
- Application flow
- Modularizing the components

## Development Flow

### Backend

- ORM implementation using SQLAlchemy
- Models and properties implementation
- Password encryption using CryptContext hashing
- Token generation for email verification
- SendGrid integration to send emails
- Email template design in SendGrid
- User authentication token implementation
- API implementation
- Documentation generation
- Validation test scripts

### Frontend

- Screen development
- State management
- API integration
- Custom hook implementation
- React Router integration
- Validation
- Component styling

## Preparing for Production

- Implemented production-ready Docker configuration.

## Further Implementations

- Use of microarchitecture for individual services
- Use of background workers for non-blocking operations

## How to Access

**Key Points:**
- Ensure you have the latest version of Docker Desktop.
- The backend runs on port 8000 and the frontend on port 80; make sure these ports are free.
- If you do not find the verification email in your inbox, please check your spam folder.

### Backend Application

**Resource:** [Backend Resource](https://drive.google.com/file/d/1m9y6x2EfVk1eFSpFjg4zJ-okmtKDYxhh/view?usp=sharing)

- Run command: `docker-compose up --build -d` in the working directory
- Test cases command: `docker-compose run api python -m pytest tests/`
- API documentation: Navigate to [API Docs](http://localhost:8000/docs)
- Application documentation: Navigate to `project_root/src/docs/source/http` and run `index.html`

### Frontend Application

**Resource:** [Frontend Resource](https://drive.google.com/file/d/145ZzryB4HQ1FSfLz8fVhroYInRDHslqC/view?usp=sharing)

- Run command: `docker-compose up --build -d` in the working directory
- Navigate to [Frontend](http://localhost) on your browser to access the application
- Application documentation: Navigate to `project_root/docs` and run `index.html`
