/**
 * Generic grid builder function. Splits input on the individual lines of raw
 * input and given a function that can parse each line into a row in the grid,
 * the function will return a 2D grid of the type that the line parser can produce.
 * @param input String the input string to parse to a grid
 * @param lineParser (Substring) -> [T] the parsing function to convert a line of
 *    input to a row in the grid
 * @return [[T]] the parsed grid
 */
func makeGrid<T>(input: String, lineParser: (Substring) -> [T]) -> [[T]] {
  var grid: [[T]] = []
  for line in input.split(separator: "\n") {
    grid.append(lineParser(line))
  }
  return grid
}
