# N-Gram Suggestion API

This project provides an API to add n-grams to a model and suggest the next word based on input text using Django and Django REST framework.

## Prerequisites

- Python 3.x
- Django
- Django REST Framework

## Installation

1. Clone the repository

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```sh
    python manage.py migrate
    ```

5. Run load_csv command for creating model:

    ```sh
    python manage.py loac_csv
    ```

6. Run the development server:

    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Home

- **URL:** `/home/`
- **Method:** `GET`
- **Description:** Renders the homepage.

### Add N-Gram

- **URL:** `/group5/add/`
- **Method:** `POST`
- **Description:** Adds an n-gram to the model.
- **Permissions:** Authenticated users only.
- **Request Body:**
    ```json
    {
        "text": "your n-gram text",
        "dataset_name": "optional dataset name, default is 'fa'"
    }
    ```
- **Response:**
    ```json
    {
        "result": "Result message"
    }
    ```

### Suggest Word

- **URL:** `/group5/suggest/`
- **Method:** `GET`
- **Description:** Suggests the next word based on the input text.
- **Request Parameters:**
    - `text` (string): Input text for word suggestion.
    - `dataset` (string, optional): Dataset name, default is 'fa'.
- **Response:**
    ```json
    {
        "suggestions": ["word1", "word2"]
    }
    ```

## Usage

1. Access the home page by navigating to `/goup5/home/`.
2. Use the `/group5/add/` endpoint to add n-grams to the model by sending a POST request with the required data.
3. Use the `/group5/suggest/` endpoint to get word suggestions based on input text by sending a GET request with the required parameters.

## Running Tests

To run tests, use the following command:

```sh
python manage.py test group5.tests
