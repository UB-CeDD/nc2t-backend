# NCCT Project - Backend

This directory contains the **Django backend** for the NCCT Project. It uses Docker and Docker Compose to containerize the application, making it easy to set up and run in any environment.

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Setup and Running the Backend](#setup-and-running-the-backend)
4. [Development Workflow](#development-workflow)
5. [Technologies Used](#technologies-used)
6. [License](#license)
7. [Contributing](#contributing)

---

## Project Structure
````
├── backend/
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── entrypoint.sh
│ └── src/ # Created automatically
│ ├── manage.py
│ └── src/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
````
---

## Prerequisites

Before running the backend, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Setup and Running the Backend

1. **Navigate to the backend directory**:
   ```bash
   cd backend
    ```
2. **Start the backend**: 
    Run the following command to build and start the Docker containers:  
    ```bash
    docker-compose build
    docker-compose up
    ```
    This will:  
      - Initialize the Django backend. 
      - Start the PostgreSQL database.
3. **Access the Django Backend**:  
      - Django Backend: http://localhost:8000
4. **Stop the backend**: To stop the containers, run:  
    ```
   docker-compose down
    ```
---
## Development Workflow
- The Django project is automatically created in the src directory.
- You can edit the Django files in the src directory on your host machine. Changes will be reflected in the container.
---
## Technologies Used
- **Backend**:
  - Django (Python)
  - PostgreSQL (Database)
- **Containerization**:
    - Docker 
    - Docker Compose
---

## License
This project is licensed under the MIT License. See the [MIT License](https://opensource.org/licenses/MIT) file for details.  <hr></hr>

---
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.