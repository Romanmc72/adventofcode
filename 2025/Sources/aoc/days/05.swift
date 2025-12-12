struct Range {
    var min: Int
    var max: Int
}

struct Day05: DayChallenge {
    func getRanges(input: [String.SubSequence]) -> [Range] {
        var ranges: [Range] = []
        for line in input {
            let splitLine = line.split(separator: "-")
            guard let min = Int(splitLine[0]) else {
                print("[ERROR] Issue getting number from line! \(line)")
                return []
            }
            guard let max = Int(splitLine[1]) else {
                print("[ERROR] Issue getting number from line! \(line)")
                return []
            }
            ranges.append(Range(min: min, max: max))
        }
        return ranges.sorted(by: {(r1: Range, r2: Range) -> Bool in return r1.min < r2.min })
    }

    func getIngredientIds(input: [String.SubSequence]) -> [Int] {
        var ingredientIds: [Int] = []
        for line in input {
            guard let n = Int(line) else {
                print("[ERROR] Error parsing ingredient id \(line)")
                return []
            }
            ingredientIds.append(n)
        }
        return ingredientIds.sorted()
    }

    func consolidateRanges(ranges: [Range]) -> [Range] {
        var consolidatedRanges: [Range] = []
        var rangeIndex = 0
        var nextRangeIndex = rangeIndex + 1
        while nextRangeIndex < ranges.count {
            var range = ranges[rangeIndex]
            var nextRange = ranges[nextRangeIndex]
            while nextRange.min <= range.max {
                range.max = max(range.max, nextRange.max)
                nextRangeIndex += 1
                if nextRangeIndex >= ranges.count {
                    break
                }
                nextRange = ranges[nextRangeIndex]
            }
            consolidatedRanges.append(range)
            rangeIndex = nextRangeIndex
            nextRangeIndex = rangeIndex + 1
        }
        let lastRange = ranges[ranges.count - 1]
        if consolidatedRanges.count > 0 && lastRange.max > consolidatedRanges[consolidatedRanges.count - 1].max {
            consolidatedRanges.append(lastRange)
        }
        return consolidatedRanges
    }

    func part1(input: String) -> Int {
        let sections = input.split(separator: "\n\n")
        let ranges = getRanges(input: String(sections[0]).split(separator: "\n"))
        let ingredientIds = getIngredientIds(input: String(sections[1]).split(separator: "\n"))
        var spoils = 0
        ingredientLoop: for ingredientId in ingredientIds {
            for range in ranges {
                if ingredientId > range.min && ingredientId < range.max {
                    spoils += 1
                    continue ingredientLoop
                }
            }
        }
        return spoils
    }
    
    func part2(input: String) -> Int {
        let sections = input.split(separator: "\n\n")
        let ranges = getRanges(input: String(sections[0]).split(separator: "\n"))
        let consolidatedRanges = consolidateRanges(ranges: ranges)
        var totalFreshRanges = 0
        for range in consolidatedRanges {
            totalFreshRanges += range.max - range.min + 1
        }
        return totalFreshRanges
    }
}
