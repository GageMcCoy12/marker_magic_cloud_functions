import os
import json
import base64
import requests
from typing import Dict, Any

# Stability AI API configuration
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

def main(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an image using Stability AI based on a prompt
    
    Args:
        context: The Appwrite function context containing the request data
        
    Returns:
        A dictionary with the base64-encoded image or an error message
    """
    # Get the prompt from the request data
    try:
        data = context.get('req', {}).get('body', {}).get('data', {})
        prompt = data.get('prompt')
        
        if not prompt:
            return {
                "success": False,
                "message": "No prompt provided"
            }
        
        # Check if API key is available
        if not STABILITY_API_KEY:
            return {
                "success": False,
                "message": "Stability AI API key not configured"
            }
        
        # Call Stability AI API
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30
        }
        
        response = requests.post(
            STABILITY_API_URL,
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"API request failed with status code {response.status_code}: {response.text}"
            }
        
        # Extract the image from the response
        response_json = response.json()
        if "artifacts" not in response_json or not response_json["artifacts"]:
            return {
                "success": False,
                "message": "No image generated in the response"
            }
        
        # Get the base64-encoded image
        base64_image = response_json["artifacts"][0]["base64"]
        
        # Return the base64-encoded image
        return base64_image
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating image: {str(e)}"
        }
