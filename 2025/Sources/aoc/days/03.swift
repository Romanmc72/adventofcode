struct Day03: DayChallenge {
    /**
     * Using recursion to solve this one!
     * Walk the line til you hit a 9 (the largest possible single digit)
     * or hit the end (where you would run out of digits if you had more
     * to search for), then chop up the line at the highest you found and
     * pass it along til there are no more battery cells to select.
     * @params
     * line: the line to search for cells in
     * cells: the number of cells that need to be found in the line
     * pasCells: the cells that were found on previous iterations in
     *      the recursion (omit on first run)
     * @return
     * Returns the array of digits that compose the number
     * Example: [8, 4, 2, 5] should be converted to 8425
     */
    func pickBestCells(line: String, cells: Int, pastCells: [Int] = []) -> [Int] {
        if cells <= 0 || line.count == 0 {
            return pastCells
        }

        var cellCopy = pastCells

        var max = 0
        var maxIndex = 0
        for (index, c) in line.enumerated() {
            guard let n = Int(String(c)) else {
                print("[ERROR] Unable to parse number for some reason")
                return []
            }
            if n > max && index <= line.count - cells {
                max = n
                maxIndex = index
            }
            if max == 9 || index == line.count - cells {
                break
            }
        }
        cellCopy.append(max)
        let remainingLine = String(line.suffix(line.count - maxIndex - 1))
        return pickBestCells(line: remainingLine, cells: cells - 1, pastCells: cellCopy)
    }

    func cellsToBattery(cells: [Int]) -> Int {
        let stringified = cells.map { String($0) }
        let joined = stringified.joined()
        return Int(joined) ?? 0
    }

    func part1(input: String) -> Any {
        var batteries: [Int] = []
        for line in input.split(separator: "\n") {
            let bestCell = pickBestCells(line: String(line), cells: 2)
            let battery = cellsToBattery(cells: bestCell)
            batteries.append(battery)
        }
        return batteries.reduce(0, +)
    }

    func part2(input: String) -> Any {
        var batteries: [Int] = []
        for line: String.SubSequence in input.split(separator: "\n") {
            let bestCell = pickBestCells(line: String(line), cells: 12)
            let battery = cellsToBattery(cells: bestCell)
            batteries.append(battery)
        }
        return batteries.reduce(0, +)
    }
}
