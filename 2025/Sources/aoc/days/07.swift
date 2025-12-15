struct TachyonGridElement {
    var symbol: Character
    var count: Int
}

struct Day07: DayChallenge {
    func part1(input: String) -> Int {
        var grid = input.split(separator: "\n").map { Array($0) }
        var splits = 0
        for (rowIndex, row) in grid.enumerated() {
            for (colIndex, char) in row.enumerated() {
                if rowIndex == 0 {
                    if char == "S" {
                        grid[rowIndex][colIndex] = "|"
                    }
                    continue
                }
                let tachyonAbove = grid[rowIndex - 1][colIndex] == "|"
                if !tachyonAbove {
                    continue
                }
                let leftClear = colIndex > 0
                let rightClear = colIndex < row.count - 1
                if char == "^" {
                    if leftClear {
                        grid[rowIndex][colIndex - 1] = "|"
                    }
                    if rightClear {
                        grid[rowIndex][colIndex + 1] = "|"
                    }
                    splits += 1
                    continue
                }
                grid[rowIndex][colIndex] = "|"
            }
        }
        return splits
    }

    func part2(input: String) -> Int {
        var grid: [[TachyonGridElement]] = input.split(separator: "\n").map { Array($0).map{ TachyonGridElement(symbol: $0, count: 0) } }
        for (rowIndex, row) in grid.enumerated() {
            for (colIndex, tach) in row.enumerated() {
                if rowIndex == 0 {
                    if tach.symbol == "S" {
                        grid[rowIndex][colIndex].symbol = "|"
                        grid[rowIndex][colIndex].count = 1
                    }
                    continue
                }
                let tachyonAbove = grid[rowIndex - 1][colIndex]
                if tachyonAbove.symbol != "|" {
                    continue
                }
                let leftClear = colIndex > 0
                let rightClear = colIndex < row.count - 1
                if tach.symbol == "^" {
                    if leftClear {
                        grid[rowIndex][colIndex - 1].symbol = "|"
                        grid[rowIndex][colIndex - 1].count = grid[rowIndex][colIndex - 1].count + tachyonAbove.count
                    }
                    if rightClear {
                        grid[rowIndex][colIndex + 1].symbol = "|"
                        grid[rowIndex][colIndex + 1].count = grid[rowIndex][colIndex + 1].count + tachyonAbove.count
                    }
                    continue
                }
                grid[rowIndex][colIndex].symbol = "|"
                grid[rowIndex][colIndex].count = grid[rowIndex][colIndex].count + tachyonAbove.count
            }
        }
        func combo(n: Int, e: TachyonGridElement) -> Int {
            return n + e.count
        }
        return grid[grid.count - 1].reduce(0, combo)
    }

    // I feel like I will use this again...
    func printGrid(grid: [[TachyonGridElement]]) {
        print(grid.map({ r in
            r.map({ t in
                if t.count == 0 {
                    return String(t.symbol)
                }
                return String(t.count)
            }).joined(separator: "")
        }).joined(separator: "\n"))
    }
}
