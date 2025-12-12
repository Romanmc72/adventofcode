struct Day02: DayChallenge {
    func invalidDetectorPart1(numStr: String) -> Bool {
        let length = numStr.count
        if length % 2 == 1 {
            return false
        }
        let left = numStr.prefix(length / 2)
        let right = numStr.suffix(length / 2)
        return left == right
    }

    /**
     * Did Gemini teach me this algorithm?...
     * Yes.
     * Yes it did.
     */
    func invalidDetectorPart2(numStr: String) -> Bool {
        let doubledNumStr = "\(numStr)\(numStr)"
        let trimmedStr = doubledNumStr.dropLast().dropFirst()
        return trimmedStr.contains(numStr)
    }

    func iterateAndDetect(input: String, detector: (String) -> Bool) -> Int {
        var invalidIds: [Int] = []
        let ranges = input.split(separator: ",")
        for range in ranges {
            let splitRange = range.split(separator: "-")
            guard let min = Int(splitRange[0]) else {
                print("[ERROR] could not get range split min from: \(range)")
                return -1
            }
            guard let max = Int(splitRange[1]) else {
                print("[ERROR] could not get range split max from: \(range)")
                return -1

            }
            for num in min...max {
                if detector("\(num)") {
                    invalidIds.append(num)
                }

            }
        }
        return invalidIds.reduce(0, +)
    }

    func part1(input: String) -> Int {
        return iterateAndDetect(input: input, detector: invalidDetectorPart1)
    }
    
    func part2(input: String) -> Int {
        return iterateAndDetect(input: input, detector: invalidDetectorPart2)
    }
}
