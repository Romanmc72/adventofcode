struct Day02: DayChallenge {
    func part1(input: String) -> Any {
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
                let numStr = "\(num)"
                let length = numStr.count
                if length % 2 == 1 {
                    continue
                }
                let left = numStr.prefix(length / 2)
                let right = numStr.suffix(length / 2)
                if left == right {
                    invalidIds.append(num)
                }
            }
        }
        return invalidIds.reduce(0, +)
    }
    
    func part2(input: String) -> Any {
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
                let numStr = "\(num)"
                let dubNumStr = "\(numStr)\(numStr)"
                let trimmedStr = dubNumStr.dropLast().dropFirst()
                if trimmedStr.contains(numStr) {
                    invalidIds.append(num)
                }
            }
        }
        return invalidIds.reduce(0, +)
    }
}
