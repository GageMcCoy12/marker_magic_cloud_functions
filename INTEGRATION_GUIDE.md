# Art Ideas Generator Integration Guide

This guide explains how to integrate the Art Ideas Generator functionality into your Marker Scanner app.

## Overview

The Art Ideas Generator uses an Appwrite function to generate creative art ideas based on the available marker colors (green, blue, and brown). This approach keeps your OpenAI API key secure by storing it in Appwrite's environment variables rather than in your local code.

## Files

1. **Appwrite Function Files**:
   - `art_ideas_function.py`: The main Python function that calls OpenAI's API
   - `function_requirements.txt`: Dependencies for the Appwrite function
   - `art_ideas_function_README.md`: Detailed deployment instructions for Appwrite

2. **Swift Integration Files**:
   - `ArtIdeasService.swift`: Service class for communicating with the Appwrite function
   - `ArtIdeasView.swift`: SwiftUI view for displaying art ideas

## Integration Steps

### 1. Deploy the Appwrite Function

Follow the instructions in `art_ideas_function_README.md` to deploy the function to your Appwrite account.

### 2. Add Swift Files to Your Project

1. Add `ArtIdeasService.swift` and `ArtIdeasView.swift` to your Xcode project.
2. Update the Appwrite configuration in `ArtIdeasService.swift` with your actual endpoint and function ID:

```swift
private let appwriteEndpoint = "https://cloud.appwrite.io/v1" // Update if using a custom domain
private let functionId = "YOUR_FUNCTION_ID" // Replace with your actual function ID
```

### 3. Update AppModel.swift

Add a reference to the ArtIdeasView in your app's navigation:

```swift
// In AppModel.swift, add a new app state
enum AppState {
    case onboarding
    case scanning
    case colorDetection
    case suggestions
    case templatePreview
    case gallery
    case artIdeas // Add this new state
}

// Add a method to navigate to the art ideas view
func moveToArtIdeas() {
    withAnimation {
        currentState = .artIdeas
    }
}
```

### 4. Update Your Main Navigation View

Add the ArtIdeasView to your main navigation structure:

```swift
// In your main content view
switch appModel.currentState {
case .onboarding:
    OnboardingView()
case .scanning:
    ScannerView()
case .colorDetection:
    ColorDetectionView()
case .suggestions:
    SuggestionsView()
case .templatePreview:
    TemplatePreviewView()
case .gallery:
    GalleryView()
case .artIdeas: // Add this case
    ArtIdeasView()
}
```

### 5. Add a Navigation Button

Add a button to navigate to the Art Ideas view from an appropriate place in your app, such as the color detection screen:

```swift
Button(action: {
    appModel.moveToArtIdeas()
}) {
    HStack {
        Image(systemName: "paintpalette.fill")
        Text("Get Art Ideas")
    }
    .font(Theme.Typography.buttonFont)
    .foregroundColor(.white)
    .frame(maxWidth: .infinity)
    .frame(height: Theme.Layout.buttonHeight)
    .background(Theme.Colors.blue)
    .cornerRadius(Theme.Layout.cornerRadius)
}
.padding(.horizontal)
```

## Customization

### Modifying Available Colors

If you want to change the available colors or make them dynamic based on detected markers:

1. Update the Python function in `art_ideas_function.py` to accept colors as input parameters.
2. Modify the `ArtIdeasService.swift` to pass the detected colors to the Appwrite function.
3. Update the UI in `ArtIdeasView.swift` to display the actual detected colors.

### Enhancing the UI

The provided UI is designed to match the existing app theme. You can customize it further by:

1. Adding animations for a more engaging experience
2. Implementing a favorites system to save preferred art ideas
3. Adding sharing functionality to export ideas to social media

## Testing

Before deploying to production:

1. Test with the sample data by calling `artIdeasService.generateSampleArtIdeas()`
2. Verify the Appwrite function works correctly by testing it directly in the Appwrite Console
3. Test the integration in your app with different network conditions

## Troubleshooting

- If you encounter CORS issues, make sure your Appwrite project has the correct CORS settings.
- If the function times out, you may need to increase the timeout limit in your Appwrite function settings.
- For debugging, check the response data by printing the JSON string in the `fetchArtIdeas()` method. 