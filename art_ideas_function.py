import os
import json
from openai import OpenAI

"""
Appwrite Function to generate art ideas based on specific colors (green, blue, and brown)
using OpenAI's API. This keeps the API key secure by storing it in Appwrite's environment variables.

Environment Variables Required:
- OPENAI_API_KEY: Your OpenAI API key
"""

def main(context):
    print("kachow")
    # Get the OpenAI API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("ERROR: OpenAI API key not found in environment variables")
        return {
            'success': False,
            'message': 'OpenAI API key not found in environment variables'
        }
    print("api key!")
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Define the available colors
    colors = ["green", "blue", "brown"]
    
    # Create the prompt for OpenAI
    prompt = f"""
    I have markers in these colors: {', '.join(colors)}. 
    
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
            model="4o-mini",  # using the 4o-mini model as specified
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
        print("Art ideas generated successfully:")
        print(art_ideas)
        
        return {
            'success': True,
            'art_ideas': art_ideas
        }
        
    except Exception as e:
        # Log the error details
        print("Error generating art ideas:")
        print(e)
        return {
            'success': False,
            'message': f'Error generating art ideas: {str(e)}'
        }
