Certainly! Here's a comprehensive README for your project, detailing all the steps, technologies, and deployments involved:

---

# YouTube Video Summarizer with GPT-4 and YouTube Transcriber APIs

This project is designed to extract transcriptions from YouTube videos using the YouTube Transcriber API and then generate concise summaries of these transcriptions using the GPT-4 API. The application includes both a terminal-based script and a Django-based web API for generating chapter titles from video transcriptions. Additionally, it involves setting up a data pipeline to synchronize data between PostgreSQL and AWS DynamoDB, and deploying the application using Docker on AWS Elastic Beanstalk.

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Setup and Installation](#setup-and-installation)
3. [Terminal Application](#terminal-application)
4. [API Version](#api-version)
5. [Containerizing with Docker](#containerizing-with-docker)
6. [Data Pipeline](#data-pipeline)
7. [Deploying to AWS Elastic Beanstalk](#deploying-to-aws-elastic-beanstalk)
8. [Conclusion](#conclusion)

## Technologies Used

- **Python**: Core programming language.
- **Django**: Web framework for the API version.
- **YouTube Transcript API**: For extracting video transcriptions.
- **OpenAI GPT-4**: For generating summaries from transcriptions.
- **PostgreSQL**: Primary database for storing video transcriptions and summaries.
- **AWS DynamoDB**: NoSQL database for storing processed data.
- **Docker**: For containerizing the application.
- **AWS Elastic Beanstalk**: For deploying the Docker container.
- **Docker Compose**: For managing multi-container applications.
- **AWS Amplify**: For real-time messaging, authentication, notifications, and deployment.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file and add your OpenAI API key, AWS credentials, and other necessary environment variables.
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_DEFAULT_REGION=your_aws_default_region
   ```

## Terminal Application

The terminal application extracts transcriptions from a YouTube video and generates chapter titles using the GPT-4 API.

1. **Script Explanation:**
   - `main.py`: Contains functions to fetch video transcriptions, group sentences, split into chapters by topic, and generate chapter titles using GPT-4.

2. **Run the Script:**
   ```bash
   python main.py <youtube_video_id>
   ```

## API Version

Transitioning from a terminal application to a web API using Django.

1. **API Endpoint:**
   - `/generate-titles/<video_id>/`: Generates and returns chapter titles for the given YouTube video ID.

2. **Run the Django Server:**
   ```bash
   python manage.py runserver
   ```

## Containerizing with Docker

Containerizing the application to ensure consistent environments across development, testing, and production.

1. **Dockerfile:**
   ```Dockerfile
   FROM python:3.11.4-slim-buster
   WORKDIR /app
   ENV PYTHONDONTWRITEBYTECODE 1
   ENV PYTHONUNBUFFERED 1
   COPY requirements.txt .
   RUN pip install --upgrade pip
   RUN pip install -r requirements.txt
   COPY . .
   ```

2. **Docker Compose:**
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       command: ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       env_file:
         - .env
       depends_on:
         - db

     db:
       image: postgres:15
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=secret
         - POSTGRES_DB=transcribed_data

     etl:
       build: .
       command: ["sh", "-c", "sleep 10 && python etl_script.py"]
       volumes:
         - .:/app
       env_file:
         - .env
       depends_on:
         - web

   volumes:
     postgres_data:
   ```

3. **Build and Run Containers:**
   ```bash
   docker-compose up --build
   ```

## Data Pipeline

Setting up an ETL pipeline to synchronize data between PostgreSQL and AWS DynamoDB.

1. **ETL Script Explanation:**
   - `etl_script.py`: Connects to PostgreSQL, fetches data, and inserts it into DynamoDB.

## Deploying to AWS Elastic Beanstalk

Deploying the Dockerized application to AWS Elastic Beanstalk for scalability and ease of management.

1. **Initialize Elastic Beanstalk:**
   ```bash
   eb init -p docker time-stamp
   ```

2. **Create and Deploy Environment:**
   ```bash
   eb create time-stamp-env
   eb deploy
   ```

## Conclusion

### Key Achievements:
- Developed a robust application to summarize YouTube videos using advanced APIs.
- Containerized the application for consistency and ease of deployment.
- Established a reliable data pipeline between PostgreSQL and AWS DynamoDB.
- Successfully deployed the application on AWS Elastic Beanstalk.

### Challenges and Solutions:
- Ensured compatibility between different APIs and services.
- Overcame data consistency issues by implementing a robust ETL pipeline.

### Future Improvements:
- Enhance the summarization algorithm for better accuracy.
- Implement user authentication and access control for the API.
- Integrate additional data sources and processing features.

## Call to Action

Try out similar projects and explore the use of APIs and cloud services in your applications. For more details, visit the project repository and check out the documentation.

