import XCTest
@testable import aoc

final class Day05Tests: XCTestCase {
    var day: Day05! 

    override func setUpWithError() throws {
        day = Day05()
    }
    
    override func tearDownWithError() throws {
        day = nil
    }
    
    func testOverlapping() {
      let result = day.part2(
        input: """
        2-7
        1-3
        """)
      XCTAssertEqual(result, 7, "The result is incorrect.")
    }
  
    func testGap() {
      let result = day.part2(
        input: """
        5-7
        1-3
        """)
      XCTAssertEqual(result, 6, "The result is incorrect.")
    }

    func testDuplicates() {
      let result = day.part2(
        input: """
        5-7
        1-3
        5-7
        1-3
        5-7
        1-3
        5-7
        1-3
        """)
      XCTAssertEqual(result, 6, "The result is incorrect.")
    }

    func testSameStartDifferentEnd() {
      let result = day.part2(
        input: """
        1-3
        1-2
        1-4
        1-5
        1-7
        1-2
        """)
      XCTAssertEqual(result, 7, "The result is incorrect when the start is the same.")
    }

    func testExample() {
      let result = day.part2(
        input: """
        3-5
        10-14
        16-20
        12-18

        1
        5
        8
        11
        17
        32
        """)
      XCTAssertEqual(result, 14, "Does not work on the example.")
    }
}
