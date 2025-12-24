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

        print(grid.map({ row in row.joined() }).joined(separator: "\n"))

        var lastPoint: Point?
        for point in self.points {
            grid[point.y][point.x] = "#"
            if lastPoint != nil {
                guard let direction = try? diffPoints(start: lastPoint!, end: point) else {
                    return []
                }
                print("direction : \(direction)")
                if lastPoint!.x + direction.x == point.x && lastPoint!.y + direction.y == point.y {
                    continue
                }
                var pointer = Point(x: lastPoint!.x + direction.x, y: lastPoint!.y + direction.y)
                while pointer.x > 0 && pointer.x < columnCount && pointer.y > 0 && pointer.y < self.maxY + 1 {
                    print("Filling POINTER \(pointer)")
                    grid[pointer.y][pointer.x] = "X"
                    pointer = Point(x: pointer.x + direction.x, y: pointer.y + direction.y)
                    if pointer == point {
                        break
                    }
                }
            }
            print("last point: \(lastPoint ?? point)")
            lastPoint = point
            print("     point: \(point)")
            print(grid.map({ row in row.joined()}).joined(separator: "\n"))
            print("\n========================\n")
        }
        lastPoint = self.points[self.points.count - 1]
        let point = self.points[0]
        guard let direction = try? diffPoints(start: lastPoint!, end: point) else {
            return []
        }
        print("direction : \(direction)")
        if lastPoint!.x + direction.x == point.x && lastPoint!.y + direction.y == point.y {
            return grid
        }
        var pointer = Point(x: lastPoint!.x + direction.x, y: lastPoint!.y + direction.y)
        while pointer.x > 0 && pointer.x < columnCount && pointer.y > 0 && pointer.y < self.maxY + 1 {
            print("Filling POINTER \(pointer)")
            grid[pointer.y][pointer.x] = "X"
            pointer = Point(x: pointer.x + direction.x, y: pointer.y + direction.y)
            if pointer == point {
                break
            }
        }
        print("last point: \(lastPoint ?? point)")
        print("     point: \(point)")
        print(grid.map({ row in row.joined()}).joined(separator: "\n"))
        print("\n========================\n")
        return grid
    }
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

struct Point {
    var x: Int
    var y: Int

    static func == (lhs: Point, rhs: Point) -> Bool {
        return lhs.x == rhs.x && lhs.y == rhs.y
    }
}

struct Day09: DayChallenge {
    func part1(input: String) -> Int {
        guard let parsed = try? parsePoints(input: input) else {
            return -1
        }

        let sizes = getSortedSizes(points: parsed.points)

		return sizes[0]
    }

    func part2(input: String) -> Int {
        guard let parsed = try? parsePoints(input: input) else {
            return -1
        }

        let grid = parsed.buildGrid()

        print(grid.map({ row in row.joined() }).joined(separator: "\n"))

		return 0
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

    func getSortedSizes(points: [Point]) -> [Int] {
        var sizes: [Int] = []
        for (i, point) in points.enumerated() {
            for k in (i + 1)..<points.count {
                let otherPoint = points[k]
                sizes.append((abs(point.x - otherPoint.x) + 1) * (abs(point.y - otherPoint.y) + 1))
            }
        }
        sizes.sort(by: >)
        return sizes
    }
}
