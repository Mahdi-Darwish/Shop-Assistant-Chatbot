# Shop Assistant Chatbot

A full-stack AI-powered assistant for a coffee shop. The application allows customers to interact with the shop through natural-language conversations, manage their cart, view orders, and track order status.

The system also includes authentication, persistent chat history, and an admin interface for managing products, users, and orders.

The chatbot is connected to the application's backend tools and PostgreSQL database, allowing it to retrieve information and perform actions rather than only generate responses.

## Features

### Customer

* User registration and login
* Authentication and authorization
* Natural-language product search
* Search products by name
* Filter products by minimum or maximum price
* Add products to the cart through the chatbot
* View items in the cart
* View orders and their items
* Check the current order status
* Persistent chat history
* Access previous conversations after logging in
* View updated order status within the conversation related to the order

### Order Tracking

Orders are connected to the customer's chat history.

When an administrator updates an order's status, the updated status is reflected in the customer's related conversation. This keeps order information synchronized between the admin side and the customer's chat experience.

### Admin

Administrators have access to protected management functionality, including:

* Add products
* Update products
* Retrieve users
* Retrieve orders
* Update order status

Changes made by administrators are reflected in the corresponding customer data and order conversations.

## AI Tool Calling

The chatbot uses an OpenAI-compatible LLM together with backend tools.

The LLM can determine which application tool is required based on the customer's request. The selected tool then interacts with the application's services and database before the result is returned to the assistant.

This allows the chatbot to perform real operations such as:

* Searching products
* Filtering products by price
* Managing the shopping cart
* Retrieving cart contents
* Retrieving order information
* Checking order status

## Application Flow

```text
Customer
   ↓
Frontend
   ↓
FastAPI
   ↓
Authentication
   ↓
LLM
   ↓
Tool Calling
   ↓
Application Services
   ↓
PostgreSQL
   ↓
Tool Result
   ↓
LLM
   ↓
Response
```

For authenticated customers, account-specific operations are associated with the logged-in user.

## Chat History

Customer conversations are stored and associated with their accounts.

After logging in, customers can access their previous conversations and continue using the assistant with their existing chat history.

Order-related conversations are also connected to the corresponding order, allowing updated order information to be reflected in the relevant conversation.

## Shopping Cart

The chatbot can interact with the customer's shopping cart through backend tools.

Customers can add products to their cart and retrieve the current contents of their cart through the assistant.

Cart data is associated with the authenticated customer.

## Orders

The system supports customer access to order information, including:

* Customer orders
* Order items
* Order status
* Updated order status

Order information is retrieved from the database and can be accessed through the chatbot.

## Admin Management

The admin functionality provides protected operations for managing the coffee shop.

Administrators can manage:

* Products
* Users
* Orders
* Order statuses

When an order status is changed, the updated information is reflected in the corresponding customer's order-related conversation.

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL
* Alembic
* Redis
* Uvicorn

### AI

* OpenAI-compatible API
* LLM tool calling
* Custom application tools

### Frontend

* HTML
* CSS
* JavaScript

### Infrastructure

* Docker
* Docker Compose

## Project Structure

```text
Shop-Assistant-Chatbot/
│
├── UI/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── app/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── tools/
│   ├── database.py
│   ├── dependencies.py
│   ├── seed.py
│   ├── server.py
│   ├── tools_register.py
│   └── tools_schema.py
│
├── alembic/
├── scripts/
│
├── insert_products.sql
├── docker-compose.yaml
├── dockerfile
├── entrypoint.sh
├── alembic.ini
├── main.py
├── requirements.txt
└── requirements_auth.txt
```

## Database

PostgreSQL is used as the primary application database.

The system stores data related to:

* Users
* Products
* Shopping carts
* Orders
* Order items
* Chat history

Alembic is used for database migrations.

```bash
alembic upgrade head
```

## Running the Project

### Requirements

* Python
* Docker
* Docker Compose
* PostgreSQL
* Redis
* API key for the configured LLM provider

### Using Docker

```bash
git clone https://github.com/Mahdi-Darwish/Shop-Assistant-Chatbot.git
cd Shop-Assistant-Chatbot
```

Configure the required environment variables and start the application:

```bash
docker compose up --build
```

The FastAPI application will be available at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Local Development

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI application:

```bash
uvicorn app.server:app --reload
```

Make sure PostgreSQL and Redis are running and the required environment variables are configured.

## Environment Variables

Create a `.env` file for local development and configure the required database and LLM settings.

Do not commit API keys, database credentials, `.env` files, or other secrets to the repository.

## Purpose

This project explores the integration of LLMs with a real backend application.

Rather than using an LLM only for conversational responses, the assistant is connected to application functionality through tools and services.

The system combines:

* Authentication
* Product management
* Product search
* Shopping carts
* Orders
* Order tracking
* Persistent chat history
* Admin management
* Database operations
* LLM tool calling

This creates a conversational interface through which customers can interact with the coffee shop's services while administrators can manage the underlying application.

## Future Improvements

* Product recommendations
* More advanced product filtering
* Order creation through the chatbot
* Payment integration
* Improved conversation memory
* Automated testing
* Production deployment
* CI/CD pipeline

## Author

**Mahdi Darwish**

GitHub: https://github.com/Mahdi-Darwish
