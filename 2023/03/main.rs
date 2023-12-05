use std::collections::{HashMap, HashSet};

mod common;
mod point;


/// Description
/// -----------
/// A number and the hash set of unique points that are "gears" meaning the
/// symbol in them is the asterisk '*' symbol.
struct NumberWithGears {
    number: u32,
    gears: HashSet<point::Point>,
}


/// Description
/// -----------
/// The main program for day 3!
///
/// Part 1) It will search through the "engine" and find all numbers with a
/// non '.' touching them (consecutive numbers are the same number) then adds
/// them all up.
///
/// Part 2) It will take the numbers that were found, and those that share a
/// common asterisk (or gear) will be multiplied together then added up.
fn main() {
    let radix = 10;
    let mut total: u32 = 0;
    let (grid, part) = common::get_file_and_part();
    let grid_clone = grid.clone();
    let mut numeric_points: HashMap<usize, HashMap<usize, NumberWithGears>> = HashMap::new();
    for (y, row) in grid_clone.iter().enumerate() {
        let mut row_hash_map: HashMap<usize, NumberWithGears> = HashMap::new();
        let mut number: u32 = 0;
        let mut has_neighbors = false;
        let mut has_gears= false;
        let mut gears: HashSet<point::Point> = HashSet::new();
        let last_x = row.chars().count() - 1;
        let row_clone = row.clone();
        for (x, character) in row_clone.chars().enumerate() {
            let digit = character.to_digit(radix);
            if digit.is_none() && has_neighbors {
                total += number;
                println!(
                    "Number={} at ({}, {}) HAD neighbors! Adding on, new total is={}",
                    number,
                    x,
                    y,
                    total
                );
                if has_gears {
                    let ng = NumberWithGears { number: number, gears: gears.clone() };
                    row_hash_map.insert(x, ng);
                }
                number = 0;
                has_neighbors = false;
                has_gears = false;
                gears = HashSet::new();
            } else if digit.is_none() && !has_neighbors {
                if number > 0 {
                    println!("Number={} at ({}, {}) HAD NO neighbors", number, x, y);
                    number = 0;
                }
            } else if digit.is_some() {
                number *= 10;
                number += digit.unwrap();
                if !has_neighbors {
                    let neighbors = scan_neighbors(&grid, x, y);
                    has_neighbors = check_neighbors_for_symbol(&neighbors);
                    for neighbor in neighbors.iter() {
                        if neighbor.is_some() {
                            let value = neighbor.clone().unwrap();
                            if value.c == '*' {
                                gears.insert(value);
                                has_gears = true;
                            }
                        }
                    }
                }
            }
        }
        // Got to catch the last number in the row!
        if number > 0 {
            let neighbors = scan_neighbors(&grid, last_x, y);
            has_neighbors = has_neighbors || check_neighbors_for_symbol(&neighbors);
            if has_neighbors {
                total += number;
                println!(
                    "Number={} at ({}, {}) HAD neighbors! Adding on, new total is={}",
                    number,
                    last_x,
                    y,
                    total
                );
            }
        }
        if has_gears {
            let ng = NumberWithGears { number: number, gears: gears.clone() };
            row_hash_map.insert(last_x, ng);
        }
        numeric_points.insert(y, row_hash_map);
    }
    println!("Part 1 Total = {}", total);
    if part == 2 {
        total = 0;
        let mut gear_map: HashMap<&point::Point, Vec<u32>> = HashMap::new();
        for (_y, row_map) in &numeric_points {
            for (_x, num_and_gear) in row_map {
                for gear in &num_and_gear.gears {
                    let num_vec = gear_map.entry(gear).or_insert(vec![]);
                    num_vec.push(num_and_gear.number);
                }
            }
        }
        for (gear, numbers) in gear_map {
            if numbers.len() > 2 {
                for num in &numbers {
                    println!("Number={}", num)
                }
                panic!("How the heck is this touching more than 2 numbers??? {} : len={}", gear, numbers.len());
            } else if numbers.len() == 2 {
                let num1 = numbers.get(0).unwrap();
                let num2 = numbers.get(1).unwrap();
                total += num1 * num2;
            } else {
                println!("Skipping gear {} as it does not have 2 numbers", gear);
            }
        }
        println!("Part 2 Total={}", total);
    }
}


/// Description
/// -----------
/// Check a vector of optional points to see if any of them contain a "symbol"
/// i.e. anything that is not a numeric digit or a period '.' character.
///
/// Params
/// ------
/// :neighbors: &Vec<Option<Point>>
/// The vector of points to check for symbols within.
///
/// Return
/// ------
/// bool
/// True if there is a symbol in the vector.
/// False if there not is a symbol in the vector.
fn check_neighbors_for_symbol(neighbors: &Vec<Option<point::Point>>) -> bool {
    let neighbors_clone = neighbors.clone();
    for neighbor in neighbors_clone.iter() {
        if neighbor.is_some() {
            let value = neighbor.clone().unwrap();
            if !value.c.is_numeric() && value.c != '.' {
                return true;
            }
        }
    }
    return false;
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
fn scan_neighbors(grid: &Vec<String>, x: usize, y: usize) -> Vec<Option<point::Point>> {
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
    return neighbors;
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
fn get_coord(grid: &Vec<String>, x: usize, y: usize) -> Option<point::Point> {
    let row = grid.get(y);
    if row.is_some() {
        let coordinate = row.unwrap().chars().nth(x);
        if coordinate.is_some() {
            return Some(
                point::Point {
                    x: x,
                    y: y,
                    c: coordinate.unwrap(),
                }
            );
        }
    }
    return None;
}
