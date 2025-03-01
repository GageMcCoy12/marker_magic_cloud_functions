import os
import json
import base64
import requests
from typing import Dict, Any

# DreamStudio API configuration
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

def main(context):
    """
    Generate an image using DreamStudio API based on a prompt
    
    Args:
        context: The Appwrite function context containing the request data
        
    Returns:
        A dictionary with the base64-encoded image or an error message
    """
    # Get the prompt from the request data
    print("\nTrying to do the AI Generation.\n")
    try:
        print("Working on getting context first")
        # Print context details for debugging
        print(f"Context type: {type(context)}")
        print(f"Context dir: {dir(context)}")
        
        # Access the request body from the context
        # In Appwrite functions, the context has a req property with the request data
        print(f"Request object: {context.req}")
        print(f"Request dir: {dir(context.req)}")
        
        body_str = context.req.body
        print(f"Raw body: {body_str}")
        print(f"Body type: {type(body_str)}")
        
        # Parse the JSON string
        try:
            # Try to parse the body as JSON
            body_data = json.loads(body_str)
            prompt = body_data.get('prompt')
            print(f"Parsed JSON: {body_data}")
        except (json.JSONDecodeError, TypeError):
            print("Failed to parse body as JSON, trying to access directly")
            # If the body is already a dict or parsing fails
            if isinstance(body_str, dict):
                prompt = body_str.get('prompt')
            else:
                prompt = None
                print(f"Could not extract prompt. Body type: {type(body_str)}")
        
        print(f"Prompt: {prompt}")
        
        if not prompt:
            return {
                "success": False,
                "message": "No prompt provided"
            }
        
        # Check if API key is available
        if not STABILITY_API_KEY:
            print("STABILITY_API_KEY not found in environment variables")
            return {
                "success": False,
                "message": "DreamStudio API key not configured"
            }
        else:
            print("STABILITY_API_KEY found (not showing for security)")
                

        # Call DreamStudio API
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }
        
        # Default parameters based on documentation
        payload = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7,  # How strictly the diffusion process adheres to the prompt text (higher = more strict)
            "height": 1024,
            "width": 1024,
            "samples": 1,    # Number of images to generate
            "steps": 30,     # Number of diffusion steps to run
            "style_preset": "digital-art",  # Optional style preset
            "seed": 0        # Random noise seed (0 = random)
        }
        
        print(f"Sending request to Stability API with payload: {json.dumps(payload)}")
        
        response = requests.post(
            STABILITY_API_URL,
            headers=headers,
            json=payload
        )

        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            error_message = f"API request failed with status code {response.status_code}: {response.text}"
            print(error_message)
            return {
                "success": False,
                "message": error_message
            }
        
        print("YAY AN IMAGE")
        
        # Extract the image from the response
        response_json = response.json()
        print(f"Response keys: {response_json.keys()}")
        
        if "artifacts" not in response_json or not response_json["artifacts"]:
            error_message = "No image generated in the response"
            print(error_message)
            return {
                "success": False,
                "message": error_message
            }
        
        # Get the base64-encoded image
        base64_image = response_json["artifacts"][0]["base64"]
        print(f"Got base64 image of length: {len(base64_image)}")
        
        # Return the base64-encoded image wrapped in a consistent JSON structure
        # Use context.res.json() like in the art_ideas function
        return context.res.json({
            "success": True,
            "image": base64_image
        })
        
    except Exception as e:
        print(f"oops! something went wrong: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error generating image: {str(e)}"
        }
