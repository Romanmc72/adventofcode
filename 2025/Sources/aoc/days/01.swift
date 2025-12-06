struct Day01: DayChallenge {
    /**
    * Fun fact, the swift modulo is not like in python where it matches the divisor.
    */
    func actuallyModulo(input: Int, divisor: Int) -> Int {
        let result = input % divisor
        return result >= 0 ? result : result + divisor
    }

    func solver(input: String, part: Int) -> Int {
        let dialCeiling = 100
        var position = 50
        var zeroStops = 0
        var zeroPasses = 0
        let lines = input.split(separator: "\n")
        for line in lines {
            let direction = line.prefix(1)
            guard let num = Int(line.dropFirst()) else {
                print("[ERROR] Unable to parse line!")
                return -1
            }
            let startedOn = position
            let normalizedTurns = num % dialCeiling

            if num > dialCeiling {
                zeroPasses += num / dialCeiling
            }

            if direction == "L" {
                position = position - normalizedTurns
            } else {
                position = position + normalizedTurns
            }

            if startedOn != 0 && (position < 0 || position > dialCeiling) {
                zeroPasses += 1
            }

            position = actuallyModulo(input: position, divisor: dialCeiling)
            if position == 0 {
                zeroStops += 1
                zeroPasses += 1
            }
        }
        if part == 1 {
            return zeroStops
        }
        return zeroPasses
    }

    func part1(input: String) -> Any {
        return solver(input: input, part: 1)
    }

    func part2(input: String) -> Any {
        return solver(input: input, part: 2)
    }
}
