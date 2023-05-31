# AI-Powered Image Generation Gallery 

This repository contains an AI-powered image generation gallery. This Flask application utilizes an AI image generation API to create images based on user prompts, then stores the generated images and prompts in an embeddings database, allowing for semantic search of generated images.

## Features

* **Image Generation**: Create unique images based on user prompts.
* **Image Gallery**: Display a gallery of generated images.
* **Semantic Search**: Search for images based on their semantic similarity to the search query.

## Getting Started

### Prerequisites

- Python 3.8 or above
- Flask
- ChromaDB
- Stability.ai API key
- OpenAI API key (for the embedding functions)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/septiannugraha/chroma-sd
   ```

2. Install Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables for the OpenAI API key and the embedding model name:
    ```text
    # STABILITY_AI_KEY is the API key for the Stability AI image generation service
    STABILITY_AI_KEY=sk-xxxxxxxxxxxx

    # ENGINE_ID is the ID of the engine you're using in Stability AI
    ENGINE_ID=stable-diffusion-xl-beta-v2-2-2

    # OPENAI_KEY is the API key for using OpenAI's embedding function
    OPENAI_KEY=sk-xxxxxxxxxxxxxxx

    # EMBEDDING_MODEL is the name of the OpenAI model used for text embeddings
    EMBEDDING_MODEL=text-embedding-ada-002
    ```
4. Run the application:
   ```
   flask run
   ```

## Usage

To generate an image, type a prompt into the text box and click the "Generate" button. The application will send a request to the image generation API and display the resulting image in the gallery.

To search for images, type a search term into the text box and click the "Search" button. The application will return a list of images that are semantically similar to the search term.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)