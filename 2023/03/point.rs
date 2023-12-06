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


impl Point {
    /// Description
    /// -----------
    /// Convenience method for creating a new point.
    pub fn new(x: usize, y: usize, c: char) -> Point {
        Point { x, y, c }
    }

    /// Description
    /// -----------
    /// Get a point off of the grid as a point.
    pub fn from_grid(x: usize, y: usize, grid: &[String]) -> Point {
        if let Some(p) = get_coord(grid, x, y) {
            return p;
        }
        panic!("Nice try stupid, no point was found!");
    }

    /// Description
    /// -----------
    /// Returns a vector containing all of neighbors of the requested cell on the
    /// grid.
    ///
    /// Params
    /// ------
    /// :grid: &Vec<String>
    /// The grid to pull values from.
    ///
    /// :x: usize
    /// The X coordinate to get neighbors for from the grid (position within the
    /// string)
    ///
    /// :y: usize
    /// The Y coordinate to get neighbors from the grid (string within the vector)
    ///
    /// Return
    /// ------
    /// Vec<Option<Point>>
    /// The vector containing optional points from within the grid.
    pub fn get_neighbors(&self, grid: &[String]) -> Vec<Option<Point>> {
        let mut neighbors = vec![
            get_coord(grid, &self.x + 1, self.y    ),
            get_coord(grid, &self.x + 1, &self.y + 1),
            get_coord(grid, self.x    , &self.y + 1),
        ];
        if self.x > 0 {
            let mut pos_x = vec![ 
                get_coord(grid, &self.x - 1, self.y    ),
                get_coord(grid, &self.x - 1, &self.y + 1),
            ];
            neighbors.append(&mut pos_x);
        }
        if self.y > 0 {
            let mut pos_y = vec![
                get_coord(grid, self.x    , &self.y - 1),
                get_coord(grid, &self.x + 1, &self.y - 1),
            ];
            neighbors.append(&mut pos_y);
        }
        if self.x > 0 && self.y > 0 {
            let mut pos_xy = vec![
                get_coord(grid, &self.x - 1, &self.y - 1),
            ];
            neighbors.append(&mut pos_xy);
        }
        neighbors
    }
}


/// Description
/// -----------
/// Get a single Point from the input grid based on its x and y position if it
/// exists. If that point does not exist this will return none.
///
/// Params
/// ------
/// :grid: &Vec<String>
/// The grid to fetch a coordinate from.
///
/// :x: usize
/// The X coordinate to fetch from the grid (position within the string).
///
/// :y: usize
/// The Y coordinate to fetch from the grid (string within the vector of strings).
///
/// Return
/// ------
/// Option<Point>
/// The point if it exists otherwise none.
fn get_coord(grid: &[String], x: usize, y: usize) -> Option<Point> {
    let row = grid.get(y);
    if row.is_some() {
        let coordinate = row.unwrap().chars().nth(x);
        if let Some(c) = coordinate {
            return Some(Point { x, y, c });
        }
    }
    None
}
