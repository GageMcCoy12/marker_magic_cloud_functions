import os
import json
from openai import OpenAI

"""
Appwrite Function to generate art ideas based on colors provided in the request
using OpenAI's API. This keeps the API key secure by storing it in Appwrite's environment variables.

Environment Variables Required:
- OPENAI_API_KEY: Your OpenAI API key
"""

def main(context):
    # Get the OpenAI API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        return {
            'success': False,
            'message': 'OpenAI API key not found in environment variables'
        }
    
    
    # Get the request data
    request_data = context.req.body
    
    # Parse the JSON string if it's a string
    if isinstance(request_data, str):
        try:
            request_data = json.loads(request_data)
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'message': f'Error parsing JSON request: {str(e)}'
            }

    # Extract color names from the request
    color_names = request_data.get('colorNames', [])
    
    # If no colors are provided, use default colors
    if not color_names or len(color_names) == 0:
        color_names = ["green", "blue", "brown"]
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create the prompt for OpenAI
    prompt = f"""
    I have markers in these colors: {', '.join(color_names)}. 
    
    Please generate 10 creative art ideas that would work well with only these colors.
    For each idea, provide:
    1. A title
    2. A brief description (1-2 sentences)
    3. A difficulty rating (Easy, Medium, Hard)
    4. How the specific colors could be used effectively
    
    Return the response as a JSON array with objects containing fields: 
    title, description, difficulty, and colorUsage.
    """
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # using the 4o-mini model as specified
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a creative art assistant that provides ideas for marker art projects."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract and parse the JSON response
        content = response.choices[0].message.content
        art_ideas = json.loads(content)
        
        # Log the art ideas for debugging
        context.log(art_ideas)
        
        return {
            'success': True,
            'art_projects': art_ideas.get('art_projects', [])
        }
        
    except Exception as e:
        # Log the error details
        return {
            'success': False,
            'message': f'Error generating art ideas: {str(e)}'
        } 
