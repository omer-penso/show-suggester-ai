import time
import requests
import logging
import json

logger = logging.getLogger(__name__)


def generate_image_for_show(show_name, show_description, output_path, lightx_api_key):
    """
    Generate an image for a TV show using the LightX API..
    """
    try:
        if not lightx_api_key:
            raise ValueError("LightX API key not found. Ensure LIGHTX_API_KEY is set in the .env file.")
        
        #Submit a request to generate an image
        url = "https://api.lightxeditor.com/external/api/v1/text2image"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": lightx_api_key
        }
        prompt = f"Create a visually stunning advertisement for a TV show called '{show_name}' with the theme: {show_description}"
        data = {"textPrompt": prompt}

        logger.info(f"Sending request to generate image for show: {show_name}")
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            logger.error(f"Image generation request failed. Status code: {response.status_code}, Response: {response.text}")
            raise Exception("Failed to submit image generation request.")
        
        response_json = response.json()
        order_id = response_json.get("body", {}).get("orderId")
        if not order_id:
            raise Exception("Order ID not found in response.")

        logger.info(f"Order ID received: {order_id}")

        #Poll the status of the request until it's "active"
        status_url = "https://api.lightxeditor.com/external/api/v1/order-status"
        status_payload = {"orderId": order_id}
        retries = 0
        max_retries = 10  # Stop polling after 10 retries
        sleep_interval = 3  # Poll every 3 seconds

        while retries < max_retries:
            status_response = requests.post(status_url, headers=headers, json=status_payload)

            if status_response.status_code != 200:
                logger.error(f"Status check failed. Status code: {status_response.status_code}, Response: {status_response.text}")
                raise Exception("Failed to check order status.")

            status_json = status_response.json()
            status = status_json.get("body", {}).get("status")
            if status == "active":
                # Image generation is complete; fetch the image URL
                image_url = status_json.get("body", {}).get("output")
                if not image_url:
                    raise Exception("Image URL not found in status response.")
                
                # Download and save the image
                logger.info(f"Image generation complete. Downloading image from: {image_url}")
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(output_path, "wb") as image_file:
                        image_file.write(image_response.content)
                    logger.info(f"Image saved to {output_path}")
                    return output_path
                else:
                    raise Exception(f"Failed to download image. Status code: {image_response.status_code}")
            elif status == "failed":
                raise Exception("Image generation failed.")
            
            retries += 1
            logger.info(f"Image not ready yet. Retrying in {sleep_interval} seconds...")
            time.sleep(sleep_interval)

        raise Exception("Image generation timed out. Max retries reached.")

    except Exception as e:
        logger.error(f"Error in generating image: {e}")
        raise

