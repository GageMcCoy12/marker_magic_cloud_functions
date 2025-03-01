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
    
    # Get the request data
    request_data = context.req.body
    print(f"Request data: {request_data}")
    
    # Parse the JSON string if it's a string
    if isinstance(request_data, str):
        try:
            request_data = json.loads(request_data)
            print(f"Parsed request data: {request_data}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {
                'success': False,
                'message': f'Error parsing JSON request: {str(e)}'
            }

    # Extract color names from the request
    color_names = request_data.get('colorNames', [])
    
    # If no colors are provided, use default colors
    if not color_names or len(color_names) == 0:
        color_names = ["green", "blue", "brown"]
        print(f"No colors provided, using defaults: {color_names}")
    else:
        print(f"Using colors from request: {color_names}")
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create the prompt for OpenAI
    prompt = f"""
        I have markers in these colors: {', '.join(color_names)}.
    
        Please generate 10 creative art ideas that work well using only these colors. For each idea, provide:
        1. A title.
        2. A brief description (1-2 sentences) that outlines the concept and includes clear, specific visual instructions for image generation. The description should mention the desired artistic style (e.g., "hyper-realistic watercolor" or "vibrant digital illustration"), lighting, perspective, and composition details.
        3. A difficulty rating (Easy, Medium, Hard). (Note: higher difficulty means more colors may be used, with a minimum of 3 and a maximum of 10.)
        4. How the specific colors could be used effectively, emphasizing a harmonious visual appearance.
        
        Constraints:
        - Only suggest projects where the colors work together in one of these harmonies: Monochromatic, Analogous, Complementary, Split Complementary, Triadic, Tetradic, or Square.
        - Do not suggest projects with a monochromatic color scheme if the color is a neutral color. (specifically browns, blacks, whites, and grays) 
        - Do not suggest abstract art ideas or patterns.
        - The visual instructions in the description must be detailed and unambiguous, suitable for direct use with an AI image generation model like Stability.ai.
        
        Return the response as a JSON array with objects containing the keys: title, description, difficulty, and colorUsage.

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
        print("Art ideas generated successfully:")
        print(art_ideas)
        
        # Format the response for Appwrite
        # Appwrite expects a dictionary that will be converted to JSON
        response_data = {}
        if 'art_projects' in art_ideas:
            response_data['art_projects'] = art_ideas['art_projects']
        else:
            response_data['art_projects'] = art_ideas
        
        # Return a properly formatted response that Appwrite can handle
        return context.res.json(response_data)
        
    except Exception as e:
        # Log the error details
        print("Error generating art ideas:")
        print(e)
        return {
            'success': False,
            'message': f'Error generating art ideas: {str(e)}'
        } 
