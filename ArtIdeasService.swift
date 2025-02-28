import SwiftUI
import Combine

/// Service for fetching art ideas from Appwrite function
class ArtIdeasService: ObservableObject {
    // MARK: - Properties
    
    /// Art idea model
    struct ArtIdea: Identifiable, Codable {
        var id = UUID()
        let title: String
        let description: String
        let difficulty: String
        let colorUsage: String
        
        enum CodingKeys: String, CodingKey {
            case title, description, difficulty, colorUsage
        }
        
        init(from decoder: Decoder) throws {
            let container = try decoder.container(keyedBy: CodingKeys.self)
            title = try container.decode(String.self, forKey: .title)
            description = try container.decode(String.self, forKey: .description)
            difficulty = try container.decode(String.self, forKey: .difficulty)
            colorUsage = try container.decode(String.self, forKey: .colorUsage)
            id = UUID()
        }
        
        init(title: String, description: String, difficulty: String, colorUsage: String) {
            self.title = title
            self.description = description
            self.difficulty = difficulty
            self.colorUsage = colorUsage
        }
    }
    
    /// Response structure from the Appwrite function
    struct ArtIdeasResponse: Codable {
        let success: Bool
        let artIdeas: ArtIdeasData
        
        enum CodingKeys: String, CodingKey {
            case success
            case artIdeas = "art_ideas"
        }
    }
    
    /// Structure containing the array of art ideas
    struct ArtIdeasData: Codable {
        let ideas: [ArtIdea]
    }
    
    // MARK: - Published Properties
    
    @Published var artIdeas: [ArtIdea] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    // MARK: - Appwrite Configuration
    
    // Replace these with your actual Appwrite endpoint and function ID
    private let appwriteEndpoint = "https://cloud.appwrite.io/v1"
    private let functionId = "YOUR_FUNCTION_ID"
    
    // MARK: - Methods
    
    /// Fetch art ideas from the Appwrite function
    func fetchArtIdeas() {
        isLoading = true
        errorMessage = nil
        
        // Create the URL for the Appwrite function execution
        guard let url = URL(string: "\(appwriteEndpoint)/functions/\(functionId)/executions") else {
            self.errorMessage = "Invalid URL"
            self.isLoading = false
            return
        }
        
        // Create the request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Add your Appwrite API key if needed
        // request.addValue("YOUR_API_KEY", forHTTPHeaderField: "X-Appwrite-Key")
        
        // Add your Appwrite project ID
        // request.addValue("YOUR_PROJECT_ID", forHTTPHeaderField: "X-Appwrite-Project")
        
        // Execute the request
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self else { return }
            
            DispatchQueue.main.async {
                self.isLoading = false
                
                if let error = error {
                    self.errorMessage = "Network error: \(error.localizedDescription)"
                    return
                }
                
                guard let data = data else {
                    self.errorMessage = "No data received"
                    return
                }
                
                do {
                    // For debugging
                    if let jsonString = String(data: data, encoding: .utf8) {
                        print("Response: \(jsonString)")
                    }
                    
                    let decoder = JSONDecoder()
                    let response = try decoder.decode(ArtIdeasResponse.self, from: data)
                    
                    if response.success {
                        self.artIdeas = response.artIdeas.ideas
                    } else {
                        self.errorMessage = "Function returned an error"
                    }
                } catch {
                    self.errorMessage = "Decoding error: \(error.localizedDescription)"
                    print("JSON decoding error: \(error)")
                }
            }
        }.resume()
    }
    
    /// Generate sample art ideas for preview and testing
    func generateSampleArtIdeas() -> [ArtIdea] {
        return [
            ArtIdea(
                title: "Forest Canopy",
                description: "A view looking up through tree branches to the sky.",
                difficulty: "Medium",
                colorUsage: "Brown for tree trunks, green for leaves, blue for sky peeking through."
            ),
            ArtIdea(
                title: "Ocean Depths",
                description: "An underwater scene with varying depths and marine life.",
                difficulty: "Hard",
                colorUsage: "Blue for water (light to dark gradient), green for seaweed, brown for rocks and coral."
            ),
            ArtIdea(
                title: "Mountain Landscape",
                description: "A serene mountain view with forests and a lake.",
                difficulty: "Medium",
                colorUsage: "Brown for mountains, green for forests, blue for lake and sky."
            )
        ]
    }
}

// MARK: - Preview Helper

extension ArtIdeasService {
    static var preview: ArtIdeasService {
        let service = ArtIdeasService()
        service.artIdeas = service.generateSampleArtIdeas()
        return service
    }
} 