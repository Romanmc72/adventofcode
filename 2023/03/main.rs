use std::collections::{HashMap, HashSet};
use point::Point;

mod common;
mod point;


/// Description
/// -----------
/// A number and the hash set of unique points that are "gears" meaning the
/// symbol in them is the asterisk '*' symbol.
struct NumberWithGears {
    number: u32,
    gears: HashSet<Point>,
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
        let mut gears: HashSet<Point> = HashSet::new();
        let last_x = row.chars().count() - 1;
        let row_clone = row.clone();
        for (x, character) in row_clone.chars().enumerate() {
            let point = Point::new(x, y, character);
            let digit = point.c.to_digit(radix);
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
                    let ng = NumberWithGears { number, gears: gears.clone() };
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
                let neighbors = point.get_neighbors(&grid);
                has_neighbors = has_neighbors || check_neighbors_for_symbol(&neighbors);
                has_gears = has_gears || update_gears(&mut gears, &neighbors);
            }
        }
        // Got to catch the last number in the row!
        if number > 0 {
            let point = Point::from_grid(last_x, y, &grid);
            let neighbors = point.get_neighbors(&grid);
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
            let ng = NumberWithGears { number, gears: gears.clone() };
            row_hash_map.insert(last_x, ng);
        }
        numeric_points.insert(y, row_hash_map);
    }
    println!("Part 1 Total = {}", total);
    if part == 2 {
        total = 0;
        let mut gear_map: HashMap<&Point, Vec<u32>> = HashMap::new();
        for row_map in numeric_points.values() {
            for num_and_gear in row_map.values() {
                for gear in &num_and_gear.gears {
                    let num_vec = gear_map.entry(gear).or_default();
                    num_vec.push(num_and_gear.number);
                }
            }
        }
        for (gear, numbers) in gear_map {
            match numbers.len() {
                num_len if num_len > 2 => {
                    for num in &numbers {
                        println!("Number={}", num);
                    }
                    panic!("How the heck is this touching more than 2 numbers??? {} : len={}", gear, numbers.len())
                },
                2 => {
                    let num1 = numbers.first().unwrap();
                    let num2 = numbers.get(1).unwrap();
                    total += num1 * num2;
                },
                _ => println!("Skipping gear {} as it does not have 2 numbers", gear),
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
fn check_neighbors_for_symbol(neighbors: &[Option<Point>]) -> bool {
    for neighbor in neighbors.iter() {
        if neighbor.is_some() {
            let value = neighbor.clone().unwrap();
            if !value.c.is_numeric() && value.c != '.' {
                return true;
            }
        }
    }
    false
}


/// Description
/// -----------
/// Given the current set of gears and the neighboring points, return whether
/// or not there are any gears in the neighboring cells and if there are,
/// update the set and return true. Otherwise return false.
///
/// Params
/// ------
/// :gears: &mut HashSet<Point>
/// The set of gears to optionally add to.
///
/// :neighbors: &Vec<Option<Point>>
/// The vector containing the neighbors to search for a gear within.
///
/// Return
/// ------
/// bool
/// True if there is at least 1 gear in the neighbors vector.
/// False if there are 0 gears in the neighbors vector.
fn update_gears(gears: &mut HashSet<Point>, neighbors: &[Option<Point>]) -> bool {
    let mut has_gears = false;
    for neighbor in neighbors.iter() {
        if neighbor.is_some() {
            let value = neighbor.clone().unwrap();
            if value.c == '*' {
                gears.insert(value);
                has_gears = true;
            }
        }
    }
    has_gears
}
