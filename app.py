import logging
import os
from flask import Flask, jsonify, render_template, request, url_for
import requests
from dotenv import load_dotenv
import chromadb
import pprint
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.config import Settings

# set up logging to catch and log errors
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# load environment variables from .env file
load_dotenv()

pp = pprint.PrettyPrinter(indent=4)

# Initialize the ChromaDB client with specified settings.
# Here, the underlying database implementation is set to "duckdb+parquet",
# and the persistent storage for the database is set to a directory named "database".
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="database"
))

# Set up an OpenAI Embedding Function for ChromaDB.
# The API key and model name are obtained from environment variables.
embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv(
    "OPENAI_KEY"), model_name=os.getenv("EMBEDDING_MODEL"))

# Get or create a collection from the ChromaDB client.
# If a collection named "image_generations" doesn't exist, it will be created.
# The collection uses the previously defined embedding function.
collection = chroma_client.get_or_create_collection(
    name="image_generations", embedding_function=embedding_function)

@app.route('/api/search_images')
def images():
    user_input = request.args.get('input')

    results = collection.query(
        query_texts=[user_input],
        n_results=10
    )
    print(results)
    result_list = []
    for doc, md in zip(results['documents'][0], results['metadatas'][0]):
        result_list.append(
            {"image_path": md['image_path'], "user_input": doc})
    return jsonify(result_list)

# API Endpoint to handle image generation requests


@app.route('/api/generate', methods=['POST'])
def generate():
    # Get user input from POST data
    data = request.get_json()
    user_input = data.get('input')

    # Define where to store generated images
    storage_directory = "static/storage"

    # Create the directory if it doesn't exist
    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)

    # Set the parameters for the image generation API
    payload = {
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "sampler": "K_DPM_2_ANCESTRAL",
        "samples": 1,
        "seed": 0,
        "steps": 75,
        "text_prompts": [
            {
                "text": user_input,
                "weight": 1
            }
        ],
        "width": 512
    }

    # Set the URL for the image generation API
    url = f"https://api.stability.ai/v1/generation/{os.getenv('ENGINE_ID')}/text-to-image"

    # Set the headers for the image generation API
    headers = {"Accept": "image/png", "Content-Type": "application/json",
               "Authorization": os.getenv("STABILITY_AI_KEY")}

    # Call the image generation API
    try:
        response = requests.post(url, json=payload, headers=headers)

        # Check if request is successful
        if response.status_code == 200:
            # Save the PNG image into the storage directory
            image_filename = f"{user_input}.png"
            image_path = os.path.join(storage_directory, image_filename)
            index = collection.count() if collection.count() is not None else 0

            # Add the new image generation request to the ChromaDB collection
            collection.add(
                documents=[user_input],
                metadatas=[{"image_path": image_path}],
                ids=[f"text_{index}"]
            )

            with open(image_path, "wb") as image_file:
                image_file.write(response.content)

            # Generate the URL for the new image and return it as JSON
            new_image_url = url_for('static', filename=image_path)
            return jsonify({'image_url': new_image_url})

        else:
            logging.error(
                f"Request failed: {response.status_code}. Reason: {response.text}")
            return jsonify({'error': f"Request failed: {response.status_code}. Reason: {response.text}"}), 500
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return jsonify({'error': f"Unexpected error occurred: {str(e)}"}), 500

# Endpoint to render the home page


@app.route("/")
def home():
    # Render the index.html template, passing in the list of user requests
    return render_template('index.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
