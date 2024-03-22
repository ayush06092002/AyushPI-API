# AyushPI-API

AyushPI-API is a REST API that fetches information from a vast database of Ayurvedic medicines. The database contains over 600 medicines (699 to be precise), with all the information from its uses to the precautions, if any. The API displays the info through a symptom search, which can be filtered while displaying using any application.

Several unit test cases have been added to the project to facilitate ease. A great amount of time has been spent to make the final_data.xlsx file which includes the simplified version of the database used:
https://arogya.maharashtra.gov.in/Site/PDFs/EDL_Ayurveda.pdf

The API page:
![Screenshot 2024-01-24 215727](https://github.com/ayush06092002/AyushPI-API/assets/22142132/6265aacc-3a6b-4d1e-bf9c-9841854edff6)

## Note
The CORS Error is now fixed and you can make api calls from your code

## Table of Contents
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the repository](#1-clone-the-repository)
    - [Build the Docker image](#2-build-the-docker-image)
    - [Resolve Docker build issues (if encountered)](#3-resolve-docker-build-issues-if-encountered)
  - [Run the server](#4-run-the-server)
  - [Create superuser](#5-create-superuser)
- [Creating User Token](#creating-user-token)
- [Authenticating](#authenticating)
- [Pushing the data to the database](#pushing-the-data-to-the-database)
- [Testing](#testing)

## Tech Stack

- Python
- Django Framework
- Postgres SQL

## Getting Started

### Prerequisites

Ensure you have Docker Desktop installed. The installation process will automatically handle other dependencies.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ayush06092002/AyushPI-API
    cd AyushPI-API
    ```

2. **Build the Docker image:**

    ```bash
    docker build .
    ```

3. **Resolve Docker build issues (if encountered):**

    If you encounter 'ERROR [internal] load metadata for docker.io/library/python:3.9-alpine3.13', follow these steps:

    - For Linux:
        - Step 1: `sudo vi ~/.docker/config.json`
        - Step 2: Update `credsStore` to `credStore`
        - Step 3: Run services with `docker-compose up your-services`

    - For Windows:
        - Step 1: Go to `C:\Users\Name\.docker`
        - Step 2: Open `config.json`
        - Step 3: Update `credsStore` to `credStore`
        - Step 4: Build again

4. **Run the server:**

    ```bash
    docker-compose up
    ```

5. **Create superuser:**

    ```bash
    docker-compose run --rm app sh -c "python manage.py createsuperuser"
    ```

    Enter the credentials and make sure you remember it.

    Access the admin page at http://127.0.0.1:8000/admin and the API Swagger UI page at http://127.0.0.1:8000/api/docs/.

### Creating User Token

In the Swagger UI page, under the user scheme:

1. Click on POST /api/user/create/ -> Try it Out
2. Enter the email, password, and the name.
3. Click Execute.
   
A 201 Response code shows successful creation of a user.

4. Click on POST /api/user/token/ -> Try it out
5. Enter your email and password and click execute.
6. Copy the token generated and paste is somewhere.

### Authenticating

1. Click on Authorize on the top right of the Swagger page.
2. Under the Token Auth type "Token 'paste your token here'" (without quotes).
3. Click Authorize

You can check your status by clicking on GET /api/user/me/ -> Try it out -> Execute

### Pushing the data to the database

1. Make sure to install pandas and openpyxl on your PC.
2. In the `api_push.py` file, edit the Token info with your token.
3. Run the script:

    ```bash
    python api_push.py
    ```

4. Sit and relax till:

    ```bash
    All data processed
    ```

### Testing

1. Under the medicine schema, click on GET /api/medicine/medicines/ -> Try it Out
2. Enter the symptoms (Check `final_data -> Sheet1 -> Normal Understandable Term` for examples). You write multiple symptoms like Dandruff, Itching.
3. Execute.
4. Enjoy your health :)
