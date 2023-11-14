# Url Shortener API

# Pre-requisites
- python3.8+
- nodejs 16+
- yarn 1.22+

# How to run the API locally
- [OPTIONAL] Create a virtual environment using `python3 -m venv venv` and then activate it using `source venv/bin/activate`
- Run `pip install -r requirements.txt` to install the dependencies
- Run `uvicorn main:app` to start the server
- Go to  http://127.0.0.1:8000/docs to use the swagger UI

# How to run the tests
- Run `pytest` to run the tests

# How to deploy the API to AWS
- Run `yarn install` to install the dependencies
- Run `yarn serverless deploy --stage dev` to deploy the API to AWS

# Design Decisions
The project uses the following architecture, frameworks and libraries:
- Domain Driven Design (DDD) to separate the application, domain and infrastructure layers
- Dependency injection to improve testability and maintainability
- FastAPI as the web framework as it is a modern, fast (high performance), web framework for building APIs with Python 3.6+ based on standard Python type hints
- Pydantic for data validation and serialization
- Sqlite as the database as it is a lightweight database that is easy to setup and use

### Why DDD?
Domain-Driven Design (DDD) is a software design approach that focuses on modeling software to match a complex business domain. Here's a simple explanation of the key design decision of using DDD:

Understand the Business: DDD emphasizes deep understanding of the business or domain you're working in. This means learning the ins and outs of how the business operates and what problems it faces.

Speak the Language: It encourages using a common language (called Ubiquitous Language) between developers and business experts. This language is used both in the code and in discussions, ensuring everyone understands each other clearly.

Model the Domain: DDD involves creating a model of the business domain. This model reflects the real-world processes, rules, and entities (like customers, orders, etc.) of the business.

Focus on Core Concepts: It distinguishes between different parts of the domain, focusing on the core - the most crucial part of the business logic - and paying less attention to less important parts.

Isolate the Domain: The domain (business logic) is kept separate from other parts of the system like the user interface, database, or external services. This isolation makes the system more flexible and the domain logic easier to understand and maintain.

In short, DDD is about creating software that mirrors real-world business complexities, using a common language and focusing on what's most important in the business.
