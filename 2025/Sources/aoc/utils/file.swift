import Foundation

/**
 * Loads the input file for a given day, selecting between real and example data.
 *
 * - Parameters:
 *      - day: The day number (1-12).
 *      - useExample: If true, loads the '.example.txt' file; otherwise loads '.txt'.
 * - Returns: The contents of the file as a single String, or nil if loading fails.
 */
func loadInput(day: Int, useExample: Bool) -> String? {
    // Format the day number with leading zero (e.g., 1 -> "01")
    let dayString = String(format: "%02d", day)
    
    // Determine the base filename (e.g., "01" or "01.example")
    let fullResourcePath = dayString + (useExample ? ".example" : "")
    
    // Note: The extension is always "txt"
    let fileExtension = "txt"

    // 1. Get the URL for the resource using the module bundle
    guard let fileURL = Bundle.module.url(forResource: fullResourcePath, withExtension: fileExtension) else {
        print("Error: Could not find resource: \(fullResourcePath).\(fileExtension)")
        return nil
    }

    do {
        // 2. Read the entire content of the file into a String
        let fileContents = try String(contentsOf: fileURL, encoding: .utf8)
        return fileContents
    } catch {
        print("Error reading file at \(fileURL.path): \(error.localizedDescription)")
        return nil
    }
}
