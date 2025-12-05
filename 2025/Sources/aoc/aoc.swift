import ArgumentParser
import Foundation

@main
struct aoc: ParsableCommand {
    static let dayMap: [Int: @Sendable () -> DayChallenge] = [
        1: { Day01() },
        2: { Day02() },
        3: { Day03() },
        4: { Day04() },
        5: { Day05() },
        6: { Day06() },
        7: { Day07() },
        8: { Day08() },
        9: { Day09() },
        10: { Day10() },
        11: { Day11() },
        12: { Day12() },
    ]

    // 1. Argument for Day (Required)
    @Argument(help: "The day number (1-12) to run.")
    var day: Int

    // 2. Argument for Part (Optional, defaults to 0 to run all)
    @Option(name: .customShort("p"), help: "The part of the challenge to run (1 or 2). Defaults to 0 (both parts).")
    var part: Int = 0

    // 3. Flag for Example Data (Boolean)
    @Flag(name: .customLong("example"), help: "Use the example data file (e.g., 01.example.txt).")
    var useExample: Bool = false
    
    func run() throws {
        guard part >= 0 && part <= 2 else {
            throw ValidationError("Part must be 0 (both), 1, or 2.")
        }

        guard let input = loadInput(day: day, useExample: useExample) else {
            print("Failed to load input for Day \(day).")
            return
        }

        // 2. Dynamically select the Day Challenge implementation using the dictionary map
        guard let dayInitializer = aoc.dayMap[day] else {
            throw ValidationError("Day \(day) implementation not found. Did you forget to add it to the dayMap?")
        }
        // 2. Dynamically select the Day Challenge implementation
        // NOTE: In a real project, you would use a Dictionary map or similar factory 
        // to instantiate the correct Day challenge class/struct. 
        // For simplicity here, we'll assume a stub:
        
        let dayInstance: DayChallenge = dayInitializer()

        // 3. Execute the requested part(s)
        
        if part == 1 || part == 0 {
            let result1 = dayInstance.part1(input: input)
            print("--- Day \(day) Part 1 (\(useExample ? "Example" : "Real")) ---")
            print("Result: \(result1)")
        }

        if part == 2 || part == 0 {
            let result2 = dayInstance.part2(input: input)
            print("--- Day \(day) Part 2 (\(useExample ? "Example" : "Real")) ---")
            print("Result: \(result2)")
        }
    }
}
