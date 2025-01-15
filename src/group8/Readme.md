<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Group 8 - Synonym Suggestion Service</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 0 auto;
      max-width: 900px;
      padding: 2em;
      background-color: #f9f9f9;
    }
    h1, h2, h3 {
      color: #333;
    }
    pre {
      background: #eee;
      padding: 1em;
      overflow-x: auto;
    }
    a {
      color: #007acc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    ul {
      margin-left: 1.5em;
    }
    code {
      background: #f4f4f4;
      padding: 0.2em 0.4em;
      border-radius: 4px;
    }
    .container {
      background-color: #fff;
      padding: 2em;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    nav ul {
      list-style: none;
      padding: 0;
    }
    nav ul li {
      margin-bottom: 0.5em;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Group 8 - Synonym Suggestion Service</h1>
    <p>This folder (<code>group8</code>) contains a <strong>Synonym Suggestion Service</strong> built using <strong>3 microservices</strong>:</p>
    <ol>
      <li><strong>Django</strong> (Python) – Handles client requests &amp; database interactions</li>
      <li><strong>Go</strong> – Processes text, tokenizes input, and fetches synonyms using a Trie data structure</li>
      <li><strong>RabbitMQ</strong> – Manages communication between Django and Go servers via two message queues</li>
    </ol>
    <p>These microservices are orchestrated using Docker Compose, allowing an easy and unified setup.</p>

    <h2>Table of Contents</h2>
    <nav>
      <ul>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#system-architecture">System Architecture</a></li>
        <li><a href="#endpoints">Endpoints</a>
          <ul>
            <li><a href="#home--landing-pages">Home &amp; Landing Pages</a></li>
            <li><a href="#synonym-generation">Synonym Generation</a></li>
            <li><a href="#history--user-specific-data">History &amp; User-Specific Data</a></li>
          </ul>
        </li>
        <li><a href="#rabbitmq-queues">RabbitMQ Queues</a></li>
        <li><a href="#go-server-responsibilities">Go Server Responsibilities</a></li>
        <li><a href="#running-the-application">Running the Application</a>
          <ul>
            <li><a href="#docker-compose">Docker Compose</a></li>
            <li><a href="#frontend">Frontend</a></li>
          </ul>
        </li>
        <li><a href="#contributing">Contributing</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#contact--further-information">Contact &amp; Further Information</a></li>
      </ul>
    </nav>

    <h2 id="overview">Overview</h2>
    <p><strong>Group8’s Synonym Suggestion Service</strong> receives text from a user (through Django), processes it in Go to find synonyms using a pre-built Trie data structure, and returns the processed result back to Django (and ultimately to the user). RabbitMQ functions as the messaging backbone, ensuring decoupled communication between Django and Go.</p>
    <p>The system provides two primary modes of operation:</p>
    <ol>
      <li><strong>On-the-fly synonym generation</strong> (without user session consideration).</li>
      <li><strong>History-based generation</strong> (where text is stored and associated with a user).</li>
    </ol>

    <h2 id="system-architecture">System Architecture</h2>
    <p>The following diagram illustrates the interaction between the components:</p>
    <pre>
flowchart LR
    A[Client (Browser/App)] -->|HTTP Requests| B[Django Server]
    B -->|Publish text to text_queue| C[RabbitMQ]
    C -->|Consume text_queue| D[Go Server]
    D -->|Publish processed text to meanings_queue| C
    C -->|Consume meanings_queue| B
    B -->|HTTP Response with synonyms| A
    </pre>
    <p><strong>Django Server</strong>: Exposes RESTful endpoints, interacts with the database for storing text/user relations, and publishes/consumes messages to/from RabbitMQ.</p>
    <p><strong>RabbitMQ</strong>: Maintains two queues (<code>text_queue</code> and <code>meanings_queue</code>) to facilitate communication between Django &amp; Go.</p>
    <p><strong>Go Server</strong>: Tokenizes incoming text, searches for synonyms in a Trie, and sends results back via the <code>meanings_queue</code>.</p>

    <h2 id="endpoints">Endpoints</h2>
    <h3 id="home--landing-pages">Home &amp; Landing Pages</h3>
    <ul>
      <li><code>path('', views.home, name='home')</code></li>
      <li><code>path('home/', views.home, name='group8')</code></li>
    </ul>
    <p>These endpoints typically return the base templates or home pages for Group8’s service.</p>

    <h3 id="synonym-generation">Synonym Generation</h3>
    <ul>
      <li><code>path('submit-text/', views.submit_text, name='submit_text')</code></li>
    </ul>
    <p><strong>Purpose</strong>: Receives a text (string) from the client without user session consideration.</p>
    <p><strong>Process</strong>:</p>
    <ul>
      <li>Publishes the text to <code>text_queue</code> in RabbitMQ.</li>
      <li>Waits for the Go service to process the text and publish results to <code>meanings_queue</code>.</li>
      <li>Returns a JSON response containing a list of words and their synonyms.</li>
    </ul>

    <h3 id="history--user-specific-data">History &amp; User-Specific Data</h3>
    <ul>
      <li><code>path('submit_text_in_history/', views.submit_text_in_history, name='submit_text_in_history')</code></li>
      <li><code>path('get_submit_texts/', views.get_submit_texts, name='get_submit_texts')</code></li>
      <li><code>path('get_last_5_text_files_content/', views.get_last_5_text_files_content, name='get_last_5_text_files_content')</code></li>
    </ul>
    <p><strong><code>submit_text_in_history/</code></strong>: Receives a text from the client and associates it with the current user. It sends the text for processing and, upon receiving the processed response, stores the text in a file and records the association in the database.</p>
    <p><strong><code>get_submit_texts/</code></strong>: Fetches all submitted texts for the current user.</p>
    <p><strong><code>get_last_5_text_files_content/</code></strong>: Returns a JSON containing up to 5 of the most recent text submissions of a specific user.</p>

    <h2 id="rabbitmq-queues">RabbitMQ Queues</h2>
    <ul>
      <li>
        <strong>text_queue</strong><br>
        <em>Publisher</em>: Django<br>
        <em>Consumer</em>: Go<br>
        <em>Payload</em>: Raw text that needs synonyms.
      </li>
      <li>
        <strong>meanings_queue</strong><br>
        <em>Publisher</em>: Go<br>
        <em>Consumer</em>: Django<br>
        <em>Payload</em>: Processed text containing token-synonym mappings or additional metadata.
      </li>
    </ul>

    <h2 id="go-server-responsibilities">Go Server Responsibilities</h2>
    <p>The <strong>Go</strong> microservice handles:</p>
    <ol>
      <li>
        <strong>Tokenization</strong>: Splits the input text into individual tokens (words) using a custom <code>Tokenizer</code> class.
      </li>
      <li>
        <strong>Synonym Lookup (Trie-based)</strong>:  
        <ul>
          <li>A Trie tree stores Persian words as nodes.</li>
          <li>Each node holds meanings (synonyms) for the respective word.</li>
          <li>Searching for a word in the Trie has a time complexity of roughly <code>O(len)</code>, where <code>len</code> is the length of the searched word.</li>
          <li>Aggregates synonyms for each token and publishes the result to the <code>meanings_queue</code>.</li>
        </ul>
      </li>
      <li>
        <strong>Communication</strong>:  
        <ul>
          <li>Consumes messages from <code>text_queue</code>.</li>
          <li>Publishes processed data to <code>meanings_queue</code>.</li>
        </ul>
      </li>
    </ol>

    <h2 id="running-the-application">Running the Application</h2>
    <h3 id="docker-compose">Docker Compose</h3>
    <p>All three microservices (Django, Go, RabbitMQ) can be launched via Docker Compose. The configuration is located in the <code>src/group8/compose.yaml</code> file.</p>
    <ol>
      <li>Navigate to the <code>group8</code> folder (or wherever <code>compose.yaml</code> is located).</li>
      <li>Run the following command:
        <pre>
docker compose up --build
        </pre>
      </li>
      <li>This command builds and launches the containers for Django, Go, and RabbitMQ. Ensure Docker is installed and running on your machine.</li>
    </ol>

    <h3 id="frontend">Frontend</h3>
    <p>If a separate frontend application is used (e.g., built with React, Vue, or Angular), refer to its specific README for instructions on:</p>
    <ul>
      <li>Installing dependencies</li>
      <li>Configuring the environment (API endpoints pointing to Django)</li>
      <li>Launching the client (e.g., using <code>npm start</code> or <code>yarn serve</code>)</li>
    </ul>

    <h2 id="contributing">Contributing</h2>
    <ol>
      <li>Fork the repository from <a href="https://github.com/moeinEN/SaltySoft-Software-Engineering-1403-01_G2/">SaltySoft - Software Engineering 1403-01 (G2)</a>.</li>
      <li>Clone your fork locally.</li>
      <li>Create a feature branch: <code>git checkout -b feature/my-new-feature</code>.</li>
      <li>Commit your changes: <code>git commit -am 'Add some feature'</code>.</li>
      <li>Push to your branch: <code>git push origin feature/my-new-feature</code>.</li>
      <li>Submit a Pull Request describing your changes.</li>
    </ol>

    <h2 id="license">License</h2>
    <p>This project is released under the <a href="../LICENSE">MIT License</a> (or the license specified by the project). Refer to the <code>LICENSE</code> file in the repository root for details.</p>

    <h2 id="contact--further-information">Contact &amp; Further Information</h2>
    <p>If you have questions or need more details, open an <a href="https://github.com/moeinEN/SaltySoft-Software-Engineering-1403-01_G2/issues">issue</a> or reach out to the project maintainers.</p>
    <p>For more context on the repository and other groups’ work, visit the main repo: <a href="https://github.com/moeinEN/SaltySoft-Software-Engineering-1403-01_G2/">SaltySoft - Software Engineering 1403-01 (G2)</a>.</p>

    <p>Thank you for using and contributing to Group8’s Synonym Suggestion Service! If you have any suggestions or encounter any issues, please let us know.</p>
  </div>
</body>
</html>
