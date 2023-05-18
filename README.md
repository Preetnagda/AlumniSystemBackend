# Alumni System Backend API

## Features

This API provides with various endpoints serve the following features:
1. Register new alumni with "firstname", "lastname", "emailaddress", "studentid" and "password".
2. Login of a registered user. On getting correct credentials i.e emailaddress and password, a limited time token is generated for authenticated requests.
3. Logged in alumni can view and download their transcripts and certificates. They also have access to a unique document number which can be provided to external users.
4. Any unauthenticated user (external user), if provided with a document number, can download the document.
5. Registred admin user can register another admin user.

## Architecture Details

- The application is based of FastAPI framework.
- The application has a database layer which can easily configured to work with a database of choice.
- Currently uses dynamodb as a database. This example can be used to develop integration with other databases.
- The application uses AWS S3 bucket for file storage and retrival.
- A **docker** image can be created with the provided dockerfile.

## Usage

Steps to install and start the application on local environment:

1. Install required python packages. <br> 
NOTE: You may create and activate a virtual environment to decouple and isolate dependencies. <br>
`pip install -r requirements.txt`

2. Start the app with uvicorn and automatic reload enabled by:<br>
`uvicorn app.main:app --reload` <br>
This will start the application on the default port 8000

### Create docker image and container

1. To create a docker image run the following command:<br>
`docker build -t <name_of_image> .`

2. Build container: <br>
`docker run -d -e AWS_DEFAULT_REGION=<default_aws_region> --name <name_of_container> -p 8000:8000 <name_of_image>`
