from data_loader import load_csv_file
from embeddings import ensure_embeddings
from user_input import validate_user_input
from recommendations import compute_average_vector, find_top_recommendations, get_user_vectors
from show_generator import generate_new_shows
from image_generator import generate_image_for_show
from dotenv import load_dotenv
import logging
import os
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        load_dotenv()

        # Load the LightX API key
        lightx_api_key = os.getenv("LIGHTX_API_KEY")
        if not lightx_api_key:
            raise ValueError("LightX API key not found. Ensure LIGHTX_API_KEY is set in the .env file")
        
        # Load OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Ensure OPENAI_API_KEY is set in the .env file.")

        csv_file = "tv_shows.csv"  
        embeddings_file = "tv_show_embeddings.pkl"
        
        df = load_csv_file(csv_file)
        titles = df["Title"].tolist()  # List of TV show titles
        descriptions = df["Description"].tolist()  # List of TV show descriptions

        embeddings = ensure_embeddings(titles, descriptions, embeddings_file, openai_api_key)

        user_shows = validate_user_input(titles)

        user_vectors = get_user_vectors(user_shows, embeddings)

        average_vector = compute_average_vector(user_vectors)

        recommendations = find_top_recommendations(average_vector, embeddings, user_shows)

        print("Here are the TV shows I think you would love:")
        for idx, (show, percentage) in enumerate(recommendations, start=1):
            print(f"{idx}. {show} ({percentage}%)")
 
        generated_shows = generate_new_shows(user_shows, openai_api_key)
        show1_name = generated_shows[0]['name']
        show1_description = generated_shows[0]['description']
        show2_name = generated_shows[1]['name']
        show2_description = generated_shows[1]['description']

        saved_image_path_show1 = generate_image_for_show(show1_name, show1_description, "show1.png", lightx_api_key)
        print(f"Image for '{show1_name}' saved to: {saved_image_path_show1}")
        saved_image_path_show2 = generate_image_for_show(show2_name, show2_description, "show2.png", lightx_api_key)
        print(f"Image for '{show2_name}' saved to: {saved_image_path_show2}")

        img1 = Image.open(saved_image_path_show1)
        img2 = Image.open(saved_image_path_show2)

        img1.show()  
        img2.show()
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        print("A critical error occurred. Please check the logs for more details.")
