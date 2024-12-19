# Stock Application

## Overview
The Stock Application is designed to cater to individual stock traders, enabling them to perform essential stock trading operations such as viewing available stocks, managing transactions (buying and selling stocks), tracking user portfolios, and maintaining transaction histories. The application provides API endpoints for all functionalities and utilizes Swagger for API documentation.

---

## Features
### Functional Requirements
- **User Registration**: Create login credentials.
- **User Login**: Authenticate users.
- **View Portfolio**: Display current holdings for a user.
- **Transaction Management**:
  - Buy Stocks.
  - Sell Stocks.
- **Transaction History**: Maintain and retrieve user-specific transaction history.
- **User Logout**: End user sessions securely.
- **Soft-Deletion**: Allow users to deregister from the platform.

---

## API Endpoints
### Designed APIs:
1. **Sign-Up API**: Register new users.
2. **Login API**: Authenticate users and initiate sessions.
3. **Logout API**: End user sessions.
4. **User's Portfolio API**: Retrieve current stock holdings.
5. **Stocks List API**: List available stocks.
6. **Buy Stock API**: Execute stock purchase transactions.
7. **Sell Stock API**: Execute stock sale transactions.
8. **Transactions History API**: Retrieve the user's transaction history.
9. **De-Register User API**: Soft-delete user accounts.

---

## Tech Stack
- **Programming Language**: Python 3.8
- **Web Framework**: Flask (Micro Web Framework)
- **Database**: MySQL
- **API Documentation**: Swagger
- **WSGI Server**: Gunicorn
- **Version Control**: Git

---

## Getting Started
### Prerequisites
1. Python 3.8 installed on your machine.
2. MySQL server set up with the required schema.
3. Required Python packages installed. Use the following command:
   ```bash
   pip install -r requirements.txt
