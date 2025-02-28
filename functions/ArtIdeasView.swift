import SwiftUI

struct ArtIdeasView: View {
    // MARK: - Properties
    
    @StateObject private var artIdeasService = ArtIdeasService()
    @State private var selectedIdea: ArtIdeasService.ArtIdea?
    @State private var showingDetail = false
    
    // MARK: - Body
    
    var body: some View {
        ZStack {
            // Background
            Theme.Colors.background.ignoresSafeArea()
            
            // Content
            VStack(spacing: 20) {
                // Header
                Text("Art Ideas")
                    .font(Theme.Typography.headerFont)
                    .foregroundColor(Theme.Colors.textPrimary)
                    .padding(.top, 20)
                
                // Color palette display
                HStack(spacing: 15) {
                    ColorCircle(color: .green, name: "Green")
                    ColorCircle(color: .blue, name: "Blue")
                    ColorCircle(color: .brown, name: "Brown")
                }
                .padding(.vertical, 10)
                
                // Ideas list
                if artIdeasService.isLoading {
                    Spacer()
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                        .scaleEffect(1.5)
                    Text("Generating creative ideas...")
                        .font(Theme.Typography.bodyFont)
                        .foregroundColor(Theme.Colors.textSecondary)
                        .padding(.top, 20)
                    Spacer()
                } else if let errorMessage = artIdeasService.errorMessage {
                    Spacer()
                    Image(systemName: "exclamationmark.triangle")
                        .font(.system(size: 50))
                        .foregroundColor(Theme.Colors.red)
                    Text("Error")
                        .font(Theme.Typography.subheaderFont)
                        .foregroundColor(Theme.Colors.textPrimary)
                        .padding(.top, 10)
                    Text(errorMessage)
                        .font(Theme.Typography.bodyFont)
                        .foregroundColor(Theme.Colors.textSecondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)
                        .padding(.top, 5)
                    Spacer()
                } else if artIdeasService.artIdeas.isEmpty {
                    Spacer()
                    Image(systemName: "paintpalette")
                        .font(.system(size: 50))
                        .foregroundColor(Theme.Colors.textSecondary)
                    Text("No Art Ideas Yet")
                        .font(Theme.Typography.subheaderFont)
                        .foregroundColor(Theme.Colors.textPrimary)
                        .padding(.top, 10)
                    Text("Tap the button below to generate creative art ideas using your available colors.")
                        .font(Theme.Typography.bodyFont)
                        .foregroundColor(Theme.Colors.textSecondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)
                        .padding(.top, 5)
                    Spacer()
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(artIdeasService.artIdeas) { idea in
                                ArtIdeaCard(idea: idea)
                                    .onTapGesture {
                                        selectedIdea = idea
                                        showingDetail = true
                                    }
                            }
                        }
                        .padding(.horizontal)
                    }
                }
                
                Spacer()
                
                // Action button
                Button(action: {
                    artIdeasService.fetchArtIdeas()
                }) {
                    HStack {
                        Image(systemName: "sparkles")
                        Text(artIdeasService.artIdeas.isEmpty ? "Generate Ideas" : "Refresh Ideas")
                    }
                    .font(Theme.Typography.buttonFont)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: Theme.Layout.buttonHeight)
                    .background(Theme.Colors.blue)
                    .cornerRadius(Theme.Layout.cornerRadius)
                }
                .padding(.horizontal)
                .padding(.bottom, 40)
                .disabled(artIdeasService.isLoading)
            }
        }
        .sheet(isPresented: $showingDetail) {
            if let idea = selectedIdea {
                ArtIdeaDetailView(idea: idea)
            }
        }
        .onAppear {
            // For preview and testing, load sample data
            #if DEBUG
            if ProcessInfo.processInfo.environment["XCODE_RUNNING_FOR_PREVIEWS"] == "1" {
                artIdeasService.artIdeas = artIdeasService.generateSampleArtIdeas()
            }
            #endif
        }
    }
}

// MARK: - Supporting Views

/// Color circle with label
struct ColorCircle: View {
    let color: Color
    let name: String
    
    var body: some View {
        VStack {
            Circle()
                .fill(color)
                .frame(width: 50, height: 50)
                .shadow(color: Color.black.opacity(0.2), radius: 3, x: 0, y: 2)
            
            Text(name)
                .font(Theme.Typography.captionFont)
                .foregroundColor(Theme.Colors.textPrimary)
        }
    }
}

/// Card view for an art idea
struct ArtIdeaCard: View {
    let idea: ArtIdeasService.ArtIdea
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Title and difficulty badge
            HStack {
                Text(idea.title)
                    .font(Theme.Typography.subheaderFont)
                    .foregroundColor(Theme.Colors.textPrimary)
                
                Spacer()
                
                Text(idea.difficulty)
                    .font(Theme.Typography.captionFont)
                    .foregroundColor(.white)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 4)
                    .background(difficultyColor(for: idea.difficulty))
                    .cornerRadius(12)
            }
            
            // Description
            Text(idea.description)
                .font(Theme.Typography.bodyFont)
                .foregroundColor(Theme.Colors.textSecondary)
                .lineLimit(2)
            
            // Color usage
            Text("Colors: \(idea.colorUsage)")
                .font(Theme.Typography.smallBodyFont)
                .foregroundColor(Theme.Colors.textPrimary)
                .lineLimit(2)
        }
        .padding(16)
        .background(Theme.Colors.cardBackground)
        .cornerRadius(Theme.Layout.cornerRadius)
        .shadow(color: Theme.Colors.shadow, radius: 4, x: 0, y: 2)
    }
    
    private func difficultyColor(for difficulty: String) -> Color {
        switch difficulty.lowercased() {
        case "easy":
            return .green
        case "medium":
            return .orange
        case "hard":
            return .red
        default:
            return Theme.Colors.blue
        }
    }
}

/// Detail view for a selected art idea
struct ArtIdeaDetailView: View {
    let idea: ArtIdeasService.ArtIdea
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        ZStack {
            Theme.Colors.background.ignoresSafeArea()
            
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Header with close button
                    HStack {
                        Spacer()
                        Button(action: {
                            presentationMode.wrappedValue.dismiss()
                        }) {
                            Image(systemName: "xmark.circle.fill")
                                .font(.system(size: 30))
                                .foregroundColor(Theme.Colors.textSecondary)
                        }
                        .padding(.top, 20)
                        .padding(.trailing, 20)
                    }
                    
                    // Title and difficulty
                    VStack(alignment: .leading, spacing: 10) {
                        Text(idea.title)
                            .font(Theme.Typography.headerFont)
                            .foregroundColor(Theme.Colors.textPrimary)
                        
                        HStack {
                            Text("Difficulty:")
                                .font(Theme.Typography.bodyFont)
                                .foregroundColor(Theme.Colors.textSecondary)
                            
                            Text(idea.difficulty)
                                .font(Theme.Typography.bodyFont)
                                .foregroundColor(.white)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 4)
                                .background(difficultyColor(for: idea.difficulty))
                                .cornerRadius(12)
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    // Description
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Description")
                            .font(Theme.Typography.subheaderFont)
                            .foregroundColor(Theme.Colors.textPrimary)
                        
                        Text(idea.description)
                            .font(Theme.Typography.bodyFont)
                            .foregroundColor(Theme.Colors.textSecondary)
                    }
                    .padding(.horizontal, 20)
                    
                    // Color usage
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Color Usage")
                            .font(Theme.Typography.subheaderFont)
                            .foregroundColor(Theme.Colors.textPrimary)
                        
                        Text(idea.colorUsage)
                            .font(Theme.Typography.bodyFont)
                            .foregroundColor(Theme.Colors.textSecondary)
                    }
                    .padding(.horizontal, 20)
                    
                    // Color palette
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Available Colors")
                            .font(Theme.Typography.subheaderFont)
                            .foregroundColor(Theme.Colors.textPrimary)
                        
                        HStack(spacing: 20) {
                            ColorCircle(color: .green, name: "Green")
                            ColorCircle(color: .blue, name: "Blue")
                            ColorCircle(color: .brown, name: "Brown")
                        }
                        .padding(.vertical, 10)
                    }
                    .padding(.horizontal, 20)
                    
                    // Tips section
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Tips")
                            .font(Theme.Typography.subheaderFont)
                            .foregroundColor(Theme.Colors.textPrimary)
                        
                        VStack(alignment: .leading, spacing: 10) {
                            TipRow(icon: "paintbrush.fill", text: "Start with light colors and build up to darker ones")
                            TipRow(icon: "drop.fill", text: "Mix colors to create new shades")
                            TipRow(icon: "sun.max.fill", text: "Use white space effectively")
                            TipRow(icon: "pencil.and.outline", text: "Sketch lightly with pencil before using markers")
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    Spacer(minLength: 40)
                }
            }
        }
    }
    
    private func difficultyColor(for difficulty: String) -> Color {
        switch difficulty.lowercased() {
        case "easy":
            return .green
        case "medium":
            return .orange
        case "hard":
            return .red
        default:
            return Theme.Colors.blue
        }
    }
}

struct TipRow: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: icon)
                .foregroundColor(Theme.Colors.blue)
                .frame(width: 24, height: 24)
            
            Text(text)
                .font(Theme.Typography.bodyFont)
                .foregroundColor(Theme.Colors.textSecondary)
        }
    }
}

// MARK: - Preview

struct ArtIdeasView_Previews: PreviewProvider {
    static var previews: some View {
        ArtIdeasView()
    }
} 
