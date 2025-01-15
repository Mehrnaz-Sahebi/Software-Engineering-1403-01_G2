
# Group8 Synonym Suggestion Service

This folder (group8) contains a Synonym Suggestion Service built using 3 microservices:

- **Django (Python)**: Handles client requests & database interactions.
- **Go**: Processes text, tokenizes input, and fetches synonyms using a Trie data structure.
- **RabbitMQ**: Manages communication between Django and Go servers via two message queues.

These microservices are orchestrated using Docker Compose, allowing an easy and unified setup.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Endpoints](#endpoints)
  - [Home & Landing Pages](#home--landing-pages)
  - [Synonym Generation](#synonym-generation)
  - [History & User-Specific Data](#history--user-specific-data)
- [RabbitMQ Queues](#rabbitmq-queues)
- [Go Server Responsibilities](#go-server-responsibilities)
- [Running the Application](#running-the-application)
  - [Docker Compose](#docker-compose)
  - [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)
- [Contact & Further Information](#contact--further-information)

---

## Overview

Group8’s Synonym Suggestion Service receives text from a user (through Django), processes it in Go to find synonyms using a pre-built Trie data structure, and returns the processed result back to Django (and ultimately to the user). RabbitMQ functions as the messaging backbone, ensuring decoupled communication between Django and Go.

The system provides two primary modes of operation:
1. On-the-fly synonym generation (without user session consideration).
2. History-based generation (where text is stored and associated with a user).

---

## System Architecture

```mermaid
flowchart LR
    A[Client (Browser/App)] -->|HTTP Requests| B[Django Server]
    B -->|Publish text to text_queue| C[RabbitMQ]
    C -->|Consume text_queue| D[Go Server]
    D -->|Publish processed text to meanings_queue| C
    C -->|Consume meanings_queue| B
    B -->|HTTP Response with synonyms| A
```

- **Django Server**: Exposes RESTful endpoints, interacts with the database for storing text/user relations, and publishes/consumes messages to/from RabbitMQ.
- **RabbitMQ**: Maintains two queues (`text_queue`, `meanings_queue`) to facilitate communication between Django & Go.
- **Go Server**: Tokenizes incoming text, looks up synonyms in a Trie, and sends results back via `meanings_queue`.

---

## Endpoints

### Home & Landing Pages

- `path('', views.home, name='home')`
- `path('home/', views.home, name='group8')`

Purpose: Returns the base templates or home pages for Group8’s service.

### Synonym Generation

- `path('submit-text/', views.submit_text, name='submit_text')`

Purpose: Receives a text (string) from the client without user session consideration.

Process:
1. Publishes the text to `text_queue` in RabbitMQ.
2. Waits for the Go service to process the text and publish results to `meanings_queue`.
3. Returns a JSON response containing a list of words and their synonyms.

### History & User-Specific Data

- `path('submit_text_in_history/', views.submit_text_in_history, name='submit_text_in_history')`

Purpose: Receives a text (string) from the client and associates it with the currently logged-in user.

Process:
1. Sends the text to the Go service as above.
2. Upon return, stores the text in a file and logs the association (user ↔ file) in the database.

- `path('get_submit_texts/', views.get_submit_texts, name='get_submit_texts')`

Purpose: Fetches all submitted texts for the current user (if needed).

- `path('get_last_5_text_files_content/', views.get_last_5_text_files_content, name='get_last_5_text_files_content')`

Purpose: Returns a JSON containing up to 5 of the most recent texts submitted by a specific user.

Process:
1. Looks up the user’s submission history.
2. Retrieves contents from the last 5 submitted text files.
3. Sends these contents back to the client in JSON format.

---

## RabbitMQ Queues

- **`text_queue`**:
  - Publisher: Django
  - Consumer: Go
  - Payload: Raw text that needs synonyms.

- **`meanings_queue`**:
  - Publisher: Go
  - Consumer: Django
  - Payload: Processed text containing token-synonym mappings or additional metadata.

---

## Go Server Responsibilities

### Tokenization

- Splits input text into individual tokens (words) using a custom Tokenizer class.

### Synonym Lookup (Trie-based)

- A Trie stores Persian words as nodes.
- Each node references meanings (synonyms) for that word.
- Searching for a word in this Trie is roughly `O(len)`, where `len` is the length of the searched word.

### Communication

- Consumes messages from `text_queue`.
- Publishes processed data to `meanings_queue`.

---

## Running the Application

### Docker Compose

All three microservices (Django, Go, RabbitMQ) can be launched via Docker Compose. 

Steps:
1. Navigate to the `group8` folder (or wherever `compose.yaml` resides).
2. Run the following command:

```bash
docker compose up --build
```

This will build and launch the containers for Django, Go, and RabbitMQ. Ensure Docker is installed and running on your machine.

### Frontend

If you have a separate frontend application (e.g., React, Vue, Angular, or a basic HTML/JS client), refer to its specific README or documentation for instructions.

---

## Contributing

1. Fork the repository.
2. Clone your fork locally.
3. Create a feature branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```
4. Commit your changes:
   ```bash
   git commit -am 'Add some feature'
   ```
5. Push to your branch:
   ```bash
   git push origin feature/my-new-feature
   ```
6. Submit a Pull Request to the main repository.

---

## License

The Group8 Synonym Suggestion Service is released under the MIT License or another license specified by the project. For more details, see the LICENSE file in the repository root.

---

## Contact & Further Information

For questions or more details, feel free to open an issue or contact any of the project maintainers.

For better understanding of the entire repository and other groups’ work, visit the main repo:
[SaltySoft - Software Engineering 1403-01 (G2)](https://github.com/moeinEN/SaltySoft-Software-Engineering-1403-01_G2)

---

Thank you for using and contributing to Group8’s Synonym Suggestion Service! If you have any suggestions or encounter any issues, please let us know.
