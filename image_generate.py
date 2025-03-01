import os
import json
import base64
import requests
import traceback
from typing import Dict, Any

# DreamStudio API configuration
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

def main(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an image using DreamStudio API based on a prompt
    
    Args:
        context: The Appwrite function context containing the request data
        
    Returns:
        A dictionary with the base64-encoded image or an error message
    """
    try:
        # Log the incoming context for debugging
        print(f"Received context: {json.dumps(context)}")
        
        # Get the prompt from the request data
        data = context.get('req', {}).get('body', {}).get('data', {})
        prompt = data.get('prompt')
        
        print(f"Extracted prompt: {prompt}")
        
        if not prompt:
            return {
                "success": False,
                "message": "No prompt provided"
            }
        
        # Check if API key is available
        if not STABILITY_API_KEY:
            return {
                "success": False,
                "message": "DreamStudio API key not configured"
            }
        
        print(f"API Key available: {bool(STABILITY_API_KEY)}")
        
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
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
            "style_preset": "digital-art",
            "seed": 0
        }
        
        print(f"Sending request to {STABILITY_API_URL}")
        
        response = requests.post(
            STABILITY_API_URL,
            headers=headers,
            json=payload
        )
        
        print(f"Received response with status code: {response.status_code}")
        
        if response.status_code != 200:
            error_message = f"API request failed with status code {response.status_code}"
            try:
                error_details = response.json()
                error_message += f": {json.dumps(error_details)}"
            except:
                error_message += f": {response.text}"
            
            print(error_message)
            return {
                "success": False,
                "message": error_message
            }
        
        # Extract the image from the response
        response_json = response.json()
        print(f"Response keys: {list(response_json.keys())}")
        
        if "artifacts" not in response_json or not response_json["artifacts"]:
            return {
                "success": False,
                "message": "No image generated in the response"
            }
        
        # Get the base64-encoded image
        base64_image = response_json["artifacts"][0]["base64"]
        print("Successfully extracted base64 image")
        
        # Return the base64-encoded image
        return base64_image
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = f"Error generating image: {str(e)}\n{error_traceback}"
        print(error_message)
        return {
            "success": False,
            "message": error_message
        }
