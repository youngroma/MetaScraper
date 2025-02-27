# MetaScraper

MetaScraper is a web application that allows users to upload a CSV file containing a list of URLs. The system asynchronously scrapes each URL to extract meta tags—such as title, description, and keywords—and stores the results in a PostgreSQL database. The application is built with FastAPI, utilizes Celery for background task processing, Redis as a message broker, and Docker for containerization.

## Features  
- **User Authentication**: Secure login system to ensure only authenticated users can access the functionalities.
- **CSV Upload**: Users upload a list of URLs for scraping.
- **Asynchronous Processing**: URLs are scraped in the background, allowing users to continue with other tasks.
- **Progress Tracking**: Check the status of ongoing scraping tasks.
- **Results Viewing**: Retrieve and view the extracted metadata for each URL.

## Architecture

The application is composed of the following components:

- **FastAPI**: Serves as the web framework for building the API.
- **PostgreSQL**: Stores user data, urls, uploaded files, and the extracted metadata.
- **Redis**: Acts as a message broker for Celery tasks.
- **Celery**: Manages asynchronous background tasks for scraping URLs.
- **Docker**: Containerizes the application for consistent and reproducible deployments.

## Getting Started


### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/youngroma/MetaScraper.git
   cd MetaScraper
   ```

2. **Environment Variables**:

   fill '.env' the file with environment variables


   Replace variables with your desired credentials.

3. **Build and Start the Application**:

   Use Docker Compose to build and start all services:

   ```bash
   docker-compose up --build
   ```

   This command will start the following containers:

   - The FastAPI application.
   - The PostgreSQL database.
   - The Redis message broker.
   - The Celery worker for background tasks.

4. **Apply Database Migrations**:

   Once the containers are running, apply the database migrations:

   ```bash
   docker-compose exec web alembic upgrade head
   ```

   This ensures that the database schema is up-to-date.

### Usage

1. **Access the Application**:

   The FastAPI application will be available at `http://localhost:8000`.

2. **Uploading a CSV File**:

   To upload a CSV file containing URLs:

   - Authenticate using your credentials.
   - Upload CVS file (for example with using Postmnan)
  
3. **Using Postman for API Testing**

    Importing the Postman Collection

    In this repository you have Postman collection 'MetaScraper.postman_collection.json' :


    - Open Postman.
    - Click Import (top-left corner).
    - Select "File", then choose MetaScraper.postman_collection.json.
    - Click Import to add the collection.
    - Before making any API requests, you need to log in and obtain an authentication token.
       - In the response, copy the "access_token".
       - Go to the Authorization tab in Postman - Select Bearer Token - Paste the copied token into the field.
    - Now you can use the predefined API requests to interact with the system.
    - Create a CSV file with URLs and upload it!


3. **Checking Scraping Progress**:

   After uploading, you can check the status of your scraping task by accessing the `/status/{task_id}` endpoint, where `{task_id}` is the ID returned upon uploading the CSV.

4. **Viewing Extracted Metadata**:

   Once scraping is complete, retrieve the extracted metadata through the `/results/{task_id}` endpoint.


