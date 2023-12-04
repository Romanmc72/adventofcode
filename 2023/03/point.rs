pub struct Point {
    x: i32,
    y: i32,
}

impl Point {
    pub fn new(x: i32, y: i32) -> Point {
        Point {x: x, y: y}
    }
    pub fn get_neighbors(&self) -> Vec<Point> {
        vec![
            Point::new(x + 1, y    ),
            Point::new(x    , y + 1),
            Point::new(x - 1, y    ),
            Point::new(x    , y - 1),
            Point::new(x + 1, y + 1),
            Point::new(x + 1, y - 1),
            Point::new(x - 1, y + 1),
            Point::new(x - 1, y - 1),
        ]
    }
}
