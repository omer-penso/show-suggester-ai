import openai
import os
from dotenv import load_dotenv
import logging
import json
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_new_shows(user_input_shows, api_key):
    """
    Generate two brand-new TV shows based on user input using OpenAI.
    """
    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
        Based on the following TV shows that the user loves: {', '.join(user_input_shows)},
        create two completely brand new TV shows. Provide the output in this JSON format:
        [
            {{"name": "Show Name 1", "description": "Description of Show 1"}},
            {{"name": "Show Name 2", "description": "Description of Show 2"}}
        ]
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "system", "content": "You are a creative assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip("```json").strip("```")
        new_shows = json.loads(content)

        return new_shows
    except json.JSONDecodeError as json_err:
        logger.error(f"Error decoding JSON response: {json_err}")
        raise
    except Exception as e:
        logger.error(f"Error generating new TV shows: {e}")
        raise


# Testing the module
if __name__ == "__main__":
    user_loved_shows = ["Game of Thrones", "Breaking Bad", "Stranger Things"]
    generated_shows = generate_new_shows(user_loved_shows)
    print("--------------------------------------")
    print("Generated TV Shows:")
    for show in generated_shows:
        print(f"name: {show['name']}")
        print(f"description: {show['description']}")
