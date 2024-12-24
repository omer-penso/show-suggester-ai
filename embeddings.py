from openai import OpenAI
import logging
import pickle
import os
from dotenv import load_dotenv
from data_loader import load_column_from_csv


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_embeddings(titles, descriptions, api_key, model="text-embedding-ada-002"):
    client = OpenAI(api_key=api_key)
    embeddings_dict = {}

    for title, desc in zip(titles, descriptions):
        try:
            logger.info(f"Generating embedding for show: {title}")
            response = client.embeddings.create(
                input=desc,
                model=model
            )
            embedding = response.data[0].embedding
            embeddings_dict[title] = embedding
        except Exception as e:
            logger.error(f"Error generating embedding for show '{title}': {e}")
            embeddings_dict[title] = None 

    return embeddings_dict


def save_embeddings(embeddings_dict, file_name):
    try:
        with open(file_name, "wb") as f:
            pickle.dump(embeddings_dict, f)
        logger.info(f"Embeddings successfully saved to {file_name}")
    except Exception as e:
        logger.error(f"Error saving embeddings to file {file_name}: {e}")
        raise


def load_embeddings(file_name):
    try:
        with open(file_name, "rb") as f:
            embeddings_dict = pickle.load(f)
        logger.info(f"Embeddings successfully loaded from {file_name}")
        return embeddings_dict
    except Exception as e:
        logger.error(f"Error loading embeddings from file {file_name}: {e}")
        raise


def ensure_embeddings(titles, descriptions, file_name, api_key, model="text-embedding-ada-002"):
    if os.path.exists(file_name):
        logger.info(f"Embeddings file '{file_name}' found. Loading embeddings...")
        return load_embeddings(file_name)
    else:
        logger.info(f"Embeddings file '{file_name}' not found. Generating embeddings...")
        embeddings = generate_embeddings(titles, descriptions, api_key, model)
        save_embeddings(embeddings, file_name)
        return embeddings



if __name__ == "__main__":
    load_dotenv()  

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Ensure OPENAI_API_KEY is set in the .env file.")

    csv_file = "tv_shows.csv"  
    titles = load_column_from_csv(csv_file, "Title")
    descriptions = load_column_from_csv(csv_file, "Description")

    embeddings_file = "tv_show_embeddings.pkl"

    logger.info("Generating embeddings for TV show descriptions...")
    ensure_embeddings(titles, descriptions, embeddings_file, api_key)
    logger.info("Embeddings process completed successfully.")