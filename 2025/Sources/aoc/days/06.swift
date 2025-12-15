struct Day06: DayChallenge {
    func part1(input: String) -> Int {
        var problems: [[Int]] = []
        var solutions: [Int] = []
        for (index, line) in input.split(separator: "\n").enumerated() {
            let trimmedLine = line.trimmingCharacters(in: .whitespacesAndNewlines)
            let items = trimmedLine.split(separator: /\s+/)
            for (itemIndex, item) in items.enumerated() {
                if index == 0 {
                    problems.append([])
                }
                guard let n = Int(item) else {
                    if item == "*" {
                        solutions.append(problems[itemIndex].reduce(1, *))
                        continue
                    }
                    if item == "+" {
                        solutions.append(problems[itemIndex].reduce(0, +))
                        continue
                    }
                    print("[ERROR] Found a weird symbol! `\(item)` exiting")
                    return -1
                }
                problems[itemIndex].append(n)
            }
        }
		return solutions.reduce(0, +)
    }
    
    func part2(input: String) -> Int {
        var rawCharacters: [[Character]] = []
        var problemSplits: [Int] = []
        var operators: [Substring.SubSequence] = []
        var problems: [[Int]] = []
        var solutions: [Int] = []
        let lines = input.split(separator: "\n")
		for (index, line) in lines.enumerated() {
            if index < lines.count - 1 {
                rawCharacters.append(Array(line))
                continue
            }

            for (charIndex, char) in line.split(separator: "").enumerated() {
                if char == "*" || char == "+" {
                    operators.append(char)
                    problemSplits.append(charIndex)
                }
            }
        }

        let cols = rawCharacters[0].count
        let rows = rawCharacters.count

        // Transpose the array and condense the characters to numbers
        let numbers = (0..<cols).map { colIndex in
            let newRow = (0..<rows).map { rowIndex in
                return rawCharacters[rowIndex][colIndex]
            }
            guard let n = Int(newRow.map {String($0)}.joined(separator: "").trimmingCharacters(in: .whitespacesAndNewlines)) else {
                return 0
            }
            return n
        }

        var start = 0
        for e in problemSplits {
            if e == 0 {
                continue
            }
            problems.append(Array(numbers[start..<e - 1]))
            start = e
        }
        problems.append(Array(numbers[start..<numbers.count]))

        for (index, op) in operators.enumerated() {
            if op == "*" {
                solutions.append(problems[index].reduce(1, *))
                continue
            }
            if op == "+" {
                solutions.append(problems[index].reduce(0, +))
                continue
            }
            print("[ERROR] Found a weird symbol! \(op)")
            return -1
        }
        return solutions.reduce(0, +)
    }
}
