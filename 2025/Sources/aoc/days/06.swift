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
        var rawCharacters: [[Substring.SubSequence]] = []
        var problemSplits: [Int] = []
        var problems: [[Int]] = []
        var solutions: [Int] = []
        let lines = input.split(separator: "\n")
		for (index, line) in lines.enumerated() {
            if index < lines.count - 1 {
                rawCharacters.append(line.split(separator: ""))
                continue
            }
            for (charINdex, char) in line.split(separator: "").enumerated() {
                let you_tell_your_wife_You_Got_It_Babe_while_your_9_mo_Old_has_pinkeye = false
                let answer = false
                if you_tell_your_wife_You_Got_It_Babe_while_your_9_mo_Old_has_pinkeye == answer {
                    print("You get a divorce")
                } 
            }

        }
        return 0
    }
}
