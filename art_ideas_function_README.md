# Art Ideas Generator Function for Appwrite

This function generates creative art ideas based on the specified colors (green, blue, and brown) using OpenAI's API.

## Files
- `art_ideas_function.py`: The main function code
- `function_requirements.txt`: Dependencies required for the function

## Deployment Instructions

### Prerequisites
1. An Appwrite account
2. An OpenAI API key

### Steps to Deploy

1. **Log in to your Appwrite Console**

2. **Create a new Function**
   - Navigate to Functions in the Appwrite Console
   - Click "Create Function"
   - Give your function a name (e.g., "Art Ideas Generator")
   - Select a runtime compatible with Python (e.g., Python 3.9 or later)

3. **Set Environment Variables**
   - In your function settings, add the following environment variable:
     - Key: `OPENAI_API_KEY`
     - Value: Your OpenAI API key

4. **Upload the Function Code**
   - Upload both `art_ideas_function.py` and `function_requirements.txt`
   - Alternatively, you can use the Appwrite CLI to deploy the function

5. **Set the Entry Point**
   - Set the entry point to `art_ideas_function.py` and the function name to `main`

6. **Deploy the Function**
   - Click "Deploy" to make your function live

## Using the Function

### HTTP Request
You can call the function via an HTTP request:

```
POST https://[YOUR_APPWRITE_ENDPOINT]/functions/[FUNCTION_ID]/executions
```

### From Your App
You can also call the function from your app using the Appwrite SDK:

```swift
// Swift example
let functions = Functions(client)
let execution = try await functions.createExecution(
    functionId: "[FUNCTION_ID]"
)

if let response = execution.response {
    // Parse the response
    // response will contain the art ideas in JSON format
}
```

### Response Format

The function returns a JSON object with the following structure:

```json
{
  "success": true,
  "art_ideas": {
    "ideas": [
      {
        "title": "Forest Canopy",
        "description": "A view looking up through tree branches to the sky.",
        "difficulty": "Medium",
        "colorUsage": "Brown for tree trunks, green for leaves, blue for sky peeking through."
      },
      // ... more ideas
    ]
  }
}
```

## Troubleshooting

- If you receive an error about the OpenAI API key, make sure it's correctly set in the environment variables.
- If you're getting timeout errors, you may need to increase the function timeout in the Appwrite Console.
- Check the function logs in the Appwrite Console for detailed error messages. 