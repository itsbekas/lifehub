# Lifehub

A personal data analytics dashboard to track and visualize the important aspects of your life.  Lifehub collects data from various sources, offering insights into finances, events, weather, and more.

## Project Overview

Lifehub empowers individuals to gain a comprehensive view of their daily lives through centralized data and visualizations.  The project is designed to support multiple users, allowing them to manage their own data securely.

### Key Elements

- User Management: Lifehub enables user signup and login functionality.  Each user has their own secure data storage within the database (under development).

- Fetchers: Cronjobs responsible for regularly retrieving data from external service APIs (e.g., financial accounts, calendars) and storing the results in the user's dedicated section of the database.  These fetchers are designed to collect historical data, enabling analysis of trends and patterns over time.

- API: A data interface built on FastAPI to deliver the collected information to a frontend application (under development). This API provides the means to visualize and interpret user-specific results.

## Technology Stack

- Python: Core programming language
- FastAPI: High-performance web framework for API development.
- SQLAlchemy: The foundation for this stack's database interactions, offering flexibility and robust ORM features.
- Pydantic: Used for data modeling, validation, and parsing, ensuring the consistency of data exchanged with your API.
- Requests: Library for building API clients to interact with external services.
- Pytest: Framework for streamlined unit testing.
- MariaDB: Relational database for data storage, with secure multi-user support.

## How It Works

1. Users sign up and log in to create their secure data storage within the database.
2. Fetchers periodically gather user-specific data from designated sources.
3. Data is normalized and securely stored within the user's designated section of the MariaDB database.
4. The FastAPI-based API makes processed data accessible to the user.
5. A frontend application (under development) will consume the API, presenting the data in visualizations and dashboards specific to the logged-in user.