struct ConnectionPair {
    let a: JunctionBox
    let b: JunctionBox
    let distance: Int
}

class JunctionBox: Hashable, CustomStringConvertible {
    let x: Int;
    let y: Int;
    let z: Int;

    var connections: [JunctionBox] = []

    init(x: Int, y: Int, z: Int) {
        self.x = x
        self.y = y
        self.z = z
    }

    func connect(jb: JunctionBox) {
        self.connections.append(jb)
        jb.connections.append(self)
    }

    func disconnect(jb: JunctionBox) {
        self.connections = self.connections.filter({ j in j != jb })
        jb.connections = jb.connections.filter({ j in j != self })
    }

    func distance(jb: JunctionBox) -> Int {
        let dx = self.x - jb.x
        let dy = self.y - jb.y
        let dz = self.z - jb.z
        return (dx * dx) + (dy * dy) + (dz * dz)
    }

    static func == (lhs: JunctionBox, rhs: JunctionBox) -> Bool {
        return lhs.x == rhs.x && lhs.y == rhs.y && lhs.z == rhs.z
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(x)
        hasher.combine(y)
        hasher.combine(z)
    }

    var description: String {
        var connections: [String] = []
        for c in self.connections {
            connections.append("{x: \(c.x), y: \(c.y), z: \(c.z), d: \(self.distance(jb: c))}")
        }
        let buff = connections.count > 0 ? "\n\t" : ""
        return "{x: \(self.x), y: \(self.y), z: \(self.z), connections: [\(buff)\(connections.joined(separator: buff))\(buff)]}"
    }
}

struct Day08: DayChallenge {
    func part1(input: String) -> Int {
        guard let junctionBoxes = try? parseJunctionBoxes(input: input) else {
            return -1
        }

        // connect
        let connectionLimit = input.count < 1000 ? 10 : 1000
        var connections: [ConnectionPair] = []
        for (i, box) in junctionBoxes.enumerated() {
            for j in (i + 1)..<junctionBoxes.count {
                let compare = junctionBoxes[j]
                connections.append(ConnectionPair(a: box, b: compare, distance: box.distance(jb: compare)))
            }
        }

        // trim connection list
        connections.sort(by: { cnxnA, cnxnB in cnxnA.distance < cnxnB.distance })
        var actualConnections = 0
        for c in connections {
            c.a.connect(jb: c.b)
            actualConnections += 1
            if actualConnections >= connectionLimit {
                break
            }
        }

        // summarize the graph
        var seenBoxes = Set<JunctionBox>()
        var subGraphs: [Int] = []
        for box in junctionBoxes {
            if seenBoxes.contains(box) {
                continue
            }
            let subGraph = enumerateGraphSection(jb: box)
            if !subGraph.isSubset(of: seenBoxes) {
                subGraphs.append(subGraph.count)
            }
            seenBoxes = seenBoxes.union(subGraph)
        }
        subGraphs.sort()
        print(subGraphs)
		return subGraphs[subGraphs.count - 1] * subGraphs[subGraphs.count - 2] * subGraphs[subGraphs.count - 3]
    }

    func enumerateGraphSection(jb: JunctionBox, subGraph: Set<JunctionBox> = Set()) -> Set<JunctionBox> {
        var g = subGraph
        for connection in jb.connections {
            if g.contains(connection) {
                continue
            }
            g.insert(connection)
            g = enumerateGraphSection(jb: connection, subGraph: g)
        }
        return g
    }

    func parseJunctionBoxes(input: String) throws -> [JunctionBox] {
        var junctionBoxes: [JunctionBox] = []
        for line in input.split(separator: "\n") {
            var points: [Int] = []
            for coord in line.split(separator: ",") {
                guard let n = Int(coord) else {
                    throw RuntimeError.parseError(description: "[ERROR] Found a non-Int value of \(coord) on line \(line)")
                }
                points.append(n)
            }
            let jb = JunctionBox(x: points[0], y: points[1], z: points[2])
            junctionBoxes.append(jb)
        }
        return junctionBoxes
    }

    func part2(input: String) -> Int {
        guard let junctionBoxes = try? parseJunctionBoxes(input: input) else {
            return -1
        }

        let jbSet = Set(junctionBoxes)

        // connect
        var connections: [ConnectionPair] = []
        for (i, box) in junctionBoxes.enumerated() {
            for j in (i + 1)..<junctionBoxes.count {
                let compare = junctionBoxes[j]
                connections.append(ConnectionPair(a: box, b: compare, distance: box.distance(jb: compare)))
            }
        }

        // trim connection list
        connections.sort(by: { cnxnA, cnxnB in cnxnA.distance < cnxnB.distance })
        for c in connections {
            c.a.connect(jb: c.b)
            let subGraph = enumerateGraphSection(jb: c.a)

            if subGraph == jbSet {
                return c.a.x * c.b.x
            }
        }
        return -1
    }
}
