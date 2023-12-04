mod common;


/// Looking for 4361 in the response for part 1 using the example problem set.
fn main() {
    let radix = 10;
    let mut total: u32 = 0;
    let (grid, _part) = common::get_file_and_part();
    let grid_clone = grid.clone();
    for (y, row) in grid_clone.iter().enumerate() {
        let mut number: u32 = 0;
        let mut has_neighbors = false;
        let last_x = row.chars().count() - 1;
        let row_clone = row.clone();
        for (x, character) in row_clone.chars().enumerate() {
            let digit = character.to_digit(radix);
            if digit.is_none() && has_neighbors {
                total += number;
                println!("Number={} at ({}, {}) HAD neighbors! Adding on, new total is={}", number, x, y, total);
                number = 0;
                has_neighbors = false;
            } else if digit.is_none() && !has_neighbors {
                if number > 0 {
                    println!("Number={} at ({}, {}) HAD NO neighbors", number, x, y);
                    number = 0;
                }
            } else if digit.is_some() {
                number *= 10;
                number += digit.unwrap();
                if !has_neighbors {
                    has_neighbors = scan_neighbors(&grid, x, y);
                }
            }
        }
        // Got to catch the last number in the row!
        if number > 0 {
            has_neighbors = has_neighbors || scan_neighbors(&grid, last_x, y);
            if has_neighbors {
                total += number;
                println!("Number={} at ({}, {}) HAD neighbors! Adding on, new total is={}", number, last_x, y, total);
            }
        }
    }
    println!("Total = {}", total);
}

fn scan_neighbors(grid: &Vec<String>, x: usize, y: usize) -> bool {
    let mut neighbors = vec![
        get_coord(&grid, x + 1, y    ),
        get_coord(&grid, x + 1, y + 1),
        get_coord(&grid, x    , y + 1),
    ];
    if x > 0 {
        let mut pos_x = vec![ 
            get_coord(&grid, x - 1, y    ),
            get_coord(&grid, x - 1, y + 1),
        ];
        neighbors.append(&mut pos_x);
    }
    if y > 0 {
        let mut pos_y = vec![
            get_coord(&grid, x    , y - 1),
            get_coord(&grid, x + 1, y - 1),
        ];
        neighbors.append(&mut pos_y);
    }
    if x >0 && y > 0 {
        let mut pos_xy = vec![
            get_coord(&grid, x - 1, y - 1),
        ];
        neighbors.append(&mut pos_xy);
    }
    for neighbor in neighbors.iter() {
        if neighbor.is_some() {
            let value = neighbor.unwrap();
            if !value.is_numeric() && value != '.' {
                return true;
            }
        }
    }
    return false;
}

// This works, now we need to iterate the characters and find the ones that
// have "neighbors" where the next door character(s) has a non-period and
// non-numeric. We also need to extract all of the numbers that exist and
// stitch them together as the whole number.
fn get_coord(grid: &Vec<String>, x: usize, y: usize) -> Option<char> {
    let row = grid.get(y);
    if row.is_some() {
        let coordinate = row.unwrap().chars().nth(x);
        if coordinate.is_some() {
            return coordinate;
        }
    }
    return None;
}