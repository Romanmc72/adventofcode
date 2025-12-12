struct Coordinate {
    let x: Int
    let y: Int
}

struct Day04: DayChallenge {
    func makeGrid(input: String) -> [[Int]] {
        var grid: [[Int]] = []
        for line in input.split(separator: "\n") {
            var row: [Int] = []
            for c in line {
                row.append(c == "@" ? 1 : 0)
            }
            grid.append(row)
        }
        return grid
    }

    func identifyRemovals(grid: [[Int]]) -> [Coordinate] {
        let accessibleIfLessThan = 4
        var accessibleRolls: [Coordinate] = []
        for (rowIndex, row) in grid.enumerated() {
            for (colIndex, roll) in row.enumerated() {
                if roll == 0 {
                    continue
                }

                let leftBound = colIndex == 0
                let rightBound = colIndex == row.count - 1
                let upBound = rowIndex == 0
                let downBound = rowIndex == grid.count - 1

                let surroundings: [Int] = [
                    leftBound || downBound ? 0 : grid[rowIndex + 1][colIndex - 1],
                    leftBound ? 0 : grid[rowIndex][colIndex - 1],
                    leftBound || upBound ? 0 : grid[rowIndex - 1][colIndex - 1],
                    upBound ? 0 : grid[rowIndex - 1][colIndex],
                    rightBound || upBound ? 0 : grid[rowIndex - 1][colIndex + 1],
                    rightBound ? 0 : grid[rowIndex][colIndex + 1],
                    rightBound || downBound ? 0 : grid[rowIndex + 1][colIndex + 1],
                    downBound ? 0 : grid[rowIndex + 1][colIndex],
                ]
                let surroundingRollCount = surroundings.reduce(0, +)
                if surroundingRollCount < accessibleIfLessThan {
                    accessibleRolls.append(Coordinate(x: colIndex, y: rowIndex))
                }
            }
        }
        return accessibleRolls
    }

    func removeRolls(grid: [[Int]], coords: [Coordinate]) -> [[Int]] {
        var copiedGrid = grid
        for coord in coords {
            copiedGrid[coord.y][coord.x] = 0
        }
        return copiedGrid
    }

    func part1(input: String) -> Int {
        let grid = makeGrid(input: input)
        let removableRolls = identifyRemovals(grid: grid)
        return removableRolls.count
    }
    
    func part2(input: String) -> Int {
        var totalRemoved = 0
        var grid = makeGrid(input: input)
        var removableRolls = identifyRemovals(grid: grid)
        while removableRolls.count > 0 {
            totalRemoved += removableRolls.count
            grid = removeRolls(grid: grid, coords: removableRolls)
            removableRolls = identifyRemovals(grid: grid)
        }
        return totalRemoved
    }
}
