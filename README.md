````Markdown
# Rufus

**Rufus** is an AI-powered scraping client designed to interact with a FastAPI-based scraping API. It is capable of dynamically fetching data from specified websites or searching for relevant data based on user instructions. Rufus is built for integrating web-scraped content into **RAG (Retrieval-Augmented Generation)** pipelines.

## Features

- **Dynamic Web Scraping**: Pass a specific website or provide a query, and Rufus will either scrape the given site or search for relevant content dynamically.
- **API Integration**: Rufus integrates with OpenAI, FastAPI, and Google Custom Search API.
- **RAG Pipeline Compatibility**: Data retrieved by Rufus can be passed directly into RAG pipelines for further processing or analysis.
- **Custom Website Search**: If no website is specified, Rufus can use Google's Custom Search API to find relevant content.

## Installation

You can install Rufus via pip:

```cmd
pip install Rufus
````

## Usage

Here is an example of how to use the `RufusClient` to scrape content from a specific website or search dynamically based on user input.

### Basic Usage

```python
import os
from Rufus import RufusClient

# Set up the API key and create a client instance
key = os.getenv('RUFUS_API_KEY')
client = RufusClient(api_key=key)

# Call the API with instructions
instructions = "Find information about AI innovations in healthcare."
documents = client.scrape(instructions)

# Output the scraped content
for doc in documents:
    print(doc)
```

### Environment Variables

- `RUFUS_API_KEY`: The API key used to authenticate your requests with the Rufus server.

### Example with a Website

You can also scrape a specific website by passing a URL to the client.

```python
instructions = "Retrieve customer reviews from https://example.com"
documents = client.scrape("https://example.com")

for doc in documents:
    print(doc)
```

## How It Works

1. **RufusClient**: This client is responsible for sending requests to the FastAPI server, which processes your instructions and retrieves the relevant data.
2. **OpenAI Integration**: Rufus uses OpenAI models to interpret user queries and determine how best to retrieve the data.
3. **Google Custom Search API**: If a website isn’t provided, Rufus dynamically finds relevant content using Google Custom Search.

## API Hosting

To host the FastAPI server, follow these steps:

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Configuration

To use Rufus effectively, you'll need to set up the following environment variables:

- **`OPENAI_API_KEY`**: API key for OpenAI.
- **`GOOGLE_API_KEY`**: Google API key for using Custom Search API.
- **`GOOGLE_CX`**: Custom Search Engine ID (CX) for Google Custom Search.

### Example

```bash
export RUFUS_API_KEY="your-rufus-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export GOOGLE_API_KEY="your-google-api-key"
export GOOGLE_CX="your-google-cx"
```

## Development

If you would like to contribute or further develop Rufus, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/rufus.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
Rufus/
│
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI server that serves the Rufus API
│
├── Rufus/
│   ├── __init__.py
│   ├── client.py            # RufusClient that communicates with the API
│
├── setup.py                 # Setup file for packaging and installation
├── requirements.txt         # Dependencies for the project
└── README.md                # Project overview and usage instructions
```

## Project Structure

### 1. `api/main.py`

This is the main FastAPI server that handles requests for scraping data based on user input.

#### `RufusAI` class

The core class that handles scraping tasks.

- **`__init__`**: Initializes the class, including setting up API keys for Google Custom Search and OpenAI.
- **`extract_website_from_prompt`**: Extracts any website mentioned in the user's prompt using regex.
- **`analyze_prompt_with_ai`**: Sends the prompt to OpenAI to generate relevant search keywords if no website is provided.
- **`search_websites`**: Queries the Google Custom Search API using the keywords from OpenAI to find relevant websites.
- **`fetch_page`**: Retrieves the HTML content from the specified website.
- **`extract_relevant_content`**: Parses the HTML using BeautifulSoup and extracts sections relevant to the user’s prompt.
- **`filter_and_rank`**: Uses OpenAI to rank and filter content based on its relevance to the original query.

#### FastAPI Endpoints

- **`POST /scrape/`**: This endpoint accepts a prompt and either scrapes a provided website or dynamically finds relevant content. It uses the `RufusAI` class to handle all scraping and content extraction logic.

### 2. `Rufus/client.py`

This file contains the `RufusClient` class, which allows users to interact with the FastAPI server.

- **`__init__`**: Initializes the client with an API key and base URL for the FastAPI server.
- **`scrape`**: Sends a POST request to the `/scrape/` endpoint of the FastAPI server with a user-provided prompt. It returns the relevant content scraped from the web.

### 3. `setup.py`

This file defines the package configuration. It specifies the package name, version, description, dependencies, and more. This file is used to package and install Rufus via pip.

### 4. `requirements.txt`

Contains a list of all dependencies required for Rufus to run, such as `requests`, `fastapi`, `openai`, `uvicorn`, etc.

### 5. `README.md`

This file provides an overview of the Rufus project, including installation instructions, usage examples, and explanations of the environment variables required to configure Rufus properly.
