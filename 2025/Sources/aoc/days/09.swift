struct ParsedPoints {
    var points: [Point] = []
    var minX: Int = 999999999
    var maxX: Int = -1
    var minY: Int = 999999999
    var maxY: Int = -1

    mutating func addPoint(p: Point) {
        self.points.append(p)
        self.minX = min(self.minX, p.x)
        self.maxX = max(self.maxX, p.x)
        self.minY = min(self.minY, p.y)
        self.maxY = max(self.maxY, p.y)
    }

    func buildGrid() -> [[String]] {
        var grid: [[String]] = []
        let columnCount = self.maxX + 1
        for _ in 0...self.maxY {
            grid.append(Array(repeating: ".", count: columnCount))
        }

        var lastPoint: Point?
        for point in self.points {
            grid[point.y][point.x] = "#"
            if lastPoint != nil {
                guard let direction = try? diffPoints(start: lastPoint!, end: point) else {
                    return []
                }
                if lastPoint!.x + direction.x == point.x && lastPoint!.y + direction.y == point.y {
                    continue
                }
                var pointer = Point(x: lastPoint!.x + direction.x, y: lastPoint!.y + direction.y)
                while pointer.x > 0 && pointer.x < columnCount && pointer.y > 0 && pointer.y < self.maxY + 1 {
                    grid[pointer.y][pointer.x] = "X"
                    pointer = Point(x: pointer.x + direction.x, y: pointer.y + direction.y)
                    if pointer == point {
                        break
                    }
                }
            }
            lastPoint = point
        }
        lastPoint = self.points[self.points.count - 1]
        let point = self.points[0]
        guard let direction = try? diffPoints(start: lastPoint!, end: point) else {
            return []
        }
        if lastPoint!.x + direction.x == point.x && lastPoint!.y + direction.y == point.y {
            return grid
        }
        var pointer = Point(x: lastPoint!.x + direction.x, y: lastPoint!.y + direction.y)
        while pointer.x > 0 && pointer.x < columnCount && pointer.y > 0 && pointer.y < self.maxY + 1 {
            grid[pointer.y][pointer.x] = "X"
            pointer = Point(x: pointer.x + direction.x, y: pointer.y + direction.y)
            if pointer == point {
                break
            }
        }
        return grid
    }

    func fillGrid(grid: [[String]]) -> [[String]] {
        var gridCopy = grid
        // This takes way too long... need to optimize but am kinda done for the year i think...
        for (rowIndex, row) in gridCopy.enumerated() {
            for (colIndex, value) in row.enumerated() {
                if value != "." {
                    continue
                }
                if isPointInsideShape(grid: grid, x: colIndex, y: rowIndex) {
                    gridCopy[rowIndex][colIndex] = "@"
                }
            }
        }
        return gridCopy
    }

    func isPointInsideShape(grid: [[String]], x: Int, y: Int) -> Bool {
        var seenPoints = Set<Point>()
        var searchDirection = Point(x: 0, y: -1)
        var pointer = Point(x: x + searchDirection.x, y: y + searchDirection.y)
        var isInside = false
        while pointer.y > 0 && pointer.x > 0 && pointer.y < grid.count && pointer.x < grid[0].count {
            let char = grid[pointer.y][pointer.x]

            if char != "." {
                searchDirection = rotatePoint(point: searchDirection)
            }
            if seenPoints.contains(pointer) {
                isInside = true
                break
            }
            seenPoints.insert(pointer)
            pointer.x = pointer.x + searchDirection.x
            pointer.y = pointer.y + searchDirection.y
        }

        return isInside
    }
}

// This will loop most of the time even if it should not
func rotatePoint(point: Point) -> Point {
    var mutatedPoint = point
    if point.x == 0 {
        if point.y == 1 {
            mutatedPoint.x = 1
        } else {
            mutatedPoint.x = -1
        }
    } else {
        mutatedPoint.x = 0
    }
    if point.y == 0 {
        if point.x == 1 {
            mutatedPoint.y = -1
        } else {
            mutatedPoint.y = 1
        }
    } else {
        mutatedPoint.y = 0
    }
    return mutatedPoint
}

func diffPoints(start: Point, end: Point) throws -> Point {
    if start.x == end.x {
        return Point(x: 0, y: start.y > end.y ? -1 : 1)
    }
    if start.y == end.y {
        return Point(x: start.x > end.x ? -1 : 1, y: 0)
    }
    throw RuntimeError.illegalState(description: "these points are either the same or are not on the same line `\(start)` & `\(end)`")
}

struct Point : Hashable {
    var x: Int
    var y: Int

    static func == (lhs: Point, rhs: Point) -> Bool {
        return lhs.x == rhs.x && lhs.y == rhs.y
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(x)
        hasher.combine(y)
    }
}

struct SizePair {
    let size: Int
    let pointA: Point
    let pointB: Point
}

struct Day09: DayChallenge {
    func part1(input: String) -> Int {
        guard let parsed = try? parsePoints(input: input) else {
            return -1
        }

        let sizes = getSortedSizes(points: parsed.points)

		return sizes[0].size
    }

    func part2(input: String) -> Int {
        guard let parsed = try? parsePoints(input: input) else {
            return -1
        }

        let sizes = getSortedSizes(points: parsed.points)

        let grid = parsed.buildGrid()

        // print(grid.map({ row in row.joined() }).joined(separator: "\n"))

        let filledGrid = parsed.fillGrid(grid: grid)

        // print(filledGrid.map({ row in row.joined() }).joined(separator: "\n"))

        for size in sizes {
            if containsOnlyInnerPoints(grid: filledGrid, pointA: size.pointA, pointB: size.pointB) {
                return size.size
            }
        }

		return 0
    }

    func containsOnlyInnerPoints(grid: [[String]], pointA: Point, pointB: Point) -> Bool {
        let minX = min(pointA.x, pointB.x)
        let maxX = max(pointA.x, pointB.x)
        let minY = min(pointA.y, pointB.y)
        let maxY = max(pointA.y, pointB.y)
        for y in minY...maxY {
            for x in minX...maxX {
                if grid[y][x] == "." {
                    return false
                }
            }
        }
        return true
    }

    func parsePoints(input: String) throws -> ParsedPoints {
        var parsed = ParsedPoints()
        for line in input.split(separator: "\n") {
            let nums = line.split(separator: ",")
            guard let x = Int(nums[0]) else {
                throw RuntimeError.parseError(description: "[ERROR] No X value found in \(line)")
            }
            guard let y = Int(nums[1]) else {
                throw RuntimeError.parseError(description: "[ERROR] No Y value found in \(line)")
            }
            parsed.addPoint(p: Point(x: x, y: y))
        }
        return parsed
    }

    func getSortedSizes(points: [Point]) -> [SizePair] {
        var sizes: [SizePair] = []
        for (i, point) in points.enumerated() {
            for k in (i + 1)..<points.count {
                let otherPoint = points[k]
                sizes.append(SizePair(size: (abs(point.x - otherPoint.x) + 1) * (abs(point.y - otherPoint.y) + 1), pointA: point, pointB: otherPoint))
            }
        }
        sizes.sort(by: ({ sizeA, sizeB in sizeA.size > sizeB.size }))
        return sizes
    }
}
