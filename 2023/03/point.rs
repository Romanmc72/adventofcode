/// Description
/// -----------
/// An X, Y coordinate and the character found at that coordinate.
#[derive(PartialEq, Eq, Hash, Debug, Clone)]
pub struct Point {
    pub x: usize,
    pub y: usize,
    pub c: char,
}

/// Description
/// -----------
/// Allows a point to be printed on the println!() macro and generally
/// converted to a string.
impl std::fmt::Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Point(x={}, y={}, '{}')", self.x, self.y, self.c)
    }
}
